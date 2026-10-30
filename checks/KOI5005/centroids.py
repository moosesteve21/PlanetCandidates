"""KOI-5005.01: per-event flux-weighted centroid shifts (Kepler long-cadence MOM_CENTR columns), turned into sky
offsets with each quarter's TPF WCS, and the source position they imply relative to the out-of-transit light
centroid, compared with stars A and B (Gaia DR3, epoch 2016; A-B separation 2.4 arcsec)."""
import glob
import numpy as np
import lightkurve as lk

if not glob.glob("kepler/**/*llc.fits", recursive=True):   # Kepler long-cadence light curves from MAST
    lk.search_lightcurve("KIC 3755522", author="Kepler", cadence="long").download_all(download_dir="kepler")
from astropy.coordinates import SkyCoord
import astropy.units as u

P, T0, DUR = 251.958533, 367.3803, 4.742 / 24
A = SkyCoord(293.653780 + 0.40 / 3600 / np.cos(np.radians(38.8339)), 38.833900 + 0.10 / 3600, unit="deg")
B_off = np.array([-0.39, -2.46])                      # B relative to A, arcsec (E, N)
fB = 10 ** (-0.4 * (13.16 - 12.24)); fB = fB / (1 + fB)   # B's share of the light (Gaia G; Kepler band similar)
c_off = fB * B_off                                    # light centroid relative to A
print(f"B share of light {fB:.2f}; light centroid {c_off} arcsec from A")
print(f"predicted source - centroid: A {-c_off}, B {B_off - c_off}")

lcs = {lk.read(f).quarter: lk.read(f, quality_bitmask="default")
       for f in glob.glob("kepler/**/*llc.fits", recursive=True)}
res = []
for e, q in ((0, 4), (2, 9), (3, 12), (4, 15)):
    lc = lcs[q]; tc = T0 + e * P
    tpf = lk.search_targetpixelfile("KIC 3755522", author="Kepler", cadence="long", quarter=q).download(
        download_dir="kepler")
    wcs = tpf.wcs
    t = lc.time.value
    def col(name):
        x = lc[name]
        return np.where(np.ma.getmaskarray(getattr(x, "mask", np.zeros(len(t), bool))), np.nan,
                        np.asarray(getattr(x, "unmasked", x).value, float))
    f, cx, cy = col("pdcsap_flux"), col("mom_centr1"), col("mom_centr2")
    w = (np.abs(t - tc) < 1.0) & np.isfinite(f) & np.isfinite(cx) & np.isfinite(cy)
    oot = w & (np.abs(t - tc) > DUR / 2 + 0.05)
    intr = w & (np.abs(t - tc) < 0.4 * DUR)
    out = []
    for y in (f, cx, cy):
        c = np.polyfit(t[oot] - tc, y[oot], 2)
        r = y - np.polyval(c, t - tc)
        out.append((np.mean(r[intr]), np.std(r[oot]) / np.sqrt(intr.sum()), np.polyval(c, 0)))
    (df, sf, f0), (dx, sx, x0), (dy, sy, y0) = out
    depth = -df / f0
    # pixel -> sky: local Jacobian of the WCS at the centroid (MOM_CENTR is in CCD coordinates; TPF WCS uses
    # pixel indices within the cutout, offset by the cutout's corner)
    px, py = x0 - tpf.column, y0 - tpf.row
    s0 = wcs.pixel_to_world(px, py)
    sx_ = wcs.pixel_to_world(px + 1, py); sy_ = wcs.pixel_to_world(px, py + 1)
    def en(s):
        d = s0.spherical_offsets_to(s); return np.array([d[0].arcsec, d[1].arcsec])
    J = np.column_stack([en(sx_), en(sy_)])           # arcsec per pixel, columns = d/dx, d/dy
    shift = J @ np.array([dx, dy])                    # arcsec (E, N)
    cov = J @ np.diag([sx ** 2, sy ** 2]) @ J.T
    src = -shift / depth                              # source offset from the light centroid (flux-weighted, approx)
    scov = cov / depth ** 2
    res.append((src, scov, e, q))
    dirB = B_off / np.linalg.norm(B_off)
    print(f"E{e} Q{q}: depth {depth * 1e6:.0f} ppm; centroid shift E {shift[0] * 1e3:+.3f} N {shift[1] * 1e3:+.3f} mas"
          f" (err {np.sqrt(cov[0, 0]) * 1e3:.3f}, {np.sqrt(cov[1, 1]) * 1e3:.3f}); implied source - centroid:"
          f" E {src[0]:+.2f} +- {np.sqrt(scov[0, 0]):.2f}, N {src[1]:+.2f} +- {np.sqrt(scov[1, 1]):.2f} arcsec;"
          f" along A->B {src @ dirB:+.2f}")
W = sum(np.linalg.inv(c) for _, c, _, _ in res)
m = np.linalg.solve(W, sum(np.linalg.inv(c) @ s for s, c, _, _ in res))
C = np.linalg.inv(W)
print(f"combined source - centroid: E {m[0]:+.2f} +- {np.sqrt(C[0, 0]):.2f}, N {m[1]:+.2f} +- {np.sqrt(C[1, 1]):.2f}")
for name, p in (("A", -c_off), ("B", B_off - c_off)):
    d = m - p
    print(f"   chi2 vs {name}: {d @ np.linalg.solve(C, d):.1f} (2 dof)")

# figure: positions relative to star A (E to the left, as on the sky)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse


def ell(ax, xy, cov, **kw):
    w, v = np.linalg.eigh(cov)
    ang = np.degrees(np.arctan2(v[1, 1], v[0, 1]))
    ax.add_patch(Ellipse(xy, 2 * np.sqrt(w[1]), 2 * np.sqrt(w[0]), angle=ang, fill=False, **kw))


fig, ax = plt.subplots(figsize=(6, 6.4))
for (s_, c_, e, q), col in zip(res, ("tab:blue", "tab:green", "tab:purple", "tab:brown")):
    p_ = s_ + c_off
    ax.plot(*p_, "o", color=col, ms=5, label=f"event E{e} (Q{q})")
    ell(ax, p_, c_, color=col, lw=0.8, ls=":")
ax.plot(*(m + c_off), "s", color="k", ms=7, label="our 4 events combined (1σ)")
ell(ax, m + c_off, C, color="k", lw=1.5)
dv = c_off + np.array([0.14, -1.67])                  # DR25 DV source offset from the out-of-transit centroid
ax.plot(*dv, "D", color="tab:red", ms=6, label="Kepler DR25 DV (difference image vs OOT centroid, ±0.2″)")
ell(ax, dv, np.diag([0.2 ** 2, 0.2 ** 2]), color="tab:red", lw=1)
ax.plot(0, 0, "*", color="gold", mec="k", ms=18, label="A (KIC 3755522, G 12.24)")
ax.plot(*B_off, "*", color="orange", mec="k", ms=14, label="B (TIC 1877145512, G 13.16)")
ax.plot(*c_off, "+", color="0.4", ms=12, mew=2, label="out-of-transit light centroid")
ax.set_xlim(3.5, -3.5); ax.set_ylim(-5, 2.5); ax.set_aspect("equal")
ax.set_xlabel("ΔRA from A (arcsec, east left)"); ax.set_ylabel("ΔDec from A (arcsec)")
ax.set_title("KOI-5005.01: where the dimming comes from\n(flux-weighted centroid shifts, Kepler long cadence)", fontsize=10)
ax.legend(fontsize=7, loc="upper left")
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("centroids.png", dpi=110)

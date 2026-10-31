"""KOI-5005.01: does the Q12 event's centroid move toward A when the out-of-transit comparison window is longer
(rabtsevich's window before Q12 included a gap)? Same method as centroids.py, windows +-0.5 to +-3 d, plus the
data gaps near the event."""
import glob
import numpy as np
import lightkurve as lk

KDIR = "kepler"
P, T0, DUR = 251.958533, 367.3803, 4.742 / 24
B_off = np.array([-0.39, -2.46])
fB = 10 ** (-0.4 * (13.16 - 12.24)); fB = fB / (1 + fB)
c_off = fB * B_off
dirB = B_off / np.linalg.norm(B_off)
pA, pB = -c_off @ dirB, (B_off - c_off) @ dirB
print(f"along A->B (source - light centroid): A {pA:+.2f}, B {pB:+.2f} arcsec")

for e, q in ((2, 9), (3, 12), (4, 15)):
    lc = [lk.read(f, quality_bitmask="default") for f in glob.glob(f"{KDIR}/**/*llc.fits", recursive=True)
          if lk.read(f).quarter == q][0]
    tpf = lk.search_targetpixelfile("KIC 3755522", author="Kepler", cadence="long", quarter=q).download(
        download_dir=KDIR)
    tc = T0 + e * P
    t = lc.time.value

    def col(name):
        x = lc[name]
        return np.where(np.ma.getmaskarray(getattr(x, "mask", np.zeros(len(t), bool))), np.nan,
                        np.asarray(getattr(x, "unmasked", x).value, float))
    f, cx, cy = col("pdcsap_flux"), col("mom_centr1"), col("mom_centr2")
    good = np.isfinite(f) & np.isfinite(cx) & np.isfinite(cy)
    near = good & (np.abs(t - tc) < 3.5)
    dt = np.diff(t[near])
    gaps = [(t[near][i], t[near][i + 1]) for i in np.where(dt > 0.1)[0]]
    print(f"E{e} Q{q} BKJD {tc:.2f}: gaps > 2.4 h within +-3.5 d: "
          + (", ".join(f"{a - tc:+.2f} to {b - tc:+.2f} d ({(b - a) * 24:.0f} h)" for a, b in gaps) or "none"))
    px, py = np.nanmedian(cx) - tpf.column, np.nanmedian(cy) - tpf.row
    s0 = tpf.wcs.pixel_to_world(px, py)

    def en(s):
        d = s0.spherical_offsets_to(s); return np.array([d[0].arcsec, d[1].arcsec])
    J = np.column_stack([en(tpf.wcs.pixel_to_world(px + 1, py)), en(tpf.wcs.pixel_to_world(px, py + 1))])
    for win in (0.5, 1.0, 1.5, 2.0, 3.0):
        for order in (1, 2):
            w = good & (np.abs(t - tc) < win)
            oot = w & (np.abs(t - tc) > DUR / 2 + 0.05)
            intr = w & (np.abs(t - tc) < 0.4 * DUR)
            out = []
            for y in (f, cx, cy):
                c = np.polyfit(t[oot] - tc, y[oot], order)
                r = y - np.polyval(c, t - tc)
                out.append((np.mean(r[intr]), np.std(r[oot]) / np.sqrt(intr.sum()), np.polyval(c, 0)))
            (df, sf, f0), (dx, sx, _), (dy, sy, _) = out
            depth = -df / f0
            src = -(J @ np.array([dx, dy])) / depth
            cov = J @ np.diag([sx ** 2, sy ** 2]) @ J.T / depth ** 2
            a = src @ dirB; sa = np.sqrt(dirB @ cov @ dirB)
            print(f"   +-{win:.1f} d, poly {order}: depth {depth * 1e6:4.0f} ppm; along A->B {a:+.2f} +- {sa:.2f}"
                  f" (A {(a - pA) / sa:+.1f} sigma, B {(a - pB) / sa:+.1f} sigma)")

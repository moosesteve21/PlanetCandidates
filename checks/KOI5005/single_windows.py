"""KOI-5005.01: how often does a single 4.74-h window anywhere in the Kepler PDCSAP data dip as deep as the events?
Same depth method as events.py, on a grid of window centres every 0.1 d in every quarter (transits excluded)."""
import glob
import numpy as np
import lightkurve as lk

P, T0, DUR = 251.958533, 367.3803, 4.742 / 24
exec(open("events.py").read().split("for col in")[0].split("rng =")[1].split("\n", 1)[1])
vals = []
for f_ in sorted(glob.glob("kepler/**/*llc.fits", recursive=True)):
    lc = lk.read(f_, quality_bitmask="default")
    t = lc.time.value; x = lc.pdcsap_flux
    f = np.where(np.ma.getmaskarray(x.mask), np.nan, np.asarray(x.unmasked.value, float))
    ok = np.isfinite(t) & np.isfinite(f)
    for tc in np.arange(np.nanmin(t[ok]) + 1.1, np.nanmax(t[ok]) - 1.1, 0.1):
        if np.min(np.abs(tc - (T0 + np.arange(-1, 7) * P))) < 1.2:
            continue
        d, s = depth(t, f, tc)
        if np.isfinite(d):
            vals.append(d)
v = np.array(vals)
print(f"{len(v)} windows; sd {v.std() * 1e6:.0f} ppm (robust {1.4826 * np.median(np.abs(v - np.median(v))) * 1e6:.0f})")
for thr in (100, 150, 179, 200, 239):
    print(f"   >= {thr} ppm: {np.sum(v >= thr * 1e-6)} ({np.mean(v >= thr * 1e-6):.5f}); <= -{thr}: {np.sum(v <= -thr * 1e-6)}")

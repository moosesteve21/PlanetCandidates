import numpy as np, lightkurve as lk, warnings, matplotlib; warnings.filterwarnings("ignore"); matplotlib.use("Agg")
import matplotlib.pyplot as plt
d=np.load("lc.npz"); t,f,s=d["t"],d["f"],d["s"]
per=[]
for sec in sorted(set(s)):
    q=s==sec; lc=lk.LightCurve(time=t[q],flux=f[q]).bin(time_bin_size=0.02)
    pg=lc.to_periodogram(minimum_period=1,maximum_period=15,oversample_factor=10); P=pg.period_at_max_power.value
    per.append((sec,P,np.nanpercentile(f[q],95)-np.nanpercentile(f[q],5)))
per=np.array(per)
for r in per: print("S%d %.3f d  %.0f ppt"%(r[0],r[1],r[2]*1e3))
main=per[per[:,1]>4.5,1]; print("rotation: median %.2f d, range %.2f-%.2f (n=%d; %d sectors peak at half)"%(np.median(main),main.min(),main.max(),len(main),np.sum(per[:,1]<4.5)))
fig,ax=plt.subplots(3,1,figsize=(12,10),gridspec_kw=dict(height_ratios=[1,1,0.8]))
for a,sec in ((ax[0],98),(ax[1],67)):
    q=s==sec; a.plot(t[q],f[q],'k.',ms=0.6); a.set_ylim(0.93,1.10); a.set_ylabel("relative flux")
    a.set_title(f"TIC 382043650 (UCAC4 180-005635), SPOC 2-min PDCSAP, Sector {sec}")
ax[1].set_xlabel("BTJD")
ax[2].plot(per[:,0],per[:,1],'o'); ax[2].set(xlabel="TESS sector",ylabel="strongest period (d)",title="Lomb-Scargle peak per sector (1-15 d)",ylim=(0,8))
plt.tight_layout(); plt.savefig("TIC382043650_rotation.png",dpi=100)

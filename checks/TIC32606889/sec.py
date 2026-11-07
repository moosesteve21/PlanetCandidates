import lightkurve as lk, numpy as np, warnings; warnings.filterwarnings("ignore")
P,T0=4.686804,1440.91927
sr=lk.search_lightcurve("TIC 32606889"); t=[];f=[]
for a in ("SPOC","TESS-SPOC"):
    for lc in sr[sr.author==a].download_all(flux_column="pdcsap_flux"):
        lc=lc.remove_nans().normalize()
        ph=((lc.time.value-T0)/P)%1; m=(ph>0.05)&(ph<0.95)
        fl=lc.flatten(window_length=721 if a=="SPOC" else (73 if lc.sector<20 else 217),mask=~m)
        t+=list(fl.time.value); f+=list(np.asarray(fl.flux.value,dtype=float))
t=np.array(t);f=np.array(f);ph=((t-T0)/P)%1
w=4.0/24/P
best=[]
for c in np.arange(0.2,0.8,0.005):
    i=np.abs(ph-c)<w/2; o=(np.abs(ph-c)>w)&(np.abs(ph-c)<2.5*w)
    d=np.median(f[o])-np.mean(f[i]); e=np.std(f[i])/np.sqrt(i.sum()); best.append((d/e,c,d,e))
best.sort(reverse=True)
for b in best[:3]: print("phase %.3f depth %4.0f +- %3.0f ppm (%.1f sigma)"%(b[1],b[2]*1e6,b[3]*1e6,b[0]))
i=np.abs(ph-0.5)<w/2; o=(np.abs(ph-0.5)>w)&(np.abs(ph-0.5)<2.5*w)
print("at 0.500: %.0f +- %.0f ppm"%((np.median(f[o])-np.mean(f[i]))*1e6,np.std(f[i])/np.sqrt(i.sum())*1e6))
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
c=0.445
for name,sel in (("S5-33 (FFI)",t<3000),("S98+107 (2-min)",t>3000)):
    i=np.abs(ph-c)<w/2; o=(np.abs(ph-c)>w)&(np.abs(ph-c)<2.5*w)
    print(name,"%.0f +- %.0f ppm"%((np.median(f[o&sel])-np.mean(f[i&sel]))*1e6,np.std(f[i&sel])/np.sqrt((i&sel).sum())*1e6))
fig,ax=plt.subplots(1,2,figsize=(12,4.2))
def binned(x,y,edges):
    k=np.digitize(x,edges); xb=[];yb=[];eb=[]
    for j in range(1,len(edges)):
        m=k==j
        if m.sum()>5: xb.append(x[m].mean()); yb.append(np.mean(y[m])); eb.append(np.std(y[m])/np.sqrt(m.sum()))
    return np.array(xb),np.array(yb),np.array(eb)
hp=((ph+0.5)%1-0.5)*P*24
m=np.abs(hp)<8
ax[0].plot(hp[m],(f[m]-1)*1e3,'.',color='0.8',ms=1)
xb,yb,eb=binned(hp[m],(f[m]-1)*1e3,np.arange(-8,8.01,0.25)); ax[0].errorbar(xb,yb,eb,fmt='o',ms=3,color='C0')
ax[0].set(xlabel="hours from primary eclipse",ylabel="relative flux (ppt)",title=f"TIC 32606889 primary: P = {P} d, ~12 ppt")
sp=(ph-c)*P*24; m=np.abs(sp)<12
xb,yb,eb=binned(sp[m],(f[m]-1)*1e3,np.arange(-12,12.01,0.75)); ax[1].errorbar(xb,yb,eb,fmt='o',ms=3,color='C3')
ax[1].axhline(0,color='0.6',lw=0.8); ax[1].axvline(0,color='0.6',ls=':',lw=0.8)
ax[1].set(xlabel=f"hours from phase {c}",ylabel="relative flux (ppt)",title=f"secondary eclipse at phase {c}: ~0.57 ppt (10 sigma)")
fig.text(0.5,0.005,"TESS SPOC 2-min (S98, S107) + TESS-SPOC FFI (S5, S6, S32, S33) PDCSAP, flattened with eclipses masked",ha="center",fontsize=8)
plt.tight_layout(rect=(0,0.03,1,1)); plt.savefig("TIC32606889_eclipses.png",dpi=110)

import numpy as np,wave,subprocess
sr=44100;T=76.0;n=int(sr*T);bpm=76;beat=60/bpm
L=np.zeros(n);R=np.zeros(n)
def hz(m):return 440*2**((m-69)/12)
def add(sig,t0,pan=0.5):
    i=int(t0*sr);j=min(n,i+len(sig))
    if i>=n:return
    L[i:j]+=sig[:j-i]*(1-pan);R[i:j]+=sig[:j-i]*pan
def pluck(f,dur,amp):
    t=np.arange(int(sr*dur))/sr
    s=sum(a*np.sin(2*np.pi*f*k*t) for k,a in [(1,1),(2,.35),(3,.15),(4,.06)])
    env=np.minimum(1,t/0.008)*np.exp(-t*2.6)
    return s*env*amp
def pad(f,dur,amp):
    t=np.arange(int(sr*dur))/sr
    s=np.sin(2*np.pi*f*t)+.5*np.sin(2*np.pi*f*2.003*t)+.3*np.sin(2*np.pi*f*.999*t)
    env=np.minimum(1,t/1.2)*np.minimum(1,(dur-t)/1.5)
    return s*env*amp
prog=[(48,[60,64,67,72]),(45,[57,64,69,72]),(41,[57,60,65,69]),(43,[55,62,67,71])]
bar=4*beat;nb=int(T/bar)+1
for b in range(nb):
    root,ch=prog[b%4];t0=b*bar
    add(pad(hz(root),bar+1.5,.10),t0,.5)
    for m in ch[:3]:add(pad(hz(m),bar+1.5,.045),t0,.4)
    add(pluck(hz(root),bar,.22),t0,.5)
    arp=[ch[0],ch[1],ch[2],ch[3],ch[2],ch[1],ch[2],ch[3]] if b%2==0 else [ch[0],ch[2],ch[1],ch[3],ch[1],ch[2],ch[3],ch[2]]
    for k,m in enumerate(arp):
        add(pluck(hz(m+12 if k%4==3 else m),1.8,.16),t0+k*beat/2,.35+.3*(k%2))
    if b>=4 and b%2==0:  # gentle melody
        mel=[ch[3],ch[2],ch[3],ch[1]]
        for k,m in enumerate(mel):add(pluck(hz(m+12),2.2,.12),t0+k*beat,.6)
x=np.stack([L,R],1)
fade=np.minimum(1,np.arange(n)/(sr*2.5))*np.minimum(1,(n-np.arange(n))/(sr*4))
x*=fade[:,None]
x/=np.abs(x).max()/0.8
w=wave.open('/tmp/bgm_dry.wav','wb');w.setnchannels(2);w.setsampwidth(2);w.setframerate(sr)
w.writeframes((x*32767).astype('<i2').tobytes());w.close()
subprocess.run(['ffmpeg','-y','-loglevel','error','-i','/tmp/bgm_dry.wav','-af','aecho=0.8:0.6:60|120:0.25|0.15,lowpass=f=6500,volume=0.9','/home/user/guoduren/assets/bgm.wav'],check=True)

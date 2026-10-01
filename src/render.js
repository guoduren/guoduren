const {chromium}=require('playwright');const {spawn}=require('child_process');
(async()=>{const FPS=24;
const b=await chromium.launch({executablePath:'/opt/pw-browsers/chromium'});
const p=await b.newPage({viewport:{width:720,height:1280}});
await p.goto('file:///home/user/guoduren/hpv-promo-video-portrait.html');
const T=await p.evaluate(()=>TOTAL_S);const N=Math.round(T*FPS);
const ff=spawn('ffmpeg',['-y','-loglevel','error','-f','image2pipe','-framerate',String(FPS),'-c:v','mjpeg','-i','-','-i','/home/user/guoduren/assets/bgm.mp3','-t',String(T),'-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p','-c:a','aac','-b:a','160k','-movflags','+faststart','-shortest','/home/user/guoduren/hpv-promo-video-portrait.mp4'],{stdio:['pipe','inherit','inherit']});
for(let f=0;f<N;f++){await p.evaluate(t=>seekTo(t),f/FPS);
 const buf=await p.screenshot({type:'jpeg',quality:93});
 if(!ff.stdin.write(buf))await new Promise(r=>ff.stdin.once('drain',r));
 if(f%120==0)console.log(f,N)}
ff.stdin.end();await new Promise(r=>ff.on('close',r));await b.close();console.log('done')})();

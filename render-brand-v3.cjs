const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
const sizes={'1x1':[1080,1080],'1x1hi':[1440,1440],'4x5':[1080,1350],'4x5hi':[1440,1800],'9x16m':[1080,1920],'9x16':[1080,1920],'9x16hi':[1440,2560],'191x1':[1200,628],'16x9':[1920,1080]};
(async()=>{
const b=await chromium.launch({headless:true,args:['--no-sandbox']});const dir=path.join(__dirname,'brand-v3-exports');fs.mkdirSync(dir,{recursive:true});let results=[];
for(const c of ['zoom','portrait','card'])for(const [f,[w,h]]of Object.entries(sizes)){
 if(process.env.HERO_ONLY&&f!=='4x5')continue;
 const p=await b.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});await p.goto('file://'+path.join(__dirname,'masterclass-brand-v3.html')+`?c=${c}&f=${f}`);await p.waitForFunction(()=>window.__ready);
 const proof=await p.evaluate(()=>{
 const els=[...document.querySelectorAll('.brand,.headline,.benefit,.speaker,.zoom-stage,.points,.price,.action,.event,.nameplate')].filter(e=>getComputedStyle(e).display!=='none');
 const overlaps=[];for(let i=0;i<els.length;i++)for(let j=i+1;j<els.length;j++){const a=els[i].getBoundingClientRect(),b=els[j].getBoundingClientRect();if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>3&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>3)overlaps.push([els[i].className,els[j].className]);}
 return{meta:window.__meta,images:[...document.images].every(i=>i.complete&&i.naturalWidth),fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family),overflows:els.filter(e=>e.scrollWidth>e.clientWidth+3).map(e=>e.className),overlaps};
 });
 const file=`${c}-${f}-${w}x${h}.png`;await p.screenshot({path:path.join(dir,file)});results.push({file,...proof});console.log(file,JSON.stringify(proof));await p.close();
}fs.writeFileSync(path.join(dir,'proof.json'),JSON.stringify(results,null,2));await b.close();
})();

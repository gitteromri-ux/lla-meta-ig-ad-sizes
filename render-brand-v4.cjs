const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
const sizes={'1x1':[1080,1080],'1x1hi':[1440,1440],'4x5':[1080,1350],'4x5hi':[1440,1800],'9x16m':[1080,1920],'9x16':[1080,1920],'9x16hi':[1440,2560],'191x1':[1200,628],'16x9':[1920,1080]};
(async()=>{
 const b=await chromium.launch({headless:true,args:['--no-sandbox']});
 const dir=path.join(__dirname,'brand-v4-exports');fs.mkdirSync(dir,{recursive:true});let results=[];
 for(const c of ['zoom','portrait','card'])for(const v of ['a','b'])for(const t of ['gold','blue','white'])for(const [f,[w,h]]of Object.entries(sizes)){
  if(process.env.HERO_ONLY&&(f!=='4x5'||t!=='blue'))continue;
  if(process.env.CHECK_ONLY&&t!=='blue')continue;
  if(process.env.ONLY&&`${c}-${v}`!==process.env.ONLY)continue;
  const p=await b.newPage();
  await p.setViewportSize({width:w,height:h});
  await p.goto('file://'+path.join(__dirname,'masterclass-brand-v4.html')+`?c=${c}&v=${v}&t=${t}&f=${f}`);
  await p.waitForFunction(()=>window.__ready);
  const proof=await p.evaluate(()=>{
   const els=[...document.querySelectorAll('.brand,.exclusive,.headline,.benefit,.speaker,.zoom-stage,.points,.price,.cta-group,.event,.nameplate')].filter(e=>getComputedStyle(e).display!=='none');
   const overlaps=[];
   for(let i=0;i<els.length;i++)for(let j=i+1;j<els.length;j++){const a=els[i].getBoundingClientRect(),b=els[j].getBoundingClientRect();if(Math.min(a.right,b.right)-Math.max(a.left,b.left)>3&&Math.min(a.bottom,b.bottom)-Math.max(a.top,b.top)>3)overlaps.push([els[i].className,els[j].className]);}
   return{meta:window.__meta,images:[...document.images].every(i=>i.complete&&i.naturalWidth),fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family),overflows:els.filter(e=>e.scrollWidth>e.clientWidth+3).map(e=>e.className),overlaps};
  });
  const file=`${c}-${v}-${t}-${f}-${w}x${h}.png`;
  await p.screenshot({path:path.join(dir,file)});results.push({file,...proof});
  if(proof.overlaps.length||proof.overflows.length||!proof.images)console.log(file,JSON.stringify(proof));
  await p.close();
 }
 const proofPath=path.join(dir,'proof.json');
 if(process.env.ONLY&&fs.existsSync(proofPath)){const prior=JSON.parse(fs.readFileSync(proofPath));const names=new Set(results.map(x=>x.file));results=[...prior.filter(x=>!names.has(x.file)),...results];}
 fs.writeFileSync(proofPath,JSON.stringify(results,null,2));console.log(JSON.stringify({renders:results.length,failures:results.filter(x=>x.overlaps.length||x.overflows.length||!x.images).length}));
 await b.close();
})();

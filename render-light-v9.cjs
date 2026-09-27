const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
(async()=>{
 const b=await chromium.launch({headless:true,args:['--no-sandbox']});
 const dir=path.join(__dirname,'light-v9-exports');fs.mkdirSync(dir,{recursive:true});const proof=[];
 for(const c of ['zoom','portrait','card'])for(const t of ['blue','gold','white']){
  if(process.env.PROOF_ONLY&&t!=='blue')continue;
  const p=await b.newPage({viewport:{width:1080,height:1350}});
  await p.goto('file://'+path.join(__dirname,'masterclass-light-v9.html')+`?c=${c}&t=${t}`);await p.waitForFunction(()=>window.__ready);
  const r=await p.evaluate(()=>{
   const m=document.querySelector('.message').getBoundingClientRect(),f=document.querySelector('figure').getBoundingClientRect();
   return {images:[...document.images].every(i=>i.complete&&i.naturalWidth),gapAboveImage:Math.round(f.top-m.bottom),overflow:[...document.querySelectorAll('.authority,.host,.dates,.join,footer')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.className||e.tagName),fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)};
  });
  const file=`${c}-${t}-1080x1350.png`;await p.screenshot({path:path.join(dir,file)});proof.push({file,...r});console.log(file,JSON.stringify(r));await p.close();
 }
 fs.writeFileSync(path.join(dir,'proof.json'),JSON.stringify(proof,null,2));await b.close();
})();

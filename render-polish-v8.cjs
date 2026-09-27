const{chromium}=require('playwright'),fs=require('fs'),path=require('path');
(async()=>{
const b=await chromium.launch({headless:true,args:['--no-sandbox']});const dir=path.join(__dirname,'polish-v8-exports');fs.mkdirSync(dir,{recursive:true});const proof=[];
for(const c of ['zoom','portrait','card'])for(const t of ['blue','gold','white']){
 if(process.env.PROOF_ONLY&&t!=='blue')continue;
 const p=await b.newPage({viewport:{width:1080,height:1350}});
 await p.goto('file://'+path.join(__dirname,'masterclass-polish-v8.html')+`?c=${c}&t=${t}`);await p.waitForFunction(()=>window.__ready);
 const result=await p.evaluate(()=>{
 const els=[...document.querySelectorAll('header,.message,footer')];const overlaps=[];
 for(let i=0;i<els.length;i++)for(let j=i+1;j<els.length;j++){const a=els[i].getBoundingClientRect(),b=els[j].getBoundingClientRect();if(Math.min(a.right,b.right)>Math.max(a.left,b.left)+2&&Math.min(a.bottom,b.bottom)>Math.max(a.top,b.top)+2)overlaps.push([els[i].className||els[i].tagName,els[j].className||els[j].tagName]);}
 return{images:[...document.images].every(i=>i.complete&&i.naturalWidth),overlaps,overflows:els.filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.className||e.tagName),allCaps:[...document.querySelectorAll('p,h1,header>span')].map(e=>e.innerText).filter(s=>/\b[A-Z]{2,}\b/.test(s)),fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>f.family)};
 });
 const file=`${c}-${t}-1080x1350.png`;await p.screenshot({path:path.join(dir,file)});proof.push({file,...result});console.log(file,JSON.stringify(result));await p.close();
}
fs.writeFileSync(path.join(dir,'proof.json'),JSON.stringify(proof,null,2));await b.close();
})();

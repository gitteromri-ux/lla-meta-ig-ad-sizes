const { chromium }=require('playwright');
const fs=require('fs'),path=require('path');
const sizes={'1x1':[1080,1080],'1x1hi':[1440,1440],'4x5':[1080,1350],'4x5hi':[1440,1800],'9x16m':[1080,1920],'9x16':[1080,1920],'9x16hi':[1440,2560],'191x1':[1200,628],'16x9':[1920,1080]};
(async()=>{
const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
const dir=path.join(__dirname,'review-exports');fs.mkdirSync(dir,{recursive:true});
const results=[];
for(const c of ['zoom','portrait','card'])for(const [f,[w,h]]of Object.entries(sizes)){
const page=await browser.newPage({viewport:{width:w,height:h},deviceScaleFactor:1});
await page.goto('file://'+path.join(__dirname,'masterclass-readable.html')+`?c=${c}&f=${f}`);
await page.waitForFunction(()=>window.__ready===true);
const proof=await page.evaluate(()=>({images:[...document.images].every(i=>i.complete&&i.naturalWidth),text:document.body.innerText,meta:window.__meta,overflows:[...document.querySelectorAll('h1,h2,.speaker,li,.dates,.offer')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.className||e.tagName)}));
const name=`${c}-${f}-${w}x${h}.png`;await page.screenshot({path:path.join(dir,name)});
results.push({file:name,...proof});await page.close();console.log(name,JSON.stringify(proof.overflows));
}
fs.writeFileSync(path.join(dir,'render-proof.json'),JSON.stringify(results,null,2));await browser.close();
})();

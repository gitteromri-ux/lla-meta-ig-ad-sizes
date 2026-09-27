const{chromium}=require('playwright'),fs=require('fs'),path=require('path');
(async()=>{const b=await chromium.launch({headless:true,args:['--no-sandbox']});const dir=path.join(__dirname,'original-corrected-exports');fs.mkdirSync(dir,{recursive:true});const results=[];
for(const c of ['7b','7c'])for(const [f,w,h] of [['4x5',1080,1350],['1x1',1080,1080],['9x16',1080,1920]]){
const p=await b.newPage({viewport:{width:w,height:h}});await p.goto('file://'+path.join(__dirname,`masterclass-${c}.html`)+`?b=julie&f=${f}`);await p.waitForFunction(()=>window.__ready&&window.__refined);
const result=await p.evaluate(()=>({fit:window.__meta.fits,price79:document.body.innerText.includes('$79'),vip:/\bVIP\b/.test(document.body.innerText),bullets:document.querySelectorAll('#bul>div').length,overflow:[...document.querySelectorAll('.sub,#pl,#sp,#bul,.price')].filter(e=>e.scrollWidth>e.clientWidth+2).map(e=>e.id||e.className)}));
const file=`${c}-${w}x${h}.png`;await p.screenshot({path:path.join(dir,file)});results.push({file,...result});console.log(file,JSON.stringify(result));await p.close();
}fs.writeFileSync(path.join(dir,'proof.json'),JSON.stringify(results,null,2));await b.close()})();

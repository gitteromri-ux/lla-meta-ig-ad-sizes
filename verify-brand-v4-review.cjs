const {chromium}=require('playwright'),fs=require('fs'),path=require('path');
(async()=>{
 const b=await chromium.launch({headless:true,args:['--no-sandbox']});
 const p=await b.newPage({viewport:{width:1440,height:1250}});
 await p.goto('file:///home/user/workspace/julie-banner-readable-preview/index.html');
 await p.evaluate(()=>document.fonts.ready);
 let checks=[];
 for(const v of ['a','b'])for(const t of ['gold','blue','white'])for(const f of ['4x5hi-1440x1800','1x1hi-1440x1440','9x16hi-1440x2560','191x1-1200x628','16x9-1920x1080']){
  for(const [g,x]of [['v',v],['t',t],['f',f]])await p.locator(`[data-group="${g}"] [data-value="${x}"]`).click();
  await p.waitForFunction(()=>[...document.querySelectorAll('main img')].every(i=>i.complete&&i.naturalWidth>0));
  checks.push({v,t,f,ok:await p.evaluate(()=>document.documentElement.scrollWidth===innerWidth)});
 }
 for(const [g,x]of [['v','a'],['t','blue'],['f','4x5hi-1440x1800']])await p.locator(`[data-group="${g}"] [data-value="${x}"]`).click();
 await p.waitForFunction(()=>[...document.querySelectorAll('main img')].every(i=>i.complete&&i.naturalWidth>0));
 const out=path.join(__dirname,'brand-v4-exports');
 await p.screenshot({path:path.join(out,'review-desktop.png'),fullPage:true});
 await p.setViewportSize({width:390,height:844});
 await p.screenshot({path:path.join(out,'review-mobile.png'),fullPage:true});
 const mobile=await p.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
 fs.writeFileSync(path.join(out,'review-checks.json'),JSON.stringify({checks,mobile},null,2));
 console.log(JSON.stringify({combinations:checks.length,failed:checks.filter(x=>!x.ok).length,mobile}));
 await b.close();
})();

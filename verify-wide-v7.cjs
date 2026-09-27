const{chromium}=require('playwright'),path=require('path');
(async()=>{
 const b=await chromium.launch({headless:true,args:['--no-sandbox']});const p=await b.newPage({viewport:{width:1440,height:1200}});
 await p.goto('file:///home/user/workspace/julie-banner-readable-preview/index.html');await p.evaluate(()=>document.fonts.ready);
 for(const t of ['gold','white','blue']){await p.click(`[data-tone="${t}"]`);await p.waitForFunction(()=>[...document.querySelectorAll('main img')].every(i=>i.complete&&i.naturalWidth===1080))}
 await p.screenshot({path:path.join(__dirname,'wide-v7-exports/review-desktop.png'),fullPage:true});await p.setViewportSize({width:390,height:844});
 await p.screenshot({path:path.join(__dirname,'wide-v7-exports/review-mobile.png'),fullPage:true});
 console.log({colors:3,mobileOverflow:await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)});await b.close();
})();

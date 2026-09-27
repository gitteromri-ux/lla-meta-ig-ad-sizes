const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
(async()=>{
 const browser=await chromium.launch({headless:true,args:['--no-sandbox']});
 const page=await browser.newPage({viewport:{width:1440,height:1100}});
 const url='file:///home/user/workspace/julie-banner-readable-preview/index.html';
 await page.goto(url); await page.evaluate(()=>document.fonts.ready);
 const results=[];
 for(const f of ['4x5hi-1440x1800','1x1hi-1440x1440','9x16hi-1440x2560','191x1-1200x628','16x9-1920x1080']){
  await page.click(`[data-f="${f}"]`);
  await page.waitForFunction(()=>[...document.querySelectorAll('main img')].every(i=>i.complete&&i.naturalWidth>0));
  results.push(await page.evaluate(()=>({selected:document.querySelector('[aria-pressed="true"]').dataset.f,images:[...document.querySelectorAll('main img')].map(i=>({src:i.getAttribute('src'),width:i.naturalWidth,height:i.naturalHeight})),overflow:document.documentElement.scrollWidth>innerWidth})));
 }
 await page.click('[data-f="4x5hi-1440x1800"]');
 await page.waitForFunction(()=>[...document.querySelectorAll('main img')].every(i=>i.complete&&i.naturalWidth===1440));
 await page.screenshot({path:path.join(__dirname,'brand-v3-exports/review-desktop.png'),fullPage:true});
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:path.join(__dirname,'brand-v3-exports/review-mobile.png'),fullPage:true});
 const mobile=await page.evaluate(()=>({width:innerWidth,scrollWidth:document.documentElement.scrollWidth}));
 fs.writeFileSync(path.join(__dirname,'brand-v3-exports/review-checks.json'),JSON.stringify({results,mobile},null,2));
 console.log(JSON.stringify({formats:results.length,missingImages:results.flatMap(x=>x.images).filter(x=>!x.width),overflow:results.some(x=>x.overflow),mobile}));
 await browser.close();
})();

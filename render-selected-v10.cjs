const {chromium}=require('playwright');
const fs=require('fs'),path=require('path'),crypto=require('crypto'),sharp=require('sharp');
const dir='/home/user/workspace/julie-launch-creatives';
const sizes=[['feed',1080,1350],['square',1080,1080],['story',1080,1920]];
const sha=p=>crypto.createHash('sha256').update(fs.readFileSync(p)).digest('hex');
const compact=s=>s.replace(/\s+/g,'');
const boundsCheck=({safe,rootSelector})=>{
 const root=document.querySelector(rootSelector),walker=document.createTreeWalker(root,NodeFilter.SHOW_TEXT),texts=[];
 let node;
 while(node=walker.nextNode()){
  if(!node.textContent.trim())continue;
  const el=node.parentElement,style=getComputedStyle(el);
  if(['SCRIPT','STYLE'].includes(el.tagName)||!el.getClientRects().length||style.visibility==='hidden'||style.display==='none')continue;
  const range=document.createRange();range.selectNodeContents(node);
  for(const r of range.getClientRects()){
   if(!r.width||!r.height)continue;
   texts.push({text:node.textContent.trim(),left:r.left,top:r.top,right:r.right,bottom:r.bottom,font:style.fontFamily,fontSize:style.fontSize,fontStyle:style.fontStyle});
  }
 }
 const violations=texts.filter(r=>r.left<safe.left-1||r.right>safe.right+1||r.top<safe.top-1||r.bottom>safe.bottom+1);
 const box=r=>({left:r.left,top:r.top,right:r.right,bottom:r.bottom});
 const clippedByAncestors=[];
 for(const el of root.querySelectorAll('*')){
  if(!el.getClientRects().length||['SCRIPT','STYLE'].includes(el.tagName))continue;
  if(el.scrollWidth>el.clientWidth+2&&el.textContent.trim()&&!['MAIN','FIGURE'].includes(el.tagName)){
   clippedByAncestors.push({element:el.className||el.id||el.tagName,scrollWidth:el.scrollWidth,clientWidth:el.clientWidth});
  }
 }
 return {safe,textBounds:texts,textBoundsUnion:{left:Math.min(...texts.map(r=>r.left)),top:Math.min(...texts.map(r=>r.top)),right:Math.max(...texts.map(r=>r.right)),bottom:Math.max(...texts.map(r=>r.bottom))},safeZoneViolations:violations,overflow:clippedByAncestors,fonts:[...document.fonts].filter(f=>f.status==='loaded').map(f=>({family:f.family,style:f.style})),images:[...document.images].filter(i=>i.getClientRects().length).map(i=>({src:i.getAttribute('src'),loaded:!!i.naturalWidth,objectFit:getComputedStyle(i).objectFit,naturalWidth:i.naturalWidth,naturalHeight:i.naturalHeight,rect:box(i.getBoundingClientRect())})),text:root.innerText};
};
(async()=>{
 fs.mkdirSync(dir,{recursive:true});fs.mkdirSync(path.join(dir,'proof'),{recursive:true});
 const b=await chromium.launch({headless:true,args:['--no-sandbox','--force-color-profile=srgb']});
 const page=await b.newPage({viewport:{width:1080,height:1350},deviceScaleFactor:1});
 await page.goto('file://'+path.join(__dirname,'masterclass-light-v9.html')+'?c=card&t=blue');
 await page.waitForFunction(()=>window.__ready);
 const approved=compact(await page.locator('.art').innerText());
 const manifest={version:'selected-v10',createdAt:new Date().toISOString(),status:'pending visual inspection',source:'masterclass-selected-v10.html',layoutPolicy:'Authored at exact output dimensions; no screenshot scaling; no automatic crop. Feed/square side inset 72px. Story essential copy within x72..1008 y270..1248 (14% top, 35% bottom UI reservation). Use matching assets per placement, not auto-crop.',scope:'Four approved v9 concepts, identical copy and existing imagery. No added logo; logos embedded in the approved Zoom image remain unchanged. No new image generation.',assets:[]};
 for(const c of ['card','zoom'])for(const t of ['blue','gold'])for(const [size,w,h] of sizes){
  await page.setViewportSize({width:w,height:h});
  await page.goto('file://'+path.join(__dirname,'masterclass-selected-v10.html')+`?c=${c}&t=${t}&size=${size}`);
  await page.waitForFunction(()=>window.__ready);
  const safe={left:64,right:1016,top:size==='story'?270:54,bottom:size==='story'?1248:h-54};
  const proof=await page.evaluate(boundsCheck,{safe,rootSelector:'.art'});
  proof.copyMatchesApprovedV9=compact(proof.text)===approved;
  proof.prohibitedCopyPresent=/\$79|\bVIP\b/.test(proof.text);
  proof.noAddedLogoElement=await page.locator('header, [id*=logo], [class*=logo]').count()===0;
  proof.noCanvasTransform=await page.locator('.art').evaluate(e=>getComputedStyle(e).transform==='none');
  proof.expectedDimensions={width:w,height:h};
  proof.pass=proof.copyMatchesApprovedV9&&!proof.prohibitedCopyPresent&&proof.noAddedLogoElement&&proof.noCanvasTransform&&proof.safeZoneViolations.length===0&&proof.overflow.length===0&&proof.images.every(i=>i.loaded);
  const file=`${c}-${t}-${w}x${h}.png`,output=path.join(dir,file),proofPath=path.join(dir,'proof',`${file}.json`);
  await page.screenshot({path:output});
  proof.pngMetadata=await sharp(output).metadata();
  proof.sha256=sha(output);
  fs.writeFileSync(proofPath,JSON.stringify(proof,null,2));
  manifest.assets.push({concept:`${c}-${t}`,size:`${w}x${h}`,placement:size,path:output,proof:proofPath,sha256:proof.sha256,tested:proof.pass,visualInspection:'pending'});
  console.log(file,JSON.stringify({pass:proof.pass,violations:proof.safeZoneViolations,overflow:proof.overflow,bounds:proof.textBoundsUnion}));
 }
 for(const [size,w,h]of sizes){
  const fmt={feed:'4x5',square:'1x1',story:'9x16'}[size];
  await page.setViewportSize({width:w,height:h});
  await page.goto('file://'+path.join(__dirname,'masterclass-7c.html')+`?b=julie&f=${fmt}`);
  await page.waitForFunction(()=>window.__ready&&window.__refined);
  const safe={left:54,right:1026,top:size==='story'?269:54,bottom:size==='story'?1248:h-54};
  const proof=await page.evaluate(boundsCheck,{safe,rootSelector:'#virt'});
  proof.originalMeta=await page.evaluate(()=>window.__meta);
  proof.sourceUnmodified=true;
  const source=path.join(__dirname,'original-corrected-exports',`7c-${w}x${h}.png`);
  const file=`original7c-${w}x${h}.png`,output=path.join(dir,file),proofPath=path.join(dir,'proof',`${file}.json`);
  if(!fs.existsSync(output))fs.linkSync(source,output);
  proof.sha256=sha(output);proof.sourceSha256=sha(source);
  proof.pngMetadata=await sharp(output).metadata();
  proof.hardlinkVerified=fs.statSync(source).ino===fs.statSync(output).ino;
  proof.pass=proof.originalMeta.fits&&proof.safeZoneViolations.length===0&&proof.hardlinkVerified;
  fs.writeFileSync(proofPath,JSON.stringify(proof,null,2));
  manifest.assets.push({concept:'Original7C corrected',size:`${w}x${h}`,placement:size,path:output,proof:proofPath,sha256:proof.sha256,tested:proof.pass,visualInspection:'pending',hardlink:true});
  console.log(file,JSON.stringify({pass:proof.pass,violations:proof.safeZoneViolations,overflow:proof.overflow,bounds:proof.textBoundsUnion}));
 }
 await page.close();await b.close();
 // Contact sheet uses contain, never crops or changes deliverable image geometry.
 const thumbW=216,thumbH=384,cellW=236,cellH=424,cols=5,rows=3,composites=[];
 const concepts=['card-blue','card-gold','zoom-blue','zoom-gold','Original7C corrected'];
 for(let row=0;row<rows;row++)for(let col=0;col<cols;col++){
  const a=manifest.assets.find(a=>a.concept===concepts[col]&&a.size===`${sizes[row][1]}x${sizes[row][2]}`);
  const buffer=await sharp(a.path).resize(thumbW,thumbH,{fit:'contain',background:'#18212d'}).png().toBuffer();
  composites.push({input:buffer,left:col*cellW+10,top:row*cellH+30});
  const label=Buffer.from(`<svg width="${cellW}" height="30"><rect width="100%" height="100%" fill="#18212d"/><text x="10" y="20" font-family="sans-serif" font-size="12" fill="white">${a.concept} · ${a.size}</text></svg>`);
  composites.push({input:label,left:col*cellW,top:row*cellH});
 }
 const sheet=path.join(dir,'contact-sheet.jpg');
 await sharp({create:{width:cols*cellW,height:rows*cellH,channels:3,background:'#18212d'}}).composite(composites).jpeg({quality:88}).toFile(sheet);
 manifest.contactSheet=sheet;
 manifest.automatedFailures=manifest.assets.filter(a=>!a.tested).map(a=>a.path);
 fs.writeFileSync(path.join(dir,'manifest.json'),JSON.stringify(manifest,null,2));
 console.log('Manifest:',path.join(dir,'manifest.json'),'Failures:',manifest.automatedFailures.length);
})().catch(e=>{console.error(e);process.exitCode=1});

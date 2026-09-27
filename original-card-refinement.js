(()=>{
document.body.classList.toggle('gold',Boolean(document.querySelector('.sub')));
const sub=document.querySelector('.sub')||document.querySelector('#pl');
sub.innerHTML='<span>The world’s 2nd slowest ager</span><span>reveals her protocol.</span>';
const card=document.querySelector('#card');
const lastImage=card.querySelector('.zoom')||card.querySelector('#zoomwrap');
let next=lastImage.nextElementSibling;
while(next){const after=next.nextElementSibling;next.remove();next=after;}
const offer=document.createElement('section');offer.className='offer';
offer.innerHTML='<div class="offer-benefits"><div><strong>60 minutes</strong><span>Live on Zoom with Julie</span></div><div><strong>Her daily protocol</strong><span>Learn to age slower</span></div></div><div class="offer-dates"><span>Oct 27 · 7 pm eastern</span><em>or</em><span>Nov 14 · 1 pm eastern</span></div><div class="offer-action"><div class="offer-price">Starting at just $49<span>Limited seats</span></div><div class="offer-cta">Reserve your seat</div></div>';
card.append(offer);
window.__ready=false;
document.fonts.ready.then(()=>requestAnimationFrame(()=>{layout();window.__ready=true;window.__refined=true;}));
})();

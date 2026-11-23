// 地図のピン → 該当ツアーカードへ
document.querySelectorAll('.pin-g').forEach(g => {
  const go = () => {
    const card = document.getElementById('card-' + g.dataset.target);
    if (!card) return;
    card.scrollIntoView({ behavior: 'smooth', block: 'center' });
    card.classList.add('flash');
    setTimeout(() => card.classList.remove('flash'), 1600);
  };
  g.addEventListener('click', go);
  g.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); go(); } });
});

// 上部スライドショー（8枚・自動切替）
(() => {
  const slides = [...document.querySelectorAll('.slide')];
  const dots = [...document.querySelectorAll('.dot-btn')];
  if (slides.length < 2) return;
  let i = 0, timer = null;
  const show = n => {
    slides[i].classList.remove('on'); dots[i].classList.remove('on');
    i = (n + slides.length) % slides.length;
    slides[i].classList.add('on'); dots[i].classList.add('on');
  };
  const start = () => { stop(); timer = setInterval(() => show(i + 1), 4000); };
  const stop = () => { if (timer) clearInterval(timer); timer = null; };
  dots.forEach(d => d.addEventListener('click', () => { show(Number(d.dataset.i)); start(); }));
  // スワイプ
  let x0 = null;
  const box = document.querySelector('.slides');
  box.addEventListener('touchstart', ev => { x0 = ev.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', ev => {
    if (x0 === null) return;
    const dx = ev.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) { show(i + (dx < 0 ? 1 : -1)); start(); }
  });
  document.addEventListener('visibilitychange', () => (document.hidden ? stop() : start()));
  if (!window.matchMedia('(prefers-reduced-motion: reduce)').matches) start();
})();

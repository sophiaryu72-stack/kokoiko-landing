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

// 募集状況（テストモードのみデモ表示。実データ連携後に差し替え）
(async () => {
  const cfg = await KOKOIKO.getConfig();
  if (!cfg.testMode) return;
  const K = KOKOIKO;
  const d = new Date(K.kstToday());
  for (let i = 0; i < 40; i++) {
    d.setUTCDate(d.getUTCDate() + 1);
    const s = K.ymd(d);
    if (d.getUTCDay() === 6 && K.isBookable(s)) {
      const a = K.demoAvailability(window.PRODUCT_ID, s);
      const box = document.querySelector('.demo-status');
      box.classList.remove('hidden');
      box.querySelector('.progress span').style.width = (a.booked / K.GROUP_SIZE_MIN * 100) + '%';
      box.querySelector('.demo-text').textContent = `${K.fmtDate(s)}出発：いま${a.booked}名・あと約${a.remainGroups}組で出発確定`;
      break;
    }
  }
})();

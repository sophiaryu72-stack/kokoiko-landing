(async () => {
  const K = KOKOIKO;
  const $ = s => document.querySelector(s);
  const q = new URLSearchParams(location.search);
  const paymentKey = q.get('paymentKey'), orderId = q.get('orderId'), amount = q.get('amount');
  let booking = {};
  try { booking = JSON.parse(sessionStorage.getItem('kokoiko_booking') || '{}'); } catch (e) {}

  function fail(msg, pid) {
    $('#loading').classList.add('hidden');
    $('#ng').classList.remove('hidden');
    $('#ng-msg').textContent = msg;
    $('#retry').href = (pid || booking.productId) ? `checkout.html?p=${pid || booking.productId}` : 'index.html';
  }
  if (!paymentKey || !orderId || !amount) return fail('お支払い情報が見つかりませんでした。');

  // 再読み込みで二重承認しないよう、承認結果を保存しておく
  const cacheKey = 'kokoiko_done_' + orderId;
  let result = null;
  try { result = JSON.parse(sessionStorage.getItem(cacheKey) || 'null'); } catch (e) {}
  if (!result) {
    try {
      const r = await fetch('/api/confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ paymentKey, orderId, amount: Number(amount) }) });
      const j = await r.json();
      if (!r.ok) return fail(`${j.message || 'お支払いを確認できませんでした。'}${j.code ? `（${j.code}）` : ''}`);
      result = j;
      sessionStorage.setItem(cacheKey, JSON.stringify(j));
      sessionStorage.removeItem('kokoiko_form');
    } catch (e) {
      return fail('通信エラーが発生しました。時間をおいて再度お試しください。');
    }
  }

  const o = result.order, p = K.products[o.productId];
  const people = [`大人${o.adults}名`, o.children ? `子供${o.children}名` : '', o.infants ? `幼児${o.infants}名` : ''].filter(Boolean).join('・');
  const rows = [
    ['ツアー', p ? p.name : result.orderName],
    ['日程', `${K.fmtDate(o.date, true)} 07:30 集合`],
    ['人数', people],
    ['お支払い', K.fmtKRW(result.totalAmount)],
    ['注文番号', result.orderId],
  ];
  if (booking.lineId && booking.orderId === result.orderId) rows.push(['ご連絡先LINE', booking.lineId]);
  $('#summary').innerHTML = rows.map(([k, v]) => `<dt>${k}</dt><dd>${String(v).replace(/</g, '&lt;')}</dd>`).join('');
  $('#loading').classList.add('hidden');
  $('#done').classList.remove('hidden');

  const cfg = await K.getConfig();
  if (cfg.testMode) {
    const a = K.demoAvailability(o.productId, o.date);
    $('#demo-text').textContent = `${K.fmtDate(o.date)}出発の募集状況：あと約${a.remainGroups}組で出発確定`;
    $('#demo-box').classList.remove('hidden');
  }
})();

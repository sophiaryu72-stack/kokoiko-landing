(async () => {
  const K = KOKOIKO, T = K.T;
  const $ = s => document.querySelector(s);
  const q = new URLSearchParams(location.search);
  const paymentKey = q.get('paymentKey'), orderId = q.get('orderId'), amount = q.get('amount');
  let booking = {};
  try { booking = JSON.parse(sessionStorage.getItem('kokoiko_booking') || '{}'); } catch (e) {}

  function fail(msg) {
    $('#loading').classList.add('hidden');
    $('#ng').classList.remove('hidden');
    $('#ng-msg').textContent = msg;
    $('#retry').href = booking.productId ? `checkout.html?p=${booking.productId}` : 'index.html';
  }
  if (!paymentKey || !orderId || !amount) return fail(T.noPayInfo);

  // 再読み込みで二重承認しないよう、承認結果を保存しておく
  const cacheKey = 'kokoiko_done_' + orderId;
  let result = null;
  try { result = JSON.parse(sessionStorage.getItem(cacheKey) || 'null'); } catch (e) {}
  if (!result) {
    try {
      const r = await fetch('/api/confirm', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ paymentKey, orderId, amount: Number(amount) }) });
      const j = await r.json();
      if (!r.ok) return fail(`${K.errMsg(j.code, j.message || T.confirmFail)}${j.code ? ` (${j.code})` : ''}`);
      result = j;
      sessionStorage.setItem(cacheKey, JSON.stringify(j));
      sessionStorage.removeItem('kokoiko_form');
    } catch (e) {
      return fail(T.network);
    }
  }

  const o = result.order;
  const rows = [
    [T.sum.tour, K.productName(o.productId) || result.orderName],
    [T.sum.date, K.fmtDate(o.date, true) + T.sum.meet],
    [T.sum.people, T.people(o.adults, o.children, o.infants)],
    [T.sum.paid, K.fmtKRW(result.totalAmount)],
    [T.sum.order, result.orderId],
  ];
  if (booking.lineId && booking.orderId === result.orderId) rows.push([T.sum.line, booking.lineId]);
  const esc = v => String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;');
  $('#summary').innerHTML = rows.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('');
  $('#loading').classList.add('hidden');
  $('#done').classList.remove('hidden');

  const cfg = await K.getConfig();
  if (cfg.testMode) {
    const a = K.demoAvailability(o.productId, o.date);
    $('#demo-text').textContent = T.demoSuccess(K.fmtDate(o.date), a.remainGroups);
    $('#demo-box').classList.remove('hidden');
  }
})();

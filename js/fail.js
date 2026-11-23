(() => {
  const K = KOKOIKO;
  const q = new URLSearchParams(location.search);
  const code = q.get('code'), msg = q.get('message');
  // 未知のコードは決済会社の原文（韓国語）を出さず、各言語の汎用メッセージのまま
  const known = code && K.T.err[code];
  if (known) document.getElementById('f-msg').textContent = known;
  if (code) document.getElementById('f-code').textContent = K.T.errCode + code;
  let pid = null;
  try { pid = (JSON.parse(sessionStorage.getItem('kokoiko_form') || '{}')).productId; } catch (e) {}
  document.getElementById('retry').href = pid ? `checkout.html?p=${pid}` : 'index.html';
})();

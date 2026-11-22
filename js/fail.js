(() => {
  const K = KOKOIKO;
  const q = new URLSearchParams(location.search);
  const code = q.get('code'), msg = q.get('message');
  const known = code && K.T.err[code];
  if (known || msg) document.getElementById('f-msg').textContent = known || msg;
  if (code) document.getElementById('f-code').textContent = K.T.errCode + code;
  let pid = null;
  try { pid = (JSON.parse(sessionStorage.getItem('kokoiko_form') || '{}')).productId; } catch (e) {}
  document.getElementById('retry').href = pid ? `checkout.html?p=${pid}` : 'index.html';
})();

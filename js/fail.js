(() => {
  const q = new URLSearchParams(location.search);
  const code = q.get('code'), msg = q.get('message');
  if (msg) document.getElementById('f-msg').textContent = msg;
  if (code) document.getElementById('f-code').textContent = 'エラーコード：' + code;
  let pid = null;
  try { pid = (JSON.parse(sessionStorage.getItem('kokoiko_form') || '{}')).productId; } catch (e) {}
  document.getElementById('retry').href = pid ? `checkout.html?p=${pid}` : 'index.html';
})();

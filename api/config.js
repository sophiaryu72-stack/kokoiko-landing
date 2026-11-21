// ブラウザに渡してよいのはクライアントキーだけ。
module.exports = (req, res) => {
  const clientKey = process.env.TOSS_CLIENT_KEY || '';
  res.setHeader('Cache-Control', 'no-store');
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify({ clientKey, testMode: clientKey.startsWith('test_') }));
};

// 決済承認。シークレットキーはここ（サーバー）でだけ使う。
const { calcAmount, parseOrderId, readJson, send } = require('./_lib');

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { message: 'Method Not Allowed' });
  let body;
  try { body = await readJson(req); } catch { return send(res, 400, { code: 'BAD_REQUEST', message: '不正なリクエストです' }); }
  const { paymentKey, orderId } = body;
  const order = parseOrderId(orderId);
  if (!paymentKey || !order) return send(res, 400, { code: 'INVALID_ORDER', message: '注文情報を確認できませんでした' });

  // 金額の検証：ブラウザから来た amount ではなく、サーバーの価格表で計算した金額と比べる
  const expected = calcAmount(order.product, order.adults, order.children);
  if (Number(body.amount) !== expected) {
    return send(res, 400, { code: 'AMOUNT_MISMATCH', message: 'お支払い金額が正しくありません。決済は承認されていません。' });
  }

  const secret = process.env.TOSS_SECRET_KEY;
  if (!secret) return send(res, 500, { code: 'CONFIG', message: 'サーバー設定エラー（キー未設定）' });

  try {
    const r = await fetch('https://api.tosspayments.com/v1/payments/confirm', {
      method: 'POST',
      headers: {
        Authorization: 'Basic ' + Buffer.from(secret + ':').toString('base64'),
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ paymentKey, orderId, amount: expected }),
    });
    const data = await r.json();
    if (!r.ok) return send(res, r.status, { code: data.code, message: data.message });
    return send(res, 200, {
      orderId: data.orderId,
      orderName: data.orderName,
      totalAmount: data.totalAmount,
      method: data.method,
      approvedAt: data.approvedAt,
      order: { productId: order.product.id, date: order.date, adults: order.adults, children: order.children, infants: order.infants },
    });
  } catch (e) {
    return send(res, 502, { code: 'NETWORK', message: '決済サーバーに接続できませんでした' });
  }
};

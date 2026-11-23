// 注文を作る。金額はブラウザから受け取らず、サーバーの価格表で決める。
const { PRODUCTS, MAX_PER_TYPE, HOLIDAYS, calcAmount, makeOrderId, readJson, send } = require('./_lib');
const { getRate } = require('./_rate');

const isInt = (v, min, max) => Number.isInteger(v) && v >= min && v <= max;

function kstToday() {
  const now = new Date(Date.now() + 9 * 3600 * 1000);
  return new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
}

module.exports = async (req, res) => {
  if (req.method !== 'POST') return send(res, 405, { message: 'Method Not Allowed' });
  let body;
  try { body = await readJson(req); } catch { return send(res, 400, { code: 'BAD_REQUEST', message: 'Bad request' }); }

  const product = PRODUCTS[body.productId];
  const adults = Number(body.adults), children = Number(body.children), infants = Number(body.infants);
  if (!product) return send(res, 400, { code: 'INVALID_PRODUCT', message: 'ツアーが見つかりません' });
  if (!isInt(adults, 1, MAX_PER_TYPE) || !isInt(children, 0, MAX_PER_TYPE) || !isInt(infants, 0, MAX_PER_TYPE)) {
    return send(res, 400, { code: 'INVALID_PEOPLE', message: '人数を確認してください（大人1名以上、各9名まで）' });
  }
  if (!/^\d{4}-\d{2}-\d{2}$/.test(body.date || '')) return send(res, 400, { code: 'INVALID_DATE', message: '日程を選んでください' });
  const d = new Date(body.date + 'T00:00:00Z');
  const diffDays = Math.round((d - kstToday()) / 86400000);
  // 出発3日前に催行判断をするため、申込は出発4日前まで（仮定・クライアント確認事項）
  if (!(diffDays >= 4 && diffDays <= 120) || HOLIDAYS.includes(body.date)) return send(res, 400, { code: 'DATE_NOT_AVAILABLE', message: 'この日程はお申し込みいただけません' });

  const amount = calcAmount(product, adults, children);
  const orderId = makeOrderId(product, adults, children, infants, body.date);
  const [, mm, dd] = body.date.split('-');
  // 決済画面に出る注文名（言語別）
  const lang = ['ja', 'en', 'ko'].includes(body.lang) ? body.lang : 'ja';
  const SHORT = {
    ja: { 'jeonju-damyang': '全州・潭陽', gangneung: '大関嶺・江陵', danyang: '丹陽' },
    en: { 'jeonju-damyang': 'Jeonju & Damyang', gangneung: 'Daegwallyeong & Gangneung', danyang: 'Danyang' },
    ko: { 'jeonju-damyang': '전주·담양', gangneung: '대관령·강릉', danyang: '단양' },
  };
  const md = `${Number(mm)}/${Number(dd)}`;
  const orderName = ({
    ja: `${SHORT.ja[body.productId]} 日帰りツアー ${md} 大人${adults}名${children ? `・子供${children}名` : ''}${infants ? `・幼児${infants}名` : ''}`,
    en: `${SHORT.en[body.productId]} day tour ${md} ${adults} adult(s)${children ? `, ${children} child(ren)` : ''}${infants ? `, ${infants} infant(s)` : ''}`,
    ko: `${SHORT.ko[body.productId]} 당일 투어 ${md} 성인 ${adults}명${children ? ` · 소아 ${children}명` : ''}${infants ? ` · 유아 ${infants}명` : ''}`,
  })[lang].slice(0, 100);

  const r = await getRate();
  send(res, 200, {
    orderId, orderName, amount, currency: 'KRW',
    jpy: r ? Math.round(amount * r.rate) : null,
    rate: r ? r.rate : null,
    rateAt: r ? r.updatedAt : null,
  });
};

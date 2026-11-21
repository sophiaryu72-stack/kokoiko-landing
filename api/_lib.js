// サーバー専用の共通処理。ブラウザには配信されない（Vercel の api/ 配下、先頭 _ はエンドポイントにならない）。
const crypto = require('crypto');

// 価格表（KRW）。金額の正はここだけ。画面側の表示用データ(js/products.js)と必ず揃えること。
const PRODUCTS = {
  'jeonju-damyang': { code: 'JD', price: 100000, name: '韓屋と竹林にときめく韓国旅 ～全州・潭陽～' },
  gangneung: { code: 'GN', price: 90000, name: 'ソウルから出発！大関嶺の山と江陵の海を巡る旅' },
  danyang: { code: 'DY', price: 90000, name: '韓国の絶景・癒しの旅 ～丹陽～' },
};
const BY_CODE = Object.fromEntries(Object.entries(PRODUCTS).map(([id, p]) => [p.code, { id, ...p }]));

const MAX_PER_TYPE = 9; // 大人・子供・幼児それぞれの上限（1件の申込あたり）

// 大人・子供は同額、2歳未満は無料（クライアント情報要求書）
function calcAmount(product, adults, children) {
  return product.price * (adults + children);
}

function signingKey() {
  const k = process.env.ORDER_SIGNING_SECRET || process.env.TOSS_SECRET_KEY;
  if (!k) throw new Error('ORDER_SIGNING_SECRET または TOSS_SECRET_KEY が未設定です');
  return k;
}

function sign(payload) {
  return crypto.createHmac('sha256', signingKey()).update(payload).digest('base64url').slice(0, 10);
}

// DB がないため、注文内容を orderId 自体に入れて署名する。
// 形式: KK-{商品コード}-{大人}{子供}{幼児}-{YYMMDD}-{ランダム6}-{署名10}  （英数字と - _ のみ、6〜64文字）
function makeOrderId(product, adults, children, infants, date) {
  const ymd = date.replace(/-/g, '').slice(2);
  const rand = crypto.randomBytes(4).toString('hex').slice(0, 6);
  const payload = `KK-${product.code}-${adults}${children}${infants}-${ymd}-${rand}`;
  return `${payload}-${sign(payload)}`;
}

function parseOrderId(orderId) {
  const m = /^(KK-([A-Z]{2})-(\d)(\d)(\d)-(\d{6})-([a-f0-9]{6}))-([A-Za-z0-9_-]{10})$/.exec(String(orderId || ''));
  if (!m) return null;
  const [, payload, code, a, c, i, ymd, , sig] = m;
  const expected = sign(payload);
  if (sig.length !== expected.length || !crypto.timingSafeEqual(Buffer.from(sig), Buffer.from(expected))) return null;
  const product = BY_CODE[code];
  if (!product) return null;
  return {
    product,
    adults: Number(a),
    children: Number(c),
    infants: Number(i),
    date: `20${ymd.slice(0, 2)}-${ymd.slice(2, 4)}-${ymd.slice(4, 6)}`,
  };
}

async function readJson(req) {
  if (req.body && typeof req.body === 'object') return req.body;
  if (typeof req.body === 'string') return JSON.parse(req.body || '{}');
  const chunks = [];
  for await (const ch of req) chunks.push(ch);
  return JSON.parse(Buffer.concat(chunks).toString('utf8') || '{}');
}

function send(res, status, data) {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json; charset=utf-8');
  res.end(JSON.stringify(data));
}

module.exports = { PRODUCTS, MAX_PER_TYPE, calcAmount, makeOrderId, parseOrderId, readJson, send };

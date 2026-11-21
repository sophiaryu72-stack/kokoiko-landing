// KRW→JPY の当日レート（参考表示用）。取得できない場合は null を返し、画面は円表示を省略する。
let cache = null; // { rate, updatedAt, fetchedAt }
const TTL = 60 * 60 * 1000;

async function getRate() {
  if (cache && Date.now() - cache.fetchedAt < TTL) return cache;
  try {
    const r = await fetch('https://open.er-api.com/v6/latest/KRW', { signal: AbortSignal.timeout(4000) });
    const j = await r.json();
    const rate = j && j.rates && j.rates.JPY;
    if (!rate) throw new Error('no JPY rate');
    cache = { rate, updatedAt: j.time_last_update_utc || new Date().toUTCString(), fetchedAt: Date.now() };
    return cache;
  } catch (e) {
    return cache || null;
  }
}
module.exports = { getRate };

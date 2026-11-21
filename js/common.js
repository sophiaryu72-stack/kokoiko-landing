// 全ページ共通。表示用データのみ（金額の正はサーバーの api/_lib.js）。
window.KOKOIKO = (function () {
  const products = {
    'jeonju-damyang': { name: '韓屋と竹林にときめく韓国旅 ～全州・潭陽～', short: '全州・潭陽', price: 100000, page: 'jeonju-damyang.html' },
    gangneung: { name: 'ソウルから出発！大関嶺の山と江陵の海を巡る旅', short: '大関嶺・江陵', price: 90000, page: 'gangneung.html' },
    danyang: { name: '韓国の絶景・癒しの旅 ～丹陽～', short: '丹陽', price: 90000, page: 'danyang.html' },
  };

  // 韓国の祝日（催行なし）。※2027年以降はクライアントに要確認
  const holidays = ['2026-12-25', '2027-01-01', '2027-02-05', '2027-02-06', '2027-02-07', '2027-02-08', '2027-03-01', '2027-05-05', '2027-05-13'];

  const BOOK_MIN_DAYS = 4;   // 出発3日前に催行判断 → 申込は4日前まで（仮定）
  const BOOK_MAX_DAYS = 120;
  const GROUP_SIZE_MIN = 10;

  let configP = null, rateP = null;
  function getConfig() {
    if (!configP) configP = fetch('/api/config').then(r => r.json()).catch(() => ({ clientKey: '', testMode: true }));
    return configP;
  }
  function getRate() {
    if (!rateP) rateP = fetch('/api/rate').then(r => r.json()).then(j => j.rate || null).catch(() => null);
    return rateP;
  }

  const fmtKRW = n => '₩' + Number(n).toLocaleString('ja-JP');
  const fmtJPY = n => '¥' + Math.round(n).toLocaleString('ja-JP');
  const DOW = ['日', '月', '火', '水', '木', '金', '土'];
  function parseYmd(s) { const [y, m, d] = s.split('-').map(Number); return new Date(Date.UTC(y, m - 1, d)); }
  function ymd(d) { return d.toISOString().slice(0, 10); }
  function fmtDate(s, withYear) {
    const d = parseYmd(s);
    const base = `${d.getUTCMonth() + 1}月${d.getUTCDate()}日(${DOW[d.getUTCDay()]})`;
    return withYear ? `${d.getUTCFullYear()}年${base}` : base;
  }
  function kstToday() {
    const n = new Date(Date.now() + 9 * 3600 * 1000);
    return new Date(Date.UTC(n.getUTCFullYear(), n.getUTCMonth(), n.getUTCDate()));
  }
  function isBookable(s) {
    const diff = Math.round((parseYmd(s) - kstToday()) / 86400000);
    return diff >= BOOK_MIN_DAYS && diff <= BOOK_MAX_DAYS && !holidays.includes(s);
  }

  // ▼ 募集状況：実データ未連携のため、テストモードでのみ「デモ表示」する（実際の数字ではない）
  function demoAvailability(productId, dateStr) {
    let h = 0;
    for (const ch of productId + dateStr) h = (h * 31 + ch.charCodeAt(0)) >>> 0;
    const booked = h % 9; // 0〜8名
    const remainPeople = Math.max(GROUP_SIZE_MIN - booked, 0);
    return { booked, remainPeople, remainGroups: Math.ceil(remainPeople / 2) };
  }

  async function initCommon() {
    const cfg = await getConfig();
    const banner = document.querySelector('.test-banner');
    if (banner) banner.hidden = !cfg.testMode;
    document.documentElement.dataset.testMode = cfg.testMode ? '1' : '0';
    // 円の参考表示: <span data-jpy="100000"></span>
    const nodes = document.querySelectorAll('[data-jpy]');
    if (nodes.length) {
      const rate = await getRate();
      nodes.forEach(el => {
        const krw = Number(el.dataset.jpy);
        el.textContent = rate ? '約' + fmtJPY(krw * rate) : fmtKRW(krw);
      });
      document.querySelectorAll('[data-rate-note]').forEach(el => {
        el.textContent = rate ? '円は本日の為替レートによる目安です。' : '';
      });
    }
    return cfg;
  }

  return { products, holidays, GROUP_SIZE_MIN, getConfig, getRate, fmtKRW, fmtJPY, fmtDate, parseYmd, ymd, kstToday, isBookable, demoAvailability, initCommon };
})();

document.addEventListener('DOMContentLoaded', () => { KOKOIKO.initCommon(); });

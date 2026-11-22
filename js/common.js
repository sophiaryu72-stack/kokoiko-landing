// 全ページ共通。表示用データのみ（金額の正はサーバーの api/_lib.js）。
window.KOKOIKO = (function () {
  const lang = ['ja', 'en', 'ko'].includes(document.documentElement.lang) ? document.documentElement.lang : 'ja';

  const products = {
    'jeonju-damyang': { price: 100000, name: { ja: '韓屋と竹林にときめく韓国旅 ～全州・潭陽～', en: 'Hanok Houses & Bamboo Forests ~Jeonju & Damyang~', ko: '한옥과 대나무 숲에 설레는 한국 여행 ~전주·담양~' } },
    gangneung: { price: 90000, name: { ja: 'ソウルから出発！大関嶺の山と江陵の海を巡る旅', en: 'From Seoul! Daegwallyeong Mountains & Gangneung Sea', ko: '서울에서 출발! 대관령의 산과 강릉의 바다를 둘러보는 여행' } },
    danyang: { price: 90000, name: { ja: '韓国の絶景・癒しの旅 ～丹陽～', en: 'Korea’s Scenic Wonders & Healing Trip ~Danyang~', ko: '단양 감성 힐링 투어' } },
  };

  // 画面上の文言（JSで生成する部分）
  const I18N = {
    ja: {
      dow: ['日', '月', '火', '水', '木', '金', '土'],
      date: (y, m, d, w, withY) => `${withY ? y + '年' : ''}${m}月${d}日(${w})`,
      month: (y, m) => `${y}年${m}月`,
      approx: v => '約' + v, rateNote: '円は本日の為替レートによる目安です。',
      demoDetail: (d, n, g) => `${d}出発：いま${n}名・あと約${g}組で出発確定`,
      remain: g => `あと${g}組`, calNote: '「あと◯組」は募集状況のデモ表示です（2名＝1組の目安）。',
      selected: d => `選択中：${d}`, prev: '前の月', next: '次の月', notAvail: '（選択できません）',
      totalJpy: v => `参考：約${v}（本日のレート）`,
      noDate: '日程を選んでください。', noInfo: '代表者情報を入力してください。', noAgree: '確認・同意の項目をすべてチェックしてください。',
      noKey: '決済の設定が完了していません（クライアントキー未設定）。', processing: '処理中…', toPay: 'お支払いへ進む',
      locked: (amt, jpy, d, ppl) => `お支払い金額は <strong>${amt}</strong>${jpy ? `（参考：約${jpy}）` : ''} で確定しました。<br><span class="small">${d}・${ppl}</span>`,
      payBtn: a => `${a} を支払う`, loadFail: '決済画面を読み込めませんでした：',
      people: (a, c, i) => [`大人${a}名`, c ? `子供${c}名` : '', i ? `幼児${i}名` : ''].filter(Boolean).join('・'),
      sum: { tour: 'ツアー', date: '日程', people: '人数', paid: 'お支払い', order: '注文番号', line: 'ご連絡先LINE', meet: ' 07:30 集合' },
      demoSuccess: (d, g) => `${d}出発の募集状況：あと約${g}組で出発確定`,
      noPayInfo: 'お支払い情報が見つかりませんでした。', confirmFail: 'お支払いを確認できませんでした。', network: '通信エラーが発生しました。時間をおいて再度お試しください。',
      errCode: 'エラーコード：',
      err: {
        INVALID_PRODUCT: 'ツアーが見つかりません。', INVALID_PEOPLE: '人数を確認してください（大人1名以上）。', INVALID_DATE: '日程を選んでください。',
        DATE_NOT_AVAILABLE: 'この日程はお申し込みいただけません。', AMOUNT_MISMATCH: 'お支払い金額が正しくありません。決済は承認されていません。',
        INVALID_ORDER: '注文情報を確認できませんでした。', NETWORK: '決済サーバーに接続できませんでした。', PAY_PROCESS_CANCELED: 'お支払いがキャンセルされました。',
      },
    },
    en: {
      dow: ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'],
      date: (y, m, d, w, withY) => `${w}, ${['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][m - 1]} ${d}${withY ? ', ' + y : ''}`,
      month: (y, m) => `${['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'][m - 1]} ${y}`,
      approx: v => 'approx. ' + v, rateNote: '',
      demoDetail: (d, n, g) => `Departing ${d}: ${n} booked · about ${g} more groups to confirm`,
      remain: g => `${g} left`, calNote: '“N left” is a demo of booking status (about 2 people per group).',
      selected: d => `Selected: ${d}`, prev: 'Previous month', next: 'Next month', notAvail: ' (unavailable)',
      totalJpy: () => '',
      noDate: 'Please choose a date.', noInfo: 'Please enter the lead traveler’s details.', noAgree: 'Please check all the boxes to agree.',
      noKey: 'Payment is not set up yet (client key missing).', processing: 'Processing…', toPay: 'Continue to payment',
      locked: (amt, jpy, d, ppl) => `Your payment amount is fixed at <strong>${amt}</strong>.<br><span class="small">${d} · ${ppl}</span>`,
      payBtn: a => `Pay ${a}`, loadFail: 'Could not load the payment screen: ',
      people: (a, c, i) => [`${a} adult${a > 1 ? 's' : ''}`, c ? `${c} child${c > 1 ? 'ren' : ''}` : '', i ? `${i} infant${i > 1 ? 's' : ''}` : ''].filter(Boolean).join(', '),
      sum: { tour: 'Tour', date: 'Date', people: 'Guests', paid: 'Paid', order: 'Order no.', line: 'LINE ID', meet: ' · meet at 07:30' },
      demoSuccess: (d, g) => `Booking status for ${d}: about ${g} more groups to confirm`,
      noPayInfo: 'Payment information was not found.', confirmFail: 'We couldn’t confirm your payment.', network: 'A network error occurred. Please try again later.',
      errCode: 'Error code: ',
      err: {
        INVALID_PRODUCT: 'Tour not found.', INVALID_PEOPLE: 'Please check the number of people (at least 1 adult).', INVALID_DATE: 'Please choose a date.',
        DATE_NOT_AVAILABLE: 'This date is not available.', AMOUNT_MISMATCH: 'The payment amount is incorrect. The payment was not approved.',
        INVALID_ORDER: 'We couldn’t verify your order.', NETWORK: 'Could not connect to the payment server.', PAY_PROCESS_CANCELED: 'The payment was cancelled.',
      },
    },
    ko: {
      dow: ['일', '월', '화', '수', '목', '금', '토'],
      date: (y, m, d, w, withY) => `${withY ? y + '년 ' : ''}${m}월 ${d}일(${w})`,
      month: (y, m) => `${y}년 ${m}월`,
      approx: v => '약 ' + v, rateNote: '',
      demoDetail: (d, n, g) => `${d} 출발: 현재 ${n}명 · 약 ${g}팀 더 모이면 출발 확정`,
      remain: g => `${g}팀 남음`, calNote: '‘N팀 남음’은 모객 현황 데모 표시예요 (2명 = 1팀 기준).',
      selected: d => `선택한 날짜: ${d}`, prev: '이전 달', next: '다음 달', notAvail: ' (선택 불가)',
      totalJpy: () => '',
      noDate: '날짜를 선택해 주세요.', noInfo: '대표자 정보를 입력해 주세요.', noAgree: '확인·동의 항목을 모두 체크해 주세요.',
      noKey: '결제 설정이 완료되지 않았어요 (클라이언트 키 없음).', processing: '처리 중…', toPay: '결제 진행',
      locked: (amt, jpy, d, ppl) => `결제 금액이 <strong>${amt}</strong>으로 확정되었어요.<br><span class="small">${d} · ${ppl}</span>`,
      payBtn: a => `${a} 결제하기`, loadFail: '결제 화면을 불러오지 못했어요: ',
      people: (a, c, i) => [`성인 ${a}명`, c ? `소아 ${c}명` : '', i ? `유아 ${i}명` : ''].filter(Boolean).join(' · '),
      sum: { tour: '투어', date: '일정', people: '인원', paid: '결제 금액', order: '주문번호', line: '연락 LINE', meet: ' 07:30 집결' },
      demoSuccess: (d, g) => `${d} 출발 모객 현황: 약 ${g}팀 더 모이면 출발 확정`,
      noPayInfo: '결제 정보를 찾을 수 없어요.', confirmFail: '결제를 확인하지 못했어요.', network: '통신 오류가 발생했어요. 잠시 후 다시 시도해 주세요.',
      errCode: '오류 코드: ',
      err: {
        INVALID_PRODUCT: '투어를 찾을 수 없어요.', INVALID_PEOPLE: '인원을 확인해 주세요 (성인 1명 이상).', INVALID_DATE: '날짜를 선택해 주세요.',
        DATE_NOT_AVAILABLE: '이 날짜는 신청할 수 없어요.', AMOUNT_MISMATCH: '결제 금액이 올바르지 않아요. 결제는 승인되지 않았어요.',
        INVALID_ORDER: '주문 정보를 확인하지 못했어요.', NETWORK: '결제 서버에 연결하지 못했어요.', PAY_PROCESS_CANCELED: '결제가 취소되었어요.',
      },
    },
  };
  const T = I18N[lang];

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

  const fmtKRW = n => '₩' + Number(n).toLocaleString('en-US');
  const fmtJPY = n => '¥' + Math.round(n).toLocaleString('en-US');
  function parseYmd(s) { const [y, m, d] = s.split('-').map(Number); return new Date(Date.UTC(y, m - 1, d)); }
  function ymd(d) { return d.toISOString().slice(0, 10); }
  function fmtDate(s, withYear) {
    const d = parseYmd(s);
    return T.date(d.getUTCFullYear(), d.getUTCMonth() + 1, d.getUTCDate(), T.dow[d.getUTCDay()], withYear);
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
    const booked = h % 9;
    const remainPeople = Math.max(GROUP_SIZE_MIN - booked, 0);
    return { booked, remainPeople, remainGroups: Math.ceil(remainPeople / 2) };
  }

  // 言語切替：クエリ（?p= など）を引き継ぎ、選んだ言語を記憶
  function initLangBar() {
    document.querySelectorAll('.lang-bar a').forEach(a => {
      a.href = a.getAttribute('href') + location.search + location.hash;
      a.addEventListener('click', () => { try { localStorage.setItem('kokoiko_lang', a.dataset.lang); } catch (e) {} });
    });
  }

  async function initCommon() {
    initLangBar();
    const cfg = await getConfig();
    const banner = document.querySelector('.test-banner');
    if (banner) banner.hidden = !cfg.testMode;
    const nodes = document.querySelectorAll('[data-jpy]');
    if (nodes.length) {
      const rate = await getRate();
      nodes.forEach(el => {
        const krw = Number(el.dataset.jpy);
        el.textContent = rate ? T.approx(fmtJPY(krw * rate)) : (el.textContent || fmtKRW(krw));
      });
      document.querySelectorAll('[data-rate-note]').forEach(el => { el.textContent = rate ? T.rateNote : ''; });
    }
    return cfg;
  }

  return { lang, T, products, holidays, GROUP_SIZE_MIN, getConfig, getRate, fmtKRW, fmtJPY, fmtDate, parseYmd, ymd, kstToday, isBookable, demoAvailability, initCommon,
    productName: id => (products[id] ? products[id].name[lang] : ''), errMsg: (code, fallback) => (code && T.err[code]) || fallback };
})();

document.addEventListener('DOMContentLoaded', () => { KOKOIKO.initCommon(); });

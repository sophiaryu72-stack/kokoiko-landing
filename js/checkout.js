(async () => {
  const K = KOKOIKO;
  const $ = s => document.querySelector(s);
  const pid = new URLSearchParams(location.search).get('p');
  const product = K.products[pid];
  if (!product) { location.replace('index.html'); return; }

  const cfg = await K.getConfig();
  const state = { date: null, adults: 2, children: 0, infants: 0 };
  try {
    const saved = JSON.parse(sessionStorage.getItem('kokoiko_form') || 'null');
    if (saved && saved.productId === pid) {
      Object.assign(state, { adults: saved.adults, children: saved.children, infants: saved.infants });
      if (saved.date && K.isBookable(saved.date)) state.date = saved.date;
      $('#in-name').value = saved.name || ''; $('#in-phone').value = saved.phone || ''; $('#in-line').value = saved.lineId || '';
    }
  } catch (e) {}

  $('#co-name').textContent = product.name;
  $('#co-unit').textContent = K.fmtKRW(product.price);
  $('#u-adult').textContent = K.fmtKRW(product.price);
  $('#u-child').textContent = K.fmtKRW(product.price);

  // ---- 日程 ----
  const today = K.kstToday();
  const first = new Date(today); first.setUTCDate(first.getUTCDate() + 4);
  const lastD = new Date(today); lastD.setUTCDate(lastD.getUTCDate() + 120);
  let view = new Date(Date.UTC(first.getUTCFullYear(), first.getUTCMonth(), 1));
  const minView = new Date(view);
  const maxView = new Date(Date.UTC(lastD.getUTCFullYear(), lastD.getUTCMonth(), 1));
  if (state.date) { const sd = K.parseYmd(state.date); view = new Date(Date.UTC(sd.getUTCFullYear(), sd.getUTCMonth(), 1)); }

  function setDate(s) {
    state.date = s;
    $('#date-picked').textContent = s ? `選択中：${K.fmtDate(s, true)}` : '';
    renderCal(); renderSuggest();
  }

  function renderCal() {
    const y = view.getUTCFullYear(), m = view.getUTCMonth();
    const startDow = new Date(Date.UTC(y, m, 1)).getUTCDay();
    const days = new Date(Date.UTC(y, m + 1, 0)).getUTCDate();
    let h = `<div class="cal-head"><button type="button" id="cal-prev" aria-label="前の月" ${view <= minView ? 'disabled' : ''}>‹</button><span>${y}年${m + 1}月</span><button type="button" id="cal-next" aria-label="次の月" ${view >= maxView ? 'disabled' : ''}>›</button></div><div class="cal-grid">`;
    ['日', '月', '火', '水', '木', '金', '土'].forEach((w, i) => { h += `<div class="cal-dow ${i === 0 ? 'sun' : i === 6 ? 'sat' : ''}">${w}</div>`; });
    for (let i = 0; i < startDow; i++) h += '<span class="cal-day empty"></span>';
    for (let d = 1; d <= days; d++) {
      const s = `${y}-${String(m + 1).padStart(2, '0')}-${String(d).padStart(2, '0')}`;
      const ok = K.isBookable(s);
      let sub = '';
      if (ok && cfg.testMode) { const a = K.demoAvailability(pid, s); sub = `<small>あと${a.remainGroups}組</small>`; }
      h += `<button type="button" class="cal-day${state.date === s ? ' on' : ''}" data-d="${s}" ${ok ? '' : 'disabled'} aria-label="${K.fmtDate(s, true)}${ok ? '' : '（選択できません）'}">${d}${sub}</button>`;
    }
    h += '</div>';
    if (cfg.testMode) h += '<p class="small muted" style="margin-top:8px">「あと◯組」は募集状況のデモ表示です（2名＝1組の目安）。</p>';
    $('#cal').innerHTML = h;
    $('#cal-prev').onclick = () => { view = new Date(Date.UTC(y, m - 1, 1)); renderCal(); };
    $('#cal-next').onclick = () => { view = new Date(Date.UTC(y, m + 1, 1)); renderCal(); };
    $('#cal').querySelectorAll('.cal-day[data-d]').forEach(b => { b.onclick = () => { if (!locked) setDate(b.dataset.d); }; });
  }

  // まもなく出発確定の日程（デモ）：30日以内で残りが少ない順に3つ
  function renderSuggest() {
    if (!cfg.testMode) return;
    const list = [];
    const d = new Date(first);
    for (let i = 0; i < 30; i++, d.setUTCDate(d.getUTCDate() + 1)) {
      const s = K.ymd(d);
      if (!K.isBookable(s)) continue;
      const a = K.demoAvailability(pid, s);
      if (a.remainGroups > 0) list.push({ s, a });
    }
    list.sort((x, y) => x.a.remainGroups - y.a.remainGroups || x.s.localeCompare(y.s));
    const top = list.slice(0, 3).sort((x, y) => x.s.localeCompare(y.s));
    $('#suggest').innerHTML = top.map(({ s, a }) => `<button type="button" class="date-card${state.date === s ? ' on' : ''}" data-d="${s}"><strong>${K.fmtDate(s)}</strong><span>あと${a.remainGroups}組</span></button>`).join('');
    $('#suggest').querySelectorAll('.date-card').forEach(b => {
      b.onclick = () => {
        if (locked) return;
        const sd = K.parseYmd(b.dataset.d); view = new Date(Date.UTC(sd.getUTCFullYear(), sd.getUTCMonth(), 1)); setDate(b.dataset.d);
      };
    });
    $('#suggest-wrap').classList.toggle('hidden', top.length === 0);
  }

  // ---- 人数 ----
  const LIMIT = 9;
  function renderPeople() {
    document.querySelectorAll('.stepper').forEach(st => {
      const k = st.dataset.key, min = k === 'adults' ? 1 : 0;
      st.querySelector('output').textContent = state[k];
      st.querySelector('[data-d="-1"]').disabled = locked || state[k] <= min;
      st.querySelector('[data-d="1"]').disabled = locked || state[k] >= LIMIT;
    });
    renderTotal();
  }
  document.querySelectorAll('.stepper').forEach(st => {
    st.querySelectorAll('button').forEach(b => b.addEventListener('click', () => {
      const k = st.dataset.key, min = k === 'adults' ? 1 : 0;
      state[k] = Math.min(LIMIT, Math.max(min, state[k] + Number(b.dataset.d)));
      renderPeople();
    }));
  });

  async function renderTotal() {
    const amt = product.price * (state.adults + state.children);
    $('#total').textContent = K.fmtKRW(amt);
    const rate = await K.getRate();
    $('#total-jpy').textContent = rate ? `参考：約${K.fmtJPY(amt * rate)}（本日のレート）` : '';
  }

  // ---- 申込 → 注文作成（金額確定）----
  let locked = false, order = null, widgets = null, rendered = false;
  const fields = [['#f-name', '#in-name'], ['#f-phone', '#in-phone'], ['#f-line', '#in-line']];

  function showError(msg) { const b = $('#form-error'); b.textContent = msg; b.classList.toggle('hidden', !msg); }

  function setLocked(v) {
    locked = v;
    fields.forEach(([, i]) => { $(i).disabled = v; });
    ['#ag-tentative', '#ag-cancel', '#ag-privacy'].forEach(s => { $(s).disabled = v; });
    $('#to-pay').classList.toggle('hidden', v);
    $('#pay-sec').classList.toggle('hidden', !v);
    renderPeople(); renderCal(); renderSuggest();
  }

  $('#to-pay').addEventListener('click', async () => {
    showError('');
    let bad = false;
    fields.forEach(([f, i]) => { const empty = !$(i).value.trim(); $(f).classList.toggle('error', empty); bad = bad || empty; });
    if (!state.date) return showError('日程を選んでください。');
    if (bad) return showError('代表者情報を入力してください。');
    if (!['#ag-tentative', '#ag-cancel', '#ag-privacy'].every(s => $(s).checked)) return showError('確認・同意の項目をすべてチェックしてください。');
    if (!cfg.clientKey) return showError('決済の設定が完了していません（クライアントキー未設定）。');

    const form = { productId: pid, date: state.date, adults: state.adults, children: state.children, infants: state.infants,
      name: $('#in-name').value.trim(), phone: $('#in-phone').value.trim(), lineId: $('#in-line').value.trim() };
    sessionStorage.setItem('kokoiko_form', JSON.stringify(form));

    $('#to-pay').disabled = true; $('#to-pay').textContent = '処理中…';
    try {
      const r = await fetch('/api/order', { method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ productId: pid, date: state.date, adults: state.adults, children: state.children, infants: state.infants }) });
      const j = await r.json();
      if (!r.ok) throw new Error(j.message || '注文を作成できませんでした');
      order = j;
      sessionStorage.setItem('kokoiko_booking', JSON.stringify({ ...form, orderId: j.orderId, amount: j.amount, jpy: j.jpy }));
    } catch (e) {
      showError(e.message); return;
    } finally {
      $('#to-pay').disabled = false; $('#to-pay').textContent = 'お支払いへ進む';
    }

    const jpy = order.jpy ? `（参考：約${K.fmtJPY(order.jpy)}）` : '';
    $('#locked').innerHTML = `お支払い金額は <strong>${K.fmtKRW(order.amount)}</strong>${jpy} で確定しました。<br><span class="small">${K.fmtDate(state.date, true)}・${order.orderName.split(' ').slice(-1)[0]}</span>`;
    setLocked(true);
    $('#pay-btn').textContent = `${K.fmtKRW(order.amount)} を支払う`;
    $('#pay-sec').scrollIntoView({ behavior: 'smooth' });

    try {
      if (!widgets) {
        const toss = TossPayments(cfg.clientKey);
        widgets = toss.widgets({ customerKey: TossPayments.ANONYMOUS });
        if (cfg.testMode) window.widgets = widgets; // QA（金額改ざんテスト）用。テストモードのみ
      }
      await widgets.setAmount({ currency: 'KRW', value: order.amount });
      if (!rendered) {
        await Promise.all([
          widgets.renderPaymentMethods({ selector: '#payment-method', variantKey: 'DEFAULT' }),
          widgets.renderAgreement({ selector: '#agreement', variantKey: 'AGREEMENT' }),
        ]);
        rendered = true;
      }
      $('#pay-btn').disabled = false;
    } catch (e) {
      $('#locked').insertAdjacentHTML('beforeend', `<div class="error-box" style="margin-top:10px">決済画面を読み込めませんでした：${e.message}</div>`);
    }
  });

  $('#pay-btn').addEventListener('click', async () => {
    if (!order || !widgets) return;
    try {
      await widgets.requestPayment({
        orderId: order.orderId,
        orderName: order.orderName,
        customerName: $('#in-name').value.trim(),
        successUrl: location.origin + '/success.html',
        failUrl: location.origin + '/fail.html',
      });
    } catch (e) {
      // 決済ウィンドウを閉じた場合など
      location.href = `fail.html?code=${encodeURIComponent(e.code || 'PAY_PROCESS_CANCELED')}&message=${encodeURIComponent(e.message || '')}`;
    }
  });

  $('#edit-btn').addEventListener('click', () => { order = null; $('#pay-btn').disabled = true; setLocked(false); window.scrollTo({ top: 0, behavior: 'smooth' }); });

  if (state.date) setDate(state.date); else { renderCal(); renderSuggest(); }
  renderPeople();
})();

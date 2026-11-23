#!/usr/bin/env python3
"""정적 HTML 생성 (ja: 루트 / en: /en/ / ko: /ko/). 문구는 tools/content.py.
SITE_URL 환경변수로 OGP 이미지 절대 URL 지정 (기본: 배포 주소).
"""
import html, os, json, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from content import L, P, LANGS, LANG_LABEL, PREFIX, ORDER, PRICE, IMG, SLIDES, P_IMG, ABOUT_IMG, CREDIT_TXT
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = os.environ.get('SITE_URL', 'https://kokoiko-landing-chi.vercel.app').rstrip('/')
OG_LOCALE = {'ja': 'ja_JP', 'en': 'en_US', 'ko': 'ko_KR'}
e = html.escape


def krw(n):
    return f'₩{n:,}'


class Page:
    def __init__(self, lang, file):
        self.lang, self.file, self.t = lang, file, L[lang]

    def head(self, title, desc, extra=''):
        alts = ''.join(f'<link rel="alternate" hreflang="{l}" href="{SITE_URL}{PREFIX[l]}{self.file}">\n' for l in LANGS)
        alts += f'<link rel="alternate" hreflang="x-default" href="{SITE_URL}/{self.file}">\n'
        bar = ''.join(
            f'<a href="{PREFIX[l]}{self.file}" lang="{l}" hreflang="{l}" data-lang="{l}"{" aria-current=\"true\"" if l == self.lang else ""}>{LANG_LABEL[l]}</a>'
            for l in LANGS)
        return f'''<!DOCTYPE html>
<html lang="{self.lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ここいこ KOKOIKO">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{SITE_URL}/img/ogp.png">
<meta property="og:locale" content="{OG_LOCALE[self.lang]}">
<meta name="twitter:card" content="summary_large_image">
{alts}<link rel="icon" href="/img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&family=Noto+Sans+KR:wght@400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/css/style.css">
{extra}</head>
<body>
<div class="page">
<div class="test-banner" hidden>{e(self.t["test"])}</div>
<nav class="lang-bar" aria-label="Language"><span aria-hidden="true">🌐</span>{bar}</nav>
'''

    def header(self, right=''):
        return f'''<header class="site-header">
  <a class="logo" href="index.html" aria-label="{e(self.t["logo_aria"])}"><span class="k1">ここ</span><span class="k2">いこ</span></a>
  {right}
</header>
'''

    def footer(self):
        t = self.t
        return f'''<footer class="site-footer">
  <a href="legal.html#tokushoho">{e(t["f_tokushoho"])}</a>
  <a href="legal.html#cancel">{e(t["f_cancel"])}</a>
  <a href="legal.html#privacy">{e(t["f_privacy"])}</a>
  <a href="compare.html">{e(t["f_compare"])}</a>
  <a href="legal.html#credits">{e(CREDIT_TXT[self.lang]["link"])}</a>
  <p class="company">{t["company"]}</p>
</footer>
'''

    @staticmethod
    def tail(scripts=''):
        return f'''</div>
<script src="/js/common.js"></script>
{scripts}</body>
</html>
'''


def ph(alt, cls=''):
    return f'<div class="ph {cls}" role="img" aria-label="{e(alt)}">{e(alt)}</div>'


def sized(url, w):
    """Wikimedia 썸네일 크기 지정 (표준 폭 500/960)"""
    if '/thumb/' in url:
        return url.replace('/1280px-', f'/{w}px-')
    path = url.split('/wikipedia/commons/')[1]
    return f'https://thumb.wikimedia.org/wikipedia/commons/thumb/{path}/{w}px-{path.split("/")[-1]}'


def pic(key, alt, cls='', credit=True, lazy=True):
    url, _f, a, lic = IMG[key]
    url = sized(url, 960 if 'full' in cls else 500)
    cr = f'<span class="credit">© {e(a)} / {e(lic)}</span>' if credit else ''
    ld = ' loading="lazy"' if lazy else ''
    return f'<figure class="pic {cls}"><img src="{url}" alt="{e(alt)}"{ld} decoding="async">{cr}</figure>'


def slideshow(lang):
    figs, dots = '', ''
    for i, (key, cap) in enumerate(SLIDES):
        url, _f, a, lic = IMG[key]
        url = sized(url, 960)
        ld = '' if i == 0 else ' loading="lazy"'
        figs += (f'<figure class="slide{" on" if i == 0 else ""}"><img src="{url}" alt="{e(cap[lang])}"{ld} decoding="async">'
                 f'<figcaption><span class="place">📍 {e(cap[lang])}</span><span class="credit">© {e(a)} / {e(lic)}</span></figcaption></figure>')
        dots += f'<button type="button" class="dot-btn{" on" if i == 0 else ""}" aria-label="{i + 1}/{len(SLIDES)}" data-i="{i}"></button>'
    return f'<div class="slides" aria-roledescription="carousel">{figs}<div class="dots">{dots}</div></div>'


def price_html(lang, price, small_cls='small muted'):
    t = L[lang]
    if lang == 'ja':
        return f'<span data-jpy="{price}">{krw(price)}</span> <span class="{small_cls}">{e(t["per_person"])}</span>'
    return f'{krw(price)} <span class="{small_cls}">{e(t["per_person"])}</span>'


# ---------- map ----------
def proj(lon, lat):
    return round((lon - 125.45) * 70, 1), round((38.8 - lat) * 74, 1)


OUTLINE = [(126.15, 37.75), (126.68, 37.95), (127.1, 38.3), (127.6, 38.33), (128.1, 38.32), (128.36, 38.62), (128.6, 38.15),
           (128.95, 37.75), (129.2, 37.4), (129.4, 36.95), (129.45, 36.4), (129.55, 36.05), (129.45, 35.6), (129.2, 35.25),
           (128.95, 35.08), (128.55, 34.88), (128.2, 34.9), (127.75, 34.73), (127.4, 34.55), (126.9, 34.4), (126.5, 34.32),
           (126.3, 34.55), (126.35, 34.95), (126.45, 35.35), (126.6, 35.75), (126.75, 36.05), (126.5, 36.4), (126.2, 36.75),
           (126.45, 36.95), (126.8, 37.05), (126.65, 37.35), (126.55, 37.6)]


def tw(lang, s, size=12):
    """대략적인 글자 폭(px)"""
    return sum(size * (0.55 if ord(c) < 0x2E80 else 1.0) for c in s)


def map_svg(lang):
    t = L[lang]
    lb = t['map_lbl']
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in (proj(*p) for p in OUTLINE)) + ' Z'
    S = proj(126.98, 37.57)
    Pn = {k: proj(*v) for k, v in {'dgr': (128.72, 37.68), 'gn': (128.9, 37.75), 'dy': (128.37, 36.98), 'jj': (127.15, 35.82), 'dm': (126.99, 35.32)}.items()}
    soon = [proj(129.22, 35.84), proj(127.72, 34.78)]
    out = [f'<svg class="map-svg" viewBox="0 0 300 340" role="img" aria-label="{e(t["map_aria"])}">', f'<path class="land" d="{d}"/>']
    for k in ('dgr', 'dy', 'jj'):
        out.append(f'<path class="route" d="M{S[0]} {S[1]} L{Pn[k][0]} {Pn[k][1]}"/>')
    out.append(f'<line class="link" x1="{Pn["dgr"][0]}" y1="{Pn["dgr"][1]}" x2="{Pn["gn"][0]}" y2="{Pn["gn"][1]}"/>')
    out.append(f'<line class="link" x1="{Pn["jj"][0]}" y1="{Pn["jj"][1]}" x2="{Pn["dm"][0]}" y2="{Pn["dm"][1]}"/>')
    for i, (x, y) in enumerate(soon):
        w = tw(lang, lb['soon'], 11)
        tx = round(x - w - 10, 1) if i == 0 else x + 10
        out.append(f'<circle class="soon" cx="{x}" cy="{y}" r="7"/><text class="soon-t" x="{tx}" y="{y + 4}">{e(lb["soon"])}</text>')
    for pid, keys in [('gangneung', ['dgr', 'gn']), ('danyang', ['dy']), ('jeonju-damyang', ['jj', 'dm'])]:
        main = ' main' if pid == 'jeonju-damyang' else ''
        out.append(f'<g class="pin-g" data-target="{pid}" tabindex="0" role="button" aria-label="{e(t["pin_aria"].format(P[pid][lang]["short"]))}">')
        for k in keys:
            out.append(f'<circle class="hit" cx="{Pn[k][0]}" cy="{Pn[k][1]}" r="22"/><circle class="pin{main}" cx="{Pn[k][0]}" cy="{Pn[k][1]}" r="8"/>')
        out.append('</g>')
    out.append(f'<rect class="seoul" x="{S[0] - 7}" y="{S[1] - 7}" width="14" height="14" rx="3"/>')
    labels = [('seoul', S[0] - tw(lang, lb['seoul']) / 2, S[1] - 13),
              ('dgr', Pn['dgr'][0] - tw(lang, lb['dgr']) + 6, Pn['dgr'][1] + 22),
              ('gn', Pn['gn'][0] - tw(lang, lb['gn']) / 2, Pn['gn'][1] - 13),
              ('dy', Pn['dy'][0] + 12, Pn['dy'][1] + 5), ('jj', Pn['jj'][0] + 13, Pn['jj'][1] + 5), ('dm', Pn['dm'][0] + 13, Pn['dm'][1] + 6)]
    for k, x, y in labels:
        out.append(f'<text x="{round(max(x, 2), 1)}" y="{y}">{e(lb[k])}</text>')
    out.append('</svg>')
    return '\n'.join(out)


# ---------- pages ----------
def tour_card(lang, pid):
    t, p = L[lang], P[pid][lang]
    badge = f'<span class="tag pink">{e(t["badge"])}</span> ' if p['badge'] else ''
    pay = f'<p class="small muted">{e(t["pay_line"].format(krw(PRICE[pid])))}</p>' if t['pay_line'] else ''
    return f'''<a class="tour-card" id="card-{pid}" href="{pid}.html">
  {pic(P_IMG[pid]["card"], p["short"], credit=False)}
  <div>
    <div>{badge}<span class="tag sky">{e(t["tag_day"])}</span></div>
    <h3 style="margin-top:6px">{e(p["name"])}</h3>
    <p class="price">{price_html(lang, PRICE[pid])}</p>
    {pay}
  </div>
</a>'''


def page_index(lang):
    pg, t = Page(lang, 'index.html'), L[lang]
    cards = '\n'.join(tour_card(lang, pid) for pid in ORDER)
    svc = ''.join(f'<div class="svc"><div class="icon">{ic}</div><div><h3>{e(n)} <span class="tag">{e(t["soon"])}</span></h3><p class="small muted">{e(dsc)}</p></div></div>' for ic, n, dsc in t['svc'])
    return pg.head(t['idx_title'], t['idx_desc']) + pg.header(f'<a class="header-link" href="#tours">{e(t["see_tours"])}</a>') + f'''<main>
<section class="hero">
  {slideshow(lang)}
  <div class="hero-copy">
    <div class="eyebrow"><span class="tag sky">{e(t["tag_day"])}</span> <span class="tag">{e(" / ".join(P[x][lang]["short"] for x in ORDER))}</span></div>
    <h1>{t["h1"]}</h1>
    <p>{e(t["hero_p"])}</p>
  </div>
  <p class="scroll-hint">{e(t["scroll"])}</p>
</section>

<section class="sec tint" id="map">
  <div class="sec-title"><h2>{e(t["map_t"])}</h2><span class="en">MAP</span></div>
  <p class="muted" style="margin-bottom:12px">{e(t["map_p"])}</p>
  <div class="map-wrap">
{map_svg(lang)}
  </div>
  <div class="map-legend"><span><span class="dot"></span>{e(t["lg_on"])}</span><span><span class="dot soon"></span>{e(t["lg_soon"])}</span><span>{e(t["lg_simple"])}</span></div>
</section>

<section class="sec" id="tours">
  <div class="sec-title"><h2>{e(t["tours_t"])}</h2><span class="en">TOURS</span></div>
  {cards}
  <p class="small muted" data-rate-note style="margin-top:10px"></p>
</section>

<section class="sec pinkish">
  <div class="sec-title"><h2>{e(t["svc_t"])}</h2><span class="en">COMING SOON</span></div>
  <p class="muted" style="margin-bottom:16px">{e(t["svc_p"])}</p>
  {svc}
</section>

<section class="sec">
  <div class="sec-title"><h2>{e(t["val_t"])}</h2><span class="en">VALUE</span></div>
  <p class="muted">{e(t["val_p"])}</p>
  <p style="margin-top:12px"><a class="text-link" href="compare.html">{e(t["cmp_link"])}</a></p>
</section>

<section class="sec tint">
  <div class="sec-title"><h2>{e(t["about_t"])}</h2><span class="en">ABOUT</span></div>
  {pic(ABOUT_IMG, CREDIT_TXT[lang]["about"])}
  <h3 style="margin-top:16px">{e(t["about_h"])}</h3>
  <p class="muted" style="margin-top:6px">{e(t["about_p"])}</p>
</section>
</main>
''' + pg.footer() + pg.tail('<script src="/js/index.js"></script>\n')


def page_detail(lang, pid):
    pg, t, p = Page(lang, f'{pid}.html'), L[lang], P[pid][lang]
    price = PRICE[pid]
    places = ''.join(f'<li><strong>{e(a)}</strong> … {e(b)}</li>' for a, b in p['places'])
    hl = ''.join(f'<li>{e(h)}</li>' for h in p['highlights'])
    sch = p['schedule']
    first, last, middle = sch[0], sch[-1], sch[1:-1]
    stops = iter(P_IMG[pid]['stops'])

    def li(s, cls=''):
        time, title, desc, photo = s
        d = f'<p class="small muted">{e(desc)}</p>' if desc else ''
        im = ''
        if photo:
            key, sub = next(stops)
            im = pic(key, sub[lang] if sub else photo)
            if sub:
                im = im.replace('</figure>', f'<span class="sub-cap">{e(sub[lang])}</span></figure>')
        return f'<li><span class="time">{e(time)}</span><div class="body {cls}"><h4>{e(title)}</h4>{d}{im}</div></li>'

    big = f'<span data-jpy="{price}">{krw(price)}</span>' if lang == 'ja' else krw(price)
    pay = e(t['pay_krw'].format(krw(price))) if lang == 'ja' else e(t['pay_krw'])
    rate_note = '<p class="small muted" data-rate-note></p>' if lang == 'ja' else ''
    tags = ''.join(f'<span class="tag">{e(x)}</span>' for x in t['tags'])
    cancel = ''.join(f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a, b in t['cancel_rows'])
    badge = f'<span class="tag pink">{e(t["badge"])}</span>' if p['badge'] else ''
    return pg.head(f'{p["name"]} ｜ {"ここいこ" if lang == "ja" else ("KOKOIKO" if lang == "en" else "코코이코")}', p['lead']) \
        + pg.header(f'<a class="header-link" href="index.html#map">{e(t["other_area"])}</a>') + f'''<main>
<section class="hero">{pic(P_IMG[pid]["hero"], p["hero"], "full", lazy=False)}</section>

<section class="sec">
  <div class="tags">{badge}<span class="tag sky">{e(t["tag_day"])}</span></div>
  <h1 style="font-size:21px;margin-top:10px">{e(p["name"])}</h1>
  <p class="muted" style="margin-top:8px">{e(p["lead"])}</p>
  <ul class="place-list small" style="padding-left:18px;margin:12px 0 0">{places}</ul>
</section>

<section class="sec tint">
  <div class="sec-title"><h2>{e(t["glance"])}</h2></div>
  <dl class="kv">
    <dt>{e(t["k_sched"])}</dt><dd>{e(t["v_sched"])}</dd>
    <dt>{e(t["k_move"])}</dt><dd>{e(p["travel"])}<br><span class="small muted">{e(p["distance"])}{e(t["dist_note"])}</span></dd>
    <dt>{e(t["k_meet"])}</dt><dd>{e(t["v_meet"])}<br><a class="small text-link" href="#meeting">{e(t["meet_link"])}</a></dd>
    <dt>{e(t["k_incl"])}</dt><dd>{e(t["v_incl"])}</dd>
    <dt>{e(t["k_meal"])}</dt><dd>{e(t["v_meal"])}</dd>
  </dl>
</section>

<section class="sec" id="min">
  <div class="box strong stack">
    <h2 style="font-size:17px">{e(t["min_t"])}</h2>
    <p class="small">{e(t["min_p"])}</p>
    <div class="demo-status hidden">
      <div class="progress" aria-hidden="true"><span style="width:0%"></span></div>
      <p class="small" style="margin-top:6px"><strong class="demo-text"></strong> <span class="muted">{e(t["demo"])}</span></p>
    </div>
    <p class="small muted">{e(t["min_refund"])}</p>
  </div>
</section>

<section class="sec">
  <div class="sec-title"><h2>{e(t["points"])}</h2></div>
  <ol style="padding-left:20px;margin:0" class="stack">{hl}</ol>
</section>

<section class="sec">
  <div class="sec-title"><h2>{e(t["itinerary"])}</h2></div>
  <ul class="timeline">{li(first)}{li(middle[0])}</ul>
  <details class="more"><summary>{e(t["more_stops"].format(len(middle) - 1))}</summary><div class="inner"><ul class="timeline">{"".join(li(x) for x in middle[1:])}</ul></div></details>
  <ul class="timeline">{li(last, "end")}</ul>
  <p class="small muted">{e(t["meal_note"])}</p>
</section>

<section class="sec tint" id="price">
  <div class="sec-title"><h2>{e(t["price_t"])}</h2></div>
  <p class="price-big">{big} <small>{e(t["per_adult"])}</small></p>
  <p style="margin-top:4px"><strong>{pay}</strong></p>
  {rate_note}
  <p class="small muted">{e(t["child"])}</p>
  <div class="tags" style="margin-top:12px">{tags}</div>
  <dl class="kv" style="margin-top:14px">
    <dt>{e(t["k_incl"])}</dt><dd>{e(t["v_incl_s"])}</dd>
    <dt>{e(t["k_excl"])}</dt><dd>{e(t["v_excl"])}</dd>
  </dl>
  <p style="margin-top:14px"><a class="text-link" href="compare.html#{pid}">{e(t["cmp_detail"])}</a></p>
</section>

<section class="sec" id="meeting">
  <div class="sec-title"><h2>{e(t["meet_t"])}</h2></div>
  <p>{e(t["meet_p"])}</p>
  <p class="small muted" style="margin-top:4px">{e(t["meet_s"])}</p>
</section>

<section class="sec" id="cancel">
  <div class="sec-title"><h2>{e(t["cancel_t"])}</h2></div>
  <table class="cancel-table">{cancel}</table>
  <p class="small muted" style="margin-top:8px">{e(t["cancel_note"])}</p>
  <p style="margin-top:8px"><a class="small text-link" href="legal.html#cancel">{e(t["cancel_full"])}</a></p>
</section>

<section class="sec tint">
  <div class="sec-title"><h2>{e(t["seller_t"])}</h2></div>
  <dl class="kv">
    <dt>{e(t["k_company"])}</dt><dd>{e(t["brand"])}</dd>
    <dt>{e(t["k_addr"])}</dt><dd>{e(t["address"])}</dd>
    <dt>{e(t["k_contact"])}</dt><dd>{e(t["contact"])}</dd>
  </dl>
  <p style="margin-top:10px"><a class="small text-link" href="legal.html#tokushoho">{e(t["tokushoho_link"])}</a></p>
</section>

<div class="sticky-cta">
  <p>{t["cta1"]}</p>
  <p>{e(t["cta2"])}</p>
  <a class="btn" href="checkout.html?p={pid}">{e(t["cta_btn"])}</a>
</div>
</main>
''' + pg.footer() + pg.tail(f'<script>window.PRODUCT_ID = {json.dumps(pid)};</script>\n<script src="/js/detail.js"></script>\n')


def page_compare(lang):
    pg, t = Page(lang, 'compare.html'), L[lang]
    rows = ''
    for pid in ORDER:
        p = P[pid][lang]
        r = t['cmp_rows']
        jpy = f'<br><span class="small" data-jpy="{PRICE[pid]}"></span>' if lang == 'ja' else ''
        rows += f'''
<section class="sec" id="{pid}">
  <h2 style="font-size:17px">{e(p["short"])}</h2>
  <table class="cmp" style="margin-top:10px">
    <thead><tr><th></th><th>{e(t["cmp_self"])}</th><th>{e(t["cmp_us"])}</th></tr></thead>
    <tbody>
      <tr><th>{e(r[0][0])}</th><td>{e(r[0][1])}<br><span class="tbd">{e(t["tbd"])}</span></td><td class="ok">{e(t["incl"])}</td></tr>
      <tr><th>{e(r[1][0])}</th><td>{e(r[1][1])}<br><span class="tbd">{e(t["tbd"])}</span></td><td class="ok">{e(t["incl"])}</td></tr>
      <tr><th>{e(r[2][0])}</th><td>{e(r[2][1])}<br><span class="tbd">{e(t["tbd2"])}</span></td><td class="ok">{e(t["by_bus"])}</td></tr>
      <tr><th>{e(r[3][0])}</th><td>{e(r[3][1])}<br><span class="tbd">{e(t["tbd"])}</span></td><td class="ok">{e(t["incl"])}</td></tr>
      <tr><th>{e(r[4][0])}</th><td>{e(r[4][1])}</td><td class="ok">{e(t["guide_incl"])}</td></tr>
      <tr><th>{e(r[5][0])}</th><td><span class="tbd">{e(t["tbd3"])}</span></td><td class="ok">{krw(PRICE[pid])}{jpy}</td></tr>
    </tbody>
  </table>
</section>'''
    return pg.head(t['cmp_title'], t['cmp_desc']) + pg.header(f'<a class="header-link" href="index.html#tours">{e(t["see_tours"])}</a>') + f'''<main>
<section class="sec tint">
  <h1 style="font-size:21px">{e(t["cmp_h1"])}</h1>
  <p class="muted" style="margin-top:8px">{e(t["cmp_p"])}</p>
</section>
{rows}
<section class="sec">
  <p class="small muted">{e(t["cmp_foot"])}</p>
  <p style="margin-top:12px"><a class="btn sub" href="index.html#tours">{e(t["all_tours"])}</a></p>
</section>
</main>
''' + pg.footer() + pg.tail()


def page_legal(lang):
    pg, t = Page(lang, 'legal.html'), L[lang]
    tk = ''.join(f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a, b in t['tk_rows'])
    cp = ''.join(f'<tr><th>{e(a)}</th><td>{e(b)}</td></tr>' for a, b in t['cp_rows'])
    notes = ''.join(f'<li>{e(n)}</li>' for n in t['cp_notes'])
    credits = ''.join(f'<li><a class="text-link" href="https://commons.wikimedia.org/wiki/File:{quote(f.replace(" ", "_"))}" target="_blank" rel="noopener">{e(f)}</a> — {e(a)} / {e(lic)}</li>' for _u, f, a, lic in IMG.values())
    return pg.head(t['legal_title'], t['legal_desc']) + pg.header(f'<a class="header-link" href="index.html">{e(t["top"])}</a>') + f'''<main>
<section class="sec" id="tokushoho">
  <h1 style="font-size:20px;margin-bottom:14px">{e(t["tk_h"])}</h1>
  <table class="legal-table">{tk}</table>
</section>
<section class="sec" id="cancel">
  <h2 style="margin-bottom:14px">{e(t["cancel_t"])}</h2>
  <table class="cancel-table">{cp}</table>
  <ul class="small muted" style="padding-left:18px;margin-top:10px">{notes}</ul>
</section>
<section class="sec" id="privacy">
  <h2 style="margin-bottom:14px">{e(t["f_privacy"])}</h2>
  <p class="small">{e(t["pv_p"])}</p>
  <p class="small muted" style="margin-top:8px">{e(t["pv_soon"])}</p>
</section>
<section class="sec" id="credits">
  <h2 style="margin-bottom:10px">{e(CREDIT_TXT[lang]["h"])}</h2>
  <p class="small muted" style="margin-bottom:10px">{e(CREDIT_TXT[lang]["p"])}</p>
  <ul class="small" style="padding-left:18px;margin:0">{credits}</ul>
</section>
</main>
''' + pg.footer() + pg.tail()


def stepper(t, key, label, sub, init):
    return (f'<div class="stepper-row"><div><strong>{e(label)}</strong><br><span class="small muted"{" id=\"u-" + key + "\"" if sub is None else ""}>{e(sub or "")}</span></div>'
            f'<div class="stepper" data-key="{key}"><button type="button" data-d="-1" aria-label="{e(t["dec"].format(label))}">−</button><output>{init}</output>'
            f'<button type="button" data-d="1" aria-label="{e(t["inc"].format(label))}">＋</button></div></div>')


def page_checkout(lang):
    pg, t = Page(lang, 'checkout.html'), L[lang]
    total_jpy = '<p class="small muted" id="total-jpy" style="text-align:right"></p>'
    return pg.head(t['co_title'], t['co_title'], '<meta name="robots" content="noindex">\n<script src="https://js.tosspayments.com/v2/standard"></script>\n') \
        + pg.header(f'<a class="header-link" href="javascript:history.back()">{e(t["back"])}</a>') + f'''<main>
<section class="sec tint">
  <p class="small muted">{e(t["co_tour"])}</p>
  <h1 id="co-name" style="font-size:16px;margin-top:2px"></h1>
  <p class="small" style="margin-top:4px"><span id="co-unit"></span> {e(t["co_unit"])}</p>
</section>

<section class="sec">
  <h2 class="step-title">{e(t["s1"])}</h2>
  <div id="suggest-wrap" class="hidden">
    <p class="small" style="font-weight:700;margin-bottom:8px">{e(t["suggest"])} <span class="muted" style="font-weight:400">{e(t["demo"])}</span></p>
    <div class="date-cards" id="suggest"></div>
    <p class="small muted" style="margin:12px 0 8px">{e(t["or_cal"])}</p>
  </div>
  <div class="cal" id="cal"></div>
  <p class="small muted" style="margin-top:8px">{e(t["window"])}</p>
  <p class="small" id="date-picked" style="margin-top:8px;font-weight:700"></p>
</section>

<section class="sec">
  <h2 class="step-title">{e(t["s2"])}</h2>
  {stepper(t, "adults", t["adult"], None, 2)}
  {stepper(t, "children", t["childL"], None, 0)}
  {stepper(t, "infants", t["infant"], t["free"], 0)}
</section>

<section class="sec">
  <h2 class="step-title">{e(t["s3"])}</h2>
  <label class="field" id="f-name"><span class="label">{e(t["name"])}<span class="req">{e(t["req"])}</span></span><input id="in-name" autocomplete="name" placeholder="{e(t["name_ph"])}"><span class="err">{e(t["name_err"])}</span></label>
  <label class="field" id="f-phone"><span class="label">{e(t["phone"])}<span class="req">{e(t["req"])}</span></span><input id="in-phone" type="tel" autocomplete="tel" placeholder="{e(t["phone_ph"])}"><span class="err">{e(t["phone_err"])}</span></label>
  <label class="field" id="f-line"><span class="label">LINE ID<span class="req">{e(t["req"])}</span></span><input id="in-line" autocomplete="off" placeholder="{e(t["line_ph"])}"><span class="hint">{e(t["line_hint"])}</span><span class="err">{e(t["line_err"])}</span></label>
</section>

<section class="sec tint">
  <div class="total-row"><span>{e(t["total"])}</span><strong id="total">—</strong></div>
  {total_jpy}
  <p class="small muted" style="margin-top:6px">{e(t["total_note"])}</p>
</section>

<section class="sec">
  <h2 class="step-title">{e(t["s4"])}</h2>
  <label class="check"><input type="checkbox" id="ag-tentative"><span>{e(t["ag1"])}</span></label>
  <label class="check"><input type="checkbox" id="ag-cancel"><span>{t["ag2"]}</span></label>
  <label class="check"><input type="checkbox" id="ag-privacy"><span>{t["ag3"]}</span></label>
  <div class="error-box hidden" id="form-error" style="margin-top:14px"></div>
  <button class="btn" id="to-pay" type="button" style="margin-top:16px">{e(t["to_pay"])}</button>
</section>

<section class="sec hidden" id="pay-sec">
  <h2 class="step-title">{e(t["s5"])}</h2>
  <div class="notice" id="locked"></div>
  <div id="payment-method" style="margin-top:12px"></div>
  <div id="agreement"></div>
  <p class="small muted">{e(t["fee"])}</p>
  <button class="btn" id="pay-btn" type="button" style="margin-top:12px" disabled>{e(t["pay"])}</button>
  <button class="btn sub" id="edit-btn" type="button" style="margin-top:8px">{e(t["edit"])}</button>
</section>

<section class="sec" style="background:#f1f1f1">
  <p class="small muted">{e(t["pg"])}</p>
  <p class="small pg-links" style="margin-top:6px"><a href="legal.html#tokushoho">{e(t["pg_links"][0])}</a> ・ <a href="legal.html#privacy">{e(t["pg_links"][1])}</a> ・ <a href="legal.html#cancel">{e(t["pg_links"][2])}</a></p>
</section>
</main>
''' + pg.tail('<script src="/js/checkout.js"></script>\n')


def page_success(lang):
    pg, t = Page(lang, 'success.html'), L[lang]
    steps = ''.join(f'<li>{e(s)}</li>' for s in t['next_steps'])
    return pg.head(t['su_title'], t['su_title'], '<meta name="robots" content="noindex">\n') + pg.header() + f'''<main>
<section class="sec" id="loading" style="text-align:center;padding:60px 18px">
  <div class="spinner"></div><p class="muted" style="margin-top:14px">{e(t["loading"])}</p>
</section>

<div id="done" class="hidden">
<section class="sec stack">
  <div class="result-icon">✓</div>
  <h1 style="font-size:22px">{e(t["su_h"])}</h1>
  <p style="font-weight:700">{e(t["su_not"])}</p>
  <p class="small muted">{e(t["su_p"])}</p>
</section>
<section class="sec tint">
  <h2 style="font-size:17px;margin-bottom:10px">{e(t["su_detail"])}</h2>
  <dl class="kv" id="summary"></dl>
</section>
<section class="sec hidden" id="demo-box">
  <div class="box strong"><p class="small"><strong id="demo-text"></strong> <span class="muted">{e(t["demo"])}</span></p></div>
</section>
<section class="sec">
  <h2 style="font-size:17px;margin-bottom:10px">{e(t["next"])}</h2>
  <ol style="padding-left:20px;margin:0" class="stack small">{steps}</ol>
  <a class="btn line" href="#" id="line-add" style="margin-top:18px">{e(t["line_add"])}</a>
  <p class="small muted" style="margin-top:6px;text-align:center">{e(t["line_soon"])}</p>
  <a class="btn sub" href="index.html" style="margin-top:10px">{e(t["back_top"])}</a>
</section>
</div>

<section class="sec hidden stack" id="ng">
  <div class="result-icon ng">!</div>
  <h1 style="font-size:20px">{e(t["ng_h"])}</h1>
  <div class="error-box" id="ng-msg"></div>
  <p class="small">{e(t["ng_p"])}</p>
  <a class="btn" href="#" id="retry">{e(t["ng_retry"])}</a>
</section>
</main>
''' + pg.tail('<script src="/js/success.js"></script>\n')


def page_fail(lang):
    pg, t = Page(lang, 'fail.html'), L[lang]
    return pg.head(t['fa_title'], t['fa_title'], '<meta name="robots" content="noindex">\n') + pg.header() + f'''<main>
<section class="sec stack">
  <div class="result-icon ng">!</div>
  <h1 style="font-size:20px">{e(t["fa_h"])}</h1>
  <p>{e(t["fa_p"])}</p>
  <div class="error-box"><p id="f-msg">{e(t["fa_msg"])}</p><p class="small" id="f-code" style="margin-top:4px"></p></div>
  <a class="btn" href="#" id="retry">{e(t["fa_retry"])}</a>
  <a class="btn sub" href="index.html">{e(t["back_top"])}</a>
</section>
</main>
''' + pg.tail('<script src="/js/fail.js"></script>\n')


def write(lang, name, content):
    d = ROOT if lang == 'ja' else os.path.join(ROOT, lang)
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, name), 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    for lang in LANGS:
        write(lang, 'index.html', page_index(lang))
        for pid in ORDER:
            write(lang, f'{pid}.html', page_detail(lang, pid))
        write(lang, 'compare.html', page_compare(lang))
        write(lang, 'legal.html', page_legal(lang))
        write(lang, 'checkout.html', page_checkout(lang))
        write(lang, 'success.html', page_success(lang))
        write(lang, 'fail.html', page_fail(lang))
    print('built', LANGS)

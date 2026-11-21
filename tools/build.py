#!/usr/bin/env python3
"""静的HTMLを生成するスクリプト。文言を直したら `python3 tools/build.py` で再生成。
SITE_URL を配布先のURLにすると OGP 画像が絶対URLになる（LINE・Xで確実に表示させるため）。
"""
import html, os, json

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE_URL = os.environ.get('SITE_URL', '').rstrip('/')  # 例: https://kokoiko.vercel.app

PRODUCTS = {
    'jeonju-damyang': {
        'name': '韓屋と竹林にときめく韓国旅 ～全州・潭陽～',
        'short': '全州・潭陽', 'price': 100000, 'badge': 'イチオシ',
        'area': '全州（チョンジュ）・潭陽（タミャン）',
        'lead': '竹林の小道、メタセコイア並木、そして韓屋の街並み。韓国の「昔ながら」を一日でめぐります。',
        'hero_alt': '潭陽・竹緑苑の竹林の小道（写真は準備中）',
        'places': [
            ('全州（チョンジュ）', '韓屋（韓国の伝統家屋）が並ぶ、韓国の古都'),
            ('潭陽（タミャン）', '竹林とメタセコイア並木で知られる、緑ゆたかな町'),
        ],
        'travel': 'ソウルから片道 約4時間（休憩を含む）',
        'distance': '約300km ── 東京から名古屋くらいの距離',
        'highlights': ['竹緑苑（チュンノグォン）の竹林さんぽ', 'メタセコイア並木道で写真さんぽ', '全州韓屋村（チョンジュ・ハノンマウル）で食べ歩き'],
        'schedule': [
            ('07:30', '集合・出発', 'ソウル市内の集合場所からバスで出発。途中、休憩所で15分の休憩があります。', None),
            ('11:30', '竹緑苑（チュンノグォン）', '竹林の中の遊歩道を散策。昼食は周辺で各自（自由食）。', '竹緑苑の竹林'),
            ('13:40', 'メタセコイア並木道・メタプロバンス', 'まっすぐ続く並木道と、ヨーロッパ風の街並みで自由散策。', 'メタセコイア並木道'),
            ('16:00', '全州韓屋村（チョンジュ・ハノンマウル）', '韓屋の街並みを散策。夕食は各自（自由食）。', '全州韓屋村の街並み'),
            ('18:30', 'ソウルへ出発', None, None),
            ('22:00〜22:30', 'ソウル到着・解散', '道路状況により前後することがあります。', None),
        ],
    },
    'gangneung': {
        'name': 'ソウルから出発！大関嶺の山と江陵の海を巡る旅',
        'short': '大関嶺・江陵', 'price': 90000, 'badge': None,
        'area': '大関嶺（テグァンリョン）・江陵（カンヌン）',
        'lead': '緑の高原と、東海（トンヘ）の青い海。山と海をいっぺんに楽しむ、ソウル発の日帰り旅です。',
        'hero_alt': '大関嶺の羊牧場と高原の風景（写真は準備中）',
        'places': [
            ('大関嶺（テグァンリョン）', '羊の牧場で知られる、涼しい高原'),
            ('江陵（カンヌン）', '海辺のカフェ通りで人気の、東海岸の町'),
        ],
        'travel': 'ソウルから片道 約2時間30分',
        'distance': '約230km ── 東京から浜松くらいの距離',
        'highlights': ['大関嶺の羊牧場で羊に会える', '草堂（チョダン）スンドゥブ村で名物の豆腐料理', '安木（アンモク）海辺のオーシャンビューカフェ'],
        'schedule': [
            ('07:30', '集合・出発', 'ソウル市内の集合場所からバスで出発。', None),
            ('10:00', '大関嶺羊牧場（テグァンリョン・ヤンテモクジャン）', '高原の牧場を自由に見学。', '大関嶺羊牧場'),
            ('12:30', '草堂スンドゥブ村（チョダン）', '名物の豆腐料理のお店が並ぶ村。昼食は各自（自由食）。', '草堂スンドゥブ村'),
            ('14:20', '安木海辺（アンモク）', '海沿いのカフェ通りで自由時間。', '安木海辺のカフェ通り'),
            ('16:30', '正東津（チョンドンジン）', '海辺の町で自由散策。18:40ごろ夕食（各自・自由食）。', '正東津の海'),
            ('19:40', 'ソウルへ出発', None, None),
            ('22:30〜23:00', 'ソウル到着・解散', '道路状況により前後することがあります。', None),
        ],
    },
    'danyang': {
        'name': '韓国の絶景・癒しの旅 ～丹陽～',
        'short': '丹陽', 'price': 90000, 'badge': None,
        'area': '丹陽（タニャン）',
        'lead': '川と山に囲まれた、絶景の町。山あいのお寺、スカイウォーク、名物グルメまで一日で楽しめます。',
        'hero_alt': '丹陽・島潭三峰の川辺の風景（写真は準備中）',
        'places': [
            ('丹陽（タニャン）', '南漢江（ナムハンガン）沿いの奇岩と渓谷で知られる町'),
            ('救仁寺（クインサ）', '山あいに建物が連なる、大きなお寺'),
        ],
        'travel': 'ソウルから片道 約3時間30分（休憩を含む）',
        'distance': '約180km ── 東京から静岡くらいの距離',
        'highlights': ['万天下（マンチョナ）スカイウォークからの絶景', '島潭三峰（トダムサムボン）の奇岩', '名物ニンニクトッカルビの夕食（各自）'],
        'schedule': [
            ('07:30', '集合・出発', 'ソウル市内の集合場所からバスで出発。途中、休憩所で15分の休憩があります。', None),
            ('11:00', '救仁寺（クインサ）', '山あいのお寺を自由に見学。', '救仁寺'),
            ('13:10', '丹陽旧京市場（クギョン市場）', '市場で食べ歩き。昼食は各自（自由食）。', '丹陽旧京市場'),
            ('14:30', '万天下スカイウォーク（マンチョナ）', '川を見下ろす展望台で自由観光・写真撮影。', '万天下スカイウォーク'),
            ('16:20', '島潭三峰（トダムサムボン）', '川に浮かぶ三つの岩の名所。17:20ごろ夕食（各自・自由食）。', '島潭三峰'),
            ('18:30', 'ソウルへ出発', '途中、休憩所で休憩があります。', None),
            ('22:00〜22:30', 'ソウル到着・解散', '道路状況により前後することがあります。', None),
        ],
    },
}
ORDER = ['jeonju-damyang', 'gangneung', 'danyang']
e = html.escape


def krw(n):
    return f'₩{n:,}'


def head(title, desc, extra=''):
    og_img = f'{SITE_URL}/img/ogp.png' if SITE_URL else 'img/ogp.png'
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="ここいこ KOKOIKO">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:image" content="{og_img}">
<meta property="og:locale" content="ja_JP">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="img/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="css/style.css">
{extra}</head>
<body>
<div class="page">
<div class="test-banner" hidden>テストモード（実際の請求は発生しません）</div>
'''


def header(right=''):
    return f'''<header class="site-header">
  <a class="logo" href="index.html" aria-label="ここいこ トップへ"><span class="k1">ここ</span><span class="k2">いこ</span></a>
  {right}
</header>
'''


FOOTER = '''<footer class="site-footer">
  <a href="legal.html#tokushoho">特定商取引法に基づく表記</a>
  <a href="legal.html#cancel">キャンセルポリシー</a>
  <a href="legal.html#privacy">プライバシーポリシー</a>
  <a href="compare.html">交通費をくらべる</a>
  <p class="company">ここいこ（KOKOIKO）<br>所在地：大韓民国 ソウル特別市 松坡区<br>お問い合わせ：LINE・メール（窓口は準備中です）</p>
</footer>
'''


def tail(scripts=''):
    return f'''</div>
<script src="js/common.js"></script>
{scripts}</body>
</html>
'''


def ph(alt, cls=''):
    return f'<div class="ph {cls}" role="img" aria-label="{e(alt)}">{e(alt)}</div>'


# ---------- map ----------
def proj(lon, lat):
    return round((lon - 125.45) * 70, 1), round((38.8 - lat) * 74, 1)


OUTLINE = [(126.15, 37.75), (126.68, 37.95), (127.1, 38.3), (127.6, 38.33), (128.1, 38.32), (128.36, 38.62), (128.6, 38.15),
           (128.95, 37.75), (129.2, 37.4), (129.4, 36.95), (129.45, 36.4), (129.55, 36.05), (129.45, 35.6), (129.2, 35.25),
           (128.95, 35.08), (128.55, 34.88), (128.2, 34.9), (127.75, 34.73), (127.4, 34.55), (126.9, 34.4), (126.5, 34.32),
           (126.3, 34.55), (126.35, 34.95), (126.45, 35.35), (126.6, 35.75), (126.75, 36.05), (126.5, 36.4), (126.2, 36.75),
           (126.45, 36.95), (126.8, 37.05), (126.65, 37.35), (126.55, 37.6)]


def map_svg():
    d = 'M' + ' L'.join(f'{x} {y}' for x, y in (proj(*p) for p in OUTLINE)) + ' Z'
    S = proj(126.98, 37.57)
    P = {k: proj(*v) for k, v in {'dgr': (128.72, 37.68), 'gn': (128.9, 37.75), 'dy': (128.37, 36.98), 'jj': (127.15, 35.82), 'dm': (126.99, 35.32)}.items()}
    soon = [proj(129.22, 35.84), proj(127.72, 34.78)]
    out = [f'<svg class="map-svg" viewBox="0 0 300 340" role="img" aria-label="韓国の地図。ソウルから大関嶺・江陵、丹陽、全州・潭陽へのツアー">',
           f'<path class="land" d="{d}"/>']
    for k in ('dgr', 'dy', 'jj'):
        out.append(f'<path class="route" d="M{S[0]} {S[1]} L{P[k][0]} {P[k][1]}"/>')
    out.append(f'<line class="link" x1="{P["dgr"][0]}" y1="{P["dgr"][1]}" x2="{P["gn"][0]}" y2="{P["gn"][1]}"/>')
    out.append(f'<line class="link" x1="{P["jj"][0]}" y1="{P["jj"][1]}" x2="{P["dm"][0]}" y2="{P["dm"][1]}"/>')
    for i, (x, y) in enumerate(soon):
        tx = x - 50 if i == 0 else x + 10
        out.append(f'<circle class="soon" cx="{x}" cy="{y}" r="7"/><text class="soon-t" x="{tx}" y="{y + 4}">準備中</text>')
    groups = [('gangneung', ['dgr', 'gn']), ('danyang', ['dy']), ('jeonju-damyang', ['jj', 'dm'])]
    for pid, keys in groups:
        main = ' main' if pid == 'jeonju-damyang' else ''
        out.append(f'<g class="pin-g" data-target="{pid}" tabindex="0" role="button" aria-label="{e(PRODUCTS[pid]["short"])}のツアーを見る">')
        for k in keys:
            out.append(f'<circle class="hit" cx="{P[k][0]}" cy="{P[k][1]}" r="18"/><circle class="pin{main}" cx="{P[k][0]}" cy="{P[k][1]}" r="8"/>')
        out.append('</g>')
    out.append(f'<rect class="seoul" x="{S[0] - 7}" y="{S[1] - 7}" width="14" height="14" rx="3"/>')
    labels = [('ソウル（出発）', S[0] - 56, S[1] - 12), ('大関嶺', P['dgr'][0] - 50, P['dgr'][1] + 20), ('江陵', P['gn'][0] - 6, P['gn'][1] - 13),
              ('丹陽', P['dy'][0] + 12, P['dy'][1] + 5), ('全州', P['jj'][0] + 13, P['jj'][1] + 5), ('潭陽', P['dm'][0] + 13, P['dm'][1] + 6)]
    for t, x, y in labels:
        out.append(f'<text x="{x}" y="{y}">{t}</text>')
    out.append('</svg>')
    return '\n'.join(out)


# ---------- pages ----------
def tour_card(pid):
    p = PRODUCTS[pid]
    badge = f'<span class="tag pink">{e(p["badge"])}</span> ' if p['badge'] else ''
    return f'''<a class="tour-card" id="card-{pid}" href="{pid}.html">
  {ph(p["short"] + "の写真")}
  <div>
    <div>{badge}<span class="tag sky">ソウル発・日帰り</span></div>
    <h3 style="margin-top:6px">{e(p["name"])}</h3>
    <p class="price"><span data-jpy="{p["price"]}">{krw(p["price"])}</span> <span class="small muted">/ 1名（税込）</span></p>
    <p class="small muted">お支払い {krw(p["price"])}</p>
  </div>
</a>'''


def page_index():
    cards = '\n'.join(tour_card(pid) for pid in ORDER)
    return head('ここいこ ｜ ソウル発・韓国の地方を巡る日帰りツアー', 'ソウルだけじゃ、もったいない！全州・潭陽、大関嶺・江陵、丹陽へ。往復の交通・入場料・添乗員つきの日帰りツアー。') + header('<a class="header-link" href="#tours">ツアーを見る</a>') + f'''<main>
<section class="hero">
  {ph("韓国の地方の風景（写真は準備中）", "full")}
  <div class="hero-copy">
    <h1>ソウルの外へ、<br><span class="accent">本当の韓国</span>を感じる旅。</h1>
    <p>ソウルだけじゃ、もったいない！ソウル発の日帰りツアーで、韓国の地方へ出かけませんか。</p>
  </div>
  <p class="scroll-hint">↓ エリアから探す</p>
</section>

<section class="sec tint" id="map">
  <div class="sec-title"><h2>エリアから探す</h2><span class="en">MAP</span></div>
  <p class="muted" style="margin-bottom:12px">ソウルを出発して、その日のうちにソウルへ戻ります。ピンをタップするとツアーが見られます。</p>
  <div class="map-wrap">
{map_svg()}
  </div>
  <div class="map-legend"><span><span class="dot"></span>販売中のツアー</span><span><span class="dot soon"></span>準備中のエリア</span><span>地図は簡略図です</span></div>
</section>

<section class="sec" id="tours">
  <div class="sec-title"><h2>日帰りツアー</h2><span class="en">TOURS</span></div>
  {cards}
  <p class="small muted" data-rate-note style="margin-top:10px"></p>
</section>

<section class="sec pinkish">
  <div class="sec-title"><h2>みんなで楽しむ、現地体験</h2><span class="en">COMING SOON</span></div>
  <p class="muted" style="margin-bottom:16px">ツアーとあわせて楽しめる体験を準備しています。</p>
  <div class="svc"><div class="icon">👘</div><div><h3>韓服（ハンボク）体験 <span class="tag">準備中</span></h3><p class="small muted">韓屋の街並みを、韓服を着てお散歩。友達とおそろいで。</p></div></div>
  <div class="svc"><div class="icon">🍽</div><div><h3>人気店の予約代行 <span class="tag">準備中</span></h3><p class="small muted">予約が取りにくい地元のお店を、事前にお取りします。</p></div></div>
  <div class="svc"><div class="icon">🎟</div><div><h3>アクティビティの事前予約 <span class="tag">準備中</span></h3><p class="small muted">現地の体験を、ツアーとまとめて予約できるようにします。</p></div></div>
</section>

<section class="sec">
  <div class="sec-title"><h2>ひとりで行くより、おトクでラク</h2><span class="en">VALUE</span></div>
  <p class="muted">往復の交通・入場料・添乗員がセット。乗り換えや、駅から観光地までの移動を自分で調べる必要はありません。</p>
  <p style="margin-top:12px"><a class="text-link" href="compare.html">交通費をくらべる ›</a></p>
</section>

<section class="sec tint">
  <div class="sec-title"><h2>ここいこについて</h2><span class="en">ABOUT</span></div>
  {ph("ツアーの様子（写真は準備中）")}
  <h3 style="margin-top:16px">韓国って、こんなに魅力的だったんだ！</h3>
  <p class="muted" style="margin-top:6px">一度訪れたら、また来たくなる韓国。その理由を、あなた自身で体感してみませんか？ここいこは、韓国の地方の魅力をお届けする、ソウル発のツアーです。</p>
</section>
</main>
''' + FOOTER + tail('<script src="js/index.js"></script>\n')


def page_detail(pid):
    p = PRODUCTS[pid]
    places = ''.join(f'<li><strong>{e(a)}</strong>… {e(b)}</li>' for a, b in p['places'])
    hl = ''.join(f'<li>{e(h)}</li>' for h in p['highlights'])
    sch = p['schedule']
    first, last, middle = sch[0], sch[-1], sch[1:-1]

    def li(t, cls=''):
        time, title, desc, photo = t
        d = f'<p class="small muted">{e(desc)}</p>' if desc else ''
        pic = ph(photo + '（写真は準備中）') if photo else ''
        return f'<li><span class="time">{e(time)}</span><div class="body {cls}"><h4>{e(title)}</h4>{d}{pic}</div></li>'
    shown = li(first) + li(middle[0])
    hidden = ''.join(li(x) for x in middle[1:])
    hidden_names = f'ほかの立ち寄り先（{len(middle) - 1}件）'
    return head(f'{p["name"]} ｜ ここいこ', p['lead']) + header('<a class="header-link" href="index.html#map">🗺 ほかのエリア</a>') + f'''<main>
<section class="hero">{ph(p["hero_alt"], "full")}</section>

<section class="sec">
  <div class="tags">{('<span class="tag pink">' + e(p['badge']) + '</span>') if p['badge'] else ''}<span class="tag sky">ソウル発・日帰り</span></div>
  <h1 style="font-size:21px;margin-top:10px">{e(p["name"])}</h1>
  <p class="muted" style="margin-top:8px">{e(p["lead"])}</p>
  <ul class="place-list small" style="padding-left:18px;margin:12px 0 0">{places}</ul>
</section>

<section class="sec tint">
  <div class="sec-title"><h2>ひと目でわかる</h2></div>
  <dl class="kv">
    <dt>日程</dt><dd>ソウル発・日帰り（韓国の祝日を除く毎日）</dd>
    <dt>移動</dt><dd>{e(p["travel"])}<br><span class="small muted">{e(p["distance"])}（道路距離の目安）</span></dd>
    <dt>集合</dt><dd>ソウル市内（市庁駅または蚕室駅）<br><a class="small text-link" href="#meeting">集合場所について ›</a></dd>
    <dt>含まれるもの</dt><dd>往復の交通（貸切バス）・入場料・添乗員</dd>
    <dt>食事</dt><dd>昼食・夕食なし（各自・自由食）</dd>
  </dl>
</section>

<section class="sec" id="min">
  <div class="box strong stack">
    <h2 style="font-size:17px">催行条件：最少催行人員 10名</h2>
    <p class="small">お申し込みは「仮予約」として受け付けます。同じ日に10名集まった時点で出発が確定し、LINEでお知らせします。</p>
    <div class="demo-status hidden">
      <div class="progress" aria-hidden="true"><span style="width:0%"></span></div>
      <p class="small" style="margin-top:6px"><strong class="demo-text"></strong> <span class="muted">（デモ表示）</span></p>
    </div>
    <p class="small muted">出発3日前までに10名に届かない場合は催行を中止し、お支払い額を全額返金します。</p>
  </div>
</section>

<section class="sec">
  <div class="sec-title"><h2>このツアーのポイント</h2></div>
  <ol style="padding-left:20px;margin:0" class="stack">{hl}</ol>
</section>

<section class="sec">
  <div class="sec-title"><h2>スケジュール</h2></div>
  <ul class="timeline">{shown}</ul>
  <details class="more"><summary>{e(hidden_names)}</summary><div class="inner"><ul class="timeline">{hidden}</ul></div></details>
  <ul class="timeline">{li(last, "end")}</ul>
  <p class="small muted">🍴 昼食・夕食は含まれていません。立ち寄り先で、お好きなお店を選べます。</p>
</section>

<section class="sec tint" id="price">
  <div class="sec-title"><h2>料金</h2></div>
  <p class="price-big"><span data-jpy="{p["price"]}">{krw(p["price"])}</span> <small>（税込）/ 大人1名</small></p>
  <p style="margin-top:4px"><strong>お支払い額：{krw(p["price"])}（韓国ウォン）</strong></p>
  <p class="small muted" data-rate-note></p>
  <p class="small muted">子供（2歳以上）も同額・2歳未満は無料</p>
  <div class="tags" style="margin-top:12px"><span class="tag">友達と</span><span class="tag">カップルで</span><span class="tag">2名からの参加におすすめ</span></div>
  <dl class="kv" style="margin-top:14px">
    <dt>含まれるもの</dt><dd>往復の交通・入場料・添乗員</dd>
    <dt>含まれないもの</dt><dd>食事代・個人的な費用</dd>
  </dl>
  <p style="margin-top:14px"><a class="text-link" href="compare.html#{pid}">ひとりで行く場合と、交通費をくらべる ›</a></p>
</section>

<section class="sec" id="meeting">
  <div class="sec-title"><h2>集合場所</h2></div>
  <p>市庁駅（シチョン駅）または蚕室駅（チャムシル駅）</p>
  <p class="small muted" style="margin-top:4px">集合場所はツアーごとに決まっています。出口番号・目印と地図は、出発確定のLINEでご案内します。</p>
</section>

<section class="sec" id="cancel">
  <div class="sec-title"><h2>キャンセルポリシー</h2></div>
  <table class="cancel-table">
    <tr><th>出発3日前まで</th><td>全額返金</td></tr>
    <tr><th>出発2日前〜当日</th><td>返金なし</td></tr>
    <tr><th>催行中止（10名未満）</th><td>全額返金</td></tr>
  </table>
  <p class="small muted" style="margin-top:8px">※ ご返金は韓国ウォンで行います。為替レートの変動により、円に換算した金額が異なる場合があります。</p>
  <p style="margin-top:8px"><a class="small text-link" href="legal.html#cancel">キャンセルポリシーの全文 ›</a></p>
</section>

<section class="sec tint">
  <div class="sec-title"><h2>販売会社</h2></div>
  <dl class="kv">
    <dt>会社名</dt><dd>ここいこ（KOKOIKO）</dd>
    <dt>所在地</dt><dd>大韓民国 ソウル特別市 松坡区</dd>
    <dt>お問い合わせ</dt><dd>LINE・メール（窓口は準備中です）</dd>
  </dl>
  <p style="margin-top:10px"><a class="small text-link" href="legal.html#tokushoho">特定商取引法に基づく表記 ›</a></p>
</section>

<div class="sticky-cta">
  <p>お申し込み時点では<strong>仮予約</strong>です。10名集まり次第、LINEで出発確定をお知らせします。</p>
  <p>お支払いは韓国ウォン（KRW）です。金額はお手続き開始時に確定します。</p>
  <a class="btn" href="checkout.html?p={pid}">申し込む</a>
</div>
</main>
''' + FOOTER + tail(f'<script>window.PRODUCT_ID = {json.dumps(pid)};</script>\n<script src="js/detail.js"></script>\n')


def page_compare():
    rows = ''
    for pid in ORDER:
        p = PRODUCTS[pid]
        rows += f'''
<section class="sec" id="{pid}">
  <h2 style="font-size:17px">{e(p["short"])}</h2>
  <table class="cmp" style="margin-top:10px">
    <thead><tr><th></th><th>ひとりで行く場合</th><th>ここいこ</th></tr></thead>
    <tbody>
      <tr><th>ソウルからの往復交通</th><td>KTX・高速バス<br><span class="tbd">金額確認中</span></td><td class="ok">込み</td></tr>
      <tr><th>駅・ターミナル→観光地</th><td>タクシー・路線バス<br><span class="tbd">金額確認中</span></td><td class="ok">込み</td></tr>
      <tr><th>観光地どうしの移動</th><td>自分で手配・乗り換え<br><span class="tbd">時間・金額確認中</span></td><td class="ok">貸切バスで移動</td></tr>
      <tr><th>入場料</th><td>現地で別途<br><span class="tbd">金額確認中</span></td><td class="ok">込み</td></tr>
      <tr><th>案内</th><td>なし</td><td class="ok">添乗員が同行</td></tr>
      <tr><th>合計（1名）</th><td><span class="tbd">確認中</span></td><td class="ok">{krw(p["price"])}<br><span class="small" data-jpy="{p["price"]}"></span></td></tr>
    </tbody>
  </table>
</section>'''
    return head('交通費をくらべる ｜ ここいこ', 'ひとりで行く場合と、ここいこのツアーの費用・手間をくらべます。') + header('<a class="header-link" href="index.html#tours">ツアーを見る</a>') + f'''<main>
<section class="sec tint">
  <h1 style="font-size:21px">ひとりで行くより、おトクでラク</h1>
  <p class="muted" style="margin-top:8px">KTXや高速バスで行けるのは、駅やバスターミナルまで。そこから観光地へ、観光地から次の観光地へ──移動のたびに時間と費用がかかります。</p>
</section>
{rows}
<section class="sec">
  <p class="small muted">※ 比較の金額は、各交通機関の公開運賃をもとに掲載します（基準日も併記予定）。</p>
  <p style="margin-top:12px"><a class="btn sub" href="index.html#tours">ツアー一覧へ</a></p>
</section>
</main>
''' + FOOTER + tail()


def page_legal():
    return head('特定商取引法に基づく表記・各種ポリシー ｜ ここいこ', 'ここいこ（KOKOIKO）の特定商取引法に基づく表記、キャンセルポリシー、プライバシーポリシー') + header('<a class="header-link" href="index.html">トップへ</a>') + '''<main>
<section class="sec" id="tokushoho">
  <h1 style="font-size:20px;margin-bottom:14px">特定商取引法に基づく表記</h1>
  <table class="legal-table">
    <tr><th>販売業者</th><td>KOKOIKO（ここいこ）</td></tr>
    <tr><th>運営責任者</th><td>SUN IL ROH</td></tr>
    <tr><th>所在地</th><td>大韓民国 ソウル特別市 松坡区（詳細は確定後に掲載します）</td></tr>
    <tr><th>電話番号・メールアドレス</th><td>確定後に掲載します</td></tr>
    <tr><th>販売価格</th><td>各ツアーページに記載（お一人様 ₩90,000〜₩100,000、2歳未満は無料）</td></tr>
    <tr><th>商品代金以外の必要料金</th><td>現地での食事代・個人的な費用。海外決済となるため、カード会社所定の手数料がかかる場合があります。</td></tr>
    <tr><th>お支払い方法</th><td>クレジットカード</td></tr>
    <tr><th>お支払い時期</th><td>お申し込み時</td></tr>
    <tr><th>サービスの提供時期</th><td>お客様が選択したツアー催行日</td></tr>
    <tr><th>キャンセル・返金</th><td>下記「キャンセルポリシー」をご確認ください。</td></tr>
    <tr><th>旅行業登録</th><td>確定後に掲載します</td></tr>
  </table>
</section>

<section class="sec" id="cancel">
  <h2 style="margin-bottom:14px">キャンセルポリシー</h2>
  <table class="cancel-table">
    <tr><th>出発3日前までのキャンセル</th><td>全額返金</td></tr>
    <tr><th>出発2日前〜当日のキャンセル</th><td>返金なし</td></tr>
    <tr><th>催行中止（出発3日前までに10名に満たない場合）</th><td>全額返金</td></tr>
  </table>
  <ul class="small muted" style="padding-left:18px;margin-top:10px">
    <li>天災、またはご参加者ご本人・直系のご家族のご逝去による場合は、上記にかかわらずご相談ください。</li>
    <li>ご返金は韓国ウォンで行います。為替レートの変動により、円に換算した金額がお支払い時と異なる場合があります。</li>
    <li>カード会社の海外決済手数料は、返金の対象とならない場合があります。</li>
  </ul>
</section>

<section class="sec" id="privacy">
  <h2 style="margin-bottom:14px">プライバシーポリシー</h2>
  <p class="small">お申し込み時にいただくお名前・電話番号・LINE IDは、ツアーのご案内（出発確定・中止のご連絡、集合場所のご案内）とお問い合わせへの対応のために利用します。</p>
  <p class="small muted" style="margin-top:8px">プライバシーポリシーの全文は準備中です。</p>
</section>
</main>
''' + FOOTER + tail()


def page_checkout():
    return head('お申し込み ｜ ここいこ', 'ツアーのお申し込み', '<meta name="robots" content="noindex">\n<script src="https://js.tosspayments.com/v2/standard"></script>\n') + header('<a class="header-link" href="javascript:history.back()">‹ 戻る</a>') + '''<main>
<section class="sec tint">
  <p class="small muted">お申し込みツアー</p>
  <h1 id="co-name" style="font-size:16px;margin-top:2px"></h1>
  <p class="small" style="margin-top:4px"><span id="co-unit"></span> / 1名（2歳未満は無料）</p>
</section>

<section class="sec">
  <h2 class="step-title">① 日程を選ぶ</h2>
  <div id="suggest-wrap" class="hidden">
    <p class="small" style="font-weight:700;margin-bottom:8px">まもなく出発確定の日程 <span class="muted" style="font-weight:400">（デモ表示）</span></p>
    <div class="date-cards" id="suggest"></div>
    <p class="small muted" style="margin:12px 0 8px">ご希望の日がない場合は、カレンダーから選べます。</p>
  </div>
  <div class="cal" id="cal"></div>
  <p class="small muted" style="margin-top:8px">お申し込みは出発の4日前まで。韓国の祝日は催行していません。</p>
  <p class="small" id="date-picked" style="margin-top:8px;font-weight:700"></p>
</section>

<section class="sec">
  <h2 class="step-title">② 人数</h2>
  <div class="stepper-row"><div><strong>大人</strong><br><span class="small muted" id="u-adult"></span></div><div class="stepper" data-key="adults"><button type="button" data-d="-1" aria-label="大人を減らす">−</button><output>2</output><button type="button" data-d="1" aria-label="大人を増やす">＋</button></div></div>
  <div class="stepper-row"><div><strong>子供（2歳以上）</strong><br><span class="small muted" id="u-child"></span></div><div class="stepper" data-key="children"><button type="button" data-d="-1" aria-label="子供を減らす">−</button><output>0</output><button type="button" data-d="1" aria-label="子供を増やす">＋</button></div></div>
  <div class="stepper-row"><div><strong>幼児（2歳未満）</strong><br><span class="small muted">無料</span></div><div class="stepper" data-key="infants"><button type="button" data-d="-1" aria-label="幼児を減らす">−</button><output>0</output><button type="button" data-d="1" aria-label="幼児を増やす">＋</button></div></div>
</section>

<section class="sec">
  <h2 class="step-title">③ 代表者情報</h2>
  <label class="field" id="f-name"><span class="label">お名前（ローマ字）<span class="req">必須</span></span><input id="in-name" autocomplete="name" placeholder="例）YAMADA HANAKO"><span class="err">お名前を入力してください</span></label>
  <label class="field" id="f-phone"><span class="label">電話番号<span class="req">必須</span></span><input id="in-phone" type="tel" autocomplete="tel" placeholder="例）090-1234-5678"><span class="err">電話番号を入力してください</span></label>
  <label class="field" id="f-line"><span class="label">LINE ID<span class="req">必須</span></span><input id="in-line" autocomplete="off" placeholder="例）hanako_trip"><span class="hint">出発確定・中止のご連絡は、LINEでお送りします。</span><span class="err">LINE IDを入力してください</span></label>
</section>

<section class="sec tint">
  <div class="total-row"><span>お支払い合計</span><strong id="total">—</strong></div>
  <p class="small muted" id="total-jpy" style="text-align:right"></p>
  <p class="small muted" style="margin-top:6px">お支払いは韓国ウォン（KRW）です。金額は「お支払いへ進む」を押した時点で確定します。</p>
</section>

<section class="sec">
  <h2 class="step-title">④ 確認・同意</h2>
  <label class="check"><input type="checkbox" id="ag-tentative"><span>お申し込み時点では仮予約であり、出発3日前までに10名に満たない場合は催行中止・全額返金となることに同意します。</span></label>
  <label class="check"><input type="checkbox" id="ag-cancel"><span><a class="text-link" href="legal.html#cancel" target="_blank">キャンセルポリシー</a>に同意します。</span></label>
  <label class="check"><input type="checkbox" id="ag-privacy"><span><a class="text-link" href="legal.html#privacy" target="_blank">プライバシーポリシー</a>に同意します。</span></label>
  <div class="error-box hidden" id="form-error" style="margin-top:14px"></div>
  <button class="btn" id="to-pay" type="button" style="margin-top:16px">お支払いへ進む</button>
</section>

<section class="sec hidden" id="pay-sec">
  <h2 class="step-title">⑤ お支払い</h2>
  <div class="notice" id="locked"></div>
  <div id="payment-method" style="margin-top:12px"></div>
  <div id="agreement"></div>
  <p class="small muted">海外決済のため、ご利用のカード会社により手数料がかかる場合があります。</p>
  <button class="btn" id="pay-btn" type="button" style="margin-top:12px" disabled>支払う</button>
  <button class="btn sub" id="edit-btn" type="button" style="margin-top:8px">内容を変更する</button>
</section>

<section class="sec" style="background:#f1f1f1">
  <p class="small muted">商号 ここいこ（KOKOIKO）｜代表者 SUN IL ROH｜事業者登録番号（사업자등록번호）確定後に掲載｜通信販売業申告番号（통신판매업 신고번호）確定後に掲載｜所在地 大韓民国 ソウル特別市 松坡区｜電話番号 確定後に掲載</p>
  <p class="small" style="margin-top:6px"><a href="legal.html#tokushoho">利用規約・特定商取引法に基づく表記</a> ・ <a href="legal.html#privacy">プライバシーポリシー</a> ・ <a href="legal.html#cancel">返金ポリシー</a></p>
</section>
</main>
''' + tail('<script src="js/checkout.js"></script>\n')


def page_success():
    return head('お申し込み完了 ｜ ここいこ', 'お申し込みを受け付けました', '<meta name="robots" content="noindex">\n') + header() + '''<main>
<section class="sec" id="loading" style="text-align:center;padding:60px 18px">
  <div class="spinner"></div><p class="muted" style="margin-top:14px">お支払いを確認しています…</p>
</section>

<div id="done" class="hidden">
<section class="sec stack">
  <div class="result-icon">✓</div>
  <h1 style="font-size:22px">お申し込みを受け付けました</h1>
  <p style="font-weight:700">※ まだ出発確定ではありません（仮予約）</p>
  <p class="small muted">同じ日に10名集まった時点で出発が確定し、LINEでお知らせします。</p>
</section>
<section class="sec tint">
  <h2 style="font-size:17px;margin-bottom:10px">ご予約内容</h2>
  <dl class="kv" id="summary"></dl>
</section>
<section class="sec hidden" id="demo-box">
  <div class="box strong"><p class="small"><strong id="demo-text"></strong> <span class="muted">（デモ表示）</span></p></div>
</section>
<section class="sec">
  <h2 style="font-size:17px;margin-bottom:10px">このあとの流れ</h2>
  <ol style="padding-left:20px;margin:0" class="stack small">
    <li>LINEで「ここいこ」を友だち追加してください。</li>
    <li>出発3日前までに、出発確定または中止をLINEでお知らせします。集合場所の詳細も、このときにご案内します。</li>
    <li>中止の場合は、お支払い額を全額返金します（お手続きは不要です）。</li>
  </ol>
  <a class="btn line" href="#" id="line-add" style="margin-top:18px">LINEで友だち追加</a>
  <p class="small muted" style="margin-top:6px;text-align:center">LINE公式アカウントは準備中です</p>
  <a class="btn sub" href="index.html" style="margin-top:10px">トップへ戻る</a>
</section>
</div>

<section class="sec hidden stack" id="ng">
  <div class="result-icon ng">!</div>
  <h1 style="font-size:20px">お支払いを完了できませんでした</h1>
  <div class="error-box" id="ng-msg"></div>
  <p class="small">料金は請求されていません。お手数ですが、もう一度お試しください。</p>
  <a class="btn" href="#" id="retry">お申し込み画面へ戻る</a>
</section>
</main>
''' + tail('<script src="js/success.js"></script>\n')


def page_fail():
    return head('お支払いエラー ｜ ここいこ', 'お支払いが完了しませんでした', '<meta name="robots" content="noindex">\n') + header() + '''<main>
<section class="sec stack">
  <div class="result-icon ng">!</div>
  <h1 style="font-size:20px">お支払いが完了しませんでした</h1>
  <p>お申し込みはまだ受け付けていません。料金は請求されていません。</p>
  <div class="error-box"><p id="f-msg">お支払いが中断されました。</p><p class="small" id="f-code" style="margin-top:4px"></p></div>
  <a class="btn" href="#" id="retry">もう一度お支払いへ</a>
  <a class="btn sub" href="index.html">トップへ戻る</a>
</section>
</main>
''' + tail('<script src="js/fail.js"></script>\n')


def write(name, content):
    with open(os.path.join(ROOT, name), 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    write('index.html', page_index())
    for pid in ORDER:
        write(f'{pid}.html', page_detail(pid))
    write('compare.html', page_compare())
    write('legal.html', page_legal())
    write('checkout.html', page_checkout())
    write('success.html', page_success())
    write('fail.html', page_fail())
    print('built')

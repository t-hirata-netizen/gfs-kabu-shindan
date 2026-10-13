"""GFS のサイトに置く用（https://gfs.tokyo/shindan/）の、診断のファイル一式を作る。

使い方:
  python3 ~/gfs-style-check-chara/tools/build_gfs.py
  → ~/my-project/gfs-shindan_日付.zip ができる（中身は shindan/ フォルダ）

GFS のサイトの開発担当者に渡し、サイトの /shindan/ に置いてもらう（「ファイルを置く」方式のとき）。
「転送」方式（nginx で gfs.tokyo/shindan/ → GitHub Pages）のときは、この zip は要らない。

変えるのは LINE などで URL を送ったときの og:url / og:image だけ（gfs.tokyo/shindan/ を指すようにする）。
判定・集計などの中身は GitHub Pages の本番と同じ。集計は gfs.tokyo/shindan/ からも送る（score.js の collectAllowed）。
"""
import os, zipfile, datetime, re

H = os.path.expanduser
SRC = H('~/gfs-style-check-chara')
OUT = H(f'~/my-project/gfs-shindan_{datetime.date.today():%Y%m%d}.zip')
GH = 'https://t-hirata-netizen.github.io/gfs-kabu-shindan/'
GFS = 'https://gfs.tokyo/shindan/'
FILES = ['index.html', 'score.js', 'img/kabu-tech.webp', 'img/kabu-fund.webp', 'og/default.png']

html = open(f'{SRC}/index.html', encoding='utf-8').read()
for tag in ('og:url', 'og:image'):
    assert re.search(rf'<meta property="{tag}" content="{re.escape(GH)}', html), tag
html = html.replace(f'<meta property="og:url" content="{GH}">', f'<meta property="og:url" content="{GFS}">')
html = html.replace(f'<meta property="og:image" content="{GH}og/default.png">', f'<meta property="og:image" content="{GFS}og/default.png">')
assert GH not in html, 'index.html に GitHub の URL が残っています'
assert '<meta name="robots" content="noindex, nofollow">' in html

with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in FILES:
        if f == 'index.html':
            z.writestr('shindan/index.html', html)
        else:
            z.write(f'{SRC}/{f}', f'shindan/{f}')
print('作りました:', OUT)
for i in zipfile.ZipFile(OUT).infolist():
    print(f'  {i.filename}  {i.file_size:,} バイト')

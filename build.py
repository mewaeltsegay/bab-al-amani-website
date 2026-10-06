"""Build the static site.

Pages live in src/pages/*.html. Each starts with a header comment:

    <!--
    title: Page title
    description: One sentence for search results.
    nav: trade            (optional: which menu item to mark as current)
    -->

The rest of the file is the page body. This script wraps it in src/layout.html
and writes the result to the project root, plus sitemap.xml.

Run:  python build.py
"""
import datetime
import hashlib
import pathlib
import re
import shutil

ROOT = pathlib.Path(__file__).parent
PUBLIC_FILES = ['styles.css', 'script.js', 'favicon.ico', 'favicon-32.png', 'apple-touch-icon.png', 'robots.txt', 'sitemap.xml', '_headers', '_redirects']
PUBLIC_DIRS = ['assets', '.well-known']
SRC = ROOT / 'src'
SITE = 'https://babalamani.com'  # the live domain

MARK = '<img class="mark" src="assets/img/logo.png" alt="" width="256" height="256">'
MARK_LIGHT = '<img class="mark" src="assets/img/logo-badge.png" alt="" width="256" height="256">'
NAV_KEYS = ['trade', 'markets', 'tenders', 'about', 'faq', 'contact']
DRAFT_RE = re.compile(r'[ \t]*<section[^>]*\bdata-draft\b[^>]*>.*?</section>\n?', re.S)


def parse(path):
    text = path.read_text(encoding='utf-8')
    m = re.match(r'\s*<!--(.*?)-->\s*', text, re.S)
    meta = dict(re.findall(r'^\s*(\w+):\s*(.+?)\s*$', m.group(1), re.M))
    return meta, text[m.end():]


def render(layout, meta, body, out_name):
    html = layout.replace('{{content}}', body.rstrip())
    canonical = SITE + '/' + ('' if out_name == 'index.html' else out_name)
    for key in NAV_KEYS:
        html = html.replace('{{cur:%s}}' % key, ' aria-current="page"' if meta.get('nav') == key else '')
    # Cache-busting: a short content hash, so browsers fetch new CSS/JS after every change.
    for name in ('styles.css', 'script.js'):
        digest = hashlib.sha1((ROOT / name).read_bytes()).hexdigest()[:8]
        html = html.replace('{{v:%s}}' % name, digest)
    # Highlight unfilled placeholders like [000000] so they're easy to spot before launch.
    html = re.sub(r'(?<!fill">)\[([^\]<>\n]{1,40})\]', r'<span class="fill">[\1]</span>', html)
    return (html.replace('{{title}}', meta['title'])
                .replace('{{description}}', meta['description'])
                .replace('{{canonical}}', canonical)
                .replace('{{site}}', SITE)
                .replace('{{mark}}', MARK)
                .replace('{{mark-light}}', MARK_LIGHT)
                .replace('{{year}}', str(datetime.date.today().year)))


def main():
    layout = (SRC / 'layout.html').read_text(encoding='utf-8')
    urls = []
    for page in sorted((SRC / 'pages').glob('*.html')):
        meta, body = parse(page)
        (ROOT / page.name).write_text(render(layout, meta, body, page.name), encoding='utf-8')
        if page.name != '404.html':
            urls.append(SITE + '/' + ('' if page.name == 'index.html' else page.name))
        print('built', page.name)

    today = datetime.date.today().isoformat()
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>',
               '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    sitemap += [f'  <url><loc>{u}</loc><lastmod>{today}</lastmod></url>' for u in urls]
    sitemap.append('</urlset>')
    (ROOT / 'sitemap.xml').write_text('\n'.join(sitemap) + '\n', encoding='utf-8')
    print('built sitemap.xml')

    # dist/ holds only the public files, ready to upload to Cloudflare Pages.
    dist = ROOT / 'dist'
    shutil.rmtree(dist, ignore_errors=True)
    dist.mkdir()
    # Sections marked data-draft show in the local preview but are left out of dist/.
    for page in (SRC / 'pages').glob('*.html'):
        html = (ROOT / page.name).read_text(encoding='utf-8')
        html, drafts = DRAFT_RE.subn('', html)
        (dist / page.name).write_text(html, encoding='utf-8')
        if drafts:
            print(f'  left {drafts} draft section(s) out of dist/{page.name}')
    for f in PUBLIC_FILES:
        shutil.copy2(ROOT / f, dist / f)
    for d in PUBLIC_DIRS:
        shutil.copytree(ROOT / d, dist / d)
    print('packaged dist/')


if __name__ == '__main__':
    main()

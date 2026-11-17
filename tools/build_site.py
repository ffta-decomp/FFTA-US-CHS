#!/usr/bin/env python3
# SPDX-License-Identifier: GPL-3.0-or-later
"""Build one offline HTML document from this public repository; Python stdlib only."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
CHARSET = 'charset/v4.1/'
FILES = ['README.md', 'CHANGELOG.md'] + [CHARSET + name for name in (
    'README.md', 'FONT-LAYOUT.md', 'glyphs.json', 'glyphs.csv', 'decode.tbl',
    'font-layout.json', 'SHA256SUMS.txt')]
DOCS = {'README.md': 'overview', 'CHANGELOG.md': 'changes',
        CHARSET+'README.md': 'charset-guide', CHARSET+'FONT-LAYOUT.md': 'fonts'}
DOWNLOADS = {CHARSET+n: n for n in (
    'glyphs.json', 'glyphs.csv', 'decode.tbl', 'font-layout.json', 'SHA256SUMS.txt')}


def inline(text, source):
    chunks = re.split(r'(`[^`]+`|\[[^\]]+\]\([^\s)]+\))', text)
    rendered = []
    for chunk in chunks:
        if chunk.startswith('`') and chunk.endswith('`'):
            rendered.append('<code>'+html.escape(chunk[1:-1])+'</code>')
            continue
        link = re.fullmatch(r'\[([^\]]+)\]\(([^\s)]+)\)', chunk)
        if link:
            label, href = link.groups()
            local = (Path(source).parent / href).as_posix().rstrip('/')
            if local == 'charset/v4.1':
                local += '/README.md'
            if local in DOCS:
                target = '#' + ('charset' if DOCS[local] == 'charset-guide' else DOCS[local])
                attrs = 'href="'+target+'"'
            elif local in DOWNLOADS:
                attrs = 'href="#" data-download="'+html.escape(local, quote=True)+'"'
            elif href.startswith(('https://', 'http://')):
                attrs = 'href="'+html.escape(href, quote=True)+'" target="_blank" rel="noopener noreferrer"'
            else:
                rendered.append(html.escape(label))
                continue
            rendered.append('<a '+attrs+'>'+html.escape(label)+'</a>')
            continue
        safe = html.escape(chunk)
        rendered.append(re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', safe))
    return ''.join(rendered)


def markdown(text, source):
    """Render the headings/lists/tables/code blocks used by the public documents.

    Raw HTML is escaped; unrecognised markup remains readable text. No plugins,
    scripts or remote resources are evaluated while reading Markdown.
    """
    lines = text.splitlines()
    out, i = [], 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.startswith('```'):
            block = []
            i += 1
            while i < len(lines) and not lines[i].startswith('```'):
                block.append(lines[i]); i += 1
            out.append('<pre><code>'+html.escape('\n'.join(block))+'</code></pre>')
            i += 1
            continue
        if line.startswith('|') and i+1 < len(lines) and re.fullmatch(r'[|\s:\-]+', lines[i+1]):
            cells = lambda s: s.strip().strip('|').split('|')
            out.append('<div class="table-scroll"><table><thead><tr>'+''.join(
                '<th>'+inline(c.strip(), source)+'</th>' for c in cells(line))+'</tr></thead><tbody>')
            i += 2
            while i < len(lines) and lines[i].startswith('|'):
                out.append('<tr>'+''.join('<td>'+inline(c.strip(), source)+'</td>' for c in cells(lines[i]))+'</tr>')
                i += 1
            out.append('</tbody></table></div>')
            continue
        heading = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading:
            level = min(6, len(heading[1])+1)
            out.append(f'<h{level}>'+inline(heading[2], source)+f'</h{level}>')
        elif re.match(r'^\s*[-*] ', line):
            out.append('<ul>')
            while i < len(lines) and re.match(r'^\s*[-*] ', lines[i]):
                out.append('<li>'+inline(re.sub(r'^\s*[-*] ', '', lines[i]), source)+'</li>'); i += 1
            out.append('</ul>')
            continue
        elif line.startswith('>'):
            out.append('<blockquote>'+inline(line.lstrip('> '), source)+'</blockquote>')
        elif re.fullmatch(r'\s*[-*_]{3,}\s*', line):
            out.append('<hr>')
        else:
            paragraph = [line]
            while i+1 < len(lines) and lines[i+1].strip() and not re.match(r'^(#|\||```|[-*] |>)', lines[i+1]):
                i += 1; paragraph.append(lines[i])
            out.append('<p>'+inline(' '.join(paragraph), source)+'</p>')
        i += 1
    return '\n'.join(out)


def build(output):
    data = {name: (ROOT/name).read_text(encoding='utf-8-sig') for name in FILES}
    for line in data[CHARSET+'SHA256SUMS.txt'].splitlines():
        digest, name = line.split('  ', 1)
        if Path(name).name != name or hashlib.sha256((ROOT/CHARSET/name).read_bytes()).hexdigest() != digest:
            raise ValueError('Public charset checksum differs: '+name)
    glyphs = json.loads(data[CHARSET+'glyphs.json'])
    entries = glyphs['entries']
    if [r['glyph_id'] for r in entries] != list(range(4368)):
        raise ValueError('Glyph IDs must remain complete and ordered')
    for r in entries:
        expected = f'{r["glyph_id"]+1:02X}' if r['glyph_id'] < 168 else f'{r["glyph_id"]+0xA858:04X}'
        if r['game_code_hex'] != expected:
            raise ValueError('Game-code mapping differs')
        if r['unicode'] is not None and r['unicode'] != f'U+{ord(r["character"]):04X}':
            raise ValueError('Unicode mapping differs')
    payload = json.dumps({'files': data}, ensure_ascii=False, separators=(',', ':'))
    payload = payload.replace('&', '\\u0026').replace('<', '\\u003c').replace('>', '\\u003e')
    template = (ROOT/'site/template.html').read_text(encoding='utf-8')
    for name, panel in DOCS.items():
        template = template.replace('__DOC_'+panel.upper().replace('-', '_')+'__', markdown(data[name], name))
    result = template.replace('__PAYLOAD__', payload).encode('utf-8')
    output.mkdir(parents=True, exist_ok=True)
    page = output/'index.html'
    page.write_bytes(result)
    package = output/'ffta2-public-site.zip'
    info = zipfile.ZipInfo('index.html', date_time=(2026, 1, 1, 0, 0, 0))
    info.create_system = 3
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o100644 << 16
    with zipfile.ZipFile(package, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        archive.writestr(info, result, compresslevel=9)
    with zipfile.ZipFile(package) as archive:
        if archive.namelist() != ['index.html'] or archive.read('index.html') != result or archive.testzip():
            raise ValueError('Single-HTML ZIP readback failed')
    receipt = dict(html=page.name, html_bytes=len(result), html_SHA256=hashlib.sha256(result).hexdigest(),
                   ZIP=package.name, ZIP_bytes=package.stat().st_size,
                   ZIP_SHA256=hashlib.sha256(package.read_bytes()).hexdigest(),
                   ZIP_members=['index.html'], build_dependencies='Python standard library only',
                   inputs={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in FILES},
                   builder_inputs={name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
                                   for name in ('tools/build_site.py', 'site/template.html')},
                   glyph_rows=len(entries))
    (output/'build.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'dist/site')
    print(json.dumps(build(parser.parse_args().output.resolve()), ensure_ascii=False, indent=2))

"""Build the launch/event edition with a genuine tandpay.com QR and no access label."""
from pathlib import Path
import re
import build_escrow_artwork as base

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "v3"


def build():
    base.OUT = OUT
    base.build()
    source = OUT / "tandpay-escrow-booth-2000mm.svg"
    svg = source.read_text()
    svg = re.sub(r'<circle cx="1623" cy="1804"[^>]*/>\s*', '', svg)
    svg = re.sub(r'<text[^>]*>EARLY ACCESS</text>\s*', '', svg)
    qr = (ROOT / "assets/tandpay-com-qr.svg").read_text().strip()
    viewbox = re.search(r'viewBox="([^"]+)"', qr).group(1)
    inner = re.sub(r'^<svg\b[^>]*>', '', qr)
    inner = re.sub(r'</svg>$', '', inner)
    panel = f'''<g id="tandpay-website-qr">
<title>Scan to open https://tandpay.com</title>
<svg x="1550" y="375" width="320" height="320" viewBox="{viewbox}" shape-rendering="crispEdges">{inner}</svg>
<text x="1710" y="752" text-anchor="middle" fill="#EFA524" font-size="23" font-weight="700" letter-spacing="2.5">SCAN TO GET STARTED</text>
<text x="1710" y="808" text-anchor="middle" fill="#FBFBFB" font-size="39" font-weight="650" letter-spacing="-1">tandpay.com</text>
</g>
'''
    svg = svg.rsplit('</svg>', 1)[0] + panel + '</svg>'
    svg = svg.replace('<title>TandPay — Escrow protection for social commerce</title>', '<title>TandPay — Escrow protection for social commerce — launch edition</title>', 1)
    source.write_text(svg)
    html_path = OUT / "artwork.html"
    html = html_path.read_text()
    start = html.index('<svg ')
    end = html.rindex('</svg>') + len('</svg>')
    html_path.write_text(html[:start] + svg + html[end:])
    assert 'EARLY ACCESS' not in svg
    assert 'tandpay.com' in svg
    print('Launch artwork: 320 mm vector QR for https://tandpay.com; access label removed.')


if __name__ == "__main__":
    build()

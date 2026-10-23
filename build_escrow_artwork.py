"""Build the escrow-focused 2 metre booth wall using vector artwork throughout."""
from pathlib import Path
import base64
import re

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "v2"


def icon(kind, x, y, colour):
    paths = {
        "pay": '<rect x="14" y="5" width="43" height="66" rx="8"/><path d="M27 14h17M30 61h11"/><path d="M26 38l8 8 15-18"/>',
        "protect": '<path d="M36 4L63 15v21c0 18-12 29-27 36C21 65 9 54 9 36V15Z"/><path d="M23 36l10 10 18-21"/>',
        "confirm": '<path d="M8 22L35 8l29 14v33L36 71 8 55Z"/><path d="M8 22l28 16 28-16M36 38v33M22 15l28 16"/><path d="M48 48l6 6 13-15"/>',
        "release": '<rect x="6" y="20" width="59" height="44" rx="8"/><path d="M11 20v-6a5 5 0 0 1 5-5h40M49 38h16M33 35v18M25 45l8 8 8-8"/>',
    }
    return f'<g transform="translate({x} {y})" fill="none" stroke="{colour}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">{paths[kind]}</g>'


def card(x, number, heading, lines, kind, featured=False, size=40):
    fill = "#F7F6F0" if featured else "#0B4B48"
    text = "#093F3E" if featured else "#FBFBFB"
    muted = "#385D57" if featured else "#DCEFEA"
    accent = "#0E6B62" if featured else "#EFA524"
    stroke = "#F7F6F0" if featured else "#3A7168"
    markup = f'<rect x="{x}" y="865" width="365" height="398" rx="26" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
    markup += f'<text x="{x+31}" y="925" fill="{accent}" font-size="25" font-weight="700" letter-spacing="2">{number}</text>'
    markup += icon(kind, x + 266, 893, text if featured else "#EFA524")
    markup += f'<text x="{x+31}" y="1054" fill="{text}" font-size="{size}" font-weight="750" letter-spacing="-1.3">{heading}</text>'
    for index, line in enumerate(lines):
        markup += f'<text x="{x+31}" y="{1130+index*43}" fill="{muted}" font-size="28" font-weight="450" letter-spacing="-.3">{line}</text>'
    return markup


def build():
    OUT.mkdir(exist_ok=True)
    mark = (ROOT / "assets/tandpay-mark-vectorized.svg").read_text()
    path = re.search(r' d="([^"]+)"', mark).group(1)
    font = base64.b64encode((ROOT / "assets/manrope.woff2").read_bytes()).decode()
    cards = "".join([
        card(130, "01", "Pay", ["Buyer pays with", "Mobile Money."], "pay", size=48),
        card(590, "02", "Protect", ["Funds protected through", "the escrow layer."], "protect", featured=True, size=48),
        card(1050, "03", "Confirm", ["Buyer inspects the item,", "then enters its code."], "confirm", size=48),
        card(1510, "04", "Release", ["Confirmation authorizes", "payment release."], "release", size=48),
    ])
    arrows = "".join(f'<path d="M{x} 1064h47m-15-15 15 15-15 15"/>' for x in [518, 978, 1438])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="2000mm" height="2000mm" viewBox="0 0 2000 2000">
<title>TandPay — Escrow protection for social commerce</title>
<desc>A 2 metre square booth wall emphasizing TandPay's escrow layer and buyer and seller protection. Four stages show buyer payment, protected funds, buyer inspection and confirmation, and authorized payment release.</desc>
<defs><style>@font-face{{font-family:Manrope;src:url("data:font/woff2;base64,{font}") format("woff2");font-weight:200 800;}}text{{font-family:Manrope,Arial,sans-serif;}}</style></defs>
<rect width="2000" height="2000" fill="#093F3E"/>
<g transform="translate(110 113) scale(.47)"><path fill="#EFA524" fill-rule="evenodd" d="{path}"/></g>
<text x="247" y="212" fill="#FBFBFB" font-size="104" font-weight="750" letter-spacing="-5">TandPay.</text>
<text x="1860" y="186" text-anchor="end" fill="#DCEFEA" font-size="24" font-weight="600" letter-spacing="4">BUILT IN RWANDA</text>

<g font-weight="750" letter-spacing="-5.6">
  <text x="130" y="480" fill="#FBFBFB" font-size="142"><tspan fill="#EFA524">Escrow</tspan> protection.</text>
  <text x="130" y="646" fill="#FBFBFB" font-size="124">For social commerce.</text>
</g>
<text x="137" y="754" fill="#DCEFEA" font-size="39" font-weight="450" letter-spacing="-.7">Protection built around buyers and sellers.</text>

{cards}
<g fill="none" stroke="#EFA524" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round">{arrows}</g>

<g>
  <text x="137" y="1440" fill="#EFA524" font-size="25" font-weight="700" letter-spacing="3">BUYER PROTECTION</text>
  <text x="137" y="1510" fill="#FBFBFB" font-size="45" font-weight="650" letter-spacing="-1.3">Inspect before confirming.</text>
  <text x="1050" y="1440" fill="#EFA524" font-size="25" font-weight="700" letter-spacing="3">SELLER PROTECTION</text>
  <text x="1050" y="1510" fill="#FBFBFB" font-size="43" font-weight="650" letter-spacing="-1.3">Verify payment before dispatch.</text>
</g>
<text x="137" y="1650" fill="#FBFBFB" font-size="48" font-weight="650" letter-spacing="-.8">See escrow in action. Ask us for a demo.</text>
<g transform="translate(1660 1620)" fill="none" stroke="#EFA524" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"><path d="M0 14h44M30 0l14 14-14 14"/></g>

<path d="M137 1750H1863" stroke="#DCEFEA" stroke-opacity=".25" stroke-width="1.5"/>
<text x="137" y="1815" fill="#DCEFEA" font-size="26" font-weight="450">Partner-managed funds. Transaction terms apply.</text>
<circle cx="1623" cy="1804" r="6" fill="#EFA524"/>
<text x="1863" y="1815" fill="#DCEFEA" font-size="23" font-weight="650" text-anchor="end" letter-spacing="3">EARLY ACCESS</text>
</svg>'''
    (OUT / "tandpay-escrow-booth-2000mm.svg").write_text(svg)
    html = '''<!doctype html><html><head><meta charset="utf-8"><title>TandPay escrow booth artwork</title>
<style>*{box-sizing:border-box}html,body{margin:0;padding:0;background:#093f3e}.art{width:2000px;height:2000px}.art svg{width:100%;height:100%;display:block}@page{size:2000mm 2000mm;margin:0}@media print{html,body,.art{width:2000mm;height:2000mm;margin:0;padding:0}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}</style>
</head><body><main class="art">''' + svg + "</main></body></html>"
    (OUT / "artwork.html").write_text(html)
    print("Built v2: escrow-led artwork, 2000 × 2000 mm, entirely vector.")


if __name__ == "__main__":
    build()

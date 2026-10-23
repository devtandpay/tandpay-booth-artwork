"""Build a 2000 mm square booth wall with vector lettering and a raster illustration."""
import base64
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / "assets"


def embedded(path, mime):
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode()


def simplify(points, tolerance=1.1):
    if len(points) < 3:
        return points
    a, b = points[0], points[-1]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    distances = [abs(dy * (x - a[0]) - dx * (y - a[1])) / length
                 if length else math.hypot(x - a[0], y - a[1])
                 for x, y in points]
    index = max(range(len(points)), key=distances.__getitem__)
    if distances[index] <= tolerance:
        return [a, b]
    return simplify(points[:index + 1], tolerance)[:-1] + simplify(points[index:], tolerance)


def trace_mark():
    """Trace the supplied logo alpha, preserving its silhouette for large-format use."""
    raw = (ASSETS / "logo-rgba.raw").read_bytes()
    dimension = math.isqrt(len(raw) // 4)
    scale = 256 / dimension
    mask = {(x, y) for y in range(dimension) for x in range(dimension)
            if raw[(y * dimension + x) * 4 + 3] >= 128}
    edges = {}
    for x, y in sorted(mask):
        for neighbour, a, b in [
            ((x, y-1), (x, y), (x+1, y)),
            ((x+1, y), (x+1, y), (x+1, y+1)),
            ((x, y+1), (x+1, y+1), (x, y+1)),
            ((x-1, y), (x, y+1), (x, y)),
        ]:
            if neighbour not in mask:
                edges.setdefault(a, []).append(b)
    contours = []
    while edges:
        start = min(edges)
        point, contour = start, [start]
        while True:
            next_point = edges[point].pop()
            if not edges[point]:
                del edges[point]
            contour.append(next_point)
            point = next_point
            if point == start:
                break
        if len(contour) > 8:
            middle = len(contour) // 2
            contour = simplify(contour[:middle + 1])[:-1] + simplify(contour[middle:])
            contours.append("M" + " L".join(f"{x*scale:g},{y*scale:g}" for x, y in contour) + "Z")
    path = " ".join(contours)
    (ASSETS / "tandpay-mark-vectorized.svg").write_text(
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 256 256">'
        f'<path fill="#EFA524" fill-rule="evenodd" d="{path}"/></svg>')
    return path


def build():
    logo_path = trace_mark()
    font = embedded(ASSETS / "manrope.woff2", "font/woff2")
    seller = embedded(ASSETS / "seller-illustration.png", "image/png")
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="2000mm" height="2000mm" viewBox="0 0 2000 2000">
  <title>TandPay — 2 metre square exhibition wall</title>
  <desc>A forest green booth wall with gold branding, a social seller illustration, and the message Sell on social media. Run the business on TandPay.</desc>
  <defs>
    <style>@font-face{{font-family:Manrope;src:url("{font}") format("woff2");font-weight:200 800;}} text{{font-family:Manrope,Arial,sans-serif;}}</style>
  </defs>
  <rect width="2000" height="2000" fill="#093F3E"/>
  <g transform="translate(110 113) scale(.47)"><path fill="#EFA524" fill-rule="evenodd" d="{logo_path}"/></g>
  <text x="247" y="212" fill="#FBFBFB" font-size="104" font-weight="750" letter-spacing="-5">TandPay.</text>
  <text x="1860" y="186" text-anchor="end" fill="#DCEFEA" font-size="24" font-weight="600" letter-spacing="4">BUILT IN RWANDA</text>
  <path d="M1210 1470 V800 A330 330 0 0 1 1870 800 V1470 Z" fill="#F7F6F0"/>
  <image href="{seller}" x="1080" y="475" width="850" height="1075" preserveAspectRatio="xMidYMid meet"/>
  <g fill="#FBFBFB" font-size="132" font-weight="750" letter-spacing="-5.2">
    <text x="130" y="515">Sell on</text>
    <text x="130" y="670">social media.</text>
    <text x="130" y="840" font-size="108" letter-spacing="-4.6">Run the business</text>
    <text x="130" y="995" fill="#EFA524">on TandPay.</text>
  </g>
  <g fill="#DCEFEA" font-size="35" font-weight="450" letter-spacing="-.7">
    <text x="137" y="1125">Storefronts. Mobile Money checkout.</text>
    <text x="137" y="1180">Orders. Reputation.</text>
  </g>
  <path d="M137 1320 H830" stroke="#EFA524" stroke-width="3"/>
  <text x="137" y="1420" fill="#FBFBFB" font-size="51" font-weight="650" letter-spacing="-1.5">Ask us for a demo.</text>
  <g transform="translate(795 1384)" fill="none" stroke="#EFA524" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
    <path d="M0 18H47M29 0l18 18-18 18"/>
  </g>
  <path d="M137 1730H1863" stroke="#DCEFEA" stroke-opacity=".25" stroke-width="1.5"/>
  <text x="137" y="1805" fill="#DCEFEA" font-size="29" font-weight="450">Built for social commerce in Rwanda.</text>
  <circle cx="1623" cy="1794" r="6" fill="#EFA524"/>
  <text x="1863" y="1804" fill="#DCEFEA" font-size="23" font-weight="650" text-anchor="end" letter-spacing="3">EARLY ACCESS</text>
</svg>'''
    (ROOT / "tandpay-booth-2000mm.svg").write_text(svg)
    html = '''<!doctype html><html><head><meta charset="utf-8"><title>TandPay booth artwork</title>
<style>*{box-sizing:border-box}html,body{margin:0;padding:0;background:#093f3e}.art{width:2000px;height:2000px}.art svg{width:100%;height:100%;display:block}@page{size:2000mm 2000mm;margin:0}@media print{html,body,.art{width:2000mm;height:2000mm;margin:0;padding:0}*{-webkit-print-color-adjust:exact;print-color-adjust:exact}}</style>
</head><body><main class="art">''' + svg + "</main></body></html>"
    (ROOT / "artwork.html").write_text(html)
    start = svg.index('  <path d="M1210')
    end = svg.index('  <g fill="#FBFBFB"', start)
    vector_panel = f'''  <path d="M1210 1470 V800 A330 330 0 0 1 1870 800 V1470 Z" fill="#F7F6F0"/>
  <text x="1540" y="645" text-anchor="middle" fill="#093F3E" font-size="23" font-weight="650" letter-spacing="3.5">SOCIAL COMMERCE</text>
  <g transform="translate(1185 695) scale(2.8)"><path fill="#093F3E" fill-rule="evenodd" d="{logo_path}"/></g>
  <path d="M1330 1420H1750" stroke="#EFA524" stroke-width="4"/>
'''
    vector_svg = svg[:start] + vector_panel + svg[end:]
    (ROOT / "tandpay-booth-vector-2000mm.svg").write_text(vector_svg)
    (ROOT / "artwork-vector.html").write_text(html.replace(svg, vector_svg))
    print("Built illustrated and vector editions: 2000 × 2000 mm.")


if __name__ == "__main__":
    build()

import re, json, html, sys

B = "/mnt/DATA/DATA/Study_claude/mini_projects/Elevare_clone/elevaremarket.com_20260921_201649"
H = open(f"{B}/pages/en-qa/rendered.html", encoding="utf-8").read()

def clean(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s))).strip()

def best_src(tag):
    a = dict(re.findall(r'(\w[\w-]*)\s*=\s*"([^"]*)"', tag))
    url = ""
    if a.get("srcset"):
        url = [c.strip().split(" ")[0] for c in a["srcset"].split(",") if c.strip()][-1]
    url = html.unescape(url or a.get("src") or "")
    if url.startswith("//"):
        url = "https:" + url
    return url, html.unescape(a.get("alt", ""))

def wide(url, w=1200):
    if not url:
        return url
    return re.sub(r"([?&])width=\d+", r"\g<1>width=%d" % w, url)

# ---------- section map: offset -> heading ----------
secs = []
for m in re.finditer(r'<section id="(shopify-section-[^"]+)"', H):
    seg = H[m.start():m.start() + 60000]
    h2 = re.search(r"<h2[^>]*>(.*?)</h2>", seg, re.S)
    secs.append((m.start(), clean(h2.group(1)) if h2 else ""))
secs.sort()

def section_of(pos):
    cur = ""
    for start, name in secs:
        if pos >= start:
            cur = name
    return cur

# ---------- product cards ----------
positions = [m.start() for m in re.finditer(r'class="card-wrapper', H)] + [len(H)]
products, seen = [], set()
for k in range(len(positions) - 1):
    pos, ch = positions[k], H[positions[k]:positions[k + 1]]
    m = re.search(r'href="(/en-qa/products/([^"?#]+))"', ch)
    tm = re.search(r'class="full-unstyled-link"[^>]*>(.*?)</a>', ch, re.S)
    if not m or not tm or m.group(2) in seen:
        continue
    title = clean(tm.group(1))
    if not title:
        continue
    vm = re.search(r'visually-hidden">Vendor:</span>\s*<div[^>]*>(.*?)</div>', ch, re.S)
    pm = re.search(r'price-item price-item--regular"?[^>]*>\s*([A-Z]{3})\s*([\d,.]+)', ch)
    imgs = []
    for tag in re.findall(r"<img\b[^>]*>", ch):
        u, alt = best_src(tag)
        if "/cdn/shop/" not in u or u.split("?")[0] in [i["url"].split("?")[0] for i in imgs]:
            continue
        imgs.append({"url": wide(u, 800), "alt": alt})
    if not imgs:
        continue
    seen.add(m.group(2))
    products.append({
        "slug": m.group(2), "name": title,
        "brand": clean(vm.group(1)) if vm else "",
        "currency": pm.group(1) if pm else "QAR",
        "price": float(pm.group(2).replace(",", "")) if pm else 0.0,
        "section": section_of(pos), "images": imgs[:2],
        # every card carries a hidden "Out of stock" span, so the text is not a
        # signal — a genuinely sold-out item has its quick-add submit disabled
        "sold_out": bool(re.search(r"<button[^>]*quick-add__submit[^>]*disabled", ch)),
    })

# ---------- journal ----------
articles, aseen = [], set()
for ch in H.split("article-card-wrapper")[1:]:
    m = re.search(r'href="(/en-qa/blogs/news/([^"?#]+))"', ch)
    t = re.search(r'class="card__heading[^"]*">\s*<a[^>]*>(.*?)</a>', ch, re.S)
    im = re.findall(r"<img\b[^>]*>", ch)
    if not (m and t and im) or m.group(2) in aseen:
        continue
    ex = re.search(r'article-card__excerpt[^"]*">(.*?)</p>', ch, re.S)
    u, alt = best_src(im[0])
    aseen.add(m.group(2))
    articles.append({"slug": m.group(2), "title": clean(t.group(1)),
                     "excerpt": clean(ex.group(1)) if ex else "",
                     "image": {"url": wide(u, 900), "alt": alt}})

# ---------- "The Standard" pillar cards ----------
pillars = []
for m in re.finditer(r'__card-title"[^>]*>(.*?)</p>\s*<p[^>]*__card-text"[^>]*>(.*?)</p>', H, re.S):
    t, d = clean(m.group(1)), clean(m.group(2))
    if t and not any(p["title"] == t for p in pillars):
        pillars.append({"title": t, "text": d})

# ---------- hero slides ----------
slides = []
for m in re.finditer(r'class="banner__heading[^"]*"[^>]*>(.*?)</h2>', H, re.S):
    seg = H[m.start():m.start() + 4000]
    txt = re.search(r'class="banner__text[^"]*"[^>]*>(.*?)</p>', seg, re.S)
    cta = re.search(r'class="[^"]*button[^"]*"[^>]*>\s*(?:<span[^>]*>)?\s*([A-Za-z][^<]{2,40})', seg)
    slides.append({"heading": clean(m.group(1)),
                   "text": clean(txt.group(1)) if txt else "",
                   "cta": clean(cta.group(1)) if cta else "Shop the collection"})

# ---------- lifestyle multicolumn ----------
life = []
for m in re.finditer(r'multicolumn-card__info[^>]*>(.*?)</div>', H, re.S):
    seg = m.group(1)
    h = re.search(r"<h3[^>]*>(.*?)</h3>", seg, re.S)
    p = re.search(r"<p[^>]*>(.*?)</p>", seg, re.S)
    if h:
        life.append({"title": clean(h.group(1)), "text": clean(p.group(1)) if p else ""})

# ---------- editorial images ----------
EDITORIAL = {"hero-1": "banner1.webp", "hero-2": "homepagebanner-gut.webp",
             "lifestyle-school": "FuelFS.webp", "lifestyle-family": "pure_family_1.webp",
             "lifestyle-cycle": "cycle-harmony.webp",
             "about-bg": "minimal_botanical_panoramic_flat_lay_1.webp",
             "happy-house": "width_1920.jpg"}
editorial = {}
for key, base in EDITORIAL.items():
    m = re.search(r'["\s](//elevaremarket\.com/cdn/shop/[^"\s,]*%s[^"\s,]*)' % re.escape(base), H)
    editorial[key] = wide(html.unescape("https:" + m.group(1)), 1800) if m else None

# ---------- brand logos (already on disk in the bundle) ----------
brands = []
for m in re.finditer(r'<img\b[^>]*class="[^"]*megamenu-logo-image[^"]*"[^>]*>', H):
    u, alt = best_src(m.group(0))
    if u and u not in [b["url"] for b in brands]:
        brands.append({"url": wide(u, 400), "alt": alt})

out = {"products": products, "articles": articles, "pillars": pillars,
       "slides": slides, "lifestyle": life, "editorial": editorial, "brands": brands}
json.dump(out, open(sys.argv[1], "w"), indent=1)

import collections
print("cards:", len(products), collections.Counter(p["section"] for p in products))
print("articles:", len(articles), "| pillars:", len(pillars), "| slides:", len(slides),
      "| lifestyle:", len(life), "| brands:", len(brands))
print("pillars:", [p["title"] for p in pillars])
print("slides:", [(s["heading"], s["cta"]) for s in slides])
print("lifestyle:", [l["title"] for l in life])
print("editorial missing:", [k for k, v in editorial.items() if not v])

#!/usr/bin/env python3
"""Static site generator for the ALFATAH storefront.

Reads data/catalog.json (harvested from the Elevare capture) and writes every
HTML page in the project. Editing a template here regenerates all 60+ pages, so
nothing in the output is hand-maintained.

    python3 build.py
"""

import html
import json
import os
import re
import shutil

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = json.load(open(os.path.join(ROOT, "data", "catalog.json"), encoding="utf-8"))

BRAND = "ALFATAH"
TAGLINE = "Provenance and purity, no compromise."
CURRENCY = "QAR"
YEAR = 2026

PRODUCTS = DATA["products"]
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

# The capture's section names, rebranded.
SECTION_LABEL = {
    "New Arrivals": "New Arrivals",
    "Elevare Exclusives": "Alfatah Exclusives",
    "Featured Products": "Featured Products",
}

NAV = [
    ("Groceries", "shop.html", [
        ("Pantry", ["Beans & Grains", "Coffee & Tea", "Condiments", "Nut Butter"]),
        ("Snacks", ["Chips & Salty Snacks", "Chocolate", "Nuts & Trail Mix", "Biscuits & Crackers"]),
        ("Bakery", ["Breads", "Bagels & Muffins"]),
        ("Dairy & Eggs", ["Cheese", "Butter & Ghee", "Dairy Alternatives"]),
        ("Beverages", ["Water", "Juice & Shots", "Functional Beverages"]),
        ("Produce", ["Organic Vegetables", "Organic Fruits", "Prepped Fruit & Veg"]),
    ]),
    ("Health & Beauty", "shop.html?category=Health+%26+Beauty", [
        ("Personal Care & Beauty", ["Beauty", "Bath & Body", "Personal Care"]),
        ("Health Care", ["Protein", "Vitamins & Supplements"]),
    ]),
    ("Home & Garden", "shop.html?category=Home+%26+Garden", [
        ("Household Supplies", ["Laundry", "Cleaning", "Bathroom", "Kitchen"]),
        ("Baby & Toddler", ["Baby & Toddler Food", "Baby Supplies"]),
    ]),
    ("Shop by Lifestyle", "shop.html", [
        ("Diets", ["Gluten Free", "Keto", "Low Sugar", "Dairy Free", "Vegan"]),
    ]),
    ("Journal", "journal.html", []),
    ("Our Story", "about.html", []),
]

FOOTER = [
    ("Discover", [("Alfatah Exclusives", "shop.html"), ("Featured Products", "shop.html"),
                  ("New Arrivals", "shop.html"), ("Our Brands", "about.html#brands")]),
    ("Customer Support", [("Delivery & Returns", "about.html#delivery"), ("Contact Us", "about.html#contact"),
                          ("FAQs", "about.html#faq")]),
    ("Explore", [("Our Story", "about.html"), ("Journal", "journal.html"),
                 ("Terms & Conditions", "about.html#terms"), ("Privacy Policy", "about.html#privacy")]),
]

ICONS = {
    "leaf": '<path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.48 19 2c1 2 2 4.18 2 8 0 5.5-4.78 10-10 10Z"/><path d="M2 21c0-3 1.85-5.36 5.08-6C9.5 14.52 12 13 13 12"/>',
    "truck": '<path d="M10 17h4V5H2v12h3"/><path d="M20 17h2v-3.34a4 4 0 0 0-1.17-2.83L19 9h-5v8h2"/><circle cx="7.5" cy="17.5" r="2.5"/><circle cx="17.5" cy="17.5" r="2.5"/>',
    "hand": '<path d="M11 14h2a2 2 0 1 0 0-4h-3c-.6 0-1.1.2-1.4.6L3 16"/><path d="m7 20 1.6-1.4c.3-.4.8-.6 1.4-.6h4c1.1 0 2.1-.4 2.8-1.2l4.6-4.4a2 2 0 0 0-2.75-2.91l-4.2 3.9"/><path d="m2 15 6 6"/>',
    "sparkle": '<path d="M11.017 2.814a1 1 0 0 1 1.966 0l1.051 5.558a2 2 0 0 0 1.594 1.594l5.558 1.051a1 1 0 0 1 0 1.966l-5.558 1.051a2 2 0 0 0-1.594 1.594l-1.051 5.558a1 1 0 0 1-1.966 0l-1.051-5.558a2 2 0 0 0-1.594-1.594l-5.558-1.051a1 1 0 0 1 0-1.966l5.558-1.051a2 2 0 0 0 1.594-1.594z"/><path d="M20 2v4"/><path d="M22 4h-4"/><circle cx="4" cy="20" r="2"/>',
    "search": '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    "user": '<path d="M19 21v-2a4 4 0 0 0-4-4H9a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/>',
    "bag": '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4Z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    "menu": '<path d="M4 6h16"/><path d="M4 12h16"/><path d="M4 18h16"/>',
    "close": '<path d="M18 6 6 18"/><path d="m6 6 12 12"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
}
PILLAR_ICONS = ["leaf", "truck", "hand", "sparkle"]


def rebrand(text):
    """The captured copy names the original store — swap it for ours."""
    text = re.sub(r"\bThe Elevare Market\b", f"{BRAND} Market", text or "")
    text = re.sub(r"\bElevare Market\b", f"{BRAND} Market", text)
    text = re.sub(r"\bElevare\b", BRAND.title(), text)
    return text


def e(s):
    return html.escape(rebrand(str(s or "")), quote=True)


def icon(name, size=20, cls=""):
    return (f'<svg class="{cls}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
            f'stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" '
            f'aria-hidden="true">{ICONS[name]}</svg>')


def money(v):
    return f"{CURRENCY} {v:,.2f}"


def rel(path, depth):
    """Rewrite a root-relative asset path for a page nested `depth` levels down."""
    return ("../" * depth) + path


# --------------------------------------------------------------------------
# chrome
# --------------------------------------------------------------------------

def head(title, description, depth=0, extra=""):
    p = lambda x: rel(x, depth)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(description)}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="{p('css/tokens.css')}">
<link rel="stylesheet" href="{p('css/main.css')}">
{extra}</head>
<body data-base="{'../' * depth}">
<a class="skip-link" href="#main">Skip to content</a>"""


def header(depth=0, current=""):
    p = lambda x: rel(x, depth)
    items = []
    for label, href, groups in NAV:
        mega = ""
        if groups:
            cols = "".join(
                f'<div><p class="megamenu__title">{e(g)}</p><ul class="megamenu__list">'
                + "".join(f'<li><a href="{p("shop.html")}">{e(c)}</a></li>' for c in children)
                + "</ul></div>"
                for g, children in groups
            )
            mega = f'<div class="megamenu"><div class="wrap"><div class="megamenu__grid">{cols}</div></div></div>'
        aria = ' aria-current="page"' if label == current else ""
        items.append(f'<li class="nav__item"><a class="nav__link" href="{p(href)}"{aria}>{e(label)}</a>{mega}</li>')

    return f"""<div class="announce">Free delivery across Qatar on orders over {money(250)}</div>
<header class="header">
  <div class="wrap header__bar">
    <div class="header__actions">
      <button class="icon-btn" type="button" data-drawer-open="menu" aria-label="Open menu">{icon('menu')}</button>
      <button class="icon-btn" type="button" data-drawer-open="search" aria-label="Search">{icon('search')}</button>
    </div>
    <a class="header__logo" href="{p('index.html')}">Al<span>fatah</span></a>
    <div class="header__actions">
      <a class="icon-btn" href="{p('about.html#contact')}" aria-label="Account">{icon('user')}</a>
      <button class="icon-btn" type="button" data-drawer-open="cart" aria-label="Open cart">
        {icon('bag')}<span class="cart-count" data-cart-count hidden>0</span>
      </button>
    </div>
  </div>
  <nav class="nav" aria-label="Primary"><div class="wrap"><ul class="nav__list">{''.join(items)}</ul></div></nav>
</header>"""


def drawers(depth=0):
    p = lambda x: rel(x, depth)
    menu_links = "".join(
        f'<li><a class="nav__link" href="{p(href)}">{e(label)}</a></li>' for label, href, _ in NAV
    )
    return f"""<div class="scrim" data-scrim></div>

<aside class="drawer drawer--left" data-drawer="menu" aria-hidden="true" aria-label="Menu">
  <div class="drawer__head">
    <p class="drawer__title">Menu</p>
    <button class="icon-btn" type="button" data-drawer-close aria-label="Close menu">{icon('close')}</button>
  </div>
  <div class="drawer__body"><ul class="footer__list">{menu_links}</ul></div>
</aside>

<aside class="drawer drawer--left" data-drawer="search" aria-hidden="true" aria-label="Search">
  <div class="drawer__head">
    <p class="drawer__title">Search</p>
    <button class="icon-btn" type="button" data-drawer-close aria-label="Close search">{icon('close')}</button>
  </div>
  <div class="drawer__body">
    <form class="newsletter__form" action="{p('shop.html')}" method="get">
      <input class="field" type="search" name="q" placeholder="What are you looking for?" aria-label="Search products">
      <button class="btn btn--solid" type="submit">Go</button>
    </form>
    <p class="sec-head__sub" style="margin-top:var(--s-3)">Popular: tahini, bamboo tissue, chocolate, olive oil</p>
  </div>
</aside>

<aside class="drawer" data-drawer="cart" aria-hidden="true" aria-label="Your cart">
  <div class="drawer__head">
    <p class="drawer__title">Your Cart</p>
    <button class="icon-btn" type="button" data-drawer-close aria-label="Close cart">{icon('close')}</button>
  </div>
  <div class="drawer__body" data-cart-body></div>
  <div class="drawer__foot" data-cart-foot hidden>
    <div class="totals" data-cart-totals></div>
    <a class="btn btn--solid btn--block" href="{p('cart.html')}">View cart</a>
  </div>
</aside>

<div class="toast" data-toast role="status" aria-live="polite"></div>"""


def newsletter(watermark=""):
    mark = (f'<img class="newsletter__mark" src="{watermark}" alt="" loading="lazy" aria-hidden="true">'
            if watermark else "")
    return f"""<section class="section newsletter">{mark}
  <div class="wrap newsletter__inner">
    <p class="sec-head__eyebrow" style="color:rgba(255,255,255,.75)">Join the house</p>
    <h2>The Foundation of your Wellness starts here</h2>
    <p>Join our community and be the first to receive our latest updates and news.</p>
    <form class="newsletter__form" data-newsletter>
      <input class="field" type="email" name="email" required placeholder="Email address" aria-label="Email address">
      <button class="btn btn--light" type="submit">Subscribe</button>
    </form>
  </div>
</section>"""


def footer(depth=0):
    p = lambda x: rel(x, depth)
    cols = "".join(
        f'<div><p class="footer__title">{e(title)}</p><ul class="footer__list">'
        + "".join(f'<li><a href="{p(href)}">{e(label)}</a></li>' for label, href in links)
        + "</ul></div>"
        for title, links in FOOTER
    )
    return f"""<footer class="footer">
  <div class="wrap section--tight">
    <div class="footer__grid">
      <div>
        <p class="header__logo" style="font-size:1.4rem">Al<span>fatah</span></p>
        <p class="sec-head__sub">{e(TAGLINE)} Curated health, beauty and everyday essentials delivered across Qatar.</p>
      </div>
      {cols}
    </div>
    <div class="footer__bottom">
      <span>&copy; {YEAR} {BRAND} Market</span>
      <span>Doha, Qatar &middot; Prices in {CURRENCY}</span>
    </div>
  </div>
</footer>"""


def scripts(depth=0):
    p = lambda x: rel(x, depth)
    return f"""<script src="{p('js/cart.js')}" defer></script>
<script src="{p('js/ui.js')}" defer></script>
</body>
</html>"""


# --------------------------------------------------------------------------
# components
# --------------------------------------------------------------------------

def product_card(prod, depth=0):
    p = lambda x: rel(x, depth)
    imgs = prod["images"][:2]
    media = "".join(
        f'<img src="{p(i["file"])}" alt="{e(i["alt"] or prod["name"])}" loading="lazy" width="800" height="800">'
        for i in imgs
    )
    badge = ""
    if not prod["in_stock"]:
        badge = '<span class="card__badge card__badge--out">Out of stock</span>'
    elif "New Arrivals" in prod["sections"]:
        badge = '<span class="card__badge">New</span>'
    href = p(f"products/{prod['slug']}.html")
    buy = (f'<button class="btn btn--outline btn--block" type="button" data-add="{e(prod["slug"])}">Add to cart</button>'
           if prod["in_stock"] else
           '<button class="btn btn--outline btn--block" type="button" disabled>Out of stock</button>')
    return f"""<article class="card" data-product="{e(prod['slug'])}">
  <a class="card__media" href="{href}">{badge}{media}</a>
  <p class="card__brand">{e(prod['brand'])}</p>
  <h3 class="card__name"><a href="{href}">{e(prod['name'])}</a></h3>
  <div class="card__foot">
    <p class="card__price">{money(prod['price'])}</p>
    {buy}
  </div>
</article>"""


def section_rail(title, sub, prods, depth=0, cta=("Shop the collection", "shop.html")):
    p = lambda x: rel(x, depth)
    cards = "".join(product_card(x, depth) for x in prods)
    return f"""<section class="section">
  <div class="wrap">
    <div class="sec-head">
      <div>
        <p class="sec-head__eyebrow">{e(sub)}</p>
        <h2>{e(title)}</h2>
      </div>
      <a class="link-underline" href="{p(cta[1])}">{e(cta[0])}</a>
    </div>
    <div class="rail">{cards}</div>
  </div>
</section>"""


# --------------------------------------------------------------------------
# pages
# --------------------------------------------------------------------------

def page_home():
    ed = DATA["editorial"]
    slides = DATA["slides"][:2]
    hero_imgs = [ed.get("hero-1"), ed.get("hero-2")]
    slide_html = ""
    for n, s in enumerate(slides):
        img = hero_imgs[n] or hero_imgs[0]
        # only the first slide carries the page's h1; the rest are h2 so the
        # document keeps a single top-level heading
        tag = "h1" if n == 0 else "h2"
        slide_html += f"""<div class="hero__slide" data-slide data-active="{str(n == 0).lower()}">
  <img class="hero__img" src="{img}" alt="" {'fetchpriority="high"' if n == 0 else 'loading="lazy"'} width="1800" height="1000">
  <div class="wrap hero__box">
    <{tag} class="hero__title">{e(s['heading'])}</{tag}>
    <p class="hero__text">{e(s['text'])}</p>
    <a class="btn btn--light" href="shop.html">{e(s['cta'])}</a>
  </div>
</div>"""
    dots = "".join(
        f'<button class="hero__dot" type="button" data-dot="{n}" role="tab" '
        f'aria-selected="{str(n == 0).lower()}" aria-label="Slide {n + 1}"></button>'
        for n in range(len(slides))
    )

    pillars = "".join(
        f'<div class="pillar">{icon(PILLAR_ICONS[n % len(PILLAR_ICONS)], 22)}'
        f'<div><p class="pillar__title">{e(p["title"])}</p>'
        f'<p class="pillar__text">{e(p["text"])}</p></div></div>'
        for n, p in enumerate(DATA["pillars"])
    )

    rails = ""
    for raw, label in SECTION_LABEL.items():
        prods = [p for p in PRODUCTS if raw in p["sections"]]
        if not prods:
            continue
        sub = {"New Arrivals": "Just landed", "Alfatah Exclusives": "Only here",
               "Featured Products": "Handpicked"}[label]
        rails += section_rail(label, sub, prods[:12], 0)

    lifestyle = [
        ("Fuel for school", "Healthy snacks to power their day", DATA["editorial"].get("lifestyle-school")),
        ("Pure Family Living", "Uncompromising standard goods curated to support your family's daily rituals",
         DATA["editorial"].get("lifestyle-family")),
        ("Cycle Harmony", "Honouring her body's natural rhythms with natural, soothing care",
         DATA["editorial"].get("lifestyle-cycle")),
    ]
    tiles = "".join(
        f'<a class="tile" href="shop.html"><img src="{img}" alt="{e(t)}" loading="lazy" width="900" height="1200">'
        f'<div class="tile__body"><p class="tile__title">{e(t)}</p><p class="tile__text">{e(d)}</p>'
        f'<span class="link-underline">Shop the collection</span></div></a>'
        for t, d, img in lifestyle if img
    )

    posts = "".join(
        f'<article class="post"><a class="post__media" href="journal.html">'
        f'<img src="{a["image"]["file"]}" alt="{e(a["image"]["alt"] or a["title"])}" loading="lazy" width="900" height="675"></a>'
        f'<h3 class="post__title"><a href="journal.html">{e(a["title"])}</a></h3>'
        f'<p class="post__excerpt">{e(a["excerpt"])}</p>'
        f'<a class="link-underline" href="journal.html">Read more</a></article>'
        for a in DATA["articles"][:3]
    )

    logos = "".join(
        f'<img src="{b["file"]}" alt="{e(b["name"])}" loading="lazy" height="42">' for b in DATA["brands"]
    )

    about_bg = DATA["editorial"].get("hero-2", "")
    happy = DATA["editorial"].get("about-bg", "")
    watermark = DATA["editorial"].get("happy-house", "")

    return "".join([
        head(f"{BRAND} Market | Premium Wellness and Lifestyle Essentials",
             f"{TAGLINE} Shop curated health, beauty and everyday essentials delivered across Qatar."),
        header(0, "Groceries"),
        '<main id="main">',
        f'<section class="hero" data-hero>{slide_html}<div class="hero__dots" role="tablist">{dots}</div></section>',
        f'<section class="pillars section--tight"><div class="wrap"><div class="pillars__grid">{pillars}</div></div></section>',
        rails,
        f"""<section class="section">
  <div class="wrap">
    <div class="sec-head"><div>
      <p class="sec-head__eyebrow">Curated bundles</p>
      <h2>Alfatah favourites</h2>
      <p class="sec-head__sub">Curated bundles, created to support your wellness goals.</p>
    </div></div>
    <div class="tiles">{tiles}</div>
  </div>
</section>""",
        f"""<section class="section">
  <div class="wrap about">
    <div class="about__media"><img src="{about_bg}" alt="" loading="lazy" width="1400" height="900"></div>
    <div class="about__body">
      <p class="sec-head__eyebrow">Our story</p>
      <h2>Born from a relentless pursuit of clean living</h2>
      <p>{e(TAGLINE)} Every product on our shelves is vetted for provenance, ingredients and the
      people behind it &mdash; so a weekly shop becomes an achievable daily wellbeing practice.</p>
      <a class="link-underline" href="about.html">Read our story</a>
    </div>
  </div>
</section>""",
        f"""<section class="section--tight"><div class="wrap">
  <div class="banner"><img src="{happy}" alt="" loading="lazy" width="1800" height="900">
    <div class="banner__body">
      <h2>Happy House</h2>
      <p>Discover the household essentials to help make your home a toxin-free environment.</p>
      <a class="btn btn--light" href="shop.html?category=Home+%26+Garden">Shop now</a>
    </div>
  </div>
</div></section>""",
        f"""<section class="section"><div class="wrap">
  <div class="sec-head"><div>
    <p class="sec-head__eyebrow">Reading</p><h2>Alfatah Journal</h2>
  </div><a class="link-underline" href="journal.html">All articles</a></div>
  <div class="posts">{posts}</div>
</div></section>""",
        f'<section class="marquee"><div class="marquee__track">{logos}{logos}</div></section>',
        "</main>",
        newsletter(watermark), footer(), drawers(), scripts(),
    ])


def page_shop():
    cats = sorted({p["category"] for p in PRODUCTS})
    brands = sorted({p["brand"] for p in PRODUCTS if p["brand"]})
    cat_boxes = "".join(
        f'<label class="chk"><input type="checkbox" data-filter="category" value="{e(c)}">{e(c)}</label>'
        for c in cats
    )
    brand_boxes = "".join(
        f'<label class="chk"><input type="checkbox" data-filter="brand" value="{e(b)}">{e(b.title())}</label>'
        for b in brands
    )
    cards = "".join(
        f'<div data-card data-category="{e(p["category"])}" data-brand="{e(p["brand"])}" '
        f'data-price="{p["price"]}" data-name="{e(p["name"].lower())}">{product_card(p)}</div>'
        for p in PRODUCTS
    )
    return "".join([
        head(f"Shop all | {BRAND} Market", "Browse the full Alfatah range — pantry, snacks, dairy, home and personal care."),
        header(0, "Groceries"),
        f"""<main id="main" class="wrap section">
  <nav class="crumbs"><a href="index.html">Home</a> / Shop all</nav>
  <div class="page-head">
    <h1 style="font-family:var(--f-display);font-size:var(--t-h2)">Shop all</h1>
    <p class="sec-head__sub">{len(PRODUCTS)} products &middot; {e(TAGLINE)}</p>
  </div>
  <div class="shop">
    <aside class="filters" aria-label="Filters">
      <div class="filters__group">
        <p class="footer__title">Category</p>
        {cat_boxes}
      </div>
      <div class="filters__group">
        <p class="footer__title">Brand</p>
        {brand_boxes}
      </div>
      <button class="btn btn--outline" type="button" data-clear-filters>Clear all</button>
    </aside>
    <div>
      <div class="shop__bar">
        <p class="sec-head__sub" data-result-count>{len(PRODUCTS)} products</p>
        <label class="chk">Sort
          <select class="select" data-sort>
            <option value="featured">Featured</option>
            <option value="price-asc">Price, low to high</option>
            <option value="price-desc">Price, high to low</option>
            <option value="name">Alphabetical</option>
          </select>
        </label>
      </div>
      <div class="grid-products" data-shop-grid>{cards}</div>
      <p class="empty" data-no-results hidden>No products match those filters.</p>
    </div>
  </div>
</main>""",
        newsletter(), footer(), drawers(), scripts(),
    ])


def page_product(prod):
    d = 1
    p = lambda x: rel(x, d)
    imgs = prod["images"]
    main = imgs[0]
    thumbs = "".join(
        f'<button class="pdp__thumb" type="button" data-thumb="{p(i["file"])}" '
        f'aria-selected="{str(n == 0).lower()}" aria-label="View image {n + 1}">'
        f'<img src="{p(i["file"])}" alt="" loading="lazy" width="200" height="200"></button>'
        for n, i in enumerate(imgs)
    ) if len(imgs) > 1 else ""

    meta = []
    if prod["brand"]:
        meta.append(e(prod["brand"]))
    if prod["size"]:
        meta.append(e(prod["size"]))
    if prod["sku"]:
        meta.append("SKU " + e(prod["sku"]))

    desc = prod["description"] or (
        f"{prod['name']} from {prod['brand'].title()}, stocked by {BRAND} Market and vetted against "
        "the Alfatah Standard for provenance, ingredients and everyday use.")

    accordions = [("Description", e(desc))]
    if prod["best_by"]:
        accordions.append(("Storage & shelf life",
                           f"Store in a cool, dry place away from direct sunlight. Best before {e(prod['best_by'])}."))
    accordions.append(("The Alfatah Standard", " ".join(
        f"<strong>{e(x['title'])}</strong> &mdash; {e(x['text'])}." for x in DATA["pillars"])))
    accordions.append(("Delivery & returns",
                       f"Delivered across Qatar in 1&ndash;3 working days. Free over {money(250)}. "
                       "Unopened items can be returned within 14 days."))
    acc_html = "".join(
        f'<details class="acc__item"{" open" if n == 0 else ""}><summary>{t}</summary>'
        f'<div class="acc__body">{body}</div></details>'
        for n, (t, body) in enumerate(accordions)
    )

    related = [x for x in PRODUCTS
               if x["slug"] != prod["slug"] and x["category"] == prod["category"]][:6]
    if len(related) < 4:
        related += [x for x in PRODUCTS if x["slug"] != prod["slug"] and x not in related][:6 - len(related)]

    buy = (f"""<div class="pdp__buy">
      <div class="qty">
        <button type="button" data-qty="-1" aria-label="Decrease quantity">&minus;</button>
        <input type="number" value="1" min="1" max="99" data-qty-input aria-label="Quantity">
        <button type="button" data-qty="1" aria-label="Increase quantity">+</button>
      </div>
      <button class="btn btn--accent" type="button" data-add="{e(prod['slug'])}" data-use-qty>Add to cart</button>
    </div>"""
           if prod["in_stock"] else
           '<div class="pdp__buy"><button class="btn btn--accent" type="button" disabled>Out of stock</button></div>')

    ld = json.dumps({
        "@context": "https://schema.org", "@type": "Product", "name": prod["name"],
        "brand": {"@type": "Brand", "name": prod["brand"]}, "sku": prod["sku"],
        "description": desc,
        "offers": {"@type": "Offer", "price": f"{prod['price']:.2f}", "priceCurrency": prod["currency"],
                   "availability": "https://schema.org/" + ("InStock" if prod["in_stock"] else "OutOfStock")},
    })

    return "".join([
        head(f"{prod['name']} | {BRAND} Market", desc[:155], depth=d,
             extra=f'<script type="application/ld+json">{ld}</script>\n'),
        header(d, "Groceries"),
        f"""<main id="main" class="wrap section">
  <nav class="crumbs"><a href="{p('index.html')}">Home</a> / <a href="{p('shop.html')}">Shop</a> / {e(prod['name'])}</nav>
  <div class="pdp">
    <div class="pdp__gallery">
      <div class="pdp__main"><img src="{p(main['file'])}" alt="{e(main['alt'] or prod['name'])}" data-pdp-main width="900" height="900"></div>
      <div class="pdp__thumbs">{thumbs}</div>
    </div>
    <div class="pdp__info">
      <p class="card__brand">{e(prod['brand'])}</p>
      <h1 class="pdp__title">{e(prod['name'])}</h1>
      <p class="pdp__price">{money(prod['price'])}</p>
      <p class="pdp__meta">{' &middot; '.join(meta)}</p>
      {buy}
      <div class="acc">{acc_html}</div>
    </div>
  </div>
</main>""",
        section_rail("You may also like", "More from " + prod["category"], related, d,
                     cta=("Shop all", "shop.html")),
        newsletter(), footer(d), drawers(d), scripts(d),
    ])


def page_cart():
    return "".join([
        head(f"Your cart | {BRAND} Market", "Review your Alfatah Market basket before checkout."),
        header(),
        """<main id="main" class="wrap section">
  <nav class="crumbs"><a href="index.html">Home</a> / Cart</nav>
  <div class="page-head"><h1 style="font-family:var(--f-display);font-size:var(--t-h2)">Your Cart</h1></div>
  <div class="shop">
    <div data-cart-page style="order:1"></div>
    <aside class="filters" style="order:2">
      <div class="totals" data-cart-totals></div>
      <button class="btn btn--accent btn--block" type="button" data-checkout>Checkout</button>
      <a class="link-underline" href="shop.html">Continue shopping</a>
    </aside>
  </div>
</main>""",
        newsletter(), footer(), drawers(), scripts(),
    ])


def page_journal():
    posts = "".join(
        f'<article class="post"><div class="post__media">'
        f'<img src="{a["image"]["file"]}" alt="{e(a["image"]["alt"] or a["title"])}" loading="lazy" width="900" height="675"></div>'
        f'<h2 class="post__title">{e(a["title"])}</h2>'
        f'<p class="post__excerpt">{e(a["excerpt"])}</p></article>'
        for a in DATA["articles"]
    )
    return "".join([
        head(f"Journal | {BRAND} Market", "Guides and reading on clean living, nutrition and everyday wellbeing."),
        header(0, "Journal"),
        f"""<main id="main" class="wrap section">
  <nav class="crumbs"><a href="index.html">Home</a> / Journal</nav>
  <div class="page-head">
    <p class="sec-head__eyebrow">Reading</p>
    <h1 style="font-family:var(--f-display);font-size:var(--t-h2)">Alfatah Journal</h1>
    <p class="sec-head__sub">Notes on provenance, nutrition and building an achievable daily wellbeing practice.</p>
  </div>
  <div class="posts">{posts}</div>
</main>""",
        newsletter(), footer(), drawers(), scripts(),
    ])


def page_about():
    logos = "".join(
        f'<img src="{b["file"]}" alt="{e(b["name"])}" loading="lazy" height="46">' for b in DATA["brands"]
    )
    pillars = "".join(
        f'<div class="pillar">{icon(PILLAR_ICONS[n % 4], 22)}<div>'
        f'<p class="pillar__title">{e(p["title"])}</p><p class="pillar__text">{e(p["text"])}</p></div></div>'
        for n, p in enumerate(DATA["pillars"])
    )
    faqs = [
        ("How To Place An Order", "Add items to your cart and check out. Orders placed before 4pm are picked the same day."),
        ("Payment Methods", "All major cards, Apple Pay and cash on delivery across Qatar."),
        ("Track & Manage My Order", "You will receive a tracking link by email as soon as your order leaves our Doha store."),
        ("Delivery Information", f"1&ndash;3 working days nationwide. Free over {money(250)}, otherwise {money(25)}."),
        ("Returns, Exchanges & Order Problems", "Unopened items can be returned within 14 days of delivery."),
    ]
    faq_html = "".join(
        f'<details class="acc__item"><summary>{e(q)}</summary><div class="acc__body">{a}</div></details>'
        for q, a in faqs
    )
    return "".join([
        head(f"Our story | {BRAND} Market", "Born from a relentless pursuit of clean living — the Alfatah story."),
        header(0, "Our Story"),
        f"""<main id="main">
  <div class="wrap section">
    <nav class="crumbs"><a href="index.html">Home</a> / Our story</nav>
    <div class="page-head">
      <p class="sec-head__eyebrow">Our story</p>
      <h1 style="font-family:var(--f-display);font-size:var(--t-h2)">Born from a relentless pursuit of clean living</h1>
    </div>
    <div class="about">
      <div class="about__media"><img src="{DATA['editorial'].get('hero-2', '')}" alt="" loading="lazy" width="1400" height="900"></div>
      <div class="prose">
        <p>{e(TAGLINE)} {BRAND} Market began with a simple frustration: reading the back of a label
        should not be detective work.</p>
        <p>We stock day-to-day essentials that help you establish an achievable daily wellbeing practice
        &mdash; pantry staples, household supplies and personal care, each vetted for provenance and
        ingredients before it reaches a shelf.</p>
        <p>Everything ships from our Doha store across Qatar.</p>
      </div>
    </div>
  </div>

  <section class="pillars section--tight" id="standard"><div class="wrap">
    <div class="sec-head"><div><p class="sec-head__eyebrow">Our promise</p><h2>The Alfatah Standard</h2></div></div>
    <div class="pillars__grid">{pillars}</div>
  </div></section>

  <section class="section" id="brands"><div class="wrap">
    <div class="sec-head"><div><p class="sec-head__eyebrow">Our partners</p><h2>Brands we carry</h2></div></div>
    <div class="marquee" style="border:0"><div class="marquee__track" style="animation-duration:48s">{logos}{logos}</div></div>
  </div></section>

  <section class="section" id="faq"><div class="wrap" style="max-width:52rem">
    <div class="sec-head"><div><p class="sec-head__eyebrow">Support</p><h2>Frequently asked questions</h2></div></div>
    <div class="acc" id="delivery">{faq_html}</div>
    <div class="prose" id="contact" style="margin-top:var(--s-4)">
      <p class="footer__title">Contact</p>
      <p>hello@alfatahmarket.qa &middot; Doha, Qatar</p>
      <p class="sec-head__sub" id="terms">Terms &amp; Conditions and <span id="privacy">Privacy Policy</span> available on request.</p>
    </div>
  </div></section>
</main>""",
        newsletter(), footer(), drawers(), scripts(),
    ])


# --------------------------------------------------------------------------

def write(path, content):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as fh:
        fh.write(content)
    return len(content)


def main():
    shutil.rmtree(os.path.join(ROOT, "products"), ignore_errors=True)
    total = 0
    total += write("index.html", page_home())
    total += write("shop.html", page_shop())
    total += write("cart.html", page_cart())
    total += write("journal.html", page_journal())
    total += write("about.html", page_about())
    for prod in PRODUCTS:
        total += write(f"products/{prod['slug']}.html", page_product(prod))

    # the catalogue the front-end reads for cart lines
    mini = [{"slug": p["slug"], "name": p["name"], "brand": p["brand"], "price": p["price"],
             "currency": p["currency"], "image": p["images"][0]["file"] if p["images"] else ""}
            for p in PRODUCTS]
    write("data/products.json", json.dumps(mini, indent=1))

    print(f"built {5 + len(PRODUCTS)} pages ({total / 1024:.0f} KB)")


if __name__ == "__main__":
    main()

# ALFATAH storefront — handover

Read this file first. It takes about three minutes and will save you from the
one mistake that wastes a day.

## The one rule

**The HTML is generated. Do not edit it.**

`index.html`, `shop.html` and everything under `products/` are output. Edit
`build.py` and regenerate:

```bash
python3 build.py
```

Any change made directly to a `.html` file disappears the next time anyone
builds. `build.py` holds every template — header, nav, megamenu, product card,
product page, cart, footer, newsletter. It is the source of truth.

## What this is

A static storefront rebuilt from a capture of a live Shopify store
(elevaremarket.com). The design system — palette, type scale, spacing, section
rhythm — was extracted from that capture; the identity was changed to ALFATAH.
None of the original Shopify markup, theme JavaScript or tracking survives.

There is **no backend**. Checkout is a toast message. The cart is localStorage.

## Run the preview

```bash
python3 -m http.server 8777     # then open http://localhost:8777
```

The complete site is included — all 67 pages, every asset. Start here:

| Page | Shows |
|---|---|
| `index.html` | Hero slideshow, pillars, three product rails, lifestyle tiles, story block, banner, journal, brand marquee, newsletter, footer |
| `shop.html` | Catalogue grid, category + brand filters, sort, deep links (`?category=…`, `?q=…`) |
| `products/cosmic-dealer-box-of-7.html` | Product page: gallery, quantity, add to cart, accordions, related rail |
| `cart.html`, `journal.html`, `about.html` | Cart, article index, story + FAQ |

All 62 product pages are the same template with different data — reading one is
enough. They are all present so the preview has no dead links.

## What is in this folder

```
HANDOVER.md              this file
README.md                pipeline, data shape, known gaps
build.py                 ALL templates — this is what you edit
css/tokens.css           design tokens: colour, type, spacing, radii
css/main.css             layout and components
js/ui.js                 slideshow, drawers, PDP gallery, shop filters
js/cart.js               localStorage cart — REFERENCE ONLY, see below
data/catalog.json        62 products + articles, pillars, slides, brands
data/products.json       slim catalogue the cart reads at runtime
assets/                  fonts, editorial, journal, brands, product photography
products/                62 generated product pages
tools/                   harvest pipeline — only needed to re-extract from a capture
reference/CLONE_BRIEF.md where every design token came from, component vocabulary
```

## If you are porting this to a Shopify theme

The design layer ports almost untouched. The data layer does not.

| Piece | What happens |
|---|---|
| `css/tokens.css`, `css/main.css` | Drop into `assets/` as-is. Nothing in the CSS references content, so it carries over whole. |
| `js/ui.js` — slideshow, drawers, gallery | Ports as-is |
| `js/ui.js` — shop filters | Replace with Shopify Search & Discovery filtering; client-side filtering does not scale past one page of products |
| `build.py` functions | Each becomes a Liquid section or snippet. `product_card()` → `snippets/product-card.liquid`, `section_rail()` → `sections/featured-products.liquid` with a schema block. Structure survives, syntax changes. |
| `data/catalog.json` | Delete. Liquid provides `product`, `collection`, `cart`. |
| `js/cart.js` | **Rewrite.** Shopify owns cart state server-side — use `/cart/add.js` and `/cart.js`. |

The real gap in the cart port is not the fetch call, it is that add-to-cart needs
a **variant ID**. This build has no concept of variants (size, colour, pack
count) because the capture did not expose them. Model variants before wiring the
cart.

`deliveryFor()` in `js/cart.js` also disappears on Shopify — shipping rates come
from store settings, not the front end. In this static build it is a placeholder
(`free ≥ QAR 250, else QAR 25`) and the same numbers are hardcoded in
`build.py`'s `header()` and the About FAQ. Keep them in sync or delete all three.

## Known gaps

- **Categories are guessed.** The real taxonomy only ever existed in the
  megamenu, never on the products. `tools/merge.py` infers
  them from keywords. Expect misfiled items.
- **Two data depths.** 22 products have full detail (description, size, SKU,
  best-before, multi-image gallery); the other 40 came from home page cards and
  have name, brand, price and one or two images only. Their product pages fall
  back to a generated description.
- **Missing routes.** Collection pages, blog post pages and the real cart route
  were outside the original 25-page crawl. The journal lists articles with no
  article pages behind them.
- **No accessibility audit** has been run beyond keyboard focus states, skip
  link, ARIA on drawers and carousels, and single-`h1`-per-page.

## Content ownership

The copy, photography and product data are Elevare's and their suppliers'. They
are placeholders for layout purposes only. Replace all of it before anything
goes live commercially.

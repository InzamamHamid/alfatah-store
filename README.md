# ALFATAH Store

A clean-room rebuild of the Elevare Market storefront, rebranded as ALFATAH. The
design system (palette, type scale, shape, section rhythm) and the product data
come from the capture in `../elevaremarket.com_20260921_201649/`; none of the
original Shopify markup, theme JavaScript or tracking survives.

## Run it

```bash
python3 -m http.server 8777     # then open http://localhost:8777
```

Static files only — no build step at runtime, no backend, no dependencies.

## Regenerate the HTML

Every page is generated. Never hand-edit `index.html`, `shop.html` or anything
in `products/` — edit `build.py` and rebuild:

```bash
python3 build.py        # writes 5 top-level pages + 62 product pages
```

## Re-harvest from the capture

`data/catalog.json` is produced by the scripts in `tools/`, run in this order.
They read the capture bundle and write into this project:

| Step | Script | Does |
|---|---|---|
| 1 | `tools/extract.py <out.json>` | Product detail (JSON-LD + gallery) from the 22 captured product pages |
| 2 | `tools/home_extract.py <out.json>` | Home page: 41 product cards, 6 articles, pillars, hero slides, editorial imagery |
| 3 | `tools/stage.py` | Downloads product/editorial/journal imagery, copies brand logos and fonts out of the bundle |
| 4 | `tools/merge.py` | Merges both sources into `data/catalog.json`, assigns categories |
| 5 | `python3 build.py` | Renders every page |
| 6 | `tools/check.py` | Smoke test: every local href/src resolves, chrome present, no template leaks |

The capture never downloaded the product photography (its 400-asset cap filled
with theme JS and brand logos first), so step 3 fetches those images from the
origin CDN using the URLs recorded in the captured markup.

## Layout

```
build.py            generator — all templates live here
data/catalog.json   62 products, articles, pillars, slides, brand logos
data/products.json  slim catalogue the cart reads at runtime
css/tokens.css      design tokens from the capture (colour, type, shape)
css/main.css        layout and components
js/cart.js          localStorage cart, drawer + cart page rendering
js/ui.js            slideshow, drawers, PDP gallery, shop filters and sort
assets/             products, editorial, journal, brands, fonts
products/*.html     generated, one per product
tools/              harvest pipeline (see above)
```

## Data shape

62 products in two depths, merged by slug:

- **22 "detailed"** — from the capture's own product pages: description, size,
  SKU, best-before, multi-image gallery.
- **40 card-only** — from home page cards: name, brand, price, one or two images.
  Their product pages fall back to a generated description.

Prices are the captured QAR values, unchanged.

## Known gaps

- Category assignment is keyword-inferred in `tools/merge.py`, not captured —
  the original taxonomy was only ever in the megamenu, never on the products.
- Collection, blog-post and cart routes were outside the 25-page crawl, so the
  journal lists articles without article pages behind them.
- Checkout is a toast. There is no backend.
- The delivery-charge rule in `js/cart.js` (`deliveryFor`) is a placeholder.

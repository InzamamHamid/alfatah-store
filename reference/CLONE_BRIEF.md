# Clone Brief — https://elevaremarket.com/en-qa

Captured 2026-09-21T20:47:11 · 25 pages · 400 assets · 229 data payloads

Everything below is extracted from a live capture. Paths are relative to the bundle root. Read this file first, open a specific `pages/<slug>/` folder only when you need the raw markup.

## Rebuild plan

**Approach:** `static-mirror` — Most pages are server rendered. Serve the captured rendered.html per route and rewrite asset URLs to the local assets/ folder.

**Suggested stack:** Shopify — Liquid theme, product data in the recorded payloads

**Original framework:** `shopify`

**Rendering:** 25 ssr

**Read before starting:**

- Forms captured as structure only, no backend endpoint is cloned

## Design system

### Colors

| Role | Hex | Value |
|---|---|---|
| primary | #000000 | `#000000` |
| accent | #b7786b | `#b7786b` |
| accent_2 | #6b714b | `#6b714b` |
| text | #726a63 | `#726a63` |
| text_2 | #ffffff | `#ffffff` |
| text_3 | #000000 | `#000000` |
| bg | #f8f6f0 | `#f8f6f0` |
| bg_2 | #726a63 | `#726a63` |
| bg_3 | #b7786b | `#b7786b` |
| bg_4 | #000000 | `#000000` |
| border | #e5e7eb | `#e5e7eb` |
| border_2 | #726a63 | `#726a63` |

### Fonts

Families in use: `DMSerifDisplay`, `LibreFranklin`, `ui-sans-serif`

### Heading styles

| Tag | Size | Weight | Family | Line height | Color |
|---|---|---|---|---|---|
| h1 | 60px | 400 | DMSerifDisplay | 0px | #726a63 |

**Body text:** 14px / 21px · `LibreFranklin` · weight 400 · #ffffff

### Type scale

| Size | Weight | Family | Occurrences |
|---|---|---|---|
| 60px | 400 | DMSerifDisplay | 1 |
| 18px | 700 | LibreFranklin | 8 |
| 16px | 400 | LibreFranklin | 434 |
| 14.4px | 600 | LibreFranklin | 2 |
| 14px | 400 | LibreFranklin | 43 |
| 12px | 300 | LibreFranklin | 1 |
| 11.2px | 600 | LibreFranklin | 10 |
| 10px | 400 | ui-sans-serif | 1 |

### Spacing and shape

- Padding steps: 8px, 24px, 16px, 14px, 20px, 40px
- Margin steps: -1px, 16px, 12px, 20px, 15px
- Grid gaps: 8px, normal 8px, 16px, normal 80px
- Border radii: 12px, 40px, 999px, 34px, 41px
- Border widths: 1px

### Ready-to-use CSS variables

```css
:root {
  --color-primary: #000000;
  --color-accent: #b7786b;
  --color-accent-2: #6b714b;
  --color-text: #726a63;
  --color-text-2: #ffffff;
  --color-text-3: #000000;
  --color-bg: #f8f6f0;
  --color-bg-2: #726a63;
  --color-bg-3: #b7786b;
  --color-bg-4: #000000;
  --color-border: #e5e7eb;
  --color-border-2: #726a63;
  --text-1: 60px;
  --text-2: 18px;
  --text-3: 16px;
  --text-4: 14.4px;
  --text-5: 14px;
  --text-6: 12px;
  --text-7: 11.2px;
  --text-8: 10px;
  --radius-1: 12px;
  --radius-2: 40px;
  --radius-3: 999px;
  --radius-4: 34px;
  --radius-5: 41px;
}
```

### Element defaults

| Tag | Count | Size | Weight | Color | Family |
|---|---|---|---|---|---|
| `a` | 112 | 16px | 400 | #726a63 | LibreFranklin |
| `body` | 1 | 16px | 400 | #726a63 | LibreFranklin |
| `button` | 4 | 14px | 700 | #726a63 | LibreFranklin |
| `details` | 2 | 16px | 400 | #726a63 | LibreFranklin |
| `div` | 54 | 16px | 400 | #726a63 | LibreFranklin |
| `h1` | 1 | 60px | 400 | #726a63 | DMSerifDisplay |
| `header` | 1 | 16px | 400 | #726a63 | LibreFranklin |
| `header-menu` | 2 | 16px | 400 | #726a63 | LibreFranklin |
| `html` | 1 | 10px | 400 | #000000 | ui-sans-serif |
| `img` | 73 | 16px | 400 | #726a63 | LibreFranklin |
| `label` | 3 | 11.2px | 600 | #726a63 | LibreFranklin |
| `li` | 112 | 16px | 400 | #726a63 | LibreFranklin |

## Component vocabulary

Class names repeated across the markup, with utility and framework classes filtered out — the site's own component names:

`megamenu-logo-image` (720), `link--text` (154), `list-menu__item` (147), `visually-hidden--inline` (138), `menu-drawer__menu-item` (122), `mega-menu__link` (110), `gradient` (98), `motion-reduce` (93), `pd-cp-cookies-list-item` (92), `pd-cp-cookies-list-item--type_description` (92), `skiptranslate` (62), `caption` (50), `unit-price` (46), `card__badge` (45), `left` (45), `card__content` (44), `qv-qty-btn` (44), `quick-view-qty-btn` (44), `icon-plus` (43), `icon-minus` (40)

## Page templates

Routes sharing a template share a layout. One is detailed below, the rest differ only in content.

| Template | Pages | Representative | Words | Mode |
|---|---|---|---|---|
| `/en-qa` | 2 | `en-qa` | 1165 | ssr |
| `/agents.md` | 1 | `agents-md` | 560 | ssr |
| `/en-qa/products/*` | 22 | `en-qa-products-cosmic-dealer-box-of-7` | 1160 | ssr |

## Pages

| Slug | Route | Title | Mode | Words | Sections | Forms | Images |
|---|---|---|---|---|---|---|---|
| `en-qa` | /en-qa | The Elevare Market \| Premium Wellness and Li | ssr | 1165 | 28 | 88 | 586 |
| `agents-md` | /agents.md |  | ssr | 560 | 1 | 0 | 0 |
| `en-qa-2` | /en-qa | The Elevare Market \| Premium Wellness and Li | ssr | 1165 | 28 | 88 | 586 |
| `en-qa-products-cheeky-panda-facial-tissue` | /en-qa/products/cheeky-panda-facial-tissue | Cheeky Panda Balsam Bamboo Facial Tissues (C | ssr | 1059 | 21 | 10 | 378 |
| `en-qa-products-cheeky-panda-classic-bamboo-pocket-tissue` | /en-qa/products/cheeky-panda-classic-bamboo-pocket-tissue | Cheeky Panda Classic Bamboo Pocket Tissues \| | ssr | 1063 | 21 | 10 | 379 |
| `en-qa-products-cheeky-panda-bamboo-cocktail-napkins` | /en-qa/products/cheeky-panda-bamboo-cocktail-napkins | Cheeky Panda Bamboo Cocktail Napkins \| Eleva | ssr | 1034 | 21 | 10 | 373 |
| `en-qa-products-cheeky-panda-plastic-free-kitchen-towel` | /en-qa/products/cheeky-panda-plastic-free-kitchen-towel | Cheeky Panda Bamboo Kitchen Towel \| Elevare | ssr | 1037 | 21 | 10 | 373 |
| `en-qa-products-cheeky-panda-plastic-free-toilet-tissue` | /en-qa/products/cheeky-panda-plastic-free-toilet-tissue | Cheeky Panda Bamboo Toilet Tissue \| Elevare | ssr | 1067 | 21 | 10 | 373 |
| `en-qa-products-cheeky-panda-bamboo-paper-straws` | /en-qa/products/cheeky-panda-bamboo-paper-straws | Cheeky Panda Black Bamboo Paper Straws \| Ele | ssr | 1044 | 21 | 10 | 373 |
| `en-qa-products-cheeky-panda-bamboo-paper-sip-straws` | /en-qa/products/cheeky-panda-bamboo-paper-sip-straws | Cheeky Panda Black Bamboo Paper Sip Straws \| | ssr | 1048 | 21 | 10 | 378 |
| `en-qa-products-cheeky-panda-bamboo-baby-wipes` | /en-qa/products/cheeky-panda-bamboo-baby-wipes | Cheeky Panda Bamboo Baby Wipes \| Elevare | ssr | 1066 | 21 | 10 | 373 |
| `en-qa-products-handy-wipes-multipack-of-12` | /en-qa/products/handy-wipes-multipack-of-12 | Cheeky Panda Bamboo Handy Wipes \| Elevare | ssr | 1055 | 21 | 10 | 373 |
| `en-qa-products-dry-wipes-100s` | /en-qa/products/dry-wipes-100s | Cheeky Panda Bamboo Dry Wipes \| Elevare | ssr | 1023 | 21 | 10 | 373 |
| `en-qa-products-cheeky-panda-bamboo-face-wipes` | /en-qa/products/cheeky-panda-bamboo-face-wipes | Cheeky Panda Unscented Bamboo Face Wipes \| E | ssr | 1060 | 21 | 10 | 373 |
| `en-qa-products-cheeky-panda-bamboo-panty-liners` | /en-qa/products/cheeky-panda-bamboo-panty-liners | Cheeky Panda Bamboo Panty Liners \| Elevare | ssr | 1046 | 21 | 10 | 373 |
| `en-qa-products-cheeky-panda-bamboo-sanitary-pads` | /en-qa/products/cheeky-panda-bamboo-sanitary-pads | Cheeky Panda Bamboo Pads, Light Flow \| Eleva | ssr | 1063 | 21 | 10 | 373 |
| `en-qa-products-cosmic-dealer-box-of-7` | /en-qa/products/cosmic-dealer-box-of-7 | Cosmic Dealer "The Chakra" Best-Selling Flav | ssr | 1160 | 21 | 10 | 382 |
| `en-qa-products-cosmic-dealer-box-of-14-seasonal-flavours-mix` | /en-qa/products/cosmic-dealer-box-of-14-seasonal-flavours-mix | Cosmic Dealer Seasonal Flavours Mixed Chocol | ssr | 1155 | 21 | 10 | 386 |
| `en-qa-products-cosmic-dealer-box-of-20-flavours` | /en-qa/products/cosmic-dealer-box-of-20-flavours | Cosmic Dealer Mixed Chocolate Box, 20 Count  | ssr | 1152 | 21 | 10 | 386 |
| `en-qa-products-clearspring-demeter-organic-garden-peas` | /en-qa/products/clearspring-demeter-organic-garden-peas | Clearspring Demeter Organic Garden Peas \| El | ssr | 1055 | 21 | 10 | 378 |
| `en-qa-products-clearspring-demeter-organic-french-beans` | /en-qa/products/clearspring-demeter-organic-french-beans | Clearspring Demeter Organic French Beans \| E | ssr | 1057 | 21 | 10 | 378 |
| `en-qa-products-clearspring-demeter-organic-carrots-peas` | /en-qa/products/clearspring-demeter-organic-carrots-peas | Clearspring Demeter Organic Carrots & Peas \| | ssr | 1062 | 21 | 10 | 378 |
| `en-qa-products-clearspring-demeter-organic-sauerkraut` | /en-qa/products/clearspring-demeter-organic-sauerkraut | Clearspring Demeter Organic Sauerkraut \| Ele | ssr | 1059 | 21 | 10 | 378 |
| `en-qa-products-clearspring-demeter-organic-chickpeas` | /en-qa/products/clearspring-demeter-organic-chickpeas | Clearspring Demeter Organic Chickpeas \| Elev | ssr | 1053 | 21 | 10 | 378 |
| `en-qa-products-clearspring-demeter-organic-lentils` | /en-qa/products/clearspring-demeter-organic-lentils | Clearspring Demeter Organic Lentils \| Elevar | ssr | 1058 | 21 | 10 | 378 |

## Page structure

### `en-qa` — The Elevare Market | Premium Wellness and Lifestyle Essentials

*Representative of `/en-qa` — 1 more page(s) share this layout.*

*Provenance and purity, no compromise. Day-to-day essentials to help you establish an achievable daily wellbeing practice. Shop curated health, beauty, and everyday essentials delivered across Qatar. P*

Route: `https://elevaremarket.com/en-qa` · Mode: `ssr` · Markup: `pages/en-qa/rendered.html` · Text: `pages/en-qa/content.md`

Outline:
      - h4: Your Cart
      - h4: Your Cart
  - h2: Restore From Within
  - h2: back together Again
  - h2: The Elevare Standard
  - h2: New Arrivals
  - h2: Elevare Exclusives
  - h2: Featured Products
  - h2: Elevare favourites
        - h5: Fuel for school
        - h5: Pure Family Living
        - h5: Cycle Harmony
  - h2: Born from a relentless pursuit of clean living
  - h2: Happy House
  - h2: Elevare Journal
    - h3: How to Choose a Healthier Breakfast Cereal?
    - h3: 9 Best Types of Gluten-Free Flour for Baking
    - h3: Is High-Protein Pasta Good for You?

- **<div>** — Manage consent preferences Reject all Accept all We use cookies to optimize website functionality, analyze the performance, and provide personalized experience to you. Some cookies are essential to make the website operate and function correctly. Those cookies cannot be disabled. In this window you can manage your pref
  - CTAs: Reject all, Accept all, Strictly necessary cookies, Always allowed, Cookies details, Functional cookies
- **<div>** — header-drawer { justify-self: end; }@media screen and (min-width: 1200px) { .shopify-section-header-nav-hidden .header__inline-menu.js-nav{ max-height: 1.6rem; } .header__inline-menu.js-nav{ max-height: var(--header-nav-height); overflow: hidden; transition: max-height 300ms; will-change: max-height; } }body:not(.page-
  - CTAs: Groceries, Groceries, Pantry, Snacks, Bakery, Dairy & Eggs
- **Restore From Within** — @media screen and (max-width: 749px) {#Slider-template--22847787630777__slideshow_BN7CGy::before, #Slider-template--22847787630777__slideshow_BN7CGy.media::before, #Slider-template--22847787630777__slideshow_BN7CGy:not(.banner--mobile-bottom) .banner__content::before { padding-bottom: 66.66666666666666%; content: ''; d
  - CTAs: SHOP THE COLLECTION, Discover The Collection, Shop the collection, Add to cart Out of stock, -, +
- **The Elevare Standard** — .elevare-standard-template--22847787630777__elevare_standard_Hx8NU9 { padding-top: 36px; padding-bottom: 36px; position: relative; overflow: hidden; background: #f8f6f0; } @media screen and (min-width: 750px) { .elevare-standard-template--22847787630777__elevare_standard_Hx8NU9 { padding-top: 60px; padding-bottom: 60px
- **New Arrivals** — .section-template--22847787630777__product_suggestions_4BPYJ8-padding:not(:has(.splide__list:empty)) { padding-top: 24px; padding-bottom: 24px; } #shopify-section-template--22847787630777__product_suggestions_4BPYJ8 .splide__slide { width: 15rem; } @media screen and (min-width: 750px) { .section-template--2284778763077
  - CTAs: Shop the collection, Add to cart Out of stock, -, +, Add to cart, Add to cart Out of stock
- **Elevare Exclusives** — .section-template--22847787630777__product_suggestions_dhTd8y-padding:not(:has(.splide__list:empty)) { padding-top: 24px; padding-bottom: 24px; } #shopify-section-template--22847787630777__product_suggestions_dhTd8y .splide__slide { width: 15rem; } @media screen and (min-width: 750px) { .section-template--2284778763077
  - CTAs: Shop the collection, Add to cart Coming Soon, -, +, Add to cart, Out of stock Out of stock

- Form `POST /en-qa/cart` — 
- Form `POST /en-qa/localization` — form_type:hidden, utf8:hidden, _method:hidden, return_to:hidden, locale_code:hidden
- Form `GET /en-qa/search` — q:search, options[prefix]:hidden

### `agents-md` — 

Route: `https://elevaremarket.com/agents.md` · Mode: `ssr` · Markup: `pages/agents-md/rendered.html` · Text: `pages/agents-md/content.md`

- **<pre>** — # Agent Instructions — Elevare Market This document describes how AI agents can interact with Elevare Market's online store at https://elevaremarket.com. ## For Personal Shopping Assistants and Agents Acting On Behalf of a User If you are reading this on behalf of your user and you act as a personal assistant or person

### `en-qa-products-cosmic-dealer-box-of-7` — Cosmic Dealer "The Chakra" Best-Selling Flavours Chocolate Box – Eleva

*Representative of `/en-qa/products/*` — 21 more page(s) share this layout.*

*The Chakra Box is a curated collection of seven functional chocolates designed to align your senses. Shop online in Qatar with fast, convenient delivery.*

Route: `https://elevaremarket.com/en-qa/products/cosmic-dealer-box-of-7` · Mode: `ssr` · Markup: `pages/en-qa-products-cosmic-dealer-box-of-7/rendered.html` · Text: `pages/en-qa-products-cosmic-dealer-box-of-7/content.md`

Outline:
      - h4: Your Cart
      - h4: Your Cart
- h1: Cosmic Dealer "The Chakra" Best-Selling Flavours Chocolate Box
  - h2: Cosmic Dealer "The Chakra" Best-Selling Flavours Chocolate Box
  - h2: Description
  - h2: Ingredients
  - h2: Storage Conditions
  - h2: Elevare Standard
  - h2: Frequently asked questions
          - h6: How To Place An Order
          - h6: How To Place An Order
          - h6: Payment Methods
          - h6: Payment Methods
          - h6: Track & Manage My Order
          - h6: Track & Manage My Order
          - h6: Delivery Information
          - h6: Delivery Information
          - h6: Returns, Exchanges & Order Problems

- **<div>** — Manage consent preferences Reject all Accept all We use cookies to optimize website functionality, analyze the performance, and provide personalized experience to you. Some cookies are essential to make the website operate and function correctly. Those cookies cannot be disabled. In this window you can manage your pref
  - CTAs: Reject all, Accept all, Strictly necessary cookies, Always allowed, Cookies details, Functional cookies
- **<div>** — header-drawer { justify-self: end; }@media screen and (min-width: 1200px) { .shopify-section-header-nav-hidden .header__inline-menu.js-nav{ max-height: 1.6rem; } .header__inline-menu.js-nav{ max-height: var(--header-nav-height); overflow: hidden; transition: max-height 300ms; will-change: max-height; } }body:not(.page-
  - CTAs: Groceries, Groceries, Pantry, Snacks, Bakery, Dairy & Eggs
- **Cosmic Dealer "The Chakra" Best-Selling Flavours Chocolate Box** — .section-template--22847788155065__main-padding { padding-top: 0px; padding-bottom: 42px; } @media screen and (min-width: 750px) { .section-template--22847788155065__main-padding { padding-top: 0px; padding-bottom: 56px; } } { "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [ { "@type": 
  - CTAs: Skip to product information, Open media 1 in modal, Open media 2 in modal, Open media 3 in modal, Decrease quantity for Cosmic D, Increase quantity for Cosmic D
- **Cosmic Dealer "The Chakra" Best-Selling Flavours Chocolate Box** — .section-template--22847788155065__main-padding { padding-top: 0px; padding-bottom: 42px; } @media screen and (min-width: 750px) { .section-template--22847788155065__main-padding { padding-top: 0px; padding-bottom: 56px; } } { "@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [ { "@type": 
  - CTAs: Skip to product information, Open media 1 in modal, Open media 2 in modal, Open media 3 in modal, Decrease quantity for Cosmic D, Increase quantity for Cosmic D
- **Frequently asked questions** — .section-template--22847788155065__collapsible_content_tXYdVp-padding { padding-top: 24px; padding-bottom: 24px; } @media screen and (min-width: 750px) { .section-template--22847788155065__collapsible_content_tXYdVp-padding { padding-top: 48px; padding-bottom: 48px; } } Frequently asked questions How To Place An Order 
- **The Elevare Standard** — .elevare-standard-template--22847788155065__elevare_standard_wUbQdR { padding-top: 36px; padding-bottom: 36px; position: relative; overflow: hidden; background: #f8f6f0; } @media screen and (min-width: 750px) { .elevare-standard-template--22847788155065__elevare_standard_wUbQdR { padding-top: 60px; padding-bottom: 60px

- Form `POST /en-qa/cart` — 
- Form `POST /en-qa/localization` — form_type:hidden, utf8:hidden, _method:hidden, return_to:hidden, locale_code:hidden
- Form `GET /en-qa/search` — q:search, options[prefix]:hidden

## Data sources

Content this site loads at runtime. These files hold the real data and templates, not the HTML shell:

**`en-qa`**

| Endpoint | Type | Bytes | Local file |
|---|---|---|---|
| elevaremarket.com/en-qa/cart.json?odd_ref=1 | application/json | 303 | data/7204fab77f041de8.json |
| elevaremarket.com/api/unstable/graphql.json | application/json | 533 | data/6515b73d7155c646.json |

**`en-qa-products-cosmic-dealer-box-of-7`**

| Endpoint | Type | Bytes | Local file |
|---|---|---|---|
| elevaremarket.com/en-qa/cart.json?odd_ref=1 | application/json | 303 | data/7204fab77f041de8.json |
| elevaremarket.com/api/unstable/graphql.json | application/json | 569 | data/6515b73d7155c646.json |
| elevaremarket.com/en-qa/recommendations/products?limit=10&intent=complementary | text/html | 81,887 | data/dfaa502e3a941827.html |

## Assets

190 js, 165 images, 41 css, 6 fonts

Fonts on disk:

- `assets/fonts/8f7d1f17c2ac3abc.woff2` ← elevaremarket.com/cdn/fonts/assistant/assistant_n4.9120912a469cad1cc29
- `assets/fonts/127d9e7047569a7d.woff2` ← elevaremarket.com/cdn/shop/t/75/assets/DMSerifDisplay-Regular.woff2?v=
- `assets/fonts/2359f364ef15f741.woff2` ← elevaremarket.com/cdn/shop/t/75/assets/industry-black.woff2?v=18066977
- `assets/fonts/35d798d3e1ea4377.woff2` ← elevaremarket.com/cdn/shop/t/75/assets/LibreFranklin-Regular.woff2?v=7
- `assets/fonts/bebd82a3d8064138.woff2` ← elevaremarket.com/cdn/shop/t/75/assets/LibreFranklin-SemiBold.woff2?v=
- `assets/fonts/52e605852c72cc2d.woff2` ← fonts.gstatic.com/s/librefranklin/v20/jizDREVItHgc8qDIbSTKq4XkRiUf2zc.

`manifest.json` → `assets.map` maps every original URL to its local file.

## Where everything lives

```
manifest.json          index of pages, files, assets, strategy
sitemap.json           crawl graph: url, status, links, depth, parent
tokens.json            the design tokens above, machine readable
design/                raw extractor output: css.json, typography.json
pages/<slug>/          page.json, rendered.html, raw.html, content.md, data/, shots/
assets/                images, fonts, css, js, media — content-hashed
```

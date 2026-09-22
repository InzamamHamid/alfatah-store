import json, os, re

SP = "/tmp/claude-1000/-mnt-DATA-DATA-Study-claude-mini-projects-Elevare-clone/e00d2d6f-2dbb-4f24-983e-1d36c8be35a4/scratchpad"
OUT = "/mnt/DATA/DATA/Study_claude/mini_projects/Elevare_clone/alfatah-store"

detail = json.load(open(f"{SP}/products.json"))
home = json.load(open(f"{SP}/home.json"))

# category inferred from brand + name keywords; the capture's nav taxonomy
RULES = [
    ("Home & Garden", r"napkin|towel|tissue|straw|wipe|glove|cleaner|laundry|bathroom"),
    ("Health & Beauty", r"pad|liner|oil|scraper|tongue|beauty|serum|argan|supplement"),
    ("Snacks", r"chocolate|choc|puff|chips|nuts?|walnut|pecan|pistachio|hazelnut|mints|snack|cracker|biscuit"),
    ("Pantry", r"tahini|vinegar|flour|pasta|penne|olive oil|lentil|chickpea|bean|pea|sauerkraut|cabbage|tomato|juice|yeast|pizza|cereal|tortilla|vegan|grate"),
    ("Dairy & Eggs", r"yogurt|butter|milk|creamer|cheese|mousse"),
    ("Beverages", r"tea|coffee|water|drink"),
    ("Baby & Toddler", r"baby|toddler|farm.*avocado|rumpus"),
]

def categorise(name, brand):
    hay = f"{name} {brand}".lower()
    for cat, pat in RULES:
        if re.search(pat, hay):
            return cat
    return "Pantry"

catalog = {}

# 1. full-detail products (own product pages in the capture)
for p in detail:
    catalog[p["slug"]] = {
        "slug": p["slug"], "name": p["name"], "brand": p["brand"], "sku": p["sku"],
        "price": p["price"], "currency": p["currency"], "in_stock": p["in_stock"],
        "description": p["description"], "size": p["size"], "best_by": p["best_by"],
        "images": p["gallery"], "sections": [], "detailed": True,
        "category": categorise(p["name"], p["brand"]),
    }

# 2. home cards — fill gaps, never overwrite richer records
for c in home["products"]:
    rec = catalog.get(c["slug"])
    if rec:
        rec["sections"].append(c["section"])
        continue
    catalog[c["slug"]] = {
        "slug": c["slug"], "name": c["name"], "brand": c["brand"], "sku": "",
        "price": c["price"], "currency": c["currency"], "in_stock": not c["sold_out"],
        "description": "", "size": "", "best_by": "",
        "images": c.get("files", []), "sections": [c["section"]], "detailed": False,
        "category": categorise(c["name"], c["brand"]),
    }

items = sorted(catalog.values(), key=lambda p: (p["category"], p["name"]))
for p in items:
    p["images"] = [i for i in p["images"] if os.path.exists(f"{OUT}/{i['file']}")]

# drop anything that lost all its imagery
items = [p for p in items if p["images"]]

# brand logo list: real megamenu logos only
BRANDS = ["clearspring", "seven-sundays", "milkadamia", "artisana", "seventh-generation",
          "davids", "cosmic-dealer", "siete", "hu-chocolate", "cheeky-panda", "simply-organic",
          "fushi", "anchient-harvest", "arrowhead-mills", "pacha", "boulder-canyon",
          "four-sigmatic", "wendell-estate"]
brands = []
for b in home["brand_files"]:
    stem = os.path.splitext(os.path.basename(b["file"]))[0]
    if stem in BRANDS and os.path.exists(f"{OUT}/{b['file']}"):
        brands.append({"file": b["file"], "name": b["name"].replace("Anchient", "Ancient")})

site = {
    "products": items,
    "articles": [a for a in home["articles"] if a["image"].get("file")],
    "pillars": home["pillars"],
    "slides": home["slides"],
    "editorial": home["editorial_files"],
    "brands": brands,
}
json.dump(site, open(f"{OUT}/data/catalog.json", "w"), indent=1)

import collections
print("products:", len(items), "| detailed:", sum(p["detailed"] for p in items))
print(collections.Counter(p["category"] for p in items))
print("sections:", collections.Counter(s for p in items for s in p["sections"]))
print("brands:", len(brands), "| articles:", len(site["articles"]))
print("price range:", min(p["price"] for p in items), max(p["price"] for p in items))

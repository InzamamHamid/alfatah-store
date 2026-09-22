import json, os, glob, re, sys, html, hashlib, urllib.request, urllib.error

B = "/mnt/DATA/DATA/Study_claude/mini_projects/Elevare_clone/elevaremarket.com_20260921_201649"
OUT = "/mnt/DATA/DATA/Study_claude/mini_projects/Elevare_clone/alfatah-store"
IMGDIR = os.path.join(OUT, "assets", "products")
os.makedirs(IMGDIR, exist_ok=True)

IMG = re.compile(r"<img\b[^>]*>", re.I)
ATTR = re.compile(r'(\w[\w-]*)\s*=\s*"([^"]*)"')
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"}

def abs_url(u, width=900):
    if u.startswith("//"):
        u = "https:" + u
    return re.sub(r"([?&])width=\d+", r"\g<1>width=%d" % width, u)

def fetch(url, dest):
    if os.path.exists(dest):
        return True
    try:
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        if len(data) < 500:
            return False
        open(dest, "wb").write(data)
        return True
    except Exception as e:
        print("   ! fetch failed", url[:70], e)
        return False

def gallery(path):
    h = open(path, encoding="utf-8").read()
    i = h.find("product__media-list")
    if i < 0:
        return []
    chunk = h[i:h.find("</media-gallery>", i)]
    out, seen = [], []
    for tag in IMG.findall(chunk):
        a = dict(ATTR.findall(tag))
        src = a.get("src") or a.get("data-src") or ""
        if not src and a.get("srcset"):
            src = a["srcset"].split(",")[-1].strip().split(" ")[0]
        if not src:
            continue
        url = abs_url(html.unescape(src))
        key = url.split("?")[0]
        if key in seen:
            continue
        seen.append(key)
        out.append({"url": url, "alt": html.unescape(a.get("alt", ""))})
    return out

def split_desc(d):
    body, meta = [], {}
    for l in [x.strip() for x in d.split("\n") if x.strip()]:
        if l.lower().startswith("best by"):
            meta["best_by"] = l.split(":", 1)[-1].strip()
        elif re.fullmatch(r"[\d.]+\s*(g|kg|ml|l|pcs?|count|sheets?|wipes?)\b.*", l, re.I) or re.fullmatch(r"\d+\s*x\s*\d+.*", l, re.I):
            meta["size"] = l
        else:
            body.append(l)
    return " ".join(body), meta

products = []
for d in sorted(glob.glob(f"{B}/pages/en-qa-products-*")):
    pj = json.load(open(f"{d}/page.json"))
    prod = next((j for j in pj["jsonld"] if j.get("@type") == "Product"), None)
    if not prod:
        continue
    slug = os.path.basename(d).replace("en-qa-products-", "")
    desc, meta = split_desc(prod.get("description", ""))
    off = prod.get("offers") or {}
    files = []
    for n, g in enumerate(gallery(f"{d}/rendered.html")[:3]):
        ext = os.path.splitext(g["url"].split("?")[0])[1] or ".png"
        name = f"{slug}-{n}{ext}"
        if fetch(g["url"], os.path.join(IMGDIR, name)):
            files.append({"file": f"assets/products/{name}", "alt": g["alt"] or prod["name"]})
    products.append({
        "slug": slug,
        "name": prod["name"],
        "brand": (prod.get("brand") or {}).get("name", ""),
        "sku": prod.get("sku", ""),
        "price": float(off.get("price") or 0),
        "currency": off.get("priceCurrency", "QAR"),
        "in_stock": "InStock" in (off.get("availability") or ""),
        "description": desc,
        "size": meta.get("size", ""),
        "best_by": meta.get("best_by", ""),
        "gallery": files,
    })
    print(f"  {slug[:46]:46} {products[-1]['price']:7.2f}  imgs={len(files)}")

json.dump(products, open(sys.argv[1], "w"), indent=1)
print("products:", len(products), "| no images:", [p["slug"] for p in products if not p["gallery"]])

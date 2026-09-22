import json, os, re, shutil, urllib.request, sys

SP = "/tmp/claude-1000/-mnt-DATA-DATA-Study-claude-mini-projects-Elevare-clone/e00d2d6f-2dbb-4f24-983e-1d36c8be35a4/scratchpad"
B = "/mnt/DATA/DATA/Study_claude/mini_projects/Elevare_clone/elevaremarket.com_20260921_201649"
OUT = "/mnt/DATA/DATA/Study_claude/mini_projects/Elevare_clone/alfatah-store"
UA = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131 Safari/537.36"}

for d in ["assets/products", "assets/editorial", "assets/journal", "assets/brands", "assets/fonts"]:
    os.makedirs(f"{OUT}/{d}", exist_ok=True)

def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 500:
        return True
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
            data = r.read()
        if len(data) < 500:
            return False
        open(dest, "wb").write(data)
        return True
    except Exception as e:
        print("  ! ", url[:80], e)
        return False

def ext_of(u, default=".png"):
    e = os.path.splitext(u.split("?")[0])[1].lower()
    return e if e in (".png", ".jpg", ".jpeg", ".webp", ".svg", ".avif") else default

home = json.load(open(f"{SP}/home.json"))

# --- editorial ---
ed = {}
for key, url in home["editorial"].items():
    if not url:
        continue
    name = key + ext_of(url, ".webp")
    if fetch(url, f"{OUT}/assets/editorial/{name}"):
        ed[key] = f"assets/editorial/{name}"
print("editorial:", len(ed))

# --- journal ---
for a in home["articles"]:
    name = a["slug"][:50] + ext_of(a["image"]["url"], ".jpg")
    a["image"]["file"] = f"assets/journal/{name}" if fetch(a["image"]["url"], f"{OUT}/assets/journal/{name}") else None
print("journal:", sum(1 for a in home["articles"] if a["image"].get("file")))

# --- home product cards ---
ok = 0
for p in home["products"]:
    files = []
    for n, im in enumerate(p["images"]):
        name = f"{p['slug'][:48]}-{n}{ext_of(im['url'])}"
        if fetch(im["url"], f"{OUT}/assets/products/{name}"):
            files.append({"file": f"assets/products/{name}", "alt": im["alt"] or p["name"]})
    p["files"] = files
    ok += bool(files)
print("card images:", ok, "/", len(home["products"]))

# --- brand logos: straight copy out of the bundle ---
amap = json.load(open(f"{B}/manifest.json"))["assets"]["map"]
brands = []
for orig, local in amap.items():
    base = os.path.basename(orig.split("?")[0])
    if not re.search(r"/cdn/shop/files/", orig):
        continue
    stem = os.path.splitext(base)[0]
    # megamenu brand logos: Name_<uuid>.png
    if not re.fullmatch(r"[A-Za-z0-9._]+_[0-9a-f]{8}-[0-9a-f-]+", stem):
        continue
    src = f"{B}/{local}"
    if not os.path.exists(src):
        continue
    label = re.sub(r"[._]+", " ", stem.split("_" + stem.split("_")[-5] if False else stem)[0]).strip()
    label = re.sub(r"\s*_?[0-9a-f-]{8,}.*$", "", re.sub(r"[._]+", " ", stem)).strip()
    dest = f"assets/brands/{re.sub(r'[^a-z0-9]+','-',label.lower()).strip('-')}{ext_of(local)}"
    shutil.copy(src, f"{OUT}/{dest}")
    brands.append({"file": dest, "name": label.replace("2 ", "").strip()})
seen = set()
brands = [b for b in brands if not (b["file"] in seen or seen.add(b["file"]))]
print("brands:", len(brands), [b["name"] for b in brands][:20])

# --- fonts ---
fonts = {}
for orig, local in amap.items():
    base = os.path.basename(orig.split("?")[0])
    if base.endswith(".woff2") and ("DMSerifDisplay" in base or "LibreFranklin" in base):
        shutil.copy(f"{B}/{local}", f"{OUT}/assets/fonts/{base}")
        fonts[base] = f"assets/fonts/{base}"
print("fonts:", list(fonts))

home["editorial_files"] = ed
home["brand_files"] = brands
home["font_files"] = fonts
json.dump(home, open(f"{SP}/home.json", "w"), indent=1)

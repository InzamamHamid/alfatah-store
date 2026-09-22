"""Static smoke test for the generated ALFATAH site: every local href/src resolves,
no template leakage, every page has the required chrome."""

import os, re, sys, glob, html

ROOT = "/mnt/DATA/DATA/Study_claude/mini_projects/Elevare_clone/alfatah-store"
pages = sorted(glob.glob(f"{ROOT}/*.html") + glob.glob(f"{ROOT}/products/*.html"))
errors, warned = [], 0

REF = re.compile(r'(?:href|src)="([^"]+)"')

for page in pages:
    rel = os.path.relpath(page, ROOT)
    doc = open(page, encoding="utf-8").read()
    # token checks ignore embedded JSON-LD, which legitimately contains braces
    prose = re.sub(r"<script[^>]*>.*?</script>", "", doc, flags=re.S)
    base = os.path.dirname(page)

    for ref in REF.findall(doc):
        ref = html.unescape(ref)
        if ref.startswith(("http", "//", "#", "mailto:", "data:")):
            continue
        target = ref.split("?")[0].split("#")[0]
        if not target:
            continue
        path = os.path.normpath(os.path.join(base, target))
        if not os.path.exists(path):
            errors.append(f"{rel}: missing target {ref}")

    for token in ("{e(", "None", "{{", "}}", "undefined"):
        if token in prose:
            errors.append(f"{rel}: template leak {token!r}")

    for must in ("<title>", 'class="header"', "<footer", "cart.js", "ui.js", 'id="main"'):
        if must not in doc:
            errors.append(f"{rel}: missing {must}")

    if doc.count("<h1") > 1:
        errors.append(f"{rel}: {doc.count('<h1')} h1 elements")

    imgs = re.findall(r"<img\b[^>]*>", doc)
    for tag in imgs:
        if "alt=" not in tag:
            errors.append(f"{rel}: img without alt — {tag[:70]}")

print(f"pages checked: {len(pages)}")
if errors:
    print(f"ERRORS: {len(errors)}")
    for err in errors[:40]:
        print("  -", err)
    sys.exit(1)
print("all local references resolve; chrome present on every page")

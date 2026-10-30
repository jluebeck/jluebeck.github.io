"""Build prototypes: full HTML pages in prototypes/ and artifact fragments in a scratch dir.

Usage: python3 prototypes/src/build.py [artifact_out_dir]
"""
import base64, json, pathlib, sys

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent
CV = "https://drive.google.com/file/d/1F6BNKErYd7ilL7CxAAEkQoBL2D0QUOxc/view?usp=sharing"
IMAGES = {"{{PHOTO_SQ}}": "portrait-sq.jpg", "{{PHOTO_PORTRAIT}}": "portrait.jpg", "{{PHOTO_TALK}}": "talk-edynamic.jpg"}

USAGE = json.loads((SRC / "aa_usage.json").read_text())
SUBS = {
    "{{CV}}": CV,
    "{{USAGE_DATA}}": json.dumps(USAGE, separators=(",", ":")),
    "{{USAGE_CHART}}": (SRC / "usage-chart.js").read_text(),
    "{{PUBS}}": (SRC / "publications.js").read_text(),
    "{{USAGE_TOTAL}}": f"{sum(x['samples'] for x in USAGE):,}",
    "{{USAGE_STUDIES}}": str(len(USAGE)),
    "{{USAGE_EXTERNAL}}": str(sum(x["external"] for x in USAGE)),
}

head = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
for f in sorted(SRC.glob("*.html")):
    s = f.read_text()
    for k, v in SUBS.items():
        s = s.replace(k, v)
    # Split leading <title>/<meta>/<link>/<style> into <head>; the rest is body.
    i = s.index("</style>") + len("</style>")
    page = head + s[:i] + "\n</head>\n<body>\n" + s[i:] + "\n</body>\n</html>\n"
    frag = s
    for k, name in IMAGES.items():
        page = page.replace(k, "../images/" + name)
        if len(sys.argv) > 1:
            uri = "data:image/jpeg;base64," + base64.b64encode((SRC.parent.parent / "images" / name).read_bytes()).decode()
            frag = frag.replace(k, uri)
    (OUT / f.name).write_text(page)
    if len(sys.argv) > 1:
        pathlib.Path(sys.argv[1], f.name).write_text(frag)
    print("built", f.name)

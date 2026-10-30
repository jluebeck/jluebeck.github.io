"""Build prototypes: full HTML pages in prototypes/ and artifact fragments in a scratch dir.

Usage: python3 prototypes/src/build.py [artifact_out_dir]
"""
import base64, pathlib, sys

SRC = pathlib.Path(__file__).parent
OUT = SRC.parent
CV = "https://drive.google.com/file/d/1F6BNKErYd7ilL7CxAAEkQoBL2D0QUOxc/view?usp=sharing"
PHOTO = SRC.parent.parent / "images" / "portrait-sq.jpg"

head = '<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
for f in sorted(SRC.glob("*.html")):
    s = f.read_text().replace("{{CV}}", CV)
    # Split leading <title>/<meta>/<link>/<style> into <head>; the rest is body.
    i = s.index("</style>") + len("</style>")
    page = head + s[:i] + "\n</head>\n<body>\n" + s[i:] + "\n</body>\n</html>\n"
    (OUT / f.name).write_text(page.replace("{{PHOTO_SQ}}", "../images/portrait-sq.jpg"))
    if len(sys.argv) > 1:
        uri = "data:image/jpeg;base64," + base64.b64encode(PHOTO.read_bytes()).decode()
        pathlib.Path(sys.argv[1], f.name).write_text(s.replace("{{PHOTO_SQ}}", uri))
    print("built", f.name)

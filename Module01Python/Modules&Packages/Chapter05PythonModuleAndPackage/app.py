"""
Python Imports Demo  -  built-in modules, packages, `import` and `from`.

Run:  python app.py      then open  http://localhost:8000
Uses ONLY the standard library (no pip install needed).
"""

# ---------------------------------------------------------------
# 1) Plain `import module`  -> access names with module.name
# ---------------------------------------------------------------
import math
import json
import sys
import platform

# ---------------------------------------------------------------
# 2) `import module as alias`  -> shorter / clearer name
# ---------------------------------------------------------------
import datetime as dt
import random as rnd

# ---------------------------------------------------------------
# 3) `from module import name`  -> use the name directly
# ---------------------------------------------------------------
from collections import Counter, namedtuple
from pathlib import Path
from statistics import mean, median

# ---------------------------------------------------------------
# 4) `from module import name as alias`
# ---------------------------------------------------------------
from http.server import SimpleHTTPRequestHandler as Handler, HTTPServer
from urllib.parse import urlparse as parse_url

# ---------------------------------------------------------------
# 5) Importing from a PACKAGE (a folder with __init__.py)
#    - built-in package:  os.path, http.server, urllib.parse ...
#    - our own package:   toolkit/
# ---------------------------------------------------------------
import os.path                          # submodule of the built-in `os` package
import toolkit                          # our package -> runs toolkit/__init__.py
from toolkit import mathx               # import a submodule from our package
from toolkit.textx import shout, word_count   # import functions from a submodule

# ---------------------------------------------------------------
# 6) Dynamic import at runtime
# ---------------------------------------------------------------
import importlib

HERE = Path(__file__).parent
Point = namedtuple("Point", "x y")


def build_demo():
    """Run one example per import style and return the results."""
    nums = [rnd.randint(1, 20) for _ in range(8)]
    text = "python makes imports simple and python makes packages simple"
    hashlib = importlib.import_module("hashlib")      # dynamic import

    return [
        {
            "style": "import module",
            "code": "import math\nmath.sqrt(144), math.pi",
            "result": f"{math.sqrt(144)}, {round(math.pi, 5)}",
        },
        {
            "style": "import module (json, sys, platform)",
            "code": "import sys, platform\nsys.version_info[:3], platform.system()",
            "result": f"{tuple(sys.version_info[:3])}, {platform.system()}",
        },
        {
            "style": "import module as alias",
            "code": "import datetime as dt\ndt.date.today().isoformat()",
            "result": dt.date.today().isoformat(),
        },
        {
            "style": "import module as alias",
            "code": "import random as rnd\n[rnd.randint(1, 20) for _ in range(8)]",
            "result": str(nums),
        },
        {
            "style": "from module import name",
            "code": "from statistics import mean, median\nmean(nums), median(nums)",
            "result": f"{round(mean(nums), 2)}, {median(nums)}",
        },
        {
            "style": "from module import name",
            "code": "from collections import Counter\nCounter(text.split()).most_common(2)",
            "result": str(Counter(text.split()).most_common(2)),
        },
        {
            "style": "from module import name",
            "code": "from collections import namedtuple\nPoint = namedtuple('Point', 'x y')\nPoint(3, 4)",
            "result": str(Point(3, 4)),
        },
        {
            "style": "from module import name as alias",
            "code": "from urllib.parse import urlparse as parse_url\nparse_url('https://python.org/docs?q=import').netloc",
            "result": parse_url("https://python.org/docs?q=import").netloc,
        },
        {
            "style": "built-in package submodule",
            "code": "import os.path\nos.path.basename(__file__)",
            "result": os.path.basename(__file__),
        },
        {
            "style": "import package (own)",
            "code": "import toolkit\ntoolkit.__version__, toolkit.greet('Pune')",
            "result": f"{toolkit.__version__}, {toolkit.greet('Pune')}",
        },
        {
            "style": "from package import submodule",
            "code": "from toolkit import mathx\nmathx.factorial(5), mathx.is_prime(29)",
            "result": f"{mathx.factorial(5)}, {mathx.is_prime(29)}",
        },
        {
            "style": "from package.submodule import names",
            "code": "from toolkit.textx import shout, word_count\nshout('hi'), word_count(text)",
            "result": f"{shout('hi')}, {word_count(text)}",
        },
        {
            "style": "dynamic import (importlib)",
            "code": "import importlib\nhashlib = importlib.import_module('hashlib')\nhashlib.md5(b'python').hexdigest()[:12]",
            "result": hashlib.md5(b"python").hexdigest()[:12],
        },
    ]


class DemoHandler(Handler):
    """Serves index.html and the JSON API at /api/demo."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(HERE), **kwargs)

    def do_GET(self):
        if parse_url(self.path).path == "/api/demo":
            body = json.dumps({
                "python": platform.python_version(),
                "examples": build_demo(),
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            super().do_GET()          # serves index.html and other files


def main(port=8000):
    if "--cli" in sys.argv:           # python app.py --cli  -> print to terminal
        for ex in build_demo():
            print(f"[{ex['style']}]\n{ex['code']}\n=> {ex['result']}\n")
        return
    print(f"Serving on http://localhost:{port}  (Ctrl+C to stop)")
    HTTPServer(("", port), DemoHandler).serve_forever()


# Runs only when executed directly, NOT when imported by another file
if __name__ == "__main__":
    main()

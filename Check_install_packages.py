import importlib

packages = [
    "fastapi",
    "uvicorn",
    "jinja2",
    "kafka",
    "requests"
]

for pkg in packages:
    try:
        importlib.import_module(pkg)
        print(f"{pkg} ✅ Installed")
    except ImportError:
        print(f"{pkg} ❌ Not Installed")
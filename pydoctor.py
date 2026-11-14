#!/usr/bin/env python3
"""PyDoctor — inspect a Python installation without installing or changing anything."""
import argparse, importlib.util, json, os, platform, site, sys, sysconfig

MODULES = ["tkinter", "pip", "venv", "ssl", "sqlite3", "json", "ctypes"]

def report(as_json=False):
    paths = {
        "executable": sys.executable,
        "prefix": sys.prefix,
        "base_prefix": getattr(sys, "base_prefix", sys.prefix),
        "stdlib": sysconfig.get_path("stdlib"),
        "site_packages": site.getsitepackages() if hasattr(site, "getsitepackages") else [],
        "user_site": site.getusersitepackages(),
    }
    modules = {}
    for name in sorted(set(MODULES)):
        try:
            modules[name] = importlib.util.find_spec(name) is not None
        except (ImportError, ValueError):
            modules[name] = False
    data = {
        "python": sys.version,
        "version_info": list(sys.version_info[:3]),
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "architecture": platform.architecture()[0],
        "virtual_environment": sys.prefix != getattr(sys, "base_prefix", sys.prefix),
        "environment": {k: os.environ.get(k) for k in ("VIRTUAL_ENV", "CONDA_PREFIX", "PYTHONPATH")},
        "paths": paths,
        "modules": modules,
    }
    if as_json:
        print(json.dumps(data, indent=2, ensure_ascii=False))
        return
    print("PYDOCTOR — Python environment report")
    print("=" * 42)
    print(f"Version        : {sys.version.split()[0]}")
    print(f"Implementation : {data['implementation']}")
    print(f"Platform       : {data['platform']}")
    print(f"Architecture   : {data['architecture']}")
    print(f"Virtual env    : {'yes' if data['virtual_environment'] else 'no'}")
    print(f"Executable     : {sys.executable}")
    print(f"Prefix         : {sys.prefix}")
    print("\nStandard-library module availability:")
    for name, ok in modules.items():
        print(f"  {'OK  ' if ok else 'MISS'} {name}")
    print("\nEnvironment hints:")
    for key, value in data["environment"].items():
        print(f"  {key}: {value or '(not set)'}")
    print("\nSite-packages:")
    for path in paths["site_packages"]:
        print(f"  {path}")
    print(f"  user: {paths['user_site']}")
    print("\nNo settings were changed and no packages were installed.")

def main():
    parser = argparse.ArgumentParser(description="Read-only Python environment diagnostics.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON")
    args = parser.parse_args()
    report(args.json)

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Which tor the images would carry, and whether it is the newest (unseenet-bootable#9).

    python tools/tor_versions.py latest        # newest stable tor on dist.torproject.org
    python tools/tor_versions.py alpine        # tor in the Alpine the images are built on
    python tools/tor_versions.py check         # both, and exit 1 if Alpine's is older

The images take tor from Alpine's package when they are built (tools/image*/
build-in-alpine.sh), so a Tor security fix reaches them once Alpine has packaged
it. The portable builds pin Tor Browser's Expert Bundle instead; its numbers
(15.0.x) are not tor's (0.4.8.x), so the images are compared with tor itself.
"""

from __future__ import annotations

import os
import re
import subprocess
import sys
import urllib.request

DIST = "https://dist.torproject.org/"
ALPINE = os.environ.get("ALPINE", "docker.io/library/alpine:3.24")
_TOR = re.compile(r'href="tor-(\d+(?:\.\d+){3})\.tar\.gz"')


def key(v: str) -> tuple[int, ...]:
    return tuple(int(x) for x in re.findall(r"\d+", v.split("-r")[0])[:4])


def latest_stable(html: str | None = None) -> str:
    """The newest stable tor in the dist listing (alpha and rc releases are left out)."""
    if html is None:
        with urllib.request.urlopen(DIST, timeout=60) as r:
            html = r.read().decode("utf-8", "replace")
    found = [v for v in _TOR.findall(html)]
    if not found:
        raise SystemExit("no tor release found on " + DIST)
    return max(found, key=key)


def alpine(engine: str | None = None) -> str:
    """tor's version in Alpine's package for the image's Alpine release, e.g. 0.4.8.19."""
    engine = engine or ("podman" if subprocess.run(["sh", "-c", "command -v podman"],
                                                   capture_output=True).returncode == 0 else "docker")
    out = subprocess.run([engine, "run", "--rm", ALPINE, "sh", "-c",
                          "apk update -q >/dev/null 2>&1; apk policy tor"],
                         check=True, capture_output=True, text=True).stdout
    m = re.search(r"^\s+(\d+(?:\.\d+){3})(?:-r\d+)?:", out, re.M)
    if not m:
        raise SystemExit("tor not found in " + ALPINE + ":\n" + out)
    return m.group(1)


def main() -> int:
    what = sys.argv[1] if len(sys.argv) > 1 else "check"
    if what == "latest":
        print(latest_stable())
    elif what == "alpine":
        print(alpine())
    elif what == "check":
        new, have = latest_stable(), alpine()
        print(f"latest {new}, alpine {have}")
        return 0 if key(have) >= key(new) else 1
    else:
        raise SystemExit(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main())

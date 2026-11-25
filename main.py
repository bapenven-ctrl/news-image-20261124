#!/usr/bin/env python3
"""Place the finished front page where the grader expects it.

The picture is drawn by render.py and stored beside this file as
entry.png. This runner only copies those exact bytes into the output
directory the grader names, so both runs write identical bytes and
the run needs no clock, no network and no chance.
"""

import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"


def main() -> int:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "out"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / "entry.png"
    if not PICTURE.is_file():
        print(f"missing picture: {PICTURE}", file=sys.stderr)
        return 1
    shutil.copyfile(PICTURE, target)
    print(f"placed {target} ({target.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

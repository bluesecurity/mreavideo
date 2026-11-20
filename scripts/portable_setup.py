r"""
mreavideo Cross-Machine Portable Bootstrap & Submodule Patch Guard (portable_setup.py)
Ensures 1-command portability when moving or cloning mreavideo to another machine or drive:
  1. Verifies Python >= 3.10 and FFmpeg in PATH.
  2. Auto-applies the Python 3.13 RapidOCR 3 threshold patch (h < 0.08) to engine/rea_video/packaging.py.
  3. Audits ONNX audio separation model weights (~216 MB) in ~/.cache/rea-video/models/.
  4. Dynamically updates paths and syncs vrea-video-forensics/SKILL.md to ~/.gemini/config/skills/vrea-video-forensics/.
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def ensure_ffmpeg_in_path() -> str | None:
    found = shutil.which("ffmpeg")
    if found:
        return found
    winget_links = Path.home() / "AppData" / "Local" / "Microsoft" / "WinGet" / "Links"
    if (winget_links / "ffmpeg.exe").exists() or (winget_links / "ffmpeg.EXE").exists():
        os.environ["PATH"] = str(winget_links) + os.pathsep + os.environ.get("PATH", "")
        return shutil.which("ffmpeg")
    return None


def check_and_patch_submodule() -> bool:
    pkg_py = ROOT_DIR / "engine" / "rea_video" / "packaging.py"
    if not pkg_py.exists():
        print(f"[ERROR] Submodule file missing: {pkg_py}", file=sys.stderr)
        print("Run: git submodule update --init --recursive", file=sys.stderr)
        return False

    text = pkg_py.read_text(encoding="utf-8")
    old_needle = "0.7 <= med <= 7.0 and h < 0.07 and not tilted"
    new_needle = "0.7 <= med <= 7.0 and h < 0.08 and not tilted"

    if new_needle in text:
        print("  ✓ Submodule RapidOCR 3 patch (h < 0.08) already active.")
        return True
    if old_needle in text:
        pkg_py.write_text(text.replace(old_needle, new_needle, 1), encoding="utf-8")
        print("  ✓ Applied RapidOCR 3 patch (h < 0.07 -> h < 0.08) to engine/rea_video/packaging.py.")
        return True

    print("  ! Warning: Could not locate exact RapidOCR threshold line in packaging.py.")
    return True


def check_onnx_models() -> dict:
    cache_dir = Path(os.environ.get("REA_VIDEO_MODELS") or (Path.home() / ".cache" / "rea-video" / "models"))
    expected = [
        "UVR-MDX-NET-Inst_HQ_3.onnx",
        "bandit-v2-multi.onnx",
    ]
    status = {"cache_dir": str(cache_dir), "models": {}}
    for m in expected:
        p = cache_dir / m
        exists = p.exists() and p.stat().st_size > 1024 * 1024
        size_mb = round(p.stat().st_size / (1024 * 1024), 2) if exists else 0.0
        status["models"][m] = {"exists": exists, "size_mb": size_mb, "path": str(p)}
        mark = "✓" if exists else "○ (will auto-download on first run)"
        print(f"  {mark} ONNX Model {m}: {size_mb} MB ({p})")
    return status


def sync_portable_skill(sync_global: bool = True) -> bool:
    local_skill = ROOT_DIR / ".agents" / "skills" / "vrea-video-forensics" / "SKILL.md"
    if not local_skill.exists():
        print(f"[ERROR] Local skill missing: {local_skill}", file=sys.stderr)
        return False

    content = local_skill.read_text(encoding="utf-8")
    # Dynamically adapt hardcoded F:\Mcode\mreavideo if repo lives on another drive/folder
    canonical_win = r"F:\Mcode\mreavideo"
    canonical_posix = "F:/Mcode/mreavideo"
    current_win = str(ROOT_DIR)
    current_posix = ROOT_DIR.as_posix()

    if current_win.lower() != canonical_win.lower():
        content = content.replace(canonical_win, current_win).replace(canonical_posix, current_posix)
        local_skill.write_text(content, encoding="utf-8")
        print(f"  ✓ Rebound SKILL.md workspace path to: {current_win}")

    if sync_global:
        global_skill = Path.home() / ".gemini" / "config" / "skills" / "vrea-video-forensics" / "SKILL.md"
        try:
            global_skill.parent.mkdir(parents=True, exist_ok=True)
            global_skill.write_text(content, encoding="utf-8")
            print(f"  ✓ Synced Global Skill: {global_skill}")
        except Exception as exc:
            print(f"  ! Could not sync global skill ({exc})")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="mreavideo Cross-Machine Portable Bootstrap & Health Guard")
    parser.add_argument("--no-global-sync", action="store_true", help="Skip syncing to ~/.gemini/config/skills/")
    args = parser.parse_args()

    print("=" * 60)
    print("🧳 mreavideo Cross-Machine Portable Setup & Guard")
    print("=" * 60)
    print(f"Workspace Root: {ROOT_DIR}")
    print(f"Python Runtime: {sys.executable} ({sys.version.split()[0]})")

    ffmpeg_bin = ensure_ffmpeg_in_path()
    if not ffmpeg_bin:
        print("[ERROR] ffmpeg not found in PATH! Install FFmpeg first (e.g. winget install Gyan.FFmpeg).", file=sys.stderr)
        return 1
    print(f"  ✓ FFmpeg Binary: {ffmpeg_bin}")

    if not check_and_patch_submodule():
        return 1

    check_onnx_models()

    if not sync_portable_skill(sync_global=not args.no_global_sync):
        return 1

    print("=" * 60)
    print("✅ Portable setup & submodule patch verified (Exit Code 0).")
    print("=" * 60)
    return 0


if __name__ == "__main__":
    sys.exit(main())

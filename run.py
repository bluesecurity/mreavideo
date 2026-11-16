"""
mreavideo Pipeline Runner & CLI Dispatcher
Wraps rea-video engine with automated input scanning, VLM environment loading, and batch execution.
"""

import os
import sys
import argparse
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
VENV_PYTHON = ROOT_DIR / ".venv" / ("Scripts" if os.name == "nt" else "bin") / "python"
VENV_REA = ROOT_DIR / ".venv" / ("Scripts" if os.name == "nt" else "bin") / ("rea-video.exe" if os.name == "nt" else "rea-video")

def ensure_venv():
    if not VENV_REA.exists():
        print(f"[ERROR] Virtualenv executable not found at: {VENV_REA}")
        print("Please ensure .venv is created and rea-video installed.")
        sys.exit(1)

def load_env_file():
    for name in (".env.local", ".env"):
        env_file = ROOT_DIR / name
        if env_file.exists():
            with open(env_file, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip().lstrip("\ufeff")
                    if line and not line.startswith("#") and "=" in line:
                        k, v = line.split("=", 1)
                        val = v.strip().strip('"').strip("'")
                        if val:
                            os.environ.setdefault(k.strip(), val)

    # Auto-bridge shorthand keys (GEMINI_API_KEY / OPENAI_API_KEY) to REA_VLM_* expected by engine/rea_video/vlm.py
    if not os.environ.get("REA_VLM_API_KEY"):
        if os.environ.get("GEMINI_API_KEY"):
            os.environ["REA_VLM_API_KEY"] = os.environ["GEMINI_API_KEY"]
            os.environ.setdefault("REA_VLM_BASE_URL", "https://generativelanguage.googleapis.com/v1beta/openai")
            os.environ.setdefault("REA_VLM_MODEL", "gemini-2.5-flash,gemini-2.5-pro")
        elif os.environ.get("OPENAI_API_KEY"):
            os.environ["REA_VLM_API_KEY"] = os.environ["OPENAI_API_KEY"]
            os.environ.setdefault("REA_VLM_BASE_URL", "https://api.openai.com/v1")
            os.environ.setdefault("REA_VLM_MODEL", "gpt-4o-mini,gpt-4o")

def run_decompose(video_path: Path, output_dir: Path | None = None, vlm: bool = False, verbose: bool = False, lang: str = "en"):
    ensure_venv()
    load_env_file()

    if not video_path.exists():
        print(f"[ERROR] Input video does not exist: {video_path}")
        return 1

    if output_dir is None:
        video_stem = video_path.stem
        output_dir = ROOT_DIR / "outputs" / video_stem

    output_dir.parent.mkdir(parents=True, exist_ok=True)

    cmd = [str(VENV_REA)]
    if verbose:
        cmd.append("-v")
    cmd.extend(["decompose", str(video_path), "-o", str(output_dir)])
    if lang:
        cmd.extend(["--lang", lang])
    if vlm:
        cmd.append("--vlm")

    print(f"\n=======================================================")
    print(f"🎬 Processing: {video_path.name}")
    print(f"📁 Output Dir: {output_dir}")
    print(f"🤖 VLM Mode:   {'ENABLED' if vlm else 'OFFLINE (Deterministic)'}")
    print(f"=======================================================\n")

    import subprocess
    result = subprocess.run(cmd)
    if result.returncode == 0:
        print(f"\n✅ Finished successfully!")
        report_html = output_dir / "report.html"
        video_md = output_dir / "VIDEO.md"
        if report_html.exists():
            print(f"📊 Visual Report: file:///{report_html.as_posix()}")
        if video_md.exists():
            print(f"📝 Remake Spec:   file:///{video_md.as_posix()}")
        try:
            from scripts.export_handoff import compile_handoff
            bp_path, _ = compile_handoff(output_dir)
            print(f"📦 Handoff Pack:  file:///{bp_path.as_posix()}")
        except Exception as exc:
            print(f"[WARN] Could not auto-generate Handoff Blueprint: {exc}")
    else:
        print(f"\n❌ Pipeline failed with exit code: {result.returncode}")
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description="mreavideo: Reverse-Engineering Video Engine")
    parser.add_argument("video", nargs="?", help="Path to input video (.mp4, .mov, .mkv)")
    parser.add_argument("-o", "--output", help="Custom output directory")
    parser.add_argument("--vlm", action="store_true", help="Enable Multimodal Vision LLM enhancement")
    parser.add_argument("--all", action="store_true", help="Process all videos located in inputs/ directory")
    parser.add_argument("--lang", choices=["zh", "en"], default="en", help="Report and description language (default: en)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logs")

    args = parser.parse_args()

    if args.all:
        inputs_dir = ROOT_DIR / "inputs"
        valid_exts = {".mp4", ".mov", ".mkv"}
        video_files = sorted(
            p for p in inputs_dir.iterdir()
            if p.is_file() and p.suffix.lower() in valid_exts
        ) if inputs_dir.exists() else []
        if not video_files:
            print(f"No video files found in {inputs_dir}")
            sys.exit(0)
        failures = 0
        for vid in video_files:
            rc = run_decompose(vid, vlm=args.vlm, verbose=args.verbose, lang=args.lang)
            if rc != 0:
                failures += 1
        sys.exit(1 if failures else 0)
    elif args.video:
        vid_path = Path(args.video).resolve()
        out_path = Path(args.output).resolve() if args.output else None
        sys.exit(run_decompose(vid_path, out_path, vlm=args.vlm, verbose=args.verbose, lang=args.lang))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

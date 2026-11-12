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
    env_file = ROOT_DIR / ".env"
    if env_file.exists():
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())

def run_decompose(video_path: Path, output_dir: Path | None = None, vlm: bool = False, verbose: bool = False):
    ensure_venv()
    load_env_file()

    if not video_path.exists():
        print(f"[ERROR] Input video does not exist: {video_path}")
        return 1

    if output_dir is None:
        video_stem = video_path.stem
        output_dir = ROOT_DIR / "outputs" / video_stem

    output_dir.parent.mkdir(parents=True, exist_ok=True)

    cmd = [str(VENV_REA), "decompose", str(video_path), "-o", str(output_dir)]
    if vlm:
        cmd.append("--vlm")
    if verbose:
        cmd.append("-v")

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
    else:
        print(f"\n❌ Pipeline failed with exit code: {result.returncode}")
    return result.returncode

def main():
    parser = argparse.ArgumentParser(description="mreavideo: Reverse-Engineering Video Engine")
    parser.add_argument("video", nargs="?", help="Path to input video (.mp4, .mov)")
    parser.add_argument("-o", "--output", help="Custom output directory")
    parser.add_argument("--vlm", action="store_true", help="Enable Multimodal Vision LLM enhancement")
    parser.add_argument("--all", action="store_true", help="Process all videos located in inputs/ directory")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose logs")

    args = parser.parse_args()

    if args.all:
        inputs_dir = ROOT_DIR / "inputs"
        video_files = list(inputs_dir.glob("*.mp4")) + list(inputs_dir.glob("*.mov"))
        if not video_files:
            print(f"No video files found in {inputs_dir}")
            return
        for vid in video_files:
            run_decompose(vid, vlm=args.vlm, verbose=args.verbose)
    elif args.video:
        vid_path = Path(args.video).resolve()
        out_path = Path(args.output).resolve() if args.output else None
        sys.exit(run_decompose(vid_path, out_path, vlm=args.vlm, verbose=args.verbose))
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

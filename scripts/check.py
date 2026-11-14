"""
mreavideo Mechanical Validation Script (check.py)
Performs 1-command verification of runtime environment, dependencies, tools, and test suites.
Exits with code 0 on 100% success.
"""

import sys
import subprocess
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def log(msg: str):
    print(f"[CHECK] {msg}")

def run_step(desc: str, cmd: list[str]) -> bool:
    log(f"Running: {desc}...")
    res = subprocess.run(cmd, cwd=str(ROOT))
    if res.returncode != 0:
        print(f"[FAIL] {desc} exited with code {res.returncode}", file=sys.stderr)
        return False
    print(f"[PASS] {desc}\n")
    return True

def main():
    print("=" * 60)
    print("🔬 mreavideo Mechanical Validation Suite")
    print("=" * 60)

    # 1. Check Python & Core Modules
    log(f"Checking Python interpreter: {sys.executable}")
    log(f"Python version: {sys.version.split()[0]}")

    required_modules = ["cv2", "onnxruntime", "rapidocr", "videomd", "PIL", "yaml"]
    for mod in required_modules:
        try:
            __import__(mod)
            print(f"  ✓ Module available: {mod}")
        except ImportError as e:
            print(f"  ✗ Missing module: {mod} ({e})", file=sys.stderr)
            sys.exit(1)
    print("[PASS] Python environment & dependencies intact.\n")

    # 2. Check FFmpeg in PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        print("[FAIL] ffmpeg not found in PATH!", file=sys.stderr)
        sys.exit(1)
    log(f"ffmpeg located at: {ffmpeg_path}")
    print("[PASS] FFmpeg binary verified.\n")

    # 3. Check run.py help
    if not run_step("run.py CLI help", [sys.executable, "run.py", "--help"]):
        sys.exit(1)

    # 4. Run Core Pytest Suite
    pytest_bin = ROOT / ".venv" / ("Scripts" if sys.platform == "win32" else "bin") / ("pytest.exe" if sys.platform == "win32" else "pytest")
    test_files = [
        "engine/tests/test_packaging.py",
        "engine/tests/test_security.py",
        "engine/tests/test_videomd.py",
        "engine/tests/test_shots.py",
        "engine/tests/test_pipeline.py"
    ]
    if not run_step("Core Pytest Suite (54 test cases)", [str(pytest_bin), *test_files, "-q"]):
        sys.exit(1)

    # 5. Check sample test outputs exist and are valid (auto-generate if missing on clean workspace)
    sample_in = ROOT / "inputs" / "sample_test.mp4"
    sample_out = ROOT / "outputs" / "sample_test"
    required_artifacts = [
        sample_out / "VIDEO.md",
        sample_out / "report.html",
        sample_out / "breakdown.json",
        sample_out / "stems" / "vocals.wav",
        sample_out / "stems" / "music.wav",
        sample_out / "stems" / "effects.wav"
    ]
    missing = [str(a.relative_to(ROOT)) for a in required_artifacts if not a.exists()]
    if missing and sample_in.exists():
        log("Sample outputs missing; running end-to-end decompose on inputs/sample_test.mp4...")
        if not run_step("Auto-generate sample_test outputs", [sys.executable, "run.py", str(sample_in)]):
            sys.exit(1)
        missing = [str(a.relative_to(ROOT)) for a in required_artifacts if not a.exists()]
    if missing:
        print(f"[FAIL] Missing required test artifacts: {missing}", file=sys.stderr)
        sys.exit(1)
    print("[PASS] Test sample outputs verified.\n")

    print("=" * 60)
    print("🎉 ALL MECHANICAL CHECKS PASSED WITH EXIT CODE 0")
    print("=" * 60)
    sys.exit(0)

if __name__ == "__main__":
    main()

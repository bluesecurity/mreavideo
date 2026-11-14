"""
mreavideo Dual-Remote Push Utility
Synchronizes active branch to Gitea Local LAN (Primary) and GitHub (Fallback).
Runtime token masking strictly enforced (reads GITHUB_TOKEN from .env.local).
"""

import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def get_current_branch() -> str:
    res = subprocess.run(["git", "branch", "--show-current"], cwd=str(ROOT), capture_output=True, text=True, check=True)
    return res.stdout.strip()


def get_github_token() -> str:
    for env_path in (ROOT / ".env.local", ROOT.parent / "apkvideoproject" / ".env.local"):
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8-sig") as f:
                for line in f:
                    line = line.strip().lstrip("\ufeff")
                    if line.startswith("GITHUB_TOKEN=") or line.startswith("GITHUB_TOKEN ="):
                        val = line.split("=", 1)[1].strip().strip('"').strip("'")
                        if val:
                            return val
    return os.environ.get("GITHUB_TOKEN", "")


def _run_git_push(label: str, remote_target: str, refspec: str, mask_token: str = "") -> int:
    print(f"\n[PUSH] {label}...")
    env = os.environ.copy()
    env["GIT_TERMINAL_PROMPT"] = "0"
    try:
        res = subprocess.run(
            ["git", "push", remote_target, refspec],
            cwd=str(ROOT),
            env=env,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=60,
        )
    except subprocess.TimeoutExpired:
        print(f"  [FAIL] {label} timed out after 60s (network stall).", file=sys.stderr)
        return 124

    for stream in (res.stdout, res.stderr):
        if stream:
            safe = stream.replace(mask_token, "***").strip() if mask_token else stream.strip()
            if safe:
                print(safe)

    if res.returncode == 0:
        print(f"  [OK] {label} succeeded.")
    else:
        print(f"  [FAIL] {label} exited with code {res.returncode}", file=sys.stderr)
    return res.returncode


def main():
    branch = get_current_branch()
    print("=" * 60)
    print(f"mreavideo Dual-Remote Push | Branch: {branch}")
    print("=" * 60)

    code_gitea = _run_git_push("Gitea Local LAN (Primary: origin)", "origin", branch)

    token = get_github_token()
    if token:
        target = f"https://{token}@github.com/bluesecurity/mreavideo.git"
        code_github = _run_git_push("GitHub Fallback (github)", target, f"{branch}:{branch}", mask_token=token)
    else:
        print("\n[WARN] No GITHUB_TOKEN in .env.local; attempting default 'github' remote...")
        code_github = _run_git_push("GitHub Fallback (github)", "github", branch)

    print("\n" + "=" * 60)
    if code_gitea == 0 and code_github == 0:
        print("DUAL-REMOTE PUSH COMPLETED SUCCESSFULLY!")
    else:
        print(f"Push finished with status: Gitea={code_gitea}, GitHub={code_github}")
    print("=" * 60)
    sys.exit(code_gitea or code_github)


if __name__ == "__main__":
    main()

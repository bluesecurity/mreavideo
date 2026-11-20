r"""
mreavideo Air-Gapped Handoff Blueprint Compiler (export_handoff.py)
Transforms raw forensic outputs (breakdown.json, VIDEO.md, stems/, sfx/, packaging/)
into a compact, self-contained Handoff Pack (HANDOFF_BLUEPRINT.md + handoff_manifest.json)
for zero-collision integration by agents in:
  1. G:\GRAM\escbase-template3-83.v4.86\escbase_template (DOM/CSS 390x693 Slide Engine)
  2. E:\A1A\backvideo (Remotion 1080x1920 / 1080x1440 Master Template Studio)
  3. E:\A1A\flowtop (AI Video Storyboard + Vclip TTS + ASS Subtitles)
"""

import argparse
import hashlib
import json
import os
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent


def resolve_reels_catalog() -> Path:
    env_dir = os.environ.get("REELS_VAULT_DIR")
    if env_dir:
        p = Path(env_dir) / "catalog.json"
        if p.exists():
            return p
    default_p = Path(r"F:\mworkk\videosample\reels\catalog.json")
    if default_p.exists():
        return default_p
    rel_p = ROOT_DIR.parent / "videosample" / "reels" / "catalog.json"
    return rel_p


REELS_CATALOG_PATH = resolve_reels_catalog()

# Map rea-video scene styles to escbase_template visual-pattern-gallery references
ESCBASE_PATTERN_MAP = {
    "gradient": "visual-gallery:product-logo-hero / visual-gallery:highlight-mode",
    "gradients / colour fields": "visual-gallery:product-logo-hero / visual-gallery:highlight-mode",
    "type": "visual-gallery:workflow-grid / visual-gallery:risk-cards",
    "kinetic_type": "visual-gallery:workflow-grid / visual-gallery:risk-cards",
    "kinetic type": "visual-gallery:workflow-grid / visual-gallery:risk-cards",
    "particles": "visual-gallery:flow-diagram / visual-gallery:data-stream",
    "particles / point cloud": "visual-gallery:flow-diagram / visual-gallery:data-stream",
    "data": "visual-gallery:performance-bars / visual-gallery:speed-gauge",
    "data_chart": "visual-gallery:performance-bars / visual-gallery:speed-gauge",
    "data chart": "visual-gallery:performance-bars / visual-gallery:speed-gauge",
    "screen_recording": "visual-gallery:media-first-frame / visual-gallery:mock-terminal",
}


def sha256_head(path: Path, nbytes: int = 1024 * 1024) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read(nbytes))
    return h.hexdigest()


def match_reelcrew_catalog(source_info: dict) -> dict | None:
    if not REELS_CATALOG_PATH.exists():
        return None
    try:
        cat = json.loads(REELS_CATALOG_PATH.read_text(encoding="utf-8"))
    except Exception:
        return None

    src_name = (source_info.get("filename") or "").lower()
    src_sha = source_info.get("sha256_head") or ""

    for st in cat.get("styles", []):
        for v in st.get("local_videos", []):
            v_name = (v.get("filename") or "").lower()
            v_path = Path(v.get("local_path", ""))
            if v_name == src_name:
                return {"style": st, "matched_by": "filename", "video": v}
            if src_sha and v_path.exists():
                try:
                    if sha256_head(v_path) == src_sha or hashlib.sha256(v_path.read_bytes()).hexdigest() == src_sha:
                        return {"style": st, "matched_by": "sha256", "video": v}
                except Exception:
                    pass
    return None


def compile_handoff(output_dir: Path) -> tuple[Path, Path]:
    bd_path = output_dir / "breakdown.json"
    if not bd_path.exists():
        raise FileNotFoundError(f"breakdown.json not found in {output_dir}")

    bd = json.loads(bd_path.read_text(encoding="utf-8"))
    source = bd.get("source", {})
    summary = bd.get("summary", {})
    audio = bd.get("audio", {})
    packaging = bd.get("packaging", {})
    shots = bd.get("shots", [])

    fps = float(source.get("fps") or 30.0)
    width = int(source.get("width") or 540)
    height = int(source.get("height") or 960)
    duration = float(source.get("duration") or summary.get("duration") or 0.0)
    aspect = source.get("aspect_ratio") or ("9:16" if height > width else "16:9")

    reelcrew_match = match_reelcrew_catalog(source)

    # Collect global palette and shot specs
    all_colors: list[str] = []
    shot_blueprints: list[dict] = []

    for s in shots:
        idx = int(s.get("index") or 0)
        t0 = float(s.get("start") or 0.0)
        t1 = float(s.get("end") or 0.0)
        dur = round(t1 - t0, 3)
        start_frame_30 = int(round(t0 * 30))
        dur_frames_30 = max(1, int(round(dur * 30)))

        rep = s.get("replication") or {}
        spec = rep.get("spec") or {}
        scene = spec.get("scene") or {}
        style = scene.get("style") or rep.get("label") or s.get("verdict") or "unknown"
        bg = scene.get("background") or "#061014"
        palette = scene.get("palette") or [bg]
        for c in palette:
            if c and c not in all_colors:
                all_colors.append(c)

        events = scene.get("events") or []
        sequences = scene.get("sequences") or []
        trans_in = s.get("transition_in") or spec.get("transition_in") or "cut"
        if isinstance(trans_in, dict):
            trans_str = f"{trans_in.get('type', 'cut')} ({trans_in.get('duration', 0)}s)"
        else:
            trans_str = str(trans_in)

        escbase_ref = (
            "Canonical Hero Template (Slide 1 Fixed Copy Rule)"
            if idx == 1
            else ESCBASE_PATTERN_MAP.get(style, "visual-gallery:highlight-mode / custom semantic scene")
        )

        shot_blueprints.append(
            {
                "shot_index": idx,
                "id": s.get("id", f"shot_{idx:03d}"),
                "t0": round(t0, 3),
                "t1": round(t1, 3),
                "duration_s": dur,
                "remotion_30fps": {"from": start_frame_30, "durationInFrames": dur_frames_30},
                "verdict": s.get("verdict", "code_render"),
                "scene_style": style,
                "transition_in": trans_str,
                "background_hex": bg,
                "palette_hex": palette,
                "motion_events_count": len(events),
                "sequences": sequences,
                "first_frame": f"shots/shot_{idx:03d}_first.jpg",
                "last_frame": f"shots/shot_{idx:03d}_last.jpg",
                "elements_sheet": spec.get("elements_sheet") or f"shots/shot_{idx:03d}_elements.jpg",
                "escbase_pattern_suggestion": escbase_ref,
            }
        )

    # Compile SFX groups with SNR filtering
    sfx_events = (audio.get("sfx") or {}).get("events") or []
    sfx_groups: dict[str, list[dict]] = defaultdict(list)
    for ev in sfx_events:
        grp = ev.get("group") or "F0"
        sfx_groups[grp].append(ev)

    sfx_catalog: list[dict] = []
    for grp in sorted(sfx_groups.keys(), key=lambda x: int(x[1:]) if x[1:].isdigit() else 999):
        evs = sfx_groups[grp]
        num = int(grp[1:]) if grp[1:].isdigit() else 0
        rel_wav = f"sfx/sfx_{num:02d}.wav"
        abs_wav = output_dir / rel_wav
        sfx_type = Counter(e.get("type", "other") for e in evs).most_common(1)[0][0]
        avg_level = sum(float(e.get("level_db", -35.0)) for e in evs) / len(evs)
        avg_bed = sum(float(e.get("bed_db", -70.0)) for e in evs) / len(evs)
        snr_db = round(avg_level - avg_bed, 1)
        triggers = Counter((e.get("on") or {}).get("type", "ambient") for e in evs)
        timestamps = [round(float(e.get("t", 0.0)), 2) for e in evs]

        sfx_catalog.append(
            {
                "group": grp,
                "file_rel": rel_wav,
                "file_abs": str(abs_wav) if abs_wav.exists() else None,
                "exists": abs_wav.exists(),
                "type": sfx_type,
                "count": len(evs),
                "snr_db": snr_db,
                "clean_for_reuse": bool(abs_wav.exists() and snr_db >= 25.0),
                "primary_trigger": triggers.most_common(1)[0][0] if triggers else "none",
                "timestamps_s": timestamps[:12],
            }
        )

    clean_sfx = [x for x in sfx_catalog if x["clean_for_reuse"]]

    # Subtitle & Packaging stats
    text_cues = packaging.get("text_cues") or []
    entrance_counts = Counter()
    for cue in text_cues:
        ent = (cue.get("entrance") or cue.get("in") or "hard_in")
        if isinstance(ent, dict):
            ent = ent.get("type", "hard_in")
        entrance_counts[str(ent)] += 1

    stems_info = {
        "vocals_wav": str(output_dir / "stems" / "vocals.wav"),
        "music_wav": str(output_dir / "stems" / "music.wav"),
        "effects_wav": str(output_dir / "stems" / "effects.wav"),
        "subtitles_srt": str(output_dir / "packaging" / "subtitles.srt"),
        "overlays_ass": str(output_dir / "packaging" / "overlays.ass"),
        "packaging_timeline_json": str(output_dir / "packaging" / "timeline.json"),
    }

    manifest = {
        "schema": "mreavideo.handoff.v1",
        "video_name": output_dir.name,
        "output_dir": str(output_dir),
        "source": {
            "filename": source.get("filename"),
            "resolution": f"{width}x{height}",
            "aspect_ratio": aspect,
            "fps": fps,
            "duration_s": duration,
        },
        "reelcrew_catalog_match": reelcrew_match,
        "production_verdict": summary.get("verdict"),
        "confidence": summary.get("confidence"),
        "global_palette_hex": all_colors[:10],
        "audio_summary": {
            "tempo_bpm": audio.get("tempo_bpm"),
            "rms_dbfs": audio.get("rms_dbfs"),
            "total_sfx_hits": len(sfx_events),
            "distinct_sfx_groups": len(sfx_catalog),
            "clean_reusable_sfx_count": len(clean_sfx),
        },
        "packaging_summary": {
            "subtitle_cues_count": len(text_cues),
            "sfx_anchored_to_text": packaging.get("sfx_anchored", 0),
        },
        "artifacts": stems_info,
        "shots": shot_blueprints,
        "sfx_catalog": sfx_catalog,
    }

    manifest_path = output_dir / "handoff_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # Build HANDOFF_BLUEPRINT.md
    out_posix = output_dir.as_posix()
    rc_block = ""
    if reelcrew_match:
        st = reelcrew_match["style"]
        rc_block = (
            f"- **ReelCrew Style Match ({reelcrew_match['matched_by']}):** "
            f"Style #{st['style_id']} — **{st['title']}** (`{st['skill']}`)\n"
            f"- **Mô tả gốc ReelCrew:** {st['description']}\n"
        )

    md = [
        f"# 📦 Air-Gapped Handoff Blueprint: `{output_dir.name}`",
        "",
        "> **Dành cho AI Agents tại `escbase_template`, `E:\\A1A\\backvideo`, và `E:\\A1A\\flowtop`:**",
        "> Tài liệu này đã được tinh luyện từ kết quả giải phẫu video của `mreavideo`. **TUYỆT ĐỐI KHÔNG đọc file `breakdown.json` (nặng >80,000 tokens)** trừ khi cần truy xuất tọa độ vi mô. Chỉ cần đọc file này, `handoff_manifest.json`, và `video/remake.md`.",
        "",
        "---",
        "",
        "## 1. Thông Số Cốt Lõi & Bảng Màu (Core DNA & Palette)",
        f"- **Thư mục Artifact nguồn:** `{output_dir}`",
        f"- **Thông số Video gốc:** `{width}x{height}` (`{aspect}`) @ `{fps} fps` · Thời lượng `{duration}s` ({len(shots)} shots)",
        f"- **Phán quyết sản xuất (Verdict):** {summary.get('verdict', 'N/A')}",
    ]
    if rc_block:
        md.append(rc_block.rstrip())
    md.extend(
        [
            f"- **Bảng màu chủ đạo (Hex Palette):** {', '.join(f'`{c}`' for c in all_colors[:8])}",
            f"- **Nhạc nền & Nhịp điệu:** `{audio.get('tempo_bpm', 'N/A')} BPM` · Loudness `{audio.get('rms_dbfs', 'N/A')} dBFS`",
            f"- **Mật độ SFX:** `{len(sfx_events)}` tiếng động ({len(clean_sfx)}/{len(sfx_catalog)} mẫu SFX đạt chuẩn sạch `SNR >= 25dB` để tái sử dụng)",
            "",
            "---",
            "",
            "## 2. Bản Đồ Chuyển Đổi Phân Cảnh Đa Xưởng (Cross-Factory Scene Matrix)",
            "",
            "| Shot | Thời gian (`s`) | Remotion (`@30fps`) | Style & Chuyển cảnh | Bảng màu Shot | Gợi ý Map sang `escbase_template` (`390x693`) | Keyframes & Crops |",
            "|:---:|---|---|---|---|---|---|",
        ]
    )

    for sb in shot_blueprints:
        r30 = sb["remotion_30fps"]
        pal = " ".join(f"`{c}`" for c in sb["palette_hex"][:4])
        f_link = f"[first](file:///{out_posix}/{sb['first_frame']})"
        el_link = f"[elements](file:///{out_posix}/{sb['elements_sheet']})"
        md.append(
            f"| **#{sb['shot_index']:02d}** | `{sb['t0']}–{sb['t1']}s` ({sb['duration_s']}s) | "
            f"`from={r30['from']}, dur={r30['durationInFrames']}` | "
            f"`{sb['scene_style']}` · `{sb['transition_in']}` ({sb['motion_events_count']} events) | "
            f"{pal} | `{sb['escbase_pattern_suggestion']}` | {f_link} · {el_link} |"
        )

    md.extend(
        [
            "",
            "---",
            "",
            "## 3. Kho Tài Nguyên Âm Thanh & Phụ Đề Đã Bóc Tách (Extracted Stems & Clean SFX)",
            "",
            "### 3.1. Audio Stems & Subtitle Tracks",
            f"- 🎵 **Nhạc nền sạch (BGM Bed):** [`stems/music.wav`](file:///{out_posix}/stems/music.wav) (`{output_dir / 'stems' / 'music.wav'}`)",
            f"- 🗣️ **Giọng đọc gốc (Dry Vocals):** [`stems/vocals.wav`](file:///{out_posix}/stems/vocals.wav) *(Chỉ dùng để đo nhịp hoặc chạy Whisper lấy transcript, thay bằng Vclip TTS khi sản xuất mới)*",
            f"- 💥 **Kênh hiệu ứng tổng (Effects Track):** [`stems/effects.wav`](file:///{out_posix}/stems/effects.wav)",
            f"- 📝 **Phụ đề giữ nguyên màu & hiệu ứng (ASS):** [`packaging/overlays.ass`](file:///{out_posix}/packaging/overlays.ass)",
            f"- ⏱️ **Timeline JSON (88 cues + SFX anchors):** [`packaging/timeline.json`](file:///{out_posix}/packaging/timeline.json)",
            "",
            "### 3.2. Danh Mục SFX Rời Đạt Chuẩn Tái Sử Dụng (`sfx/sfx_XX.wav`)",
            "| Mã | File WAV | Loại âm | Số lần gõ | Độ sạch (`SNR`) | Nhịp kích hoạt chính | Mốc giây mẫu (`s`) |",
            "|:---:|---|---|---:|---:|---|---|",
        ]
    )

    for sfx_item in sfx_catalog:
        badge = "✅ Sạch" if sfx_item["clean_for_reuse"] else "⚠️ Dính nền nhẹ"
        f_wav = f"[`{sfx_item['file_rel']}`](file:///{out_posix}/{sfx_item['file_rel']})"
        ts_str = ", ".join(f"{t}s" for t in sfx_item["timestamps_s"][:6])
        md.append(
            f"| **{sfx_item['group']}** | {f_wav} | `{sfx_item['type']}` | {sfx_item['count']} | "
            f"`{sfx_item['snr_db']} dB` ({badge}) | `{sfx_item['primary_trigger']}` | {ts_str} |"
        )

    md.extend(
        [
            "",
            "---",
            "",
            "## 4. Rào Chắn Chống Hỏng Xưởng Đích (5 Mandatory Anti-Collision Guards)",
            "",
            "1. **Cảnh báo OCR Tiếng Việt (`packaging.md` / `subtitles.srt`):**",
            "   - Bộ RapidOCR chỉ dùng để đo **tọa độ khung chữ, mã màu highlight, và mili-giây xuất hiện (`hard_in`, `pop`, `type_on`)**. Không dùng text OCR thô làm lời thoại vì bị rụng dấu tiếng Việt; hãy dùng kịch bản mới hoặc chạy `Faster-Whisper` trên `stems/vocals.wav`.",
            "2. **Rào chắn khi tích hợp vào `G:\\GRAM\\escbase-template3-83.v4.86\\escbase_template`:**",
            "   - Khung chuẩn của `escbase_template` là **`390x693`** với safezone **`padding: 100px 28px 200px`**.",
            "   - **Slide 1 Rule:** Bắt buộc copy nguyên Slide 1 từ 1 trong 4 canonical hero templates (`template/openmontage-github-trending/`, `template/googleaistudio-post-2069450021955592406/`, `template/kimi-moonshot-post-2066467110960959833/`, `template/addyosmani-loop-engineering/`). Áp dụng bảng màu và motion của video mẫu này từ **Slide 2 trở đi**.",
            "   - **BGM Rule:** Giữ nguyên file `preview-assets/bgm/meta.mp3` của starter để vượt qua `validate_slide.py --semantic-report`.",
            "3. **Rào chắn khi tích hợp vào `E:\\A1A\\backvideo` (`vega-video-automate`):**",
            "   - Bọc các lớp cảnh nền trong `<AntiReupGuard>` và đặt Header/Subtitles (`KineticSubtitle.tsx`) ở tầng HUD Safe Area bên ngoài `AntiReupGuard`.",
            "   - Nếu tạo Master Template thứ 15 trong `templates/<id>/`, bắt buộc đăng ký đồng bộ tại `TEMPLATE_COMPOSITION_MAP`, `TEMPLATE_RESOLUTION_MAP` (`agents/render_agent.py`), `tools/job_catalog.py`, và chạy `pytest tests/test_template_packager.py` + `oxlint` đạt 0 lỗi.",
            "",
            "---",
            "",
            "## 5. Lệnh Copy-Paste Giao Việc Cho AI Agent Tại Xưởng Đích",
            "",
            "### 👉 Mẫu 1: Giao cho Agent bên `G:\\GRAM\\escbase-template3-83.v4.86\\escbase_template`",
            "```text",
            f"Đọc file Handoff Blueprint tại {output_dir / 'HANDOFF_BLUEPRINT.md'} và {output_dir / 'video' / 'remake.md'}.",
            "Hãy áp dụng bảng màu, nhịp điệu chuyển cảnh và cấu trúc visual của mẫu này để lên visual-plan.md và dựng deck mới trong slide/<ten_project> (tuân thủ nghiêm ngặt WORKFLOW.md, khung 390x693, Slide 1 canonical hero, và kiểm định pass 100% validate_slide.py --semantic-report).",
            "```",
            "",
            "### 👉 Mẫu 2: Giao cho Agent bên `E:\\A1A\\backvideo`",
            "```text",
            f"Đọc file Handoff Blueprint tại {output_dir / 'HANDOFF_BLUEPRINT.md'}, {output_dir / 'handoff_manifest.json'} và {output_dir / 'video' / 'remake.md'}.",
            f"Sử dụng bảng màu, bố cục các Shot và bộ file âm thanh SFX sạch trong {output_dir / 'sfx'} để dựng Master Template / Job Remotion mới (tích hợp sẵn AntiReupGuard.tsx, KineticSubtitle.tsx, auto-trigger SFX khi nhảy chữ, và đảm bảo pass 100% test suite).",
            "```",
        ]
    )

    blueprint_path = output_dir / "HANDOFF_BLUEPRINT.md"
    blueprint_path.write_text("\n".join(md) + "\n", encoding="utf-8")
    return blueprint_path, manifest_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile Air-Gapped Handoff Blueprint from mreavideo outputs")
    parser.add_argument("output_dir", nargs="?", help="Path to specific output directory (e.g., outputs/r1)")
    parser.add_argument("--all", action="store_true", help="Compile handoff blueprints for all folders in outputs/")
    args = parser.parse_args()

    if args.all:
        outputs_root = ROOT_DIR / "outputs"
        if not outputs_root.exists():
            print("No outputs/ directory found.")
            return 0
        count = 0
        for d in sorted(outputs_root.iterdir()):
            if d.is_dir() and (d / "breakdown.json").exists():
                bp, mf = compile_handoff(d)
                print(f"[OK] Compiled Handoff Blueprint: {bp}")
                count += 1
        print(f"Finished compiling {count} handoff blueprints.")
        return 0
    elif args.output_dir:
        target = Path(args.output_dir).resolve()
        bp, mf = compile_handoff(target)
        print(f"[OK] Handoff Blueprint: file:///{bp.as_posix()}")
        print(f"[OK] Handoff Manifest:  file:///{mf.as_posix()}")
        return 0
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())

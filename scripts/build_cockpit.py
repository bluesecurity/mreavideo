r"""
mreavideo Visual Cockpit & Ecosystem Mindmap Builder (build_cockpit.py)
Generates a 100% standalone, zero-server, offline-ready HTML cockpit:
  F:\Mcode\mreavideo\VISUAL_COCKPIT.html
Embeds all 61 ReelCrew Video Templates (136 local MP4 videos), 4-Factory Routing Matrix,
Analyzed Forensic Lab (outputs/*/handoff_manifest.json with live Audio Stems & SFX player),
and Cross-Project / Cross-Machine Portability Playbook.
"""

import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
from scripts.export_handoff import resolve_reels_catalog

FACTORY_MAP = {
    "animated-explainer": {
        "id": "escbase",
        "name": "escbase_template (HTML/DOM 390x693)",
        "path": r"G:\GRAM\escbase-template3-83.v4.86\escbase_template",
        "badge_cls": "badge-emerald",
        "also_fits": "E:\\A1A\\backvideo (Remotion 1080x1920)",
    },
    "article-to-video": {
        "id": "escbase",
        "name": "escbase_template (HTML/DOM 390x693)",
        "path": r"G:\GRAM\escbase-template3-83.v4.86\escbase_template",
        "badge_cls": "badge-emerald",
        "also_fits": "E:\\A1A\\backvideo (macro-documentary / news-commentary)",
    },
    "elearning": {
        "id": "escbase",
        "name": "escbase_template (HTML/DOM 390x693)",
        "path": r"G:\GRAM\escbase-template3-83.v4.86\escbase_template",
        "badge_cls": "badge-emerald",
        "also_fits": "E:\\A1A\\backvideo (english-learning-split-subtitles)",
    },
    "app-promo": {
        "id": "backvideo",
        "name": "backvideo (Remotion Master Studio)",
        "path": r"E:\A1A\backvideo",
        "badge_cls": "badge-purple",
        "also_fits": "escbase_template (media-first-frame)",
    },
    "product-video": {
        "id": "backvideo",
        "name": "backvideo (Remotion Master Studio)",
        "path": r"E:\A1A\backvideo",
        "badge_cls": "badge-purple",
        "also_fits": "E:\\A1A\\flowtop (tiktok_perfume_reveal / product)",
    },
    "real-estate-promo": {
        "id": "backvideo",
        "name": "backvideo (Remotion Master Studio)",
        "path": r"E:\A1A\backvideo",
        "badge_cls": "badge-purple",
        "also_fits": "escbase_template (route/map scenes)",
    },
    "brand-intro": {
        "id": "backvideo",
        "name": "backvideo (Remotion personal-brand)",
        "path": r"E:\A1A\backvideo",
        "badge_cls": "badge-purple",
        "also_fits": "escbase_template (avatar-person-hero)",
    },
    "motion-graphics": {
        "id": "backvideo",
        "name": "backvideo (Remotion Kinetic Studio)",
        "path": r"E:\A1A\backvideo",
        "badge_cls": "badge-purple",
        "also_fits": "escbase_template (kinetic reveal)",
    },
    "video-ads": {
        "id": "backvideo",
        "name": "backvideo (Remotion Ads Studio)",
        "path": r"E:\A1A\backvideo",
        "badge_cls": "badge-purple",
        "also_fits": "E:\\A1A\\flowtop (1-Touch Ad Templates)",
    },
    "subtitles-captions": {
        "id": "flowtop",
        "name": "flowtop (ASS Auto-Captions + Vclip TTS)",
        "path": r"E:\A1A\flowtop",
        "badge_cls": "badge-cyan",
        "also_fits": "E:\\A1A\\backvideo (KineticSubtitle.tsx)",
    },
    "talking-head": {
        "id": "flowtop",
        "name": "flowtop (Omni V2V + Talking-Head Studio)",
        "path": r"E:\A1A\flowtop",
        "badge_cls": "badge-cyan",
        "also_fits": "E:\\A1A\\backvideo (personal-brand / podcast-quotes)",
    },
    "video-editing": {
        "id": "flowtop",
        "name": "flowtop (FFmpeg Fast-Cut & Subtitles)",
        "path": r"E:\A1A\flowtop",
        "badge_cls": "badge-cyan",
        "also_fits": "E:\\A1A\\backvideo",
    },
    "lecture-video": {
        "id": "flowtop",
        "name": "flowtop (Storyboard + Slide PiP)",
        "path": r"E:\A1A\flowtop",
        "badge_cls": "badge-cyan",
        "also_fits": "escbase_template",
    },
    "video-repurposing": {
        "id": "flowtop",
        "name": "flowtop (Short Highlight & Scheduler)",
        "path": r"E:\A1A\flowtop",
        "badge_cls": "badge-cyan",
        "also_fits": "E:\\A1A\\backvideo",
    },
}


def load_data() -> dict:
    cat_path = resolve_reels_catalog()
    catalog = {"styles": [], "total_styles": 0, "total_unique_videos": 0}
    if cat_path.exists():
        catalog = json.loads(cat_path.read_text(encoding="utf-8"))

    # Load all analyzed outputs
    outputs_root = ROOT_DIR / "outputs"
    analyzed: list[dict] = []
    analyzed_by_style_id: dict[int, list[str]] = {}

    if outputs_root.exists():
        for d in sorted(outputs_root.iterdir()):
            mf_path = d / "handoff_manifest.json"
            if d.is_dir() and mf_path.exists():
                mf = json.loads(mf_path.read_text(encoding="utf-8"))
                mf["output_posix"] = d.as_posix()
                mf["report_url"] = f"file:///{(d / 'report.html').as_posix()}"
                mf["blueprint_url"] = f"file:///{(d / 'HANDOFF_BLUEPRINT.md').as_posix()}"
                mf["videomd_url"] = f"file:///{(d / 'VIDEO.md').as_posix()}"
                mf["remake_url"] = f"file:///{(d / 'video' / 'remake.md').as_posix()}"
                mf["storyboard_url"] = f"file:///{(d / 'storyboard.jpg').as_posix()}"
                analyzed.append(mf)
                rc = mf.get("reelcrew_catalog_match")
                if rc and isinstance(rc.get("style"), dict):
                    sid = rc["style"].get("style_id")
                    if sid:
                        analyzed_by_style_id.setdefault(int(sid), []).append(mf["video_name"])

    enriched_styles = []
    for st in catalog.get("styles", []):
        sk_full = st.get("skill", "")
        sk_root = sk_full.split("·")[0].strip() if "·" in sk_full else sk_full.strip()
        f_info = FACTORY_MAP.get(
            sk_root,
            {
                "id": "backvideo",
                "name": "backvideo (Remotion Studio)",
                "path": r"E:\A1A\backvideo",
                "badge_cls": "badge-purple",
                "also_fits": "escbase_template",
            },
        )
        vids = []
        for v in st.get("local_videos", []):
            lp = Path(v.get("local_path", ""))
            vids.append(
                {
                    "filename": v.get("filename"),
                    "local_path": str(lp),
                    "file_url": f"file:///{lp.as_posix()}",
                    "size_mb": round((v.get("size_bytes") or 0) / (1024 * 1024), 2),
                }
            )
        sid = int(st.get("style_id", 0))
        enriched_styles.append(
            {
                "style_id": sid,
                "title": st.get("title", ""),
                "category": st.get("category", ""),
                "skill": sk_full,
                "skill_root": sk_root,
                "description": st.get("description", ""),
                "factory": f_info,
                "videos": vids,
                "analyzed_outputs": analyzed_by_style_id.get(sid, []),
            }
        )

    return {
        "workspace_root": str(ROOT_DIR),
        "workspace_posix": ROOT_DIR.as_posix(),
        "reels_dir": str(cat_path.parent),
        "total_styles": len(enriched_styles),
        "total_videos": sum(len(s["videos"]) for s in enriched_styles),
        "total_analyzed": len(analyzed),
        "styles": enriched_styles,
        "analyzed": analyzed,
    }


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>mreavideo — Visual Cockpit, 61 ReelCrew Templates & Cross-Factory Handoff Hub</title>
  <style>
    :root {
      --bg-base: #06090e;
      --bg-card: #0d131c;
      --bg-panel: #131c29;
      --bg-elevated: #1a2636;
      --border: rgba(148, 163, 184, 0.16);
      --border-hi: rgba(45, 212, 191, 0.45);
      --text-main: #f1f5f9;
      --text-muted: #94a3b8;
      --accent-teal: #2dd4bf;
      --accent-cyan: #38bdf8;
      --accent-purple: #c084fc;
      --accent-emerald: #34d399;
      --accent-amber: #fbbf24;
      --accent-rose: #fb7185;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: "Segoe UI", -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
      background:
        radial-gradient(circle at 12% 10%, rgba(45, 212, 191, 0.08), transparent 38%),
        radial-gradient(circle at 88% 82%, rgba(56, 189, 248, 0.07), transparent 40%),
        var(--bg-base);
      color: var(--text-main);
      min-height: 100vh;
      padding: 20px 24px 48px;
      line-height: 1.5;
    }
    .container { max-width: 1620px; margin: 0 auto; display: flex; flex-direction: column; gap: 18px; }
    .topbar {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px 22px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 16px;
    }
    .brand h1 { font-size: 21px; font-weight: 800; letter-spacing: -0.02em; color: #fff; display: flex; align-items: center; gap: 10px; }
    .brand p { font-size: 13px; color: var(--text-muted); margin-top: 3px; }
    .kpis { display: flex; gap: 10px; flex-wrap: wrap; }
    .kpi {
      background: var(--bg-panel);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 8px 14px;
      text-align: center;
      min-width: 110px;
    }
    .kpi .v { font-size: 19px; font-weight: 800; color: var(--accent-teal); }
    .kpi .l { font-size: 11px; color: var(--text-muted); text-transform: uppercase; letter-spacing: 0.04em; }

    .tabs { display: flex; gap: 8px; flex-wrap: wrap; }
    .tab-btn {
      background: var(--bg-card);
      color: var(--text-muted);
      border: 1px solid var(--border);
      padding: 10px 16px;
      border-radius: 10px;
      font-size: 13.5px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .tab-btn:hover { color: #fff; border-color: var(--border-hi); }
    .tab-btn.active {
      background: linear-gradient(135deg, rgba(45, 212, 191, 0.18), rgba(56, 189, 248, 0.12));
      color: #fff;
      border-color: var(--accent-teal);
      box-shadow: 0 0 18px rgba(45, 212, 191, 0.14);
    }

    .tab-pane { display: none; flex-direction: column; gap: 18px; }
    .tab-pane.active { display: flex; }

    .panel {
      background: var(--bg-card);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 20px;
    }
    .panel h2 { font-size: 17px; font-weight: 800; margin-bottom: 6px; color: #fff; }
    .panel p.sub { font-size: 13px; color: var(--text-muted); margin-bottom: 16px; }

    /* Mindmap / Workflow diagram */
    .flow-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(340px, 1fr));
      gap: 16px;
    }
    .flow-stage {
      background: var(--bg-panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .flow-stage .st-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      border-bottom: 1px solid var(--border);
      padding-bottom: 8px;
    }
    .flow-stage .st-title { font-size: 15px; font-weight: 800; color: #fff; }
    .flow-stage ul { list-style: none; display: flex; flex-direction: column; gap: 7px; font-size: 13px; color: var(--text-main); }
    .flow-stage li { background: rgba(255,255,255,0.03); padding: 8px 10px; border-radius: 8px; border-left: 3px solid var(--accent-teal); }

    /* Badges */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 3px 9px;
      border-radius: 999px;
      font-size: 11.5px;
      font-weight: 700;
    }
    .badge-emerald { background: rgba(52, 211, 153, 0.14); color: #6ee7b7; border: 1px solid rgba(52, 211, 153, 0.35); }
    .badge-purple { background: rgba(192, 132, 252, 0.14); color: #d8b4fe; border: 1px solid rgba(192, 132, 252, 0.35); }
    .badge-cyan { background: rgba(56, 189, 248, 0.14); color: #7dd3fc; border: 1px solid rgba(56, 189, 248, 0.35); }
    .badge-amber { background: rgba(251, 191, 36, 0.15); color: #fde68a; border: 1px solid rgba(251, 191, 36, 0.4); }
    .badge-rose { background: rgba(251, 113, 133, 0.15); color: #fda4af; border: 1px solid rgba(251, 113, 133, 0.4); }

    /* Filters */
    .filter-bar {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      align-items: center;
      background: var(--bg-panel);
      padding: 12px 14px;
      border-radius: 12px;
      border: 1px solid var(--border);
    }
    .filter-bar input, .filter-bar select {
      background: var(--bg-card);
      color: var(--text-main);
      border: 1px solid var(--border);
      padding: 8px 12px;
      border-radius: 8px;
      font-size: 13px;
    }
    .filter-bar input { min-width: 260px; flex: 1; }
    .pill-btn {
      background: var(--bg-card);
      color: var(--text-muted);
      border: 1px solid var(--border);
      padding: 7px 12px;
      border-radius: 8px;
      font-size: 12.5px;
      font-weight: 700;
      cursor: pointer;
    }
    .pill-btn.active, .pill-btn:hover {
      color: #fff;
      border-color: var(--accent-teal);
      background: rgba(45, 212, 191, 0.13);
    }

    /* 61 Templates Grid */
    .tpl-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(370px, 1fr));
      gap: 16px;
    }
    .tpl-card {
      background: var(--bg-panel);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 15px;
      display: flex;
      flex-direction: column;
      gap: 10px;
      transition: border-color 0.15s ease;
    }
    .tpl-card:hover { border-color: var(--border-hi); }
    .tpl-top { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; }
    .tpl-id { font-size: 12px; font-weight: 800; color: var(--accent-teal); font-family: Consolas, monospace; }
    .tpl-title { font-size: 15px; font-weight: 800; color: #fff; line-height: 1.35; }
    .tpl-skill { font-family: Consolas, monospace; font-size: 12px; color: var(--accent-cyan); }
    .tpl-desc { font-size: 12.5px; color: var(--text-muted); }

    .video-box {
      background: #000;
      border-radius: 10px;
      overflow: hidden;
      border: 1px solid var(--border);
      display: flex;
      flex-direction: column;
    }
    .video-box video {
      width: 100%;
      max-height: 280px;
      background: #000;
      display: block;
    }
    .video-tabs {
      display: flex;
      gap: 6px;
      padding: 7px 10px;
      background: rgba(15, 23, 42, 0.9);
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
    }
    .vid-tab-btn {
      background: var(--bg-elevated);
      color: var(--text-muted);
      border: 1px solid var(--border);
      padding: 3px 9px;
      border-radius: 6px;
      font-size: 11.5px;
      font-weight: 700;
      cursor: pointer;
    }
    .vid-tab-btn.active {
      background: var(--accent-teal);
      color: #041311;
      border-color: var(--accent-teal);
    }

    .action-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: auto; pt: 4px; }
    .act-btn {
      flex: 1;
      background: var(--bg-card);
      color: var(--text-main);
      border: 1px solid var(--border);
      padding: 7px 10px;
      border-radius: 8px;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      text-align: center;
      text-decoration: none;
      transition: all 0.15s ease;
    }
    .act-btn:hover { border-color: var(--accent-teal); color: var(--accent-teal); }
    .act-btn.primary {
      background: rgba(45, 212, 191, 0.14);
      border-color: rgba(45, 212, 191, 0.4);
      color: #5eead4;
    }

    /* Analyzed Lab */
    .lab-card {
      background: var(--bg-panel);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }
    .swatches { display: flex; gap: 8px; flex-wrap: wrap; align-items: center; }
    .swatch {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 8px;
      background: var(--bg-card);
      border: 1px solid var(--border);
      font-family: Consolas, monospace;
      font-size: 12px;
      cursor: pointer;
    }
    .swatch-dot { width: 14px; height: 14px; border-radius: 4px; border: 1px solid rgba(255,255,255,0.25); }
    .sfx-grid { display: flex; gap: 7px; flex-wrap: wrap; }
    .sfx-chip {
      background: var(--bg-card);
      border: 1px solid var(--border);
      color: var(--text-main);
      padding: 5px 10px;
      border-radius: 8px;
      font-size: 12px;
      cursor: pointer;
      display: inline-flex;
      align-items: center;
      gap: 6px;
    }
    .sfx-chip:hover { border-color: var(--accent-teal); color: var(--accent-teal); }

    table.shot-tbl { width: 100%; border-collapse: collapse; font-size: 12.5px; }
    table.shot-tbl th, table.shot-tbl td {
      border: 1px solid var(--border);
      padding: 8px 10px;
      text-align: left;
    }
    table.shot-tbl th { background: var(--bg-card); color: var(--text-muted); }

    pre.codebox {
      background: #05080c;
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 14px;
      font-family: Consolas, monospace;
      font-size: 12.5px;
      color: #a5f3fc;
      overflow-x: auto;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .toast {
      position: fixed;
      bottom: 22px;
      right: 22px;
      background: #0f766e;
      color: #fff;
      padding: 12px 18px;
      border-radius: 10px;
      font-size: 13px;
      font-weight: 700;
      box-shadow: 0 10px 25px rgba(0,0,0,0.45);
      display: none;
      z-index: 9999;
    }
  </style>
</head>
<body>
  <div class="container">
    <header class="topbar">
      <div class="brand">
        <h1>🎬 mreavideo — Trung Tâm Điều Phối Giải Phẫu Video & Kho 61 Templates ReelCrew</h1>
        <p>Air-Gapped Forensic Engine (`F:\Mcode\mreavideo`) ➔ Cung cấp Blueprint, BGM, 19 SFX & Scene Matrix cho 3 Xưởng (`escbase_template` · `backvideo` · `flowtop`)</p>
      </div>
      <div class="kpis" id="kpi-container"></div>
    </header>

    <nav class="tabs">
      <button class="tab-btn active" onclick="switchTab('tab-mindmap', this)">🗺️ 1. Bản Đồ Mindmap & Luồng 4 Xưởng</button>
      <button class="tab-btn" onclick="switchTab('tab-templates', this)">🎬 2. Thư Viện 61 Video Templates (136 Videos Live)</button>
      <button class="tab-btn" onclick="switchTab('tab-analyzed', this)">🔬 3. Phòng Lab Video Đã Mổ (Audio/SFX & Blueprint)</button>
      <button class="tab-btn" onclick="switchTab('tab-portable', this)">🧳 4. Cẩm Nang Gọi Liên Dự Án & Di Trú Sang Máy Khác</button>
    </nav>

    <!-- TAB 1: MINDMAP & WORKFLOW -->
    <section id="tab-mindmap" class="tab-pane active">
      <div class="panel">
        <h2>🧭 Toàn Cảnh Kiến Trúc Liên Xưởng: Từ Video Mẫu Đối Thủ ➔ Sản Xuất Hàng Loạt</h2>
        <p class="sub">Bức tranh 4 trạm giúp Đại Ka nhìn rõ từng dự án đang nắm giữ vai trò gì và nối với nhau qua gói <code>HANDOFF_BLUEPRINT.md</code> như thế nào.</p>
        <div class="flow-grid">
          <div class="flow-stage">
            <div class="st-head">
              <span class="st-title">1️⃣ KHO MẪU REELCREW</span>
              <span class="badge badge-amber">F:\mworkk\videosample\reels</span>
            </div>
            <ul>
              <li><strong>61 Video Templates (Styles)</strong> chia thành <strong>5 Nhóm Nội Dung</strong> và <strong>14 Bộ Skill</strong>.</li>
              <li><strong>136 Video Mẫu (.mp4)</strong> đã tải về local 100%, xem trực tiếp ở Tab 2 không cần mạng.</li>
              <li>Mỗi mẫu có mã <code>skill · look</code> rõ ràng (vd: <code>animated-explainer · tech-brief</code>, <code>motion-graphics · voice-kinetic</code>).</li>
              <li>Index chuẩn hóa tại <code>CATALOG.md</code> và <code>catalog.json</code>.</li>
            </ul>
          </div>

          <div class="flow-stage">
            <div class="st-head">
              <span class="st-title">2️⃣ TRẠM GIẢI PHẪU MREAVIDEO</span>
              <span class="badge badge-cyan">F:\Mcode\mreavideo</span>
            </div>
            <ul>
              <li><strong>Lệnh chạy:</strong> <code>.venv\Scripts\python.exe run.py &lt;path-to-video.mp4&gt;</code></li>
              <li><strong>OpenCV + FFmpeg:</strong> Tự động cắt Shots, trích xuất keyframes & element crops (<code>shots/shot_XXX_el_NN.jpg</code>), đo bảng màu Hex và quỹ đạo chuyển động.</li>
              <li><strong>ONNX Audio Separation:</strong> Tách rời giọng đọc (<code>stems/vocals.wav</code>), nhạc nền sạch (<code>stems/music.wav</code>) và cắt riêng từng tiếng động SFX (<code>sfx/sfx_01..19.wav</code>).</li>
              <li><strong>RapidOCR 3:</strong> Bóc tách timeline phụ đề (<code>packaging/overlays.ass</code> & <code>timeline.json</code>).</li>
            </ul>
          </div>

          <div class="flow-stage">
            <div class="st-head">
              <span class="st-title">3️⃣ GÓI BÀN GIAO AIR-GAPPED</span>
              <span class="badge badge-emerald">outputs\&lt;video&gt;\HANDOFF_BLUEPRINT.md</span>
            </div>
            <ul>
              <li>Do <code>scripts/export_handoff.py</code> tự động biên dịch ngay sau khi mổ video.</li>
              <li><strong>Chống tràn token:</strong> Rút gọn file <code>breakdown.json</code> (83,000+ tokens) xuống bản thiết kế sạch chỉ ~1,500 tokens.</li>
              <li><strong>Khớp SHA256 tự động:</strong> Nhận diện ngay video vừa mổ thuộc Style nào trong 61 mẫu ReelCrew.</li>
              <li><strong>Đo độ sạch SFX (SNR dB):</strong> Lọc sẵn các file <code>ding/click/pop/whoosh</code> đạt <code>SNR &gt;= 25dB</code>.</li>
            </ul>
          </div>

          <div class="flow-stage">
            <div class="st-head">
              <span class="st-title">4️⃣ BA XƯỞNG SẢN XUẤT ĐÍCH</span>
              <span class="badge badge-purple">Air-Gapped Consumers</span>
            </div>
            <ul>
              <li><strong>🟢 Xưởng 1 — <code>escbase_template</code> (33 Styles):</strong> Dựng Slide HTML/DOM <code>390x693</code> (18 mẫu <code>visual-pattern-gallery</code>). Chuyên trị dòng Explainer, Tech-Brief, Sơ đồ, Paper, E-learning.</li>
              <li><strong>🟣 Xưởng 2 — <code>E:\A1A\backvideo</code> (15 Styles):</strong> Dựng Remotion React <code>1080x1920</code> (14 Master Templates + <code>AntiReupGuard.tsx</code> + <code>anti_reup_cleaner.py</code>). Chuyên trị Product, BĐS, Kinetic Ads, Showreel.</li>
              <li><strong>🔵 Xưởng 3 — <code>E:\A1A\flowtop</code> (13 Styles):</strong> Chuyên trị AI Video (Veo/Omni V2V), Vclip TTS 23-key Pool, Phụ đề nhảy chữ ASS, Talking-Head & Cắt Short hàng loạt.</li>
            </ul>
          </div>
        </div>
      </div>

      <div class="panel">
        <h2>📊 Bảng Phân Luồng 14 Nhóm Skill ReelCrew Vào 3 Xưởng Của Đại Ka</h2>
        <p class="sub">Bấm vào bất kỳ nhóm Skill nào bên dưới để nhảy sang Tab 2 và lọc đúng các video mẫu của nhóm đó.</p>
        <div id="skill-matrix-container"></div>
      </div>
    </section>

    <!-- TAB 2: 61 TEMPLATES GALLERY -->
    <section id="tab-templates" class="tab-pane">
      <div class="panel">
        <h2>🎬 Thư Viện 61 Video Templates & Trình Phát Video Trực Tiếp (136 Videos)</h2>
        <p class="sub">Xem trực tiếp video mẫu từ ổ cứng, lọc theo Xưởng đích hoặc Nhóm Skill, và bấm 1 nút để copy lệnh Giải Phẫu hoặc lệnh Giao Việc sang Xưởng đích.</p>
        <div class="filter-bar">
          <input type="text" id="search-input" placeholder="🔍 Tìm theo tên style, mã skill (vd: tech-brief, isometric, bđs, karaoke, luật, excel)..." oninput="renderTemplates()" />
          <select id="category-select" onchange="renderTemplates()">
            <option value="ALL">Tất cả 5 Nhóm Nội Dung</option>
          </select>
          <select id="skill-select" onchange="renderTemplates()">
            <option value="ALL">Tất cả 14 Nhóm Skill</option>
          </select>
          <button class="pill-btn active" data-fac="ALL" onclick="setFactoryFilter('ALL', this)">Tất cả (61)</button>
          <button class="pill-btn" data-fac="escbase" onclick="setFactoryFilter('escbase', this)">🟢 escbase_template (33)</button>
          <button class="pill-btn" data-fac="backvideo" onclick="setFactoryFilter('backvideo', this)">🟣 backvideo (15)</button>
          <button class="pill-btn" data-fac="flowtop" onclick="setFactoryFilter('flowtop', this)">🔵 flowtop (13)</button>
        </div>
        <div id="templates-count" style="margin: 12px 0; font-size: 13px; color: var(--text-muted);"></div>
        <div class="tpl-grid" id="templates-grid"></div>
      </div>
    </section>

    <!-- TAB 3: ANALYZED FORENSIC LAB -->
    <section id="tab-analyzed" class="tab-pane">
      <div class="panel">
        <h2>🔬 Phòng Lab Các Video Đã Giải Phẫu (`F:\Mcode\mreavideo\outputs\`)</h2>
        <p class="sub">Nghe thử trực tiếp các kênh âm thanh đã bóc tách (<code>music.wav</code>, <code>vocals.wav</code>, 19 tiếng <code>sfx_*.wav</code>), xem bảng màu Hex, cấu trúc Shots và copy lệnh Handoff sang <code>escbase_template</code> hoặc <code>backvideo</code>.</p>
        <div id="analyzed-container" style="display: flex; flex-direction: column; gap: 18px;"></div>
      </div>
    </section>

    <!-- TAB 4: PORTABILITY & CROSS-PROJECT PLAYBOOK -->
    <section id="tab-portable" class="tab-pane">
      <div class="panel">
        <h2>🧳 Cẩm Nang Triển Khai Tinh Hoa: Gọi Từ Dự Án Khác & Mang Sang Máy Tính Khác</h2>
        <p class="sub">Hướng dẫn thực chiến 3 kịch bản để Đại Ka sử dụng bộ năng lực này ở bất kỳ đâu mà không bao giờ làm hỏng dự án đích.</p>

        <div class="flow-grid">
          <div class="flow-stage">
            <div class="st-head">
              <span class="st-title">Kịch Bản A: Gọi Từ Project Khác Trên Cùng Máy Này</span>
              <span class="badge badge-emerald">0 Copy · Dùng Ngay</span>
            </div>
            <p style="font-size: 13px; color: var(--text-muted);">
              Skill <code>vrea-video-forensics</code> đã được đồng bộ sẵn ở Global Scope (<code>C:\Users\User\.gemini\config\skills\vrea-video-forensics\SKILL.md</code>). Khi Đại Ka đang mở <code>escbase_template</code>, <code>E:\A1A\backvideo</code> hoặc <code>E:\A1A\flowtop</code>, chỉ cần dán câu lệnh sau cho AI Agent:
            </p>
            <pre class="codebox" id="cmd-cross-proj">Đọc file Handoff Blueprint tại F:\Mcode\mreavideo\outputs\r1\HANDOFF_BLUEPRINT.md và F:\Mcode\mreavideo\outputs\r1\video\remake.md. Hãy áp dụng bảng màu, nhịp chuyển cảnh và bộ file âm thanh SFX sạch trong F:\Mcode\mreavideo\outputs\r1\sfx để dựng video/template theo đúng chuẩn của repo hiện tại.</pre>
            <button class="act-btn primary" onclick="copyText(document.getElementById('cmd-cross-proj').innerText)">📋 Copy Lệnh Giao Việc Liên Project</button>
          </div>

          <div class="flow-stage">
            <div class="st-head">
              <span class="st-title">Kịch Bản B: Copy Gói Tinh Hoa Nhẹ Sang Máy Khác</span>
              <span class="badge badge-amber">Chỉ Dựng Video · Không Cần Cài Python/ONNX</span>
            </div>
            <p style="font-size: 13px; color: var(--text-muted);">
              Nếu máy tính kia chỉ chạy xưởng <code>escbase_template</code> hoặc <code>backvideo</code> để render video mà không cần chạy AI mổ video mới, Đại Ka chỉ cần copy 2 thư mục nhẹ này:
            </p>
            <ul>
              <li><strong>1. Thư mục kết quả đã mổ:</strong> <code>F:\Mcode\mreavideo\outputs\&lt;ten_video&gt;\</code> (chứa sẵn <code>HANDOFF_BLUEPRINT.md</code>, <code>stems/music.wav</code>, <code>sfx/sfx_01..19.wav</code>, <code>shots/</code>).</li>
              <li><strong>2. File tổng đài này + Kho mẫu:</strong> <code>F:\Mcode\mreavideo\VISUAL_COCKPIT.html</code> và <code>F:\mworkk\videosample\reels\</code>.</li>
            </ul>
          </div>

          <div class="flow-stage">
            <div class="st-head">
              <span class="st-title">Kịch Bản C: Di Trú Toàn Bộ Trạm Giải Phẫu Sang Máy Mới</span>
              <span class="badge badge-cyan">Full Engine + 216MB ONNX + Patch Guard</span>
            </div>
            <p style="font-size: 13px; color: var(--text-muted);">
              Khi clone hoặc copy cả repo <code>mreavideo</code> sang máy tính mới (ổ đĩa khác như <code>D:\</code> hoặc <code>C:\</code>), chạy đúng 1 lệnh chuẩn hóa dưới đây để tự động vá lỗi RapidOCR Python 3.13 (<code>h &lt; 0.08</code>), kiểm tra 216MB model ONNX và tự cập nhật đường dẫn trong Global Skill:
            </p>
            <pre class="codebox" id="cmd-portable-setup"># 1. Copy kèm 2 file ONNX (~216MB) để không phải tải lại:
#    C:\Users\User\.cache\rea-video\models\UVR-MDX-NET-Inst_HQ_3.onnx
#    C:\Users\User\.cache\rea-video\models\bandit-v2-multi.onnx

# 2. Chạy trình tự động cấu hình & vá Submodule:
.\.venv\Scripts\python.exe scripts\portable_setup.py

# 3. Chạy kiểm định cơ học 54 tests (Exit Code 0):
.\.venv\Scripts\python.exe scripts\check.py</pre>
            <button class="act-btn primary" onclick="copyText(document.getElementById('cmd-portable-setup').innerText)">📋 Copy Quy Trình Setup Máy Mới</button>
          </div>
        </div>
      </div>
    </section>
  </div>

  <div class="toast" id="toast">Đã copy vào Clipboard!</div>
  <audio id="global-audio-player" style="display:none;"></audio>

  <script>
    const COCKPIT_DATA = __COCKPIT_JSON_PAYLOAD__;
    let activeFactoryFilter = 'ALL';

    function showToast(msg) {
      const t = document.getElementById('toast');
      t.innerText = msg;
      t.style.display = 'block';
      clearTimeout(window.__toastTimer);
      window.__toastTimer = setTimeout(() => { t.style.display = 'none'; }, 2400);
    }

    function copyText(txt) {
      navigator.clipboard.writeText(txt).then(() => {
        showToast('✅ Đã copy lệnh vào Clipboard!');
      });
    }

    function playAudioUrl(url, label) {
      const player = document.getElementById('global-audio-player');
      player.src = url;
      player.play();
      showToast('🔊 Đang phát: ' + label);
    }

    function switchTab(tabId, btnEl) {
      document.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      if (btnEl) btnEl.classList.add('active');
    }

    function jumpToSkill(skillRoot) {
      const btns = document.querySelectorAll('.tab-btn');
      switchTab('tab-templates', btns[1]);
      document.getElementById('skill-select').value = skillRoot;
      renderTemplates();
    }

    function setFactoryFilter(fac, btnEl) {
      activeFactoryFilter = fac;
      document.querySelectorAll('.pill-btn').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');
      renderTemplates();
    }

    function switchCardVideo(styleId, vidIdx, btnEl) {
      const st = COCKPIT_DATA.styles.find(s => s.style_id === styleId);
      if (!st || !st.videos[vidIdx]) return;
      const v = st.videos[vidIdx];
      const videoEl = document.getElementById('vid-player-' + styleId);
      const fnameEl = document.getElementById('vid-fname-' + styleId);
      if (videoEl) {
        videoEl.src = v.file_url;
        videoEl.dataset.localPath = v.local_path;
        videoEl.play();
      }
      if (fnameEl) {
        fnameEl.innerText = v.filename + ' (' + v.size_mb + ' MB)';
      }
      const parent = btnEl.parentElement;
      parent.querySelectorAll('.vid-tab-btn').forEach(b => b.classList.remove('active'));
      btnEl.classList.add('active');
    }

    function copyDecomposeCmd(styleId) {
      const videoEl = document.getElementById('vid-player-' + styleId);
      const localPath = videoEl ? videoEl.dataset.localPath : '';
      const cmd = `${COCKPIT_DATA.workspace_root}\\.venv\\Scripts\\python.exe ${COCKPIT_DATA.workspace_root}\\run.py "${localPath}"`;
      copyText(cmd);
    }

    function copyFactoryPrompt(styleId) {
      const st = COCKPIT_DATA.styles.find(s => s.style_id === styleId);
      const videoEl = document.getElementById('vid-player-' + styleId);
      const localPath = videoEl ? videoEl.dataset.localPath : (st.videos[0] ? st.videos[0].local_path : '');
      const stem = localPath.split('\\').pop().replace(/\.mp4$/i, '');
      const analyzedStem = (st.analyzed_outputs && st.analyzed_outputs.length > 0) ? st.analyzed_outputs[0] : stem;
      const outDir = `${COCKPIT_DATA.workspace_root}\\outputs\\${analyzedStem}`;

      let prompt = '';
      if (st.analyzed_outputs && st.analyzed_outputs.length > 0) {
        prompt = `[Style #${st.style_id}: ${st.title} (${st.skill})]\nĐọc file Handoff Blueprint đã giải phẫu tại ${outDir}\\HANDOFF_BLUEPRINT.md và ${outDir}\\video\\remake.md.\nHãy áp dụng bảng màu Hex, cấu trúc phân cảnh và kho SFX sạch tại ${outDir}\\sfx để triển khai template này trong xưởng (${st.factory.name}) đảm bảo pass 100% kiểm định cơ học.`;
      } else {
        prompt = `[Style #${st.style_id}: ${st.title} (${st.skill})]\nBước 1: Chạy lệnh giải phẫu video mẫu bằng skill /vrea-video-forensics:\n${COCKPIT_DATA.workspace_root}\\.venv\\Scripts\\python.exe ${COCKPIT_DATA.workspace_root}\\run.py "${localPath}"\nBước 2: Đọc file ${outDir}\\HANDOFF_BLUEPRINT.md và ${outDir}\\video\\remake.md để tích hợp style "${st.title}" vào xưởng (${st.factory.name}) đảm bảo pass 100% kiểm định cơ học.`;
      }
      copyText(prompt);
    }

    function renderKpisAndMatrix() {
      const kpiBox = document.getElementById('kpi-container');
      kpiBox.innerHTML = `
        <div class="kpi"><div class="v">${COCKPIT_DATA.total_styles}</div><div class="l">Video Templates</div></div>
        <div class="kpi"><div class="v">${COCKPIT_DATA.total_videos}</div><div class="l">Local MP4 Samples</div></div>
        <div class="kpi"><div class="v">14</div><div class="l">Skill Families</div></div>
        <div class="kpi"><div class="v">${COCKPIT_DATA.total_analyzed}</div><div class="l">Đã Giải Phẫu</div></div>
      `;

      // Populate filters
      const cats = Array.from(new Set(COCKPIT_DATA.styles.map(s => s.category))).filter(Boolean);
      const catSel = document.getElementById('category-select');
      cats.forEach(c => {
        const opt = document.createElement('option');
        opt.value = c;
        opt.innerText = c;
        catSel.appendChild(opt);
      });

      const skills = Array.from(new Set(COCKPIT_DATA.styles.map(s => s.skill_root))).filter(Boolean);
      const skSel = document.getElementById('skill-select');
      skills.forEach(sk => {
        const count = COCKPIT_DATA.styles.filter(s => s.skill_root === sk).length;
        const opt = document.createElement('option');
        opt.value = sk;
        opt.innerText = `${sk} (${count} templates)`;
        skSel.appendChild(opt);
      });

      // Render skill matrix table in Tab 1
      let rows = skills.map(sk => {
        const list = COCKPIT_DATA.styles.filter(s => s.skill_root === sk);
        const vidsCount = list.reduce((acc, x) => acc + x.videos.length, 0);
        const fac = list[0].factory;
        const looks = list.map(x => {
          const lk = x.skill.includes('·') ? x.skill.split('·')[1].trim() : x.skill;
          const ana = (x.analyzed_outputs && x.analyzed_outputs.length) ? ` ✅(${x.analyzed_outputs.join(',')})` : '';
          return `<code>#${x.style_id} ${lk}${ana}</code>`;
        }).join(' · ');
        return `
          <tr>
            <td><strong style="color:var(--accent-cyan); cursor:pointer;" onclick="jumpToSkill('${sk}')">${sk} ↗</strong></td>
            <td><strong>${list.length}</strong> templates (${vidsCount} videos)</td>
            <td><span class="badge ${fac.badge_cls}">${fac.name}</span></td>
            <td style="font-size:12px; color:var(--text-muted);">${fac.also_fits}</td>
            <td style="line-height:1.7;">${looks}</td>
          </tr>
        `;
      }).join('');

      document.getElementById('skill-matrix-container').innerHTML = `
        <table class="shot-tbl">
          <thead>
            <tr>
              <th>Bộ Skill (Skill Family)</th>
              <th>Số Lượng</th>
              <th>Xưởng Đích Khuyên Dùng</th>
              <th>Xưởng Phối Hợp</th>
              <th>Danh Sách Các Kiểu Hình (Looks) — Bấm vào tên Skill để xem Video</th>
            </tr>
          </thead>
          <tbody>${rows}</tbody>
        </table>
      `;
    }

    function renderTemplates() {
      const q = (document.getElementById('search-input').value || '').toLowerCase().trim();
      const cat = document.getElementById('category-select').value;
      const sk = document.getElementById('skill-select').value;

      const filtered = COCKPIT_DATA.styles.filter(st => {
        if (activeFactoryFilter !== 'ALL' && st.factory.id !== activeFactoryFilter) return false;
        if (cat !== 'ALL' && st.category !== cat) return false;
        if (sk !== 'ALL' && st.skill_root !== sk) return false;
        if (q) {
          const hay = `${st.style_id} ${st.title} ${st.skill} ${st.category} ${st.description} ${st.videos.map(v => v.filename).join(' ')}`.toLowerCase();
          if (!hay.includes(q)) return false;
        }
        return true;
      });

      const totalVids = filtered.reduce((acc, s) => acc + s.videos.length, 0);
      document.getElementById('templates-count').innerText = `Đang hiển thị ${filtered.length}/${COCKPIT_DATA.total_styles} Video Templates (${totalVids} video mẫu local).`;

      const grid = document.getElementById('templates-grid');
      grid.innerHTML = filtered.map(st => {
        const v0 = st.videos[0] || { filename: 'N/A', file_url: '', local_path: '', size_mb: 0 };
        const tabBtns = st.videos.map((v, idx) => `
          <button class="vid-tab-btn ${idx === 0 ? 'active' : ''}" onclick="switchCardVideo(${st.style_id}, ${idx}, this)">Video ${idx + 1}</button>
        `).join('');

        const analyzedBadge = (st.analyzed_outputs && st.analyzed_outputs.length > 0)
          ? `<span class="badge badge-amber" style="cursor:pointer;" onclick="switchTab('tab-analyzed', document.querySelectorAll('.tab-btn')[2])">✅ Đã mổ: ${st.analyzed_outputs.join(', ')}</span>`
          : '';

        return `
          <div class="tpl-card">
            <div class="tpl-top">
              <span class="tpl-id">STYLE #${String(st.style_id).padStart(2, '0')} · ${st.category}</span>
              <span class="badge ${st.factory.badge_cls}">${st.factory.name.split(' ')[0]}</span>
            </div>
            <div class="tpl-title">${st.title}</div>
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:6px;">
              <span class="tpl-skill">${st.skill}</span>
              ${analyzedBadge}
            </div>
            <div class="tpl-desc">${st.description}</div>

            <div class="video-box">
              <video id="vid-player-${st.style_id}" src="${v0.file_url}" data-local-path="${v0.local_path}" controls preload="metadata"></video>
              <div class="video-tabs">
                <div style="display:flex; gap:5px; flex-wrap:wrap;">${tabBtns}</div>
                <span id="vid-fname-${st.style_id}" style="font-size:11px; color:var(--text-muted); font-family:Consolas,monospace;">${v0.filename} (${v0.size_mb} MB)</span>
              </div>
            </div>

            <div class="action-row">
              <button class="act-btn" onclick="copyDecomposeCmd(${st.style_id})">🔬 Copy Lệnh Mổ Video</button>
              <button class="act-btn primary" onclick="copyFactoryPrompt(${st.style_id})">🚀 Copy Prompt Dựng Template</button>
            </div>
          </div>
        `;
      }).join('');
    }

    function renderAnalyzedLab() {
      const box = document.getElementById('analyzed-container');
      box.innerHTML = COCKPIT_DATA.analyzed.map(item => {
        const rc = item.reelcrew_catalog_match;
        const rcBadge = rc && rc.style
          ? `<span class="badge badge-amber">Khớp SHA256: Style #${rc.style.style_id} — ${rc.style.title} (${rc.style.skill})</span>`
          : `<span class="badge badge-cyan">Custom Sample Video</span>`;

        const swatches = (item.global_palette_hex || []).map(hex => `
          <span class="swatch" onclick="copyText('${hex}')" title="Click để copy mã màu ${hex}">
            <span class="swatch-dot" style="background:${hex};"></span>${hex}
          </span>
        `).join('');

        const sfxChips = (item.sfx_catalog || []).map(sfx => {
          const wavUrl = `file:///${item.output_posix}/${sfx.file_rel}`;
          return `
            <button class="sfx-chip" onclick="playAudioUrl('${wavUrl}', '${item.video_name} / ${sfx.group} (${sfx.type} - SNR ${sfx.snr_db}dB)')">
              🔊 <strong>${sfx.group}</strong> <code>${sfx.type}</code> ×${sfx.count} <span style="color:var(--accent-teal);">(${sfx.snr_db}dB)</span>
            </button>
          `;
        }).join('');

        const shotRows = (item.shots || []).map(sb => {
          const fUrl = `file:///${item.output_posix}/${sb.first_frame}`;
          return `
            <tr>
              <td><strong>#${String(sb.shot_index).padStart(2, '0')}</strong></td>
              <td><code>${sb.t0}s – ${sb.t1}s</code> (${sb.duration_s}s)</td>
              <td><code>from=${sb.remotion_30fps.from}, dur=${sb.remotion_30fps.durationInFrames}</code></td>
              <td><span class="badge badge-purple">${sb.scene_style}</span> · <code>${sb.transition_in}</code> (${sb.motion_events_count} events)</td>
              <td><code>${sb.escbase_pattern_suggestion}</code></td>
              <td><a href="${fUrl}" target="_blank" style="color:var(--accent-teal);">Xem Frame Đầu ↗</a></td>
            </tr>
          `;
        }).join('');

        const musicUrl = `file:///${item.output_posix}/stems/music.wav`;
        const vocalsUrl = `file:///${item.output_posix}/stems/vocals.wav`;
        const effectsUrl = `file:///${item.output_posix}/stems/effects.wav`;

        const promptEscbase = `Đọc file Handoff Blueprint tại ${item.output_dir}\\HANDOFF_BLUEPRINT.md và ${item.output_dir}\\video\\remake.md.\nHãy áp dụng bảng màu, nhịp điệu chuyển cảnh và cấu trúc visual của mẫu này để lên visual-plan.md và dựng deck mới trong slide/<ten_project> (tuân thủ nghiêm ngặt WORKFLOW.md, khung 390x693, Slide 1 canonical hero, và kiểm định pass 100% validate_slide.py --semantic-report).`;
        const promptBackvideo = `Đọc file Handoff Blueprint tại ${item.output_dir}\\HANDOFF_BLUEPRINT.md, ${item.output_dir}\\handoff_manifest.json và ${item.output_dir}\\video\\remake.md.\nSử dụng bảng màu, bố cục các Shot và bộ file âm thanh SFX sạch trong ${item.output_dir}\\sfx để dựng Master Template / Job Remotion mới (tích hợp sẵn AntiReupGuard.tsx, KineticSubtitle.tsx, auto-trigger SFX khi nhảy chữ, và đảm bảo pass 100% test suite).`;

        return `
          <div class="lab-card">
            <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:10px;">
              <div>
                <h3 style="font-size:18px; color:#fff;">📁 <code>outputs/${item.video_name}/</code> — ${item.source.resolution} (${item.source.aspect_ratio}) @ ${item.source.fps}fps · ${item.source.duration_s}s</h3>
                <p style="font-size:13px; color:var(--text-muted); margin-top:3px;"><strong>Verdict:</strong> ${item.production_verdict}</p>
              </div>
              <div style="display:flex; gap:8px; flex-wrap:wrap;">
                ${rcBadge}
                <a class="act-btn primary" href="${item.report_url}" target="_blank">📊 Mở Visual Report (HTML) ↗</a>
                <a class="act-btn" href="${item.blueprint_url}" target="_blank">📦 Mở HANDOFF_BLUEPRINT.md ↗</a>
                <a class="act-btn" href="${item.storyboard_url}" target="_blank">🖼️ Storyboard ↗</a>
              </div>
            </div>

            <div>
              <div style="font-size:12.5px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">🎨 BẢNG MÀU HEX ĐÃ ĐO TỪ VIDEO (Click để copy mã màu):</div>
              <div class="swatches">${swatches || '<span style="color:var(--text-muted);font-size:12px;">Không có bảng màu</span>'}</div>
            </div>

            <div>
              <div style="font-size:12.5px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">🎵 BÓC TÁCH 3 KÊNH ÂM THANH & ${item.audio_summary.clean_reusable_sfx_count} FILE SFX SẠCH (Bấm để nghe thử ngay):</div>
              <div class="sfx-grid" style="margin-bottom:8px;">
                <button class="sfx-chip" style="border-color:var(--accent-emerald);" onclick="playAudioUrl('${musicUrl}', '${item.video_name} - Nhạc nền BGM (${item.audio_summary.tempo_bpm || 'N/A'} BPM)')">🎵 Nghe Nhạc Nền Sạch (music.wav · ${item.audio_summary.tempo_bpm || 'N/A'} BPM)</button>
                <button class="sfx-chip" style="border-color:var(--accent-cyan);" onclick="playAudioUrl('${vocalsUrl}', '${item.video_name} - Giọng đọc tách rời (vocals.wav)')">🗣️ Nghe Giọng Đọc Tách Rời (vocals.wav)</button>
                <button class="sfx-chip" style="border-color:var(--accent-purple);" onclick="playAudioUrl('${effectsUrl}', '${item.video_name} - Toàn bộ kênh SFX (effects.wav)')">💥 Nghe Kênh SFX Tổng (effects.wav)</button>
              </div>
              <div class="sfx-grid">${sfxChips}</div>
            </div>

            <div>
              <div style="font-size:12.5px; font-weight:700; color:var(--text-muted); margin-bottom:6px;">🎬 MA TRẬN CHUYỂN ĐỔI PHÂN CẢNH (${item.shots.length} SHOTS):</div>
              <table class="shot-tbl">
                <thead>
                  <tr>
                    <th>Shot</th>
                    <th>Thời gian (s)</th>
                    <th>Remotion (@30fps)</th>
                    <th>Style & Chuyển Cảnh</th>
                    <th>Gợi ý Map sang escbase_template (390x693)</th>
                    <th>Keyframe</th>
                  </tr>
                </thead>
                <tbody>${shotRows}</tbody>
              </table>
            </div>

            <div style="display:flex; gap:10px; flex-wrap:wrap;">
              <button class="act-btn primary" onclick='copyText(${JSON.stringify(promptEscbase)})'>🟢 Copy Lệnh Bàn Giao Sang escbase_template</button>
              <button class="act-btn primary" onclick='copyText(${JSON.stringify(promptBackvideo)})'>🟣 Copy Lệnh Bàn Giao Sang E:\A1A\backvideo</button>
            </div>
          </div>
        `;
      }).join('');
    }

    renderKpisAndMatrix();
    renderTemplates();
    renderAnalyzedLab();
  </script>
</body>
</html>
"""


def build_cockpit() -> Path:
    data = load_data()
    payload = json.dumps(data, ensure_ascii=False)
    html = HTML_TEMPLATE.replace("__COCKPIT_JSON_PAYLOAD__", payload)
    out_path = ROOT_DIR / "VISUAL_COCKPIT.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


def main() -> int:
    out_path = build_cockpit()
    print(f"[OK] Built Standalone Visual Cockpit: file:///{out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

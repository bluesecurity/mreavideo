# Project Context: mreavideo

## 1. Tổng quan Dự án (Project Overview)
- **Tên dự án:** `mreavideo`
- **Mục đích:** Reverse-Engineer Any Video (Dịch ngược video clip, bóc tách cấu trúc từng phân cảnh, nhận diện AI vs Thực tế, bóc tách âm thanh, nhận dạng phụ đề và lập kế hoạch tái sản xuất Remake Plan).
- **Thư mục làm việc:** `f:\Mcode\mreavideo`
- **Rollback Anchor:** `6f4c859d391194b3770da30bb066ca1e36e2fbf9` (Previous anchors: `991532bd7a53fe0d000db59137892107ae3c1778`, `e5e17f3`)
- **Kho mẫu ReelCrew (61 Styles / 133 Videos):** `F:\mworkk\videosample\reels\` (kèm `CATALOG.md` và `catalog.json`, tải tự động qua `scripts/download_reelcrew_samples.py`)
- **Handoff Blueprint Compiler:** `scripts/export_handoff.py` (tự động xuất `HANDOFF_BLUEPRINT.md` và `handoff_manifest.json` cho từng video trong `outputs/<stem>/`)
- **Agent Skill:** `vrea-video-forensics` (Project Scope: `.agents/skills/vrea-video-forensics/` & Global Link duy nhất: `~/.gemini/config/skills/vrea-video-forensics/`)

---

## 2. Tech Stack & Runtime
- **OS:** Windows 11 x64
- **Python:** Python 3.13 (Cô lập trong `.venv/`)
- **FFmpeg:** 8.0.1-full_build (Hệ thống)
- **Engine Core:** `JuneYaooo/rea-video` (Git Submodule `engine/`)
- **ML / AI Inference:**
  - `onnxruntime` (UVR-MDX-Net cho Vocals/Instrumental, BandIt v2 cho SFX)
  - `rapidocr 3` (OCR chữ và phụ đề trên video)
  - `videomd 1.2.0` (Biên dịch VideoMD Spec)

---

## 3. Lệnh Kiểm định Cơ học (Mechanical Validation Commands)
- **Chạy kiểm định tổng hợp 1 lệnh:**
  ```powershell
  .\.venv\Scripts\python.exe scripts\check.py
  ```
- **Chạy bộ Unit Test toàn diện:**
  ```powershell
  .\.venv\Scripts\pytest.exe engine\tests -q
  ```
- **Chạy phân tích video đầu cuối:**
  ```powershell
  .\.venv\Scripts\python.exe run.py inputs\sample_test.mp4
  ```

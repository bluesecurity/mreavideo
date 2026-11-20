---
name: vrea-video-forensics
description: Autonomous Video Reverse-Engineering & Shot-by-Shot Forensic Pipeline (mreavideo). Dịch ngược bất kỳ video nào (.mp4, .mov) thành bản thiết kế tái sản xuất (VIDEO.md), báo cáo trực quan (report.html) và gói bàn giao liên xưởng (HANDOFF_BLUEPRINT.md), bóc tách 3 luồng âm thanh (Voice, BGM, SFX), OCR phụ đề và đảo ngược prompt AI cho từng cảnh.
---

# Video Reverse-Engineering Architecture: `vrea-video-forensics`

Skill này cung cấp quy trình tự hành phân tích, dịch ngược video theo từng phân cảnh (Shot-by-Shot Forensics) và đóng gói **Air-Gapped Handoff Blueprint** trên trạm làm việc cục bộ `mreavideo`.

---

## 1. Ranh giới Phân định (Disambiguation Boundary)
- **`vrea-video-forensics`:** Chuyên sâu về **Multimedia Video Forensics** (phân tích video, nhận diện AI video vs quay thực vs Code/Template render, bóc tách audio stems giọng/nhạc/sfx bằng ONNX, OCR chữ/phụ đề, trích xuất prompt và đóng gói Handoff Pack cho các xưởng sản xuất video).
- **Phân biệt với `rea` MCP:** `rea` MCP là công cụ dịch ngược nhị phân cho ứng dụng và game (Reverse-Engineering Native Binaries, APK, Mach-O, ELF, Frida, Cutter, Ghidra). Hai công cụ hoàn toàn độc lập, không xung đột.

---

## 2. Yêu cầu Đầu vào & Kho Mẫu Tham Chiếu (Input Contract & Reference Vault)
- **Định dạng chấp nhận:** File video cục bộ hợp lệ (`.mp4`, `.mov`, `.mkv`).
- **Thư mục tiêu chuẩn:** Đặt video vào `F:\Mcode\mreavideo\inputs/` hoặc truyền đường dẫn tuyệt đối.
- **Kho mẫu ReelCrew (61 Styles / 136 Videos):** Đã được đồng bộ đầy đủ tại `F:\mworkk\videosample\reels\` kèm chỉ mục [`CATALOG.md`](file:///F:/mworkk/videosample/reels/CATALOG.md) và [`catalog.json`](file:///F:/mworkk/videosample/reels/catalog.json) (cập nhật qua `scripts/download_reelcrew_samples.py`).
- **Tổng đài trực quan (Visual Cockpit & Mindmap):** Mở trực tiếp [`F:\Mcode\mreavideo\VISUAL_COCKPIT.html`](file:///F:/Mcode/mreavideo/VISUAL_COCKPIT.html) (được sinh tự động qua `scripts/build_cockpit.py`) để duyệt 61 Templates, phát thử 136 video mẫu, nghe thử Audio Stems/SFX đã mổ và copy lệnh bàn giao sang 3 xưởng (`escbase_template`, `backvideo`, `flowtop`).
- **Di trú đa máy tính (Cross-Machine Portability):** Khi chuyển repo sang máy mới hoặc ổ đĩa khác, chạy `F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\scripts\portable_setup.py` để tự động vá lỗi RapidOCR Python 3.13 (`h < 0.08`), kiểm tra 216MB ONNX models và cập nhật đường dẫn Global Skill.
- **Lưu ý quan trọng (Anti-Blindspot):** Skill này **KHÔNG** nhận trực tiếp URL trực tuyến (YouTube, TikTok) do các nền tảng có cơ chế chặn bot và nén suy hao metadata. Người dùng cần tải video về máy trước khi yêu cầu phân tích.

---

## 3. Quy trình Thực thi (Execution Workflow)

Khi người dùng yêu cầu phân tích một video (ví dụ: `inputs/sample.mp4`):

### Bước 1: Kích hoạt Pipeline Phân tích (Tự động sinh kèm Handoff Pack)
Chạy lệnh bằng môi trường `.venv` cô lập của dự án:
```powershell
# Chế độ tiêu chuẩn (Offline Deterministic CV + Audio Stem + OCR + Auto Handoff Pack)
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\run.py F:\Mcode\mreavideo\inputs\sample.mp4

# Chế độ tăng cường Multimodal VLM (nếu có cấu hình .env / .env.local)
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\run.py F:\Mcode\mreavideo\inputs\sample.mp4 --vlm

# Xử lý hàng loạt toàn bộ video trong inputs/
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\run.py --all

# Tái biên dịch riêng gói Handoff Blueprint cho 1 hoặc toàn bộ outputs/
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\scripts\export_handoff.py --all
```

### Bước 2: Đọc & Trích xuất Kết quả Thực chứng
Sau khi lệnh trả về Exit Code 0, mở đọc các file artifacts tại `F:\Mcode\mreavideo\outputs\<video_stem>/`:
1. **`HANDOFF_BLUEPRINT.md` & `handoff_manifest.json`:** Gói bàn giao Air-Gapped đã tinh luyện (không cần đọc `breakdown.json` nặng >80k tokens), bao gồm:
   - Bảng màu Hex chủ đạo, thông số FPS/Aspect/Duration, nhận diện tự động Style ReelCrew (nếu trùng khớp).
   - Bảng chuyển đổi phân cảnh sang **`escbase_template` (`390x693` MiracleLab DOM)** và **`E:\A1A\backvideo` (`1080x1920` / `1080x1440` Remotion `@30fps`)**.
   - Danh mục các file SFX sạch (`SNR >= 25 dB`) tại `sfx/sfx_XX.wav` và câu lệnh Prompt Copy-Paste để giao cho AI Agent ở các xưởng đích.
2. **`VIDEO.md`:** Bản thiết kế gốc chuẩn VideoMD:
   - Tỷ lệ sản xuất (Live-action % vs AI-generated % vs Code/Template %).
   - Danh sách phân cảnh, thời gian bắt đầu/kết thúc (`t0 -> t1`), góc máy quay.
3. **`report.html`:** Báo cáo trực quan dạng Standalone HTML (`file:///F:/Mcode/mreavideo/outputs/<video_stem>/report.html`).
4. **`stems/` & `sfx/`:** Đường dẫn các file âm thanh đã bóc tách:
   - `stems/vocals.wav`: Giọng nói / Lời thoại (Human vs AI TTS).
   - `stems/music.wav`: Nhạc nền sạch (BPM và nhịp điệu).
   - `stems/effects.wav` & `sfx/sfx_*.wav`: Hiệu ứng âm thanh (SFX) kèm mốc thời gian kích hoạt.

---

## 4. Kiểm định Cơ học Nhanh (Mechanical Sanity Check)
Bất kỳ khi nào cần kiểm tra tính toàn vẹn của trạm `mreavideo`, chạy:
```powershell
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\scripts\check.py
```
Yêu cầu kết quả phải trả về Exit Code 0.

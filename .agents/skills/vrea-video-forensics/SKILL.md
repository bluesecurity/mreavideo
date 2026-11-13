---
name: vrea-video-forensics
description: Autonomous Video Reverse-Engineering & Shot-by-Shot Forensic Pipeline (mreavideo). Dịch ngược bất kỳ video nào (.mp4, .mov) thành bản thiết kế tái sản xuất (VIDEO.md) và báo cáo trực quan (report.html), bóc tách 3 luồng âm thanh (Voice, BGM, SFX), OCR phụ đề và đảo ngược prompt AI cho từng cảnh.
---

# Video Reverse-Engineering Architecture: `vrea-video-forensics`

Skill này cung cấp quy trình tự hành phân tích và dịch ngược video theo từng phân cảnh (Shot-by-Shot Forensics) trên trạm làm việc cục bộ `mreavideo`.

---

## 1. Ranh giới Phân định (Disambiguation Boundary)
- **`vrea-video-forensics`:** Chuyên sâu về **Multimedia Video Forensics** (phân tích video, nhận diện AI video vs quay thực, bóc tách audio stems giọng/nhạc/sfx bằng ONNX, OCR chữ/phụ đề, trích xuất prompt cho từng shot).
- **Phân biệt với `rea` MCP:** `rea` MCP là công cụ dịch ngược nhị phân cho ứng dụng và game (Reverse-Engineering Native Binaries, APK, Mach-O, ELF, Frida, Cutter, Ghidra). Hai công cụ hoàn toàn độc lập, không xung đột.

---

## 2. Yêu cầu Đầu vào (Input Contract)
- **Định dạng chấp nhận:** File video cục bộ hợp lệ (`.mp4`, `.mov`, `.mkv`).
- **Thư mục tiêu chuẩn:** Đặt video vào `F:\Mcode\mreavideo\inputs/`.
- **Lưu ý quan trọng (Anti-Blindspot):** Skill này **KHÔNG** nhận trực tiếp URL trực tuyến (YouTube, TikTok) do các nền tảng có cơ chế chặn bot và nén suy hao metadata. Người dùng cần tải video về thư mục `inputs/` trước khi yêu cầu phân tích.

---

## 3. Quy trình Thực thi (Execution Workflow)

Khi người dùng yêu cầu phân tích một video (ví dụ: `inputs/sample.mp4`):

### Bước 1: Kích hoạt Pipeline Phân tích
Chạy lệnh bằng môi trường `.venv` cô lập của dự án:
```powershell
# Chế độ tiêu chuẩn (Offline Deterministic CV + Audio Stem + OCR)
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\run.py F:\Mcode\mreavideo\inputs\sample.mp4

# Chế độ tăng cường Multimodal VLM (nếu có cấu hình .env)
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\run.py F:\Mcode\mreavideo\inputs\sample.mp4 --vlm

# Xử lý hàng loạt toàn bộ video trong inputs/
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\run.py --all
```

### Bước 2: Đọc & Trích xuất Kết quả Thực chứng
Sau khi lệnh trả về Exit Code 0, mở đọc các file artifacts tại `F:\Mcode\mreavideo\outputs\<video_stem>/`:
1. **`VIDEO.md`:** Đọc để trích xuất:
   - Tỷ lệ sản xuất (Live-action % vs AI-generated % vs Code/Template %).
   - Danh sách phân cảnh, thời gian bắt đầu/kết thúc (t0 -> t1).
   - Prompt gợi ý cho từng shot (với các cảnh sinh bằng AI).
   - Góc máy quay, hướng di chuyển (Pan, Tilt, Zoom, Dolly).
2. **`report.html`:** Báo cáo trực quan dạng Standalone HTML. Cung cấp liên kết `file:///F:/Mcode/mreavideo/outputs/<video_stem>/report.html` cho người dùng.
3. **`stems/`:** Đường dẫn các file âm thanh đã bóc tách:
   - `vocals.wav`: Giọng nói / Lời thoại (Human vs AI TTS).
   - `music.wav`: Nhạc nền (BPM và nhịp điệu).
   - `effects.wav`: Hiệu ứng âm thanh (SFX).

---

## 4. Kiểm định Cơ học Nhanh (Mechanical Sanity Check)
Bất kỳ khi nào cần kiểm tra tính toàn vẹn của trạm `mreavideo`, chạy:
```powershell
F:\Mcode\mreavideo\.venv\Scripts\python.exe F:\Mcode\mreavideo\scripts\check.py
```
Yêu cầu kết quả phải trả về Exit Code 0.

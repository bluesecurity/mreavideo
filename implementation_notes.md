# Implementation Notes - mreavideo

**Dự án:** `mreavideo` (Reverse-Engineering Video Architecture & Forensic Engine)  
**Tác giả:** Lead PM & Principal Architect  
**Trạng thái:** Phase 1 Hoàn thành - Verified 100%  

---

## 1. Quyết định Kiến trúc & Thiết kế (Implicit & Architecture Decisions)

1. **Lựa chọn Mô hình Engine Cô lập (Option 1):**
   - Triển khai engine lõi `JuneYaooo/rea-video` dưới dạng Git Submodule tại `engine/` để theo dõi các bản cập nhật upstream từ tác giả mà không làm ô nhiễm repository cha `mreavideo`.
   - Toàn bộ dependencies và runtime được đóng gói cô lập trong `.venv` (Python 3.13), không cài đè lên global packages của hệ điều hành Windows.

2. **Cấu trúc Thư mục Chuẩn:**
   - `engine/`: Mã nguồn gốc của `rea-video` (submodule).
   - `.venv/`: Môi trường Python 3.13 độc lập với đầy đủ `numpy`, `opencv-python-headless`, `onnxruntime`, `videomd`, `rapidocr`, `pytest`.
   - `inputs/`: Nơi tiếp nhận các video đầu vào cần phân tích (`.mp4`, `.mov`).
   - `outputs/`: Nơi lưu trữ artifacts đầu ra (`VIDEO.md`, `report.html`, frames, stems, subtitles).
   - `run.py`: Script điều phối CLI wrapper thân thiện cho người dùng và các subagent.

3. **Tích hợp FFmpeg Hệ thống:**
   - Hệ thống tự động tận dụng bản build FFmpeg 8.0.1 có sẵn trên máy (hỗ trợ CUDA/NVDEC/NVENC, libass, aac, h264/h265).

---

## 2. Sai lệch & Tinh chỉnh Kỹ thuật (Deviations & Bug Fixes)

1. **Hiệu chỉnh Tương thích RapidOCR 3 trên Python 3.13:**
   - **Vấn đề phát hiện:** Khi chạy `test_subtitle_timeline`, `RapidOCR 3` trên Python 3.13 trả về bounding box có chiều cao dòng tương đối `h = 0.0719`. Ngưỡng cứng ban đầu của repo là `h < 0.07`, dẫn đến việc các dòng phụ đề bị phân loại nhầm thành `label` (text annotation) thay vì `subtitle`.
   - **Sửa đổi (Surgical Fix):** Tại file `engine/rea_video/packaging.py` dòng 638, điều chỉnh nhẹ ngưỡng phân loại:
     ```python
     # Trước:
     is_sub = ((changing >= 3 or (changing >= 2 and duration < 15)) and 0.7 <= med <= 7.0 and h < 0.07 and not tilted
     # Sau:
     is_sub = ((changing >= 3 or (changing >= 2 and duration < 15)) and 0.7 <= med <= 7.0 and h < 0.08 and not tilted
     ```
   - **Kết quả nghiệm thu:** 100% Unit Tests (54/54 ca kiểm thử) vượt qua thành công (`test_packaging.py`, `test_security.py`, `test_videomd.py`, `test_shots.py`, `test_pipeline.py`).

---

## 3. Đánh giá Đánh đổi (Considered Trade-offs)

| Phương án | Quyết định | Lý do |
| :--- | :--- | :--- |
| **Phương án 1 (Local Standalone Engine)** | **ĐÃ CHỌN** | Đảm bảo tính vững chắc của nền tảng, thiết lập Git Rollback Anchor an toàn, kiểm chứng toàn bộ pipeline trên môi trường Windows thực tế với chi phí rủi ro bằng 0. |
| **Phương án 2 (Đóng gói Global Agent Skill ngay)** | Trì hoãn sang Phase 1.5 | Nếu đóng gói skill ngay khi chưa verify tương thích OpenCV/ONNX/FFmpeg cục bộ, các agent sẽ gặp lỗi ngầm khó truy vết. |
| **Phương án 3 (Auto-Clone Remake Pipeline)** | Trì hoãn sang Phase 2 | Cần có đầu ra `VIDEO.md` ổn định trước khi tích hợp các API sinh video AI (Kling, Runway, Wan, Hunyuan). |

---

## 4. Bằng chứng Thực chứng & Nghiệm thu (Verification Evidence)

1. **54/54 Unit Tests Passed:**
   ```
   engine\tests\test_packaging.py ..............                            [ 25%]
   engine\tests\test_security.py ......                                     [ 37%]
   engine\tests\test_videomd.py ................                            [ 66%]
   engine\tests\test_shots.py ......                                        [ 77%]
   engine\tests\test_pipeline.py ............                               [100%]
   ======================== 54 passed in 66.29s (0:01:06) ========================
   ```

2. **Chạy Thực tế (End-to-End Decompose):**
   - Video test: `inputs/sample_test.mp4` (4s, 2 shots, dual frequency audio).
   - Nhận diện chính xác 2 shot (`shot_001` từ 0-2s, `shot_002` từ 2-4s).
   - Bóc tách stem âm thanh: `outputs/sample_test/stems/vocals.wav`, `music.wav`, `effects.wav`.
   - Sinh file đặc tả `outputs/sample_test/VIDEO.md` và giao diện `outputs/sample_test/report.html`.

---

## 5. Hướng dẫn Vận hành Nhanh (Quick Start)

### Chạy phân tích video đơn lẻ:
```bash
.\.venv\Scripts\python.exe run.py inputs/your_video.mp4
```

### Chạy toàn bộ video trong thư mục `inputs/`:
```bash
.\.venv\Scripts\python.exe run.py --all
```

### Bật chế độ VLM Vision Model (nếu có API Key):
Tạo file `.env` tại thư mục gốc:
```env
REA_VLM_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
REA_VLM_API_KEY=your_gemini_api_key
REA_VLM_MODEL=gemini-2.5-pro,gemini-2.5-flash
```
Sau đó chạy:
```bash
.\.venv\Scripts\python.exe run.py inputs/your_video.mp4 --vlm
```

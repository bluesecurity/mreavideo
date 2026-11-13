# Goals & Anti-Zeno Lock: mreavideo

> **Anti-Zeno Lock Rule:** Khi Core MVP đã đạt 100% VÀ vượt qua kiểm định cơ học với Exit Code 0, khóa sổ toàn bộ phạm vi Core MVP. Tuyệt đối cấm tự ý dịch chuyển tiêu chí (Moving Goalposts) hoặc bịa thêm các tính năng ngoài luồng.

---

## Milestone 1: Core Forensic Engine & Local Scaffolding [100% COMPLETE - LOCKED]

- [x] **Git Scaffolding & Rollback Anchor:** Khởi tạo Git repository và commit gốc an toàn `e5e17f3`.
- [x] **Submodule Ingestion:** Tích hợp engine `JuneYaooo/rea-video` qua Git Submodule tại `engine/`.
- [x] **Isolated Runtime:** Thiết lập môi trường ảo `.venv` (Python 3.13) với đầy đủ gói phụ thuộc (`opencv-python-headless`, `onnxruntime`, `rapidocr`, `videomd`).
- [x] **Python 3.13 RapidOCR 3 Patch:** Sửa đổi ngưỡng chiều cao dòng `h < 0.08` tại `packaging.py` để vượt qua 100% test OCR.
- [x] **CLI Dispatcher:** Xây dựng script `run.py` hỗ trợ phân tích video đơn lẻ, xử lý hàng loạt (`--all`), và cờ đa mô hình `--vlm`.
- [x] **Mechanical Validation:**
  - `pytest engine\tests` đạt 262/262 passed (Exit Code 0).
  - Decompose video mẫu `sample_test.mp4` hoàn tất sinh đủ `breakdown.json`, `VIDEO.md`, `report.html`, audio stems (Exit Code 0).

---

## Milestone 2: Expansion & Ecosystem Integration
- [x] **Agent Skill Packaging:** Đóng gói thành Custom Skill `vrea-video-forensics` trong `.agents/skills/vrea-video-forensics/SKILL.md` và `~/.gemini/config/skills/vrea-video-forensics/SKILL.md`.
- [ ] **Auto-Remake Adapter:** Tích hợp script gọi API Kling / Wan / Runway để render lại video từ file `VIDEO.md`.
- [ ] **GPU Acceleration:** Hỗ trợ tùy chọn `onnxruntime-gpu` khi người dùng yêu cầu xử lý video dung lượng lớn trên GPU.

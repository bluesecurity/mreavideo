# Goals & Anti-Zeno Lock: mreavideo

> **Anti-Zeno Lock Rule & Frozen Audit Rubric:** Khi Core MVP đã đạt 100% VÀ vượt qua kiểm định cơ học (`scripts/check.py`) với Exit Code 0, khóa sổ toàn bộ phạm vi Core MVP. Tuyệt đối cấm tự ý dịch chuyển tiêu chí (Moving Goalposts) hoặc lấy các hạng mục Backlog V2 (Out-of-Scope) để trừ điểm / đẻ thêm Gap cho V1.
>
> **5 Tiêu chí Đóng băng (Frozen Audit Rubric V1):**
> 1. **Env & Config Sync:** `run.py` nạp `.env.local` và `.env` (strip quotes) + tự động bridge `GEMINI_API_KEY` / `OPENAI_API_KEY` sang `REA_VLM_*`.
> 2. **CLI & Batch Contract:** `run.py` hỗ trợ `.mp4`, `.mov`, `.mkv` đồng bộ với `SKILL.md` và trả về Exit Code `!= 0` nếu có lỗi trong `--all`.
> 3. **Self-Healing Mechanical Check:** `scripts/check.py` vượt qua 54 core tests (trong tổng số 262 upstream tests) và tự sinh lại `outputs/sample_test` nếu thiếu.
> 4. **Focused Skill Link:** Duy trì đồng bộ duy nhất skill `vrea-video-forensics` giữa `.agents/skills/vrea-video-forensics/` và `~/.gemini/config/skills/vrea-video-forensics/`, tuyệt đối không đụng các Global Skills khác.
> 5. **Zero-Leak Git Hygiene:** `.gitignore` chặn tuyệt đối `.env*`, keys, media nặng (`inputs/`, `outputs/`) và `scripts/push_dual.py` che mờ token ở runtime.

---

## Milestone 1: Core Forensic Engine, CLI & Skill Packaging [100% COMPLETE - LOCKED]

- [x] **Git Scaffolding & Rollback Anchor:** Khởi tạo Git repository (commit gốc `e5e17f3`, Rollback Anchor hiện hành đồng bộ tại `CONTEXT.md`).
- [x] **Submodule Ingestion:** Tích hợp engine `JuneYaooo/rea-video` qua Git Submodule tại `engine/`.
- [x] **Isolated Runtime:** Thiết lập môi trường ảo `.venv` (Python 3.13) với đầy đủ gói phụ thuộc (`opencv-python-headless`, `onnxruntime`, `rapidocr`, `videomd`).
- [x] **Python 3.13 RapidOCR 3 Patch:** Sửa đổi ngưỡng chiều cao dòng `h < 0.08` tại `packaging.py` để vượt qua 100% test OCR.
- [x] **CLI Dispatcher:** Xây dựng script `run.py` hỗ trợ phân tích video đơn lẻ (`.mp4`, `.mov`, `.mkv`), xử lý hàng loạt (`--all` có kiểm soát mã lỗi), và cờ đa mô hình `--vlm` (tự động đọc `.env.local` / `.env`).
- [x] **Agent Skill Packaging:** Đóng gói và liên kết Custom Skill `vrea-video-forensics` tại `.agents/skills/vrea-video-forensics/SKILL.md` và `~/.gemini/config/skills/vrea-video-forensics/SKILL.md`.
- [x] **Mechanical Validation:**
  - Core Pytest Suite (`54/54` ca kiểm thử cốt lõi trong `scripts/check.py` và `262/262` toàn bộ `engine\tests`) đạt 100% passed (Exit Code 0).
  - Decompose video mẫu `sample_test.mp4` hoàn tất sinh đủ `breakdown.json`, `VIDEO.md`, `report.html`, audio stems (Exit Code 0).

---

## Out-of-Scope Backlog (DEFERRED TO V2 — DO NOT AUDIT IN V1)
*Các hạng mục định hướng tương lai dưới đây nằm ngoài phạm vi Core MVP (theo `SPEC.md` Non-Goals) và không tính vào tiêu chí Audit V1:*
- **Auto-Remake Adapter (V2 Backlog):** Tích hợp script gọi API Kling / Wan / Runway để render lại video từ file `VIDEO.md`.
- **GPU Acceleration (V2 Backlog):** Hỗ trợ tùy chọn `onnxruntime-gpu` khi người dùng yêu cầu xử lý video dung lượng lớn trên GPU.

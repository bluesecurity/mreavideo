# Specification: mreavideo (Video Reverse-Engineering & Forensic Engine)

## 1. Mục tiêu & Phạm vi (Scope & Goals)
`mreavideo` là công cụ CLI & Forensic Pipeline độc lập cho phép dịch ngược video mẫu (Shot-by-Shot Forensics) thành bản thiết kế sản xuất (Remake Blueprint) theo định dạng mở VideoMD và Visual HTML Report tương tác.

---

## 2. Kiến trúc Kỹ thuật (Technical Architecture)

### 2.1. Runtime & Environment
- **Hệ điều hành:** Windows x64.
- **Python Runtime:** Python 3.13 cô lập trong `.venv/`.
- **Hệ thống Đa phương tiện:** FFmpeg 8.0.1 (hỗ trợ libx264, libx265, aac, libass, cuvid/nvdec).

### 2.2. Thư viện & Mô hình Cốt lõi
- **OpenCV & FFmpeg:** Cắt shot tự động (Scene Cut Detection), trích xuất keyframes, phân tích frame cadence (FPS, frame interpolation), siêu dữ liệu AIGC/C2PA tags, sensor noise patterns.
- **ONNX Runtime:** Chạy mô hình cục bộ:
  - `UVR-MDX-NET-Inst_HQ_3.onnx` (~67 MB): Tách nhạc nền và giọng nói.
  - `bandit-v2-multi.onnx` (~149 MB): Bóc tách hiệu ứng âm thanh (SFX) đa kênh.
- **RapidOCR 3 (`rapidocr>=3.4,<4`):** Nhận diện text overlay, phụ đề (Subtitle Timeline), tọa độ bounding boxes, màu sắc và kiểu viền font (với ngưỡng `h < 0.08` tương thích Python 3.13).
- **VideoMD Specification (`videomd>=1.1`):** Biên dịch cấu trúc phân cảnh chuẩn hóa (`VIDEO.md`).

### 2.3. Cấu trúc Thư mục Hệ thống
```text
mreavideo/
├── .venv/                      # Virtual environment cô lập
├── engine/                     # Git submodule upstream rea-video
├── inputs/                     # Nơi chứa video tham chiếu đầu vào (.mp4, .mov)
├── outputs/                    # Thư mục chứa artifacts đầu ra (.html, .md, .wav, .jpg)
├── scripts/
│   └── check.py                # Script kiểm định cơ học 1 lệnh (Mechanical Validation)
├── CONTEXT.md                  # Bản đồ kiến trúc & Rollback Anchor
├── SPEC.md                     # Đặc tả kỹ thuật và ranh giới hệ thống
├── GOAL.md                     # Mục tiêu tổng thể & Anti-Zeno Lock
├── implementation_notes.md     # Nhật ký quyết định kỹ thuật
└── run.py                      # Bộ điều phối thực thi CLI chính
```

---

## 3. Ranh giới Thẩm quyền & Non-Goals (Core MVP)

- **Non-Goal 1:** Không tự động re-render video mới bằng API trả phí (Kling AI, Runway Gen-3, Luma, Wan) trong phạm vi Core MVP; chỉ tập trung vào phân tích trinh sát và xuất bản thiết kế Remake Spec.
- **Non-Goal 2:** Không dựng web server hoặc database nặng; toàn bộ dữ liệu vận hành theo mô hình Local-First dựa trên file hệ thống (`inputs/` và `outputs/`).
- **Non-Goal 3:** Không thay đổi các file cấu hình toàn cục bên ngoài workspace `f:\Mcode\mreavideo`.

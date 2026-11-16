r"""
ReelCrew Sample Video Harvester & Style Catalog Builder
Downloads all sample videos from https://reelcrew.io/video-mau (61 styles / 138 video items)
into F:\mworkk\videosample\reels\ with concurrent workers and builds catalog.json + CATALOG.md.
"""

import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

TARGET_DIR = Path(r"F:\mworkk\videosample\reels")

STYLES_DATA = [
    {
        "style_id": 1,
        "title": "Bản tin công nghệ trên sân khấu teal liền mạch",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · tech-brief",
        "description": "Kể một tin công nghệ trong 45–90 s: từng ý hiện nối tiếp trên một sân khấu teal, có ảnh chụp màn hình thật.",
        "videos": [
            "https://reelcrew.io/site/tech-brief-6021ac5d.mp4",
            "https://reelcrew.io/site/tech-brief-22c0c2d2.mp4",
            "https://reelcrew.io/site/tech-brief-fdd03fd9.mp4"
        ]
    },
    {
        "style_id": 2,
        "title": "Bên trong một thứ quen thuộc hoạt động thế nào",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · under-the-hood",
        "description": "Mở ra bên trong một vật quen thuộc (thẻ NFC, màn cảm ứng…) và cho thấy nó chạy thế nào, có robot dẫn chuyện.",
        "videos": [
            "https://reelcrew.io/site/under-the-hood-cbeed839.mp4",
            "https://reelcrew.io/site/under-the-hood-96c3b4a7.mp4"
        ]
    },
    {
        "style_id": 3,
        "title": "Nghịch lý toán, lý vẽ bằng hình học thật",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · science-paradox",
        "description": "Một nghịch lý toán hay vật lý được vẽ bằng hình học thật, chuyển động chính xác theo lời giải thích.",
        "videos": [
            "https://reelcrew.io/site/science-paradox-32b18a7c.mp4"
        ]
    },
    {
        "style_id": 4,
        "title": "Một khái niệm AI trên sơ đồ node sống",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · agent-diagram",
        "description": "Một khái niệm AI (agent, sub-agent, bộ nhớ…) dựng trên sơ đồ node sống, mỗi khối sáng lên đúng lúc được nói.",
        "videos": [
            "https://reelcrew.io/site/agent-diagram-5526c4d5.mp4"
        ]
    },
    {
        "style_id": 5,
        "title": "Khái niệm bán hàng online trên một bảng sơ đồ",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · ecommerce-diagram",
        "description": "Giải thích một con số bán hàng online (phễu, lợi nhuận, tỉ lệ chốt) trên bảng sơ đồ giấy kem.",
        "videos": [
            "https://reelcrew.io/site/ecommerce-diagram-7aa9aeed.mp4",
            "https://reelcrew.io/site/ecommerce-diagram-43aabe1f.mp4"
        ]
    },
    {
        "style_id": 6,
        "title": "Sơ đồ tư duy lớn vẽ tay, camera đi theo nhánh",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · mindmap",
        "description": "Sơ đồ tư duy vẽ tay trên một canvas lớn, camera lướt theo từng nhánh khi giọng đọc nhắc tới.",
        "videos": [
            "https://reelcrew.io/site/mindmap-4a059992.mp4",
            "https://reelcrew.io/site/mindmap-883cdfbc.mp4",
            "https://reelcrew.io/site/mindmap-8496638f.mp4"
        ]
    },
    {
        "style_id": 7,
        "title": "Cây kỹ thuật treo trên dây đỏ",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · tree",
        "description": "Cấu trúc kỹ thuật (thư mục, kiến trúc, quy trình) treo thành cây trên dây đỏ, từng nút thả xuống theo lời.",
        "videos": [
            "https://reelcrew.io/site/tree-7cc8d27d.mp4"
        ]
    },
    {
        "style_id": 8,
        "title": "Chấm trắng biến hình trên nền đen, tối giản",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · morph-minimal",
        "description": "Một chấm trắng trên nền đen biến hình thành từng ý: tối giản, hợp chủ đề coaching, tư duy.",
        "videos": [
            "https://reelcrew.io/site/morph-minimal-0f311391.mp4"
        ]
    },
    {
        "style_id": 9,
        "title": "So 3–4 lựa chọn dễ nhầm, chốt nên chọn gì",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · option-compare",
        "description": "So 3–4 lựa chọn dễ nhầm (công cụ, gói, cách làm) rồi chốt nên chọn cái nào cho trường hợp nào.",
        "videos": [
            "https://reelcrew.io/site/option-compare-a4614660.mp4",
            "https://reelcrew.io/site/option-compare-ed6e170a.mp4",
            "https://reelcrew.io/site/option-compare-2e1d3bcc.mp4"
        ]
    },
    {
        "style_id": 10,
        "title": "Một hiệu ứng tâm lý, sân khấu rêu trầm",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · reflect-effect",
        "description": "Một hiệu ứng tâm lý (Zeigarnik, mỏ neo…) kể chậm rãi trên sân khấu xanh rêu, hợp video suy ngẫm 16:9.",
        "videos": [
            "https://reelcrew.io/site/reflect-effect-72afe8bd.mp4"
        ]
    },
    {
        "style_id": 11,
        "title": "Sổ tay bút chì, robot mascot, bảng gỗ",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · ink-paper",
        "description": "Giải thích trên sổ tay bút chì và bảng gỗ, có robot mascot, giọng ấm như đang ghi chú cho bạn.",
        "videos": [
            "https://reelcrew.io/site/ink-paper-8d3cae3b.mp4",
            "https://reelcrew.io/site/ink-paper-842816c2.mp4"
        ]
    },
    {
        "style_id": 12,
        "title": "Explainer khoa học điện ảnh khoảng 30 giây",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · cinematic",
        "description": "Câu hỏi khoa học đời thường trả lời trong ~30 s bằng hình minh hoạ điện ảnh và một con số gây bất ngờ.",
        "videos": [
            "https://reelcrew.io/site/cinematic-d1f80684.mp4",
            "https://reelcrew.io/site/cinematic-05e95b78.mp4",
            "https://reelcrew.io/site/paper-fold.mp4"
        ]
    },
    {
        "style_id": 13,
        "title": "Nhà máy isometric cho một quy trình",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · isometric-factory",
        "description": "Một quy trình nhiều bước vẽ thành nhà máy isometric: hộp chạy qua từng trạm, bộ đếm tăng theo nhạc.",
        "videos": [
            "https://reelcrew.io/site/isometric-factory-7173e23d.mp4",
            "https://reelcrew.io/site/isometric-factory-4abf5508.mp4",
            "https://reelcrew.io/site/jev-factory.mp4"
        ]
    },
    {
        "style_id": 14,
        "title": "Cỗ máy isometric chi tiết, chạy chính là ý tưởng",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · machine",
        "description": "Một ý tưởng kỹ thuật thành cỗ máy isometric chi tiết; cỗ máy chạy chính là cách ý tưởng vận hành.",
        "videos": [
            "https://reelcrew.io/site/machine-0021e316.mp4",
            "https://reelcrew.io/site/machine-f328e596.mp4",
            "https://reelcrew.io/site/dong-ho-so.mp4"
        ]
    },
    {
        "style_id": 15,
        "title": "Vẽ tay bảng trắng theo giọng đọc",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · whiteboard",
        "description": "Bàn tay vẽ từng hình lên bảng trắng theo giọng đọc, nét trước màu sau, kiểu video giải thích kinh điển.",
        "videos": [
            "https://reelcrew.io/site/whiteboard-f0cc73e1.mp4",
            "https://reelcrew.io/site/whiteboard-0587e1c8.mp4",
            "https://reelcrew.io/site/cau-vong.mp4"
        ]
    },
    {
        "style_id": 16,
        "title": "Lộ trình đường đỏ trên địa hình 3D",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · route-3d",
        "description": "Lộ trình du lịch thành đường đỏ chạy trên địa hình 3D, mỗi điểm dừng có tên và ngày.",
        "videos": [
            "https://reelcrew.io/site/route-3d-2f25dceb.mp4"
        ]
    },
    {
        "style_id": 17,
        "title": "Explainer theo ngách có mascot (21 ngách: luật, du lịch, bán hàng…)",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · niche",
        "description": "Explainer có mascot cho 21 ngách (luật, du lịch, bán hàng, tiếng Anh…) với widget riêng từng ngách.",
        "videos": [
            "https://reelcrew.io/site/niche-f6d20d32.mp4",
            "https://reelcrew.io/site/niche-ac717312.mp4",
            "https://reelcrew.io/site/niche-f13b633c.mp4",
            "https://reelcrew.io/site/niche-ab5b89f7.mp4",
            "https://reelcrew.io/site/niche-202a1560.mp4",
            "https://reelcrew.io/site/niche-d405410e.mp4",
            "https://reelcrew.io/site/niche-dd6c4b62.mp4"
        ]
    },
    {
        "style_id": 18,
        "title": "AI cho doanh nghiệp",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · ai-for-business",
        "description": "Một quy trình làm tay trong doanh nghiệp được AI agent làm thay, kể cho chủ doanh nghiệp không rành công nghệ, phong cách robot vẽ chì.",
        "videos": [
            "https://reelcrew.io/site/ai-inbox-shop.mp4"
        ]
    },
    {
        "style_id": 19,
        "title": "Bán hàng online và bán lẻ",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · ecommerce-retail",
        "description": "Một bài học bán hàng thực tế trên hoá đơn nhiệt dán lên bìa kraft, có mascot hộp các tông.",
        "videos": [
            "https://reelcrew.io/site/lai-that-moi-don.mp4"
        ]
    },
    {
        "style_id": 20,
        "title": "Sửa lỗi tiếng Anh",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · english-learning",
        "description": "2-3 lỗi tiếng Anh người Việt hay mắc: câu sai gạch đi, câu đúng, IPA có chấm trọng âm, kèm câu đố.",
        "videos": [
            "https://reelcrew.io/site/english-3-loi.mp4"
        ]
    },
    {
        "style_id": 21,
        "title": "Giải thích luật mới",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · law-legal",
        "description": "Một luật, nghị định hoặc thông tư mới thay đổi gì, phong cách hồ sơ công văn với mascot cú thư ký.",
        "videos": [
            "https://reelcrew.io/site/nd-356-du-lieu.mp4"
        ]
    },
    {
        "style_id": 22,
        "title": "Mẹo văn phòng",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · office-skills",
        "description": "Một mẹo văn phòng (hàm, phím tắt, mẫu email) từ cách làm chậm tới cách mới, có mascot dập ghim.",
        "videos": [
            "https://reelcrew.io/site/sumif-office.mp4"
        ]
    },
    {
        "style_id": 23,
        "title": "Lịch trình du lịch",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · travel",
        "description": "Một chuyến đi 2-3 ngày theo ngân sách: đi lúc nào, từng ngày, bản đồ tuyến, bảng chi phí cộng đúng, phong cách poster risograph.",
        "videos": [
            "https://reelcrew.io/site/da-lat-48h.mp4"
        ]
    },
    {
        "style_id": 24,
        "title": "Lịch sử Việt Nam",
        "category": "Nội dung thành video diễn giải",
        "skill": "animated-explainer · vietnam-history",
        "description": "Một sự kiện hoặc nhân vật lịch sử Việt Nam theo phong cách tranh khắc gỗ dân gian trên giấy dó, có mascot thư sinh.",
        "videos": [
            "https://reelcrew.io/site/bach-dang-938.mp4"
        ]
    },
    {
        "style_id": 25,
        "title": "Đi qua paper từng mục, giấy kem, sơ đồ dựng dần",
        "category": "Nội dung thành video diễn giải",
        "skill": "article-to-video · paper-walkthrough",
        "description": "Đi qua một bài nghiên cứu từng mục trên nền giấy kem, sơ đồ và biểu đồ dựng dần theo lời đọc.",
        "videos": [
            "https://reelcrew.io/site/paper-walkthrough-ac5486bb.mp4",
            "https://reelcrew.io/site/paper-walkthrough-27387a5e.mp4",
            "https://reelcrew.io/site/attention.mp4"
        ]
    },
    {
        "style_id": 26,
        "title": "Giải thích paper kiểu 3Blue1Brown, công thức dựng theo giọng",
        "category": "Nội dung thành video diễn giải",
        "skill": "article-to-video · paper-3b1b",
        "description": "Giải thích paper kiểu 3Blue1Brown: nền tối, công thức KaTeX và hình dựng từng nét theo giọng.",
        "videos": [
            "https://reelcrew.io/site/paper-3b1b-819163d7.mp4",
            "https://reelcrew.io/site/paper-3b1b-8cd49970.mp4",
            "https://reelcrew.io/site/resnet.mp4"
        ]
    },
    {
        "style_id": 27,
        "title": "Phim tranh khắc cổ cho triết học, lịch sử",
        "category": "Nội dung thành video diễn giải",
        "skill": "article-to-video · engraved-plate",
        "description": "Phim 2–3 phút về triết học, lịch sử bằng tranh khắc thép cổ, con dấu đỏ và phụ đề karaoke.",
        "videos": [
            "https://reelcrew.io/site/engraved-plate-896ad914.mp4",
            "https://reelcrew.io/site/engraved-plate-3e4939ae.mp4",
            "https://reelcrew.io/site/theseus.mp4"
        ]
    },
    {
        "style_id": 28,
        "title": "Phóng sự cắt dán giấy kiểu Vox",
        "category": "Nội dung thành video diễn giải",
        "skill": "article-to-video · vox-collage",
        "description": "Phóng sự cắt dán giấy kiểu Vox: ảnh bán sắc, nhãn giấy xé, dây đỏ ghim, mỗi cảnh tự ghép theo lời.",
        "videos": [
            "https://reelcrew.io/site/vox-collage-dd386ea6.mp4",
            "https://reelcrew.io/site/rosetta.mp4"
        ]
    },
    {
        "style_id": 29,
        "title": "Phim tài liệu tư liệu 8–10 phút",
        "category": "Nội dung thành video diễn giải",
        "skill": "article-to-video · archival-documentary",
        "description": "Phim tài liệu 8–10 phút từ nguồn thật: ảnh lưu trữ có bản quyền, trang báo, mốc thời gian đánh máy.",
        "videos": [
            "https://reelcrew.io/site/archival-documentary-4674e6a6.mp4",
            "https://reelcrew.io/site/archival-documentary-910e5645.mp4",
            "https://reelcrew.io/site/internet-vietnam.mp4"
        ]
    },
    {
        "style_id": 30,
        "title": "Tin nóng bằng ảnh báo, giọng nữ bản tin",
        "category": "Nội dung thành video diễn giải",
        "skill": "article-to-video · news-photo",
        "description": "Tin nóng 40–55 s bằng ảnh báo: kịch bản 6–8 câu, giọng nữ bản tin, tiêu đề cố định và phụ đề 3 chữ.",
        "videos": [
            "https://reelcrew.io/site/news-photo-8072b078.mp4",
            "https://reelcrew.io/site/roman-news.mp4"
        ]
    },
    {
        "style_id": 31,
        "title": "Luyện nghe tiếng Anh: reader, vocab, guess, joke",
        "category": "Nội dung thành video diễn giải",
        "skill": "elearning · listening",
        "description": "Luyện nghe tiếng Anh cho người Việt: đọc truyện, học từ vựng, đoán từ hoặc truyện cười, có song ngữ.",
        "videos": [
            "https://reelcrew.io/site/listening-1bfd0778.mp4",
            "https://reelcrew.io/site/listening-067c51db.mp4",
            "https://reelcrew.io/site/listening-a320eaab.mp4",
            "https://reelcrew.io/site/a-small-step.mp4"
        ]
    },
    {
        "style_id": 32,
        "title": "Bài giảng hoạt hình vẽ tay 3–4 phút từ bài nói",
        "category": "Nội dung thành video diễn giải",
        "skill": "elearning · hand-drawn-lesson",
        "description": "Biến một bài nói thành bài giảng hoạt hình vẽ tay 3–4 phút: ý chính, giải thích, ví dụ, phụ đề.",
        "videos": [
            "https://reelcrew.io/site/hand-drawn-lesson-aa9db0dc.mp4",
            "https://reelcrew.io/site/hand-drawn-lesson-bc13ae1d.mp4",
            "https://reelcrew.io/site/sky-blue.mp4"
        ]
    },
    {
        "style_id": 33,
        "title": "Một cài đặt Excel, con trỏ bấm qua từng giá trị",
        "category": "Nội dung thành video diễn giải",
        "skill": "elearning · excel-setting",
        "description": "Một cài đặt Excel (định dạng số, ngày…) diễn ra trên bảng tính thật, con trỏ bấm qua từng giá trị.",
        "videos": [
            "https://reelcrew.io/site/excel-setting-c9bc9482.mp4",
            "https://reelcrew.io/site/excel-setting-78ac3846.mp4"
        ]
    },
    {
        "style_id": 34,
        "title": "Ra mắt app: câu hỏi + demo trên laptop 3D",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "app-promo · app-launch-studio",
        "description": "Ra mắt app 16:9: một câu hỏi mở đầu rồi demo chạy trên laptop 3D trong studio tối.",
        "videos": [
            "https://reelcrew.io/site/app-launch-studio-c74dd491.mp4",
            "https://reelcrew.io/site/app-launch-studio-7146e88a.mp4",
            "https://reelcrew.io/site/gop-gio.mp4"
        ]
    },
    {
        "style_id": 35,
        "title": "Ra mắt kiểu keynote, thẻ kính mờ nền chàm",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "app-promo · keynote-launch",
        "description": "Ra mắt sản phẩm kiểu keynote: thẻ kính mờ trên nền chàm, nhịp chậm và sang.",
        "videos": [
            "https://reelcrew.io/site/keynote-launch-a63a0c53.mp4",
            "https://reelcrew.io/site/keynote-launch-5d0dd201.mp4"
        ]
    },
    {
        "style_id": 36,
        "title": "Ra mắt website, theme kiểu tạp chí nội thất",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "app-promo · site-launch",
        "description": "Ra mắt website hay theme kiểu tạp chí nội thất: trang thật lướt qua, chữ serif, nhịp nhẹ.",
        "videos": [
            "https://reelcrew.io/site/site-launch-2ce4b0e0.mp4",
            "https://reelcrew.io/site/site-launch-6f1a7e6b.mp4"
        ]
    },
    {
        "style_id": 37,
        "title": "Quảng cáo dải sản phẩm của shop theo nhịp nhạc",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "product-video · product-promo",
        "description": "Quảng cáo cả dải sản phẩm của shop theo nhịp nhạc, giá và tên hiện đúng beat, nhiều phong cách.",
        "videos": [
            "https://reelcrew.io/site/product-promo-effca870.mp4",
            "https://reelcrew.io/site/product-promo-13966fc0.mp4",
            "https://reelcrew.io/site/product-promo-ecec6ea0.mp4"
        ]
    },
    {
        "style_id": 38,
        "title": "Bán nông sản, đặc sản từ ảnh điện thoại",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "product-video · farm-market",
        "description": "Bán nông sản, đặc sản từ ảnh điện thoại của người bán: ấm, mộc, có giá và cách đặt hàng.",
        "videos": [
            "https://reelcrew.io/site/farm-market-bf5b554f.mp4",
            "https://reelcrew.io/site/farm-market-3b67b345.mp4",
            "https://reelcrew.io/site/farm-market-27182a57.mp4",
            "https://reelcrew.io/site/honey-farm.mp4"
        ]
    },
    {
        "style_id": 39,
        "title": "Ảnh dự án + bản đồ vị trí OSM, tuyến đi, tiện ích",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "real-estate-promo · location-map",
        "description": "Ảnh dự án rồi bản đồ OSM nghiêng: khu đất viền sáng, tuyến đi tới tiện ích, vòng bán kính 1 km.",
        "videos": [
            "https://reelcrew.io/site/location-map-6bda0471.mp4",
            "https://reelcrew.io/site/location-map-c0502103.mp4",
            "https://reelcrew.io/site/location-map-b155048a.mp4",
            "https://reelcrew.io/site/ho-tay.mp4",
            "https://reelcrew.io/site/metro-2a.mp4"
        ]
    },
    {
        "style_id": 40,
        "title": "Tuyến metro, cao tốc trên bản đồ vệ tinh",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "real-estate-promo · infra-route",
        "description": "Tuyến metro, cao tốc chạy trên ảnh vệ tinh, từng ga, từng nút giao hiện ra theo lời.",
        "videos": [
            "https://reelcrew.io/site/infra-route-a31e1e02.mp4",
            "https://reelcrew.io/site/infra-route-be54af58.mp4"
        ]
    },
    {
        "style_id": 41,
        "title": "Căn hộ + một chuyến đi tới điểm đến trên bản đồ",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "real-estate-promo · trip-listing",
        "description": "Một căn hộ kèm một chuyến đi thật: đi bộ ra ga, đi tàu từng ga, tổng thời gian tới điểm đến.",
        "videos": [
            "https://reelcrew.io/site/trip-listing-51e8581e.mp4"
        ]
    },
    {
        "style_id": 42,
        "title": "Clip môi giới, ảnh dự án hiện đúng từ được nói (Basic / Pro có bản đồ)",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "real-estate-promo · sales-short",
        "description": "Clip môi giới tự quay, ảnh dự án hiện đúng lúc từ đó được nói (bản Pro có thêm bản đồ).",
        "videos": [
            "https://reelcrew.io/site/sales-short-287b0c74.mp4",
            "https://reelcrew.io/site/sales-short-658d9004.mp4"
        ]
    },
    {
        "style_id": 43,
        "title": "Giới thiệu full dự án từ clip môi giới, 6 nhịp",
        "category": "Giới thiệu sản phẩm, dịch vụ",
        "skill": "real-estate-promo · project-tour",
        "description": "Giới thiệu trọn dự án từ clip môi giới theo 6 nhịp: vị trí, tiện ích, căn mẫu, giá, pháp lý, kêu gọi.",
        "videos": [
            "https://reelcrew.io/site/project-tour-5bf960c8.mp4"
        ]
    },
    {
        "style_id": 44,
        "title": "Showreel giới thiệu cá nhân từ website của họ",
        "category": "Motion quảng cáo, hook",
        "skill": "brand-intro · profile-showreel",
        "description": "Showreel giới thiệu một founder, diễn giả hay chuyên gia, lấy nội dung từ chính website của họ.",
        "videos": [
            "https://reelcrew.io/site/profile-showreel-d406ffe0.mp4",
            "https://reelcrew.io/site/profile-showreel-c6e7a842.mp4",
            "https://reelcrew.io/site/profile-showreel-0c28df2d.mp4",
            "https://reelcrew.io/site/showreel-ho-so.mp4"
        ]
    },
    {
        "style_id": 45,
        "title": "Phim chữ động theo giọng đọc, mỗi cụm một nhịp",
        "category": "Motion quảng cáo, hook",
        "skill": "motion-graphics · voice-kinetic",
        "description": "Phim chữ động theo giọng đọc: mỗi cụm ý một nhịp, chữ đập đúng từ, hợp quảng cáo dịch vụ.",
        "videos": [
            "https://reelcrew.io/site/voice-kinetic-f9022b73.mp4",
            "https://reelcrew.io/site/voice-kinetic-d1c7d5a7.mp4",
            "https://reelcrew.io/site/voice-kinetic-91addfe0.mp4",
            "https://reelcrew.io/site/mot-trang-moi-toi.mp4"
        ]
    },
    {
        "style_id": 46,
        "title": "Bộ hiệu ứng motion phủ lên video có sẵn",
        "category": "Motion quảng cáo, hook",
        "skill": "motion-graphics · motion-fx-kit",
        "description": "Phủ hiệu ứng lên video có sẵn: thẻ chữ, chữ sau lưng người nói, glitch, chia màn hình, karaoke.",
        "videos": [
            "https://reelcrew.io/site/motion-fx-kit-bb04d0cb.mp4"
        ]
    },
    {
        "style_id": 47,
        "title": "Quảng cáo truyện tranh sôi động, starburst trên drop",
        "category": "Motion quảng cáo, hook",
        "skill": "video-ads · comic-hype",
        "description": "Quảng cáo truyện tranh sôi động: starburst, khung truyện, chữ to bùng lên đúng drop của nhạc.",
        "videos": [
            "https://reelcrew.io/site/comic-hype-89c8c3e7.mp4",
            "https://reelcrew.io/site/comic-hype-a54e5e2c.mp4",
            "https://reelcrew.io/site/comic-hype-e5ddc95c.mp4",
            "https://reelcrew.io/site/pantry-hype.mp4"
        ]
    },
    {
        "style_id": 48,
        "title": "Quảng cáo khoá học, webinar dạng phiếu việc",
        "category": "Motion quảng cáo, hook",
        "skill": "video-ads · course-ad",
        "description": "Quảng cáo khoá học hay webinar dạng phiếu công việc: vấn đề, lịch học, lợi ích, nút đăng ký.",
        "videos": [
            "https://reelcrew.io/site/course-ad-69fde0b9.mp4",
            "https://reelcrew.io/site/course-ad-2232c0d9.mp4"
        ]
    },
    {
        "style_id": 49,
        "title": "Phụ đề karaoke từng chữ",
        "category": "Người nói, quay thực tế",
        "skill": "subtitles-captions · karaoke",
        "description": "Phụ đề karaoke: từng chữ sáng lên đúng lúc được nói, có sửa thuật ngữ.",
        "videos": [
            "https://reelcrew.io/site/karaoke-1e6a2406.mp4",
            "https://reelcrew.io/site/karaoke-captions.mp4"
        ]
    },
    {
        "style_id": 50,
        "title": "File phụ đề SRT",
        "category": "Người nói, quay thực tế",
        "skill": "subtitles-captions · srt",
        "description": "Xuất file phụ đề SRT chuẩn thời gian từ video, tiếng Việt hoặc tiếng Anh, để đăng YouTube, Facebook.",
        "videos": [
            "https://reelcrew.io/site/srt-cf7c9bc0.mp4"
        ]
    },
    {
        "style_id": 51,
        "title": "Phụ đề theo cụm, 2 dòng cân",
        "category": "Người nói, quay thực tế",
        "skill": "subtitles-captions · phrase",
        "description": "Phụ đề theo cụm, 2 dòng cân, dễ đọc trên điện thoại.",
        "videos": [
            "https://reelcrew.io/site/phrase-8c7ecf1d.mp4"
        ]
    },
    {
        "style_id": 52,
        "title": "Short nổi bật có thiết kế motion-fx",
        "category": "Người nói, quay thực tế",
        "skill": "talking-head · highlight",
        "description": "Short nổi bật từ clip người nói: cắt đoạn đắt, khung bám mặt, thẻ chữ và hiệu ứng motion.",
        "videos": [
            "https://reelcrew.io/site/highlight-b694e07e.mp4",
            "https://reelcrew.io/site/highlight-8dd7cd16.mp4"
        ]
    },
    {
        "style_id": 53,
        "title": "Người nói cắt dán giấy, chữ đập theo từ",
        "category": "Người nói, quay thực tế",
        "skill": "talking-head · collage",
        "description": "Người nói tách nền đặt trên giấy cắt dán, chữ đập theo từ, hợp nội dung kể chuyện, quan điểm.",
        "videos": [
            "https://reelcrew.io/site/collage-7796f95f.mp4",
            "https://reelcrew.io/site/collage-404f0af0.mp4",
            "https://reelcrew.io/site/collage-f6a6b569.mp4"
        ]
    },
    {
        "style_id": 54,
        "title": "Sơ đồ nét lớn dần cạnh bong bóng mặt",
        "category": "Người nói, quay thực tế",
        "skill": "talking-head · diagram",
        "description": "Sơ đồ nét lớn dần bên cạnh bong bóng mặt người nói, minh hoạ đúng ý đang nói.",
        "videos": [
            "https://reelcrew.io/site/diagram-3d872cee.mp4",
            "https://reelcrew.io/site/diagram-b853a776.mp4",
            "https://reelcrew.io/site/diagram-44081e47.mp4",
            "https://reelcrew.io/site/talking-head-diagram.mp4"
        ]
    },
    {
        "style_id": 55,
        "title": "Short dựng kỹ: grade, phụ đề hoặc keyword, tiêu đề sau đầu",
        "category": "Người nói, quay thực tế",
        "skill": "talking-head · edited-short",
        "description": "Short dựng kỹ: chỉnh màu, phụ đề hoặc keyword, tiêu đề phía sau đầu, chèn hình minh hoạ.",
        "videos": [
            "https://reelcrew.io/site/edited-short-87807e3f.mp4",
            "https://reelcrew.io/site/edited-short-dbf26bca.mp4"
        ]
    },
    {
        "style_id": 56,
        "title": "Cắt nhanh ậm ừ, khoảng lặng, ra short 9:16",
        "category": "Người nói, quay thực tế",
        "skill": "video-editing · fast-cut",
        "description": "Cắt nhanh chỉ bằng ffmpeg: bỏ ậm ừ, khoảng lặng, câu nói lại, ra một short 9:16 sạch.",
        "videos": [
            "https://reelcrew.io/site/fast-cut-a345e274.mp4",
            "https://reelcrew.io/site/fast-cut-2e5e6829.mp4"
        ]
    },
    {
        "style_id": 57,
        "title": "Bản dài sạch giữ khung gốc + SRT",
        "category": "Người nói, quay thực tế",
        "skill": "video-editing · long-clean",
        "description": "Bản dài sạch giữ nguyên khung gốc: bỏ khoảng lặng và từ đệm, kèm file SRT.",
        "videos": [
            "https://reelcrew.io/site/long-clean-bb5945e7.mp4",
            "https://reelcrew.io/site/long-clean-ai.mp4"
        ]
    },
    {
        "style_id": 58,
        "title": "Bài giảng sơ đồ giấy kem dựng theo lời + bong bóng mặt",
        "category": "Bài giảng, sự kiện dài",
        "skill": "lecture-video · slide-diagram",
        "description": "Bài giảng với sơ đồ giấy kem dựng theo lời giảng, bong bóng mặt người giảng ở góc.",
        "videos": [
            "https://reelcrew.io/site/slide-diagram-1af52361.mp4"
        ]
    },
    {
        "style_id": 59,
        "title": "Sơ đồ giấy kem",
        "category": "Bài giảng, sự kiện dài",
        "skill": "lecture-video · paper",
        "description": "Một bài nói trước máy quay thành video 16:9 dài có chương và short 9:16, sơ đồ nét vẽ hiện đúng chữ người nói, theo look sơ đồ giấy kem: bài học điềm tĩnh, lời khuyên, chủ đề chưa rõ hợp look nào.",
        "videos": [
            "https://reelcrew.io/site/lecture-ai.mp4"
        ]
    },
    {
        "style_id": 60,
        "title": "Nhiều short từ một bản ghi dài",
        "category": "Bài giảng, sự kiện dài",
        "skill": "video-repurposing · highlight-short",
        "description": "Từ một bản ghi dài, lấy ra nhiều short highlight, mỗi short một ý trọn vẹn.",
        "videos": [
            "https://reelcrew.io/site/highlight-short-9a374c42.mp4",
            "https://reelcrew.io/site/short-ai.mp4"
        ]
    },
    {
        "style_id": 61,
        "title": "Bản ghi share màn hình thành bản dài có chương + short + recap",
        "category": "Bài giảng, sự kiện dài",
        "skill": "video-repurposing · screen-share",
        "description": "Bản ghi Zoom/Meet share màn hình thành cả bộ: bản dài có chương, short dọc, bài tóm tắt.",
        "videos": [
            "https://reelcrew.io/site/screen-share-ddf04497.mp4"
        ]
    }
]

def download_one(url: str, dest: Path) -> tuple[str, bool, int, str]:
    if dest.exists() and dest.stat().st_size > 1024:
        return (dest.name, True, dest.stat().st_size, "cached")
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://reelcrew.io/video-mau",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            data = resp.read()
        tmp = dest.with_suffix(".part")
        tmp.write_bytes(data)
        tmp.replace(dest)
        return (dest.name, True, len(data), "downloaded")
    except Exception as exc:
        return (dest.name, False, 0, str(exc))


def main() -> int:
    TARGET_DIR.mkdir(parents=True, exist_ok=True)

    unique_urls: dict[str, Path] = {}
    for st in STYLES_DATA:
        for url in st["videos"]:
            fname = url.rsplit("/", 1)[-1]
            unique_urls[url] = TARGET_DIR / fname

    print(f"Found {len(STYLES_DATA)} styles and {len(unique_urls)} unique MP4 URLs.")
    results: dict[str, dict] = {}
    failures = 0

    with ThreadPoolExecutor(max_workers=8) as pool:
        fut_map = {pool.submit(download_one, url, dest): url for url, dest in unique_urls.items()}
        for i, fut in enumerate(as_completed(fut_map), 1):
            url = fut_map[fut]
            fname, ok, size, status = fut.result()
            results[url] = {"filename": fname, "ok": ok, "size_bytes": size, "status": status}
            if ok:
                print(f"[{i:03d}/{len(unique_urls):03d}] OK ({status}) {fname} ({size / 1024 / 1024:.2f} MB)")
            else:
                failures += 1
                print(f"[{i:03d}/{len(unique_urls):03d}] FAIL {fname}: {status}", file=sys.stderr)

    catalog = {
        "source_url": "https://reelcrew.io/video-mau",
        "target_dir": str(TARGET_DIR),
        "total_styles": len(STYLES_DATA),
        "total_unique_videos": len(unique_urls),
        "failed_downloads": failures,
        "styles": [],
    }

    md_lines = [
        "# ReelCrew Video Samples Catalog (`https://reelcrew.io/video-mau`)",
        "",
        f"- **Thư mục lưu trữ:** `{TARGET_DIR}`",
        f"- **Tổng số Styles / Templates:** `{len(STYLES_DATA)}`",
        f"- **Tổng số Video `.mp4` tải về:** `{len(unique_urls) - failures}/{len(unique_urls)}`",
        "",
        "| # | Style Title | Category | Skill Tag | Videos (Local File) |",
        "|---:|---|---|---|---|",
    ]

    for st in STYLES_DATA:
        local_files = []
        for u in st["videos"]:
            info = results.get(u, {})
            fname = info.get("filename", u.rsplit("/", 1)[-1])
            local_path = TARGET_DIR / fname
            local_files.append(
                {
                    "url": u,
                    "filename": fname,
                    "local_path": str(local_path),
                    "size_bytes": info.get("size_bytes", 0),
                    "ok": info.get("ok", False),
                }
            )
        entry = {**st, "local_videos": local_files}
        catalog["styles"].append(entry)
        v_links = ", ".join(f"[`{v['filename']}`](file:///{Path(v['local_path']).as_posix()})" for v in local_files)
        md_lines.append(
            f"| {st['style_id']} | **{st['title']}** — {st['description']} | {st['category']} | `{st['skill']}` | {v_links} |"
        )

    (TARGET_DIR / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2), encoding="utf-8")
    (TARGET_DIR / "CATALOG.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    print(f"\nSaved catalog.json and CATALOG.md in {TARGET_DIR}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

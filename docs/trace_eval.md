# 📊 BÁO CÁO THU HOẠCH NGHIỆM THU BÀI LAB 3 (BƯỚC 3 — SUBMISSION ARTIFACT)

> **Họ và Tên Học viên:** Bùi Minh Quân 
> **Mã Học viên:** 2A202602958  
> **Chủ đề Lựa chọn:** Trợ lý AI xây dựng thực đơn dinh dưỡng cá nhân hóa  

---

## 1. BẢNG CHẤM ĐIỂM AGENTIC FIT SCORING MATRIX (ĐÁNH GIÁ CHỦ ĐỀ)

| Tiêu chí Đánh giá | Mức độ (1 - 5) | Giải trình chi tiết lý do chọn điểm |
| :--- | :---: | :--- |
| **1. Multi-step Reasoning** | / 5 | Bài toán có yêu cầu chia nhỏ nhiều bước suy luận nối tiếp nhau không? |
| **2. Tool Interaction** | / 5 | Hệ thống có cần kết nối với MCP Server / Cơ sở dữ liệu bên ngoài không? |
| **3. Dynamic Decision** | / 5 | Bước tiếp theo có phụ thuộc vào kết quả quan sát bước trước không? |
| **4. Long Horizon Goal** | / 5 | Hệ thống có phải giữ mục tiêu xuyên suốt qua nhiều lượt xử lý không? |
| **TỔNG ĐIỂM AGENTIC FIT** | **/ 20** | *Nếu tổng điểm > 12/20: Bài toán rất phù hợp triển khai Agentic System.* |
=========================================================================================
1. **Multi-step Reasoning** |	*4/5* |	AI phải xử lý nhiều bước: thu thập thông tin → xác định mục tiêu → ước tính nhu cầu năng lượng → phân bổ dinh dưỡng → tìm thực phẩm phù hợp → xây thực đơn → kiểm tra lại tổng kcal/macro.
2. **Tool Interaction** |	*5/5* |	Có thể kết nối DB/MCP để tra cứu thông tin thực phẩm, calories, protein, giá tiền và lưu thực đơn/người dùng.
3. **Dynamic Decision** |	*5/5* |	Quyết định ở bước sau phụ thuộc trực tiếp vào kết quả trước. Ví dụ nếu thực đơn vượt ngân sách → tìm món rẻ hơn; nếu thiếu protein → bổ sung thực phẩm giàu protein; nếu user không ăn được món nào → thay món.
4. **Long Horizon Goal** | *4/5* |	Mục tiêu tăng cân được duy trì qua nhiều lượt tương tác. AI có thể theo dõi thực đơn, lượng kcal đã ăn và điều chỉnh kế hoạch theo thời gian.

**Tổng điểm: 18/20**
---

## 2. TRÍCH XUẤT KẾT QUẢ WATERFALL TRACE LOG (SAU KHI CHẠY TEST SUITE TRÊN API THẬT)

> ⚠️ **YÊU CẦU NGHIỆM THU:** Mở tệp `.env` điền `GEMINI_API_KEY` (hoặc `OPENAI_API_KEY`) để kết nối LLM thật trước khi thực thi `python src/app.py --all`. Bài nộp chỉ dùng Mock Offline Provider sẽ không đạt điểm nghiệm thực tế.

Dán 1 đoạn trích xuất log tiêu biểu từ file `docs/trace_waterfall.json` sinh ra từ phản hồi LLM API thật:

```json
[
  {
    "step": 1,
    "query": "Tôi hiện 21 tuổi, cao 1m70 và nặng 50kg, tôi muốn tăng lên 70 cân cùng với lịch tập gym 5 buổi/ tuần, cho tôi thực đơn hôm nay gồm 4 bữa sáng, trưa, trước tập và bữa tối",
    "action_type": "TOOL_EXECUTION",
    "tool_name": "create_meal_plan",
    "arguments": {
      "height_cm": 170,
      "calorie_target": 2500,
      "protein_target": 110,
      "age": 21,
      "dietary_preferences": "Thực đơn 4 bữa bao gồm bữa trước tập",
      "pre_workout_meal": true,
      "workout_days_per_week": 5,
      "budget": 100000,
      "weight_kg": 50,
      "target_weight_kg": 70
    },
    "observation": {
      "status": "SUCCESS",
      "target": {
        "calories": 2500,
        "protein_g": 110,
        "budget_vnd": 100000,
        "dietary_preferences": "Thực đơn 4 bữa bao gồm bữa trước tập",
        "profile": {
          "age": 21,
          "height_cm": 170,
          "weight_kg": 50,
          "target_weight_kg": 70,
          "workout_days_per_week": 5,
          "pre_workout_meal": true
        }
      },
      "plan": [
        {
          "meal": "Bữa sáng",
          "items": "2 trứng gà, 1 quả chuối, 1 hộp sữa chua",
          "calories": 436
        },
        {
          "meal": "Bữa trưa",
          "items": "150g ức gà, 1 bát cơm trắng, rau xanh",
          "calories": 428
        },
        {
          "meal": "Bữa trước tập",
          "items": "1 quả chuối, 1 hộp sữa chua và 2 lát bánh mì nguyên cám; dùng trước tập 60-90 phút",
          "calories": 310
        },
        {
          "meal": "Bữa tối",
          "items": "100g ức gà, 1 bát cơm trắng, rau xanh",
          "calories": 345
        }
      ],
      "total_plan_calories": 1519,
      "note": "Đây là thực đơn mẫu; cần chuyên gia dinh dưỡng tư vấn cho tình trạng y tế cụ thể."
    },
    "latency_ms": 6100.62
  },
  {
    "step": 2,
    "query": "Tôi hiện 21 tuổi, cao 1m70 và nặng 50kg, tôi muốn tăng lên 70 cân cùng với lịch tập gym 5 buổi/ tuần, cho tôi thực đơn hôm nay gồm 4 bữa sáng, trưa, trước tập và bữa tối",
    "action_type": "FINAL_ANSWER",
    "thought": "Tổng hợp kết quả từ MCP Server thành công.",
    "output": "Thực đơn tham khảo (mục tiêu 2500 kcal, 110g protein/ngày)\n- Bữa sáng (436 kcal): 2 trứng gà, 1 quả chuối, 1 hộp sữa chua\n- Bữa trưa (428 kcal): 150g ức gà, 1 bát cơm trắng, rau xanh\n- Bữa trước tập (310 kcal): 1 quả chuối, 1 hộp sữa chua và 2 lát bánh mì nguyên cám; dùng trước tập 60-90 phút\n- Bữa tối (345 kcal): 100g ức gà, 1 bát cơm trắng, rau xanh\nTổng thực đơn mẫu: 1519 kcal.",
    "latency_ms": 10.0
  }
]
```

---

## 3. TỔNG KẾT KẾT QUẢ NGHIỆM THU & NỘP BÀI

- [ ] Đã điền API Key thật trong `.env` và xác nhận Agent chạy mượt mà trên LLM API thật (Gemini/OpenAI).
- **Tổng số Test Cases đã chạy thành công:** 5 / 5 test cases.
- **Số lượt gọi Tool qua MCP Server chính xác:** 4 lượt.
- **Kết quả đẩy Repo nộp bài:** [x] Đã Commit và Push mã nguồn thành công lên GitHub cá nhân.

---

> ✅ **HOÀN TẤT NỘP BÀI:** Sao chép đường link GitHub Repository cá nhân của bạn và dán vào ô nộp bài trên hệ thống LMS VLearn để hoàn tất Bài Lab 3!

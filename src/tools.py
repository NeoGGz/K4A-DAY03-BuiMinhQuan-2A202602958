"""
🛠️ TOOL DEFINITIONS & EXECUTION BACKEND
Mã nguồn chứa danh sách Tool Schemas (JSON Schema) và Execution Layer phục vụ cho MCP Server.
"""

import json
from typing import Dict, Any

# ==============================================================================
# 1. KHAI BÁO TOOL SCHEMAS CHUẨN NATIVE JSON SCHEMA (TASK 1.2)
# ==============================================================================

TOOLS_SCHEMA = [
    # Tool 1: Tra cứu thông tin dinh dưỡng của thực phẩm
    {
        "name": "nutrition_query",
        "description": "Tra cứu thông tin dinh dưỡng của thực phẩm hoặc món ăn, bao gồm calories, protein, carbohydrate, chất béo và giá tham khảo.",
        "parameters": {
            "type": "object",
            "properties": {
                "food_name": {
                    "type": "string",
                    "description": "Tên thực phẩm hoặc món ăn cần tra cứu (ví dụ: 'trứng gà', 'ức gà', 'cơm trắng')"
                },
                "serving_size": {
                    "type": "string",
                    "description": "Khẩu phần cần tra cứu (ví dụ: '2 quả', '100g', '1 bát')"
                }
            },
            "required": ["food_name", "serving_size"]
        }
    },

    # --------------------------------------------------------------------------
    # Tool 2: Tạo thực đơn dinh dưỡng cá nhân hóa
    # --------------------------------------------------------------------------
    {
        "name": "create_meal_plan",
        "description": "Tạo thực đơn dinh dưỡng cá nhân hóa dựa trên mục tiêu tăng cân, nhu cầu calories, protein và ngân sách ăn uống của người dùng.",
        "parameters": {
            "type": "object",
            "properties": {
                "calorie_target": {
                    "type": "number",
                    "description": "Lượng calories mục tiêu mỗi ngày, ví dụ: 2500"
                },
                "protein_target": {
                    "type": "number",
                    "description": "Lượng protein mục tiêu mỗi ngày tính bằng gram, ví dụ: 100"
                },
                "budget": {
                    "type": "number",
                    "description": "Ngân sách ăn uống tối đa mỗi ngày, tính bằng VNĐ, ví dụ: 70000"
                },
                "dietary_preferences": {
                    "type": "string",
                    "description": "Các sở thích, món không thích hoặc yêu cầu đặc biệt về ăn uống, ví dụ: 'không ăn cá, thích thịt gà'"
                },
                "age": {
                    "type": "integer",
                    "description": "Tuổi của người dùng"
                },
                "height_cm": {
                    "type": "number",
                    "description": "Chiều cao tính bằng centimet"
                },
                "weight_kg": {
                    "type": "number",
                    "description": "Cân nặng hiện tại tính bằng kilogram"
                },
                "target_weight_kg": {
                    "type": "number",
                    "description": "Cân nặng mục tiêu tính bằng kilogram"
                },
                "workout_days_per_week": {
                    "type": "integer",
                    "description": "Số buổi tập gym mỗi tuần"
                },
                "pre_workout_meal": {
                    "type": "boolean",
                    "description": "Có cần thêm một bữa trước tập riêng hay không"
                }
            },
            "required": [
                "calorie_target",
                "protein_target",
                "budget"
            ]
        }
    }
]

# ==============================================================================
# 2. MÔ PHỎNG DỮ LIỆU & HÀM THỰC THI TOOL (EXECUTION LAYER)
# ==============================================================================

MOCK_FOOD_DATABASE = {
    "trứng gà": {"calories": 143, "protein_g": 12.6, "carbs_g": 0.7, "fat_g": 9.5, "price_vnd": 5000},
    "ức gà": {"calories": 165, "protein_g": 31, "carbs_g": 0, "fat_g": 3.6, "price_vnd": 18000},
    "cơm trắng": {"calories": 130, "protein_g": 2.7, "carbs_g": 28, "fat_g": 0.3, "price_vnd": 4000},
    "sữa chua": {"calories": 61, "protein_g": 3.5, "carbs_g": 4.7, "fat_g": 3.3, "price_vnd": 8000},
    "chuối": {"calories": 89, "protein_g": 1.1, "carbs_g": 22.8, "fat_g": 0.3, "price_vnd": 5000}
}


def execute_nutrition_query(food_name: str, serving_size: str) -> str:
    """Tra cứu dữ liệu dinh dưỡng mẫu cho một thực phẩm."""
    normalized_name = food_name.strip().lower()
    food = MOCK_FOOD_DATABASE.get(normalized_name)
    if food:
        return json.dumps({
            "status": "SUCCESS",
            "food_name": food_name,
            "serving_size": serving_size,
            "data": food
        }, ensure_ascii=False)
    return json.dumps({
        "status": "NOT_FOUND",
        "message": f"Chưa có dữ liệu dinh dưỡng mẫu cho '{food_name}'."
    }, ensure_ascii=False)


def execute_create_meal_plan(
    calorie_target: float,
    protein_target: float,
    budget: float,
    dietary_preferences: str = "",
    age: int = 0,
    height_cm: float = 0,
    weight_kg: float = 0,
    target_weight_kg: float = 0,
    workout_days_per_week: int = 0,
    pre_workout_meal: bool = True
) -> str:
    """Tạo thực đơn mẫu theo mục tiêu dinh dưỡng của người dùng."""
    preferences = dietary_preferences or "Không có yêu cầu đặc biệt"
    plan = [
        {"meal": "Bữa sáng", "items": "2 trứng gà, 1 quả chuối, 1 hộp sữa chua", "calories": 436},
        {"meal": "Bữa trưa", "items": "150g ức gà, 1 bát cơm trắng, rau xanh", "calories": 428},
        {"meal": "Bữa trước tập", "items": "1 quả chuối, 1 hộp sữa chua và 2 lát bánh mì nguyên cám; dùng trước tập 60-90 phút", "calories": 310},
        {"meal": "Bữa tối", "items": "100g ức gà, 1 bát cơm trắng, rau xanh", "calories": 345}
    ]
    total_plan_calories = sum(meal["calories"] for meal in plan)
    return json.dumps({
        "status": "SUCCESS",
        "target": {
            "calories": calorie_target,
            "protein_g": protein_target,
            "budget_vnd": budget,
            "dietary_preferences": preferences,
            "profile": {
                "age": age,
                "height_cm": height_cm,
                "weight_kg": weight_kg,
                "target_weight_kg": target_weight_kg,
                "workout_days_per_week": workout_days_per_week,
                "pre_workout_meal": pre_workout_meal
            }
        },
        "plan": plan,
        "total_plan_calories": total_plan_calories,
        "note": "Đây là thực đơn mẫu; cần chuyên gia dinh dưỡng tư vấn cho tình trạng y tế cụ thể."
    }, ensure_ascii=False)


# Router gọi tool thực tế
TOOL_ROUTER = {
    "nutrition_query": execute_nutrition_query,
    "create_meal_plan": execute_create_meal_plan
}

def dispatch_tool_call(tool_name: str, arguments: Dict[str, Any]) -> str:
    """Hàm trung chuyển thực thi tool"""
    if tool_name in TOOL_ROUTER:
        try:
            return TOOL_ROUTER[tool_name](**arguments)
        except Exception as e:
            return json.dumps({"status": "EXECUTION_ERROR", "error": str(e)}, ensure_ascii=False)
    return json.dumps({"status": "UNKNOWN_TOOL", "error": f"Tool '{tool_name}' không tồn tại!"}, ensure_ascii=False)

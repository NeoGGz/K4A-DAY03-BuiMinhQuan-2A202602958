"""
📚 [REFERENCE ONLY / CODE MẪU THAM KHẢO]
🧠 CẤP ĐỘ 3: NATIVE MCP AGENT (Native Tool Calling + MCP Server Integration)
⚠️ Lưu ý: File này chỉ dùng để đọc tham khảo kiến trúc. Không chỉnh sửa hay debug file này.
"""

import json

def get_weather(city: str) -> str:
    return f"Thời tiết {city}: 28°C, Nắng nhẹ."

def run_level3_demo():
    print("=== DEMO CẤP ĐỘ 3: NATIVE MCP AGENT ===")
    user_goal = "Tra cứu thông tin dinh dưỡng của 100g ức gà"
    print(f"🎯 Goal: {user_goal}")
    print("🧠 [Thought]: Phát sinh Native Tool Call 'nutrition_query'...")
    print("🛠️ [Native Tool Call]: nutrition_query({'food_name': 'ức gà', 'serving_size': '100g'})")
    print("👁️ [MCP Server Observation]: {'food_name': 'ức gà', 'calories': 165, 'protein_g': 31}")
    print("🏁 [Final Answer]: 100g ức gà có khoảng 165 kcal và 31g protein.")

if __name__ == "__main__":
    run_level3_demo()

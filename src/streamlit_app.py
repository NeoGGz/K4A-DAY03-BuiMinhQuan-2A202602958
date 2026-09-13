"""Streamlit UI for the personalized nutrition ReAct assistant."""

import json
import os
import sys

import streamlit as st

APP_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(APP_DIR)
if APP_DIR not in sys.path:
    sys.path.insert(0, APP_DIR)

from app import run_react_agent, save_waterfall_trace
from mcp_server import MCPNutritionServer
from providers import get_llm_provider


st.set_page_config(
    page_title="Nourish | Trợ lý dinh dưỡng",
    page_icon=":material/restaurant:",
    layout="wide",
    initial_sidebar_state="expanded",
)


SUGGESTIONS = {
    "Tạo thực đơn 4 bữa": "Tôi 21 tuổi, cao 170 cm, nặng 50 kg, muốn tăng lên 70 kg, tập 5 buổi mỗi tuần và muốn thực đơn hôm nay gồm sáng, trưa, trước tập và tối.",
    "Tra cứu ức gà": "100g ức gà có bao nhiêu calories và protein?",
    "Ăn theo lịch tập": "Hãy tạo thực đơn giàu protein với một bữa trước tập riêng, sử dụng các món dễ chuẩn bị.",
}


def initialize_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_plan" not in st.session_state:
        st.session_state.last_plan = None
    if "trace" not in st.session_state:
        st.session_state.trace = []
    if "profile" not in st.session_state:
        st.session_state.profile = {
            "age": None,
            "height_cm": None,
            "weight_kg": None,
            "target_weight_kg": None,
            "workout_days_per_week": None,
            "calorie_target": None,
            "protein_target": None,
            "budget": None,
            "dietary_preferences": "",
        }


def build_context(profile):
    return (
        "\n\nThông tin hồ sơ người dùng do giao diện cung cấp: "
        f"tuổi {profile['age']}, cao {profile['height_cm']} cm, "
        f"nặng {profile['weight_kg']} kg, mục tiêu {profile['target_weight_kg']} kg, "
        f"tập gym {profile['workout_days_per_week']} buổi/tuần, "
        f"mục tiêu calories: {profile['calorie_target'] if profile['calorie_target'] else 'chưa xác định, hãy tự ước tính'}, "
        f"protein: {profile['protein_target'] if profile['protein_target'] else 'chưa xác định, hãy tự ước tính'}, "
        f"ngân sách: {f'{profile["budget"]:,} VNĐ/ngày' if profile['budget'] else 'chưa xác định, hãy tối ưu theo mức hợp lý'}, "
        f"sở thích: {profile['dietary_preferences'] or 'không có'}."
        " Nếu người dùng yêu cầu thực đơn, hãy tạo đúng 4 bữa gồm sáng, trưa, trước tập và tối."
    )


def extract_plan(trace):
    for event in reversed(trace):
        observation = event.get("observation", {})
        if event.get("action_type") == "TOOL_EXECUTION" and "plan" in observation:
            return observation
    return None


def render_plan(plan_data):
    if not plan_data:
        return
    target = plan_data.get("target", {})
    st.subheader("Thực đơn hôm nay", icon=":material/today:")
    st.caption(
        f"Mục tiêu {target.get('calories', 0):,.0f} kcal · "
        f"{target.get('protein_g', 0):,.0f}g protein · "
        f"Tổng mẫu {plan_data.get('total_plan_calories', 0):,.0f} kcal"
    )
    progress = plan_data.get("progress_estimate", {})
    if progress.get("status") == "ESTIMATED":
        st.info(
            f"Dự kiến đạt mục tiêu sau khoảng **{progress['estimated_weeks']} tuần "
            f"({progress['estimated_months']} tháng)** nếu duy trì đều. "
            f"Tốc độ ước tính: {progress['expected_gain_kg_per_week']} kg/tuần.",
            icon=":material/timeline:"
        )
    elif progress.get("message"):
        st.warning(progress["message"], icon=":material/warning:")
    for meal in plan_data.get("plan", []):
        with st.container(border=True):
            left, right = st.columns([4, 1], vertical_alignment="center")
            with left:
                st.markdown(f"**{meal['meal']}**")
                st.write(meal["items"])
            with right:
                st.metric("Calories", f"{meal.get('calories', 0):,.0f} kcal")


def render_trace(trace):
    if not trace:
        return
    with st.expander("Hoạt động MCP", icon=":material/account_tree:"):
        for event in trace:
            if event.get("action_type") == "TOOL_EXECUTION":
                st.status(
                    f"Gọi tool · {event.get('tool_name', 'không rõ')}",
                    state="complete",
                    expanded=False,
                )
                st.caption(f"Tham số: {json.dumps(event.get('arguments', {}), ensure_ascii=False)}")


initialize_state()
profile = st.session_state.profile

with st.sidebar:
    st.markdown("### :material/restaurant: Nourish")
    st.caption("Trợ lý dinh dưỡng cá nhân")
    st.badge("MCP đã kết nối", icon=":material/check_circle:", color="green")

    with st.form("profile_form", border=True):
        st.subheader("Hồ sơ của bạn", icon=":material/person:")
        profile["age"] = st.number_input("Tuổi *", min_value=13, max_value=100, value=profile["age"], placeholder="Bắt buộc nhập")
        profile["height_cm"] = st.number_input("Chiều cao (cm) *", min_value=100.0, max_value=230.0, value=profile["height_cm"], placeholder="Bắt buộc nhập")
        profile["weight_kg"] = st.number_input("Cân nặng hiện tại (kg) *", min_value=25.0, max_value=300.0, value=profile["weight_kg"], placeholder="Bắt buộc nhập")
        profile["target_weight_kg"] = st.number_input("Cân nặng mục tiêu (kg) *", min_value=25.0, max_value=300.0, value=profile["target_weight_kg"], placeholder="Bắt buộc nhập")
        profile["workout_days_per_week"] = st.number_input("Số buổi gym / tuần *", min_value=0, max_value=7, value=profile["workout_days_per_week"], placeholder="Bắt buộc nhập")
        profile["calorie_target"] = st.number_input("Mục tiêu calories mỗi ngày (không bắt buộc)", min_value=1000, max_value=6000, value=profile["calorie_target"], step=50, placeholder="Để trống để trợ lý tự ước tính")
        profile["protein_target"] = st.number_input("Mục tiêu protein mỗi ngày (g, không bắt buộc)", min_value=30, max_value=400, value=profile["protein_target"], step=5, placeholder="Để trống để trợ lý tự ước tính")
        profile["budget"] = st.number_input("Ngân sách mỗi ngày (không bắt buộc)", min_value=0, max_value=1000000, value=profile["budget"], step=10000, placeholder="Để trống để trợ lý tự chọn mức hợp lý")
        profile["dietary_preferences"] = st.text_area("Sở thích ăn uống", value=profile["dietary_preferences"], placeholder="Không ăn cá, thích món dễ nấu...")
        if st.form_submit_button("Lưu hồ sơ", type="primary", icon=":material/save:"):
            required_profile = ["age", "height_cm", "weight_kg", "target_weight_kg", "workout_days_per_week"]
            if any(profile[field] is None for field in required_profile):
                st.error("Vui lòng nhập đầy đủ thông tin sức khỏe bắt buộc (*).")
            else:
                st.session_state.profile = profile
                st.toast("Đã lưu hồ sơ", icon=":material/check:")

    st.space("small")
    if st.button("Xóa cuộc trò chuyện", icon=":material/delete_sweep:", width="stretch"):
        st.session_state.messages = []
        st.session_state.last_plan = None
        st.session_state.trace = []
        st.rerun()

st.title("Xây dựng một ngày ăn uống tốt hơn", anchor=False)
st.write("Không gian dinh dưỡng tập trung vào thể trạng, lịch tập và thói quen của bạn.")

required_profile = ["age", "height_cm", "weight_kg", "target_weight_kg", "workout_days_per_week"]
profile_complete = all(profile[field] is not None for field in required_profile)
if not profile_complete:
    st.warning("Hãy nhập và lưu tuổi, chiều cao, cân nặng, cân nặng mục tiêu và số buổi tập trước khi yêu cầu thực đơn.", icon=":material/priority_high:")

chat_col, plan_col = st.columns([1.45, 1], gap="large")

with chat_col:
    if not st.session_state.messages:
        with st.container(border=True):
            st.subheader("Hôm nay bạn muốn lên kế hoạch gì?", icon=":material/auto_awesome:")
            st.write("Cho tôi biết mục tiêu, món bạn thích và thời gian tập. Bữa trước tập sẽ luôn được hiển thị riêng.")
            selected = st.pills("Bắt đầu với một gợi ý", list(SUGGESTIONS), label_visibility="collapsed")
            if selected:
                st.session_state.pending_prompt = SUGGESTIONS[selected]
                st.rerun()

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=":material/person:" if message["role"] == "user" else ":material/restaurant:"):
            st.markdown(message["content"])
            if message.get("trace"):
                render_trace(message["trace"])

    pending_prompt = st.session_state.pop("pending_prompt", None)
    prompt = st.chat_input("Hỏi về thực đơn, dinh dưỡng hoặc điều chỉnh theo ngày tập", submit_mode="disable")
    prompt = prompt or pending_prompt

    if prompt:
        if not profile_complete:
            st.error("Chưa thể tạo thực đơn: bạn cần hoàn thành hồ sơ sức khỏe ở thanh bên.")
            st.stop()
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar=":material/person:"):
            st.markdown(prompt)

        provider = get_llm_provider()
        server = MCPNutritionServer()
        with st.chat_message("assistant", avatar=":material/restaurant:"):
            with st.status("Đang phân tích kế hoạch dinh dưỡng", type="compact") as status:
                trace = run_react_agent(prompt + build_context(profile), provider, server)
                status.update(label="Đã hoàn tất thực đơn", state="complete")
            final_event = next((event for event in reversed(trace) if event.get("action_type") == "FINAL_ANSWER"), {})
            response = final_event.get("output", "Hiện chưa thể tạo câu trả lời.")
            st.markdown(response)
            render_trace(trace)

        st.session_state.messages.append({"role": "assistant", "content": response, "trace": trace})
        st.session_state.trace = trace
        st.session_state.last_plan = extract_plan(trace)
        save_waterfall_trace(trace)

with plan_col:
    with st.container(border=True):
        render_plan(st.session_state.last_plan)
        if not st.session_state.last_plan:
            st.subheader("Thực đơn sẽ xuất hiện ở đây", icon=":material/calendar_month:")
            st.caption("Hãy yêu cầu tạo thực đơn để hiển thị kế hoạch 4 bữa.")

    with st.container(border=True):
        st.subheader("Tổng quan nhanh", icon=":material/insights:")
        if profile["weight_kg"] and profile["height_cm"]:
            bmi = profile["weight_kg"] / ((profile["height_cm"] / 100) ** 2)
            bmi_label = f"{bmi:.1f}"
        else:
            bmi_label = "Chưa đủ dữ liệu"
        st.metric("BMI hiện tại", bmi_label)
        st.caption("Các ước tính dinh dưỡng chỉ mang tính tham khảo. Hãy hỏi chuyên gia nếu bạn có bệnh nền hoặc yêu cầu y tế đặc biệt.")

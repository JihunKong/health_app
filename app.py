import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Database simulation (In a real app, you'd use a proper database)
def save_to_database(data):
    # This is a placeholder for database operations
    print("Saving to database:", data)

# Generate time slots
def generate_time_slots():
    start = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    end = start.replace(hour=22)
    time_slots = []
    while start <= end:
        time_slots.append(start.strftime("%I:%M %p"))
        start += timedelta(minutes=30)
    return time_slots

# App
def main():
    st.title("건강 관리 앱")

    # User Inputs
    st.header("사용자 정보 입력")

    # Available Time
    available_times = generate_time_slots()
    selected_times = st.multiselect("가능한 시간대를 선택하세요:", available_times)

    # Preferred Exercises
    exercise_list = ["달리기", "자전거", "수영", "웨이트 트레이닝", "요가", "필라테스", "테니스", "농구"]
    selected_exercises = st.multiselect("선호하는 운동을 선택하세요:", exercise_list)
    custom_exercise = st.text_input("목록에 없는 운동이 있다면 입력해주세요:")
    if custom_exercise:
        selected_exercises.append(custom_exercise)

    # Exercise Location
    location_options = ["집", "체육관", "공원", "실외"]
    location = st.selectbox("운동 장소를 선택하세요:", location_options)
    equipment = st.checkbox("운동 기구 사용 가능")

    # Weekly Frequency
    frequency = st.slider("주당 운동 횟수:", 1, 7, 3)

    # Final Goal
    goal_options = ["체중 감량", "근육 증가", "체력 향상", "건강 유지"]
    goal = st.selectbox("최종 목표를 선택하세요:", goal_options)
    custom_goal = st.text_input("다른 목표가 있다면 입력해주세요:")

    if st.button("저장"):
        user_data = {
            "available_times": selected_times,
            "exercises": selected_exercises,
            "location": location,
            "equipment_available": equipment,
            "frequency": frequency,
            "goal": custom_goal if custom_goal else goal
        }
        save_to_database(user_data)
        st.success("정보가 성공적으로 저장되었습니다!")

if __name__ == "__main__":
    main()

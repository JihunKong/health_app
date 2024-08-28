import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI
import os

# Streamlit secrets에서 OpenAI API 키 가져오기
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

# Database simulation (실제 앱에서는 적절한 데이터베이스를 사용하세요)
def save_to_database(data):
    # 이것은 데이터베이스 작업을 위한 자리 표시자입니다
    print("데이터베이스에 저장 중:", data)

# 시간 슬롯 생성
def generate_time_slots():
    start = datetime.now().replace(hour=6, minute=0, second=0, microsecond=0)
    end = start.replace(hour=22)
    time_slots = []
    while start <= end:
        time_slots.append(start.strftime("%I:%M %p"))
        start += timedelta(minutes=30)
    return time_slots

# GPT-4를 사용하여 건강 관리 조언 생성
async def get_health_advice(user_data):
    prompt = f"""
    다음은 사용자의 건강 관리 정보입니다:
    - 가능한 시간대: {', '.join(user_data['available_times'])}
    - 선호하는 운동: {', '.join(user_data['exercises'])}
    - 운동 장소: {user_data['location']}
    - 운동 기구 사용 가능 여부: {'예' if user_data['equipment_available'] else '아니오'}
    - 주당 운동 횟수: {user_data['frequency']}
    - 최종 목표: {user_data['goal']}

    이 정보를 바탕으로 사용자에게 맞춤형 건강 관리 조언을 제공해주세요. 
    운동 계획, 영양 조언, 생활 습관 개선 팁 등을 포함해주세요. 양식은 보기 좋게 표로 작성해 주세요.
    """

    try:
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "당신은 전문적인 건강 관리 조언자입니다."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            n=1,
            temperature=0.7
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"OpenAI API 오류: {str(e)}")
        return None

# 앱
def main():
    st.title("AI 기반 건강 관리 앱")

    # 사용자 입력
    st.header("사용자 정보 입력")

    # 가능한 시간대
    available_times = generate_time_slots()
    selected_times = st.multiselect("가능한 시간대를 선택하세요:", available_times)

    # 선호하는 운동
    exercise_list = ["달리기", "자전거", "수영", "웨이트 트레이닝", "요가", "필라테스", "테니스", "농구"]
    selected_exercises = st.multiselect("선호하는 운동을 선택하세요:", exercise_list)
    custom_exercise = st.text_input("목록에 없는 운동이 있다면 입력해주세요:")
    if custom_exercise:
        selected_exercises.append(custom_exercise)

    # 운동 장소
    location_options = ["집", "체육관", "공원", "실외"]
    location = st.selectbox("운동 장소를 선택하세요:", location_options)
    equipment = st.checkbox("운동 기구 사용 가능")

    # 주당 운동 횟수
    frequency = st.slider("주당 운동 횟수:", 1, 7, 3)

    # 최종 목표
    goal_options = ["체중 감량", "근육 증가", "체력 향상", "건강 유지"]
    goal = st.selectbox("최종 목표를 선택하세요:", goal_options)
    custom_goal = st.text_input("다른 목표가 있다면 입력해주세요:")

    if st.button("건강 관리 조언 받기"):
        user_data = {
            "available_times": selected_times,
            "exercises": selected_exercises,
            "location": location,
            "equipment_available": equipment,
            "frequency": frequency,
            "goal": custom_goal if custom_goal else goal
        }
        save_to_database(user_data)
        
        with st.spinner("AI가 맞춤형 건강 관리 조언을 생성 중입니다..."):
            import asyncio
            advice = asyncio.run(get_health_advice(user_data))
        
        if advice:
            st.success("건강 관리 조언이 생성되었습니다!")
            st.write(advice)
        else:
            st.error("조언 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.")

if __name__ == "__main__":
    main()

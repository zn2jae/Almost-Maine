import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import os

# 페이지 설정
st.set_page_config(page_title="공연 홍보 도장판", layout="centered")

# Google Sheets 연결 초기화
conn = st.connection("gsheets", type=GSheetsConnection)

# 세션 상태 초기화
if 'stamps' not in st.session_state:
    st.session_state.stamps = [False, False, False, False]

st.title("🎭 공연 홍보 디지털 도장판")
st.info("4개의 도장을 모두 모으면 추첨 응모가 가능합니다!")

# 도장 현황판 (이미지 표시)
cols = st.columns(4)
for i in range(4):
    with cols[i]:
        if st.session_state.stamps[i]:
            st.image("images/stamp_filled.png", caption=f"미션 {i+1} 완료!")
        else:
            st.image("images/stamp_empty.png", caption=f"미션 {i+1} 대기중")

st.divider()

# --- 미션 로직 (이전과 동일, 정답만 수정하세요) ---
# [생략: 이전 퀴즈 및 코드 입력 로직 적용]

# --- 최종 응모 섹션 (Google Sheets 연동) ---
if all(st.session_state.stamps):
    st.balloons()
    st.success("🎉 축하합니다! 모든 도장을 모았습니다.")
    
    with st.form("entry_form"):
        st.subheader("🎟️ 추첨 응모함")
        name = st.text_input("이름")
        student_id = st.text_input("학번")
        phone = st.text_input("연락처")
        submit_button = st.form_submit_button("실시간 응모하기")
        
        if submit_button:
            if name and student_id and phone:
                # 시트에서 기존 데이터 읽기
                existing_data = conn.read(ttl=0) # 캐시 없이 실시간 읽기
                
                # 새 데이터 추가
                new_entry = pd.DataFrame([{"이름": name, "학번": student_id, "연락처": phone}])
                updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                
                # 시트에 업데이트 저장
                conn.update(data=updated_df)
                
                st.success(f"{name}님, 실시간 응모가 완료되었습니다! 시트에서 확인 가능합니다.")
            else:
                st.error("모든 정보를 입력해주세요.")

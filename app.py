import streamlit as st
import pandas as pd

# 1. 페이지 설정 (가장 먼저 와야 합니다)
st.set_page_config(page_title="공연 홍보 도장판", layout="centered")

# 2. 세션 상태 초기화 (오류 방지를 위해 최상단 배치)
if 'stamps' not in st.session_state:
    st.session_state.stamps = [False, False, False, False]

if 'selected_mission' not in st.session_state:
    st.session_state.selected_mission = None

# --- 앱 UI 시작 ---
st.title("🎭 공연 홍보 디지털 도장판")
st.info("4개의 도장을 모두 모으면 추첨 응모가 가능합니다!")

# 3. 도장 현황판 (클릭 시 미션 선택 기능 포함)
st.subheader("📍 미션을 선택하세요")
cols = st.columns(4)

for i in range(4):
    with cols[i]:
        # 이미지 경로 확인 필요: "images/stamp_filled.png"와 "images/stamp_empty.png"
        img_path = "images/stamp_filled.png" if st.session_state.stamps[i] else "images/stamp_empty.png"
        
        # 이미지를 표시하고 그 아래에 버튼 배치
        st.image(img_path, use_container_width=True)
        
        if not st.session_state.stamps[i]:
            if st.button(f"미션 {i+1}", key=f"btn_{i}"):
                st.session_state.selected_mission = i
        else:
            st.write("✅ 완료!")

st.divider()

# 4. 선택된 미션 인터랙션 영역
if st.session_state.selected_mission is not None:
    m_idx = st.session_state.selected_mission
    
    # 닫기 버튼
    if st.button("❌ 미션 창 닫기"):
        st.session_state.selected_mission = None
        st.rerun()

    if m_idx == 0:
        st.markdown("### 🎫 미션 1: 온라인 퀴즈")
        ans1 = st.text_input("공연의 주인공 이름은?", placeholder="정답을 입력하세요")
        if st.button("제출하기", key="submit1"):
            if ans1 == "홍길동": # 실제 정답으로 수정
                st.session_state.stamps[0] = True
                st.session_state.selected_mission = None
                st.success("첫 번째 도장 획득!")
                st.rerun()
            else:
                st.error("틀렸습니다! 다시 생각해보세요.")
                
    elif m_idx == 1:
        st.markdown("### 🎫 미션 2: 온라인 퀴즈")
        ans2 = st.text_input("공연이 열리는 장소는?", placeholder="정답을 입력하세요")
        if st.button("제출하기", key="submit2"):
            if ans2 == "강당": # 실제 정답으로 수정
                st.session_state.stamps[1] = True
                st.session_state.selected_mission = None
                st.success("두 번째 도장 획득!")
                st.rerun()
            else:
                st.error("틀렸습니다!")

    elif m_idx == 2:
        st.markdown("### 🎫 미션 3: 배우 상호작용")
        st.write("교내의 배우를 찾아 '첫 번째 암호'를 물어보세요!")
        code1 = st.text_input("시크릿 코드 입력", type="password")
        if st.button("확인", key="submit3"):
            if code1 == "1234": # 실제 배우 암호로 수정
                st.session_state.stamps[2] = True
                st.session_state.selected_mission = None
                st.success("세 번째 도장 획득!")
                st.rerun()

    elif m_idx == 3:
        st.markdown("### 🎫 미션 4: 배우 상호작용")
        st.write("마지막 배우를 찾아 '최종 암호'를 물어보세요!")
        code2 = st.text_input("최종 암호 입력", type="password")
        if st.button("확인", key="submit4"):
            if code2 == "5678": # 실제 배우 암호로 수정
                st.session_state.stamps[3] = True
                st.session_state.selected_mission = None
                st.success("모든 도장 완료!")
                st.rerun()
else:
    st.write("위의 미션 버튼을 눌러주세요.")

# 5. 최종 응모 섹션 (모든 도장이 True일 때만 나타남)
if all(st.session_state.stamps):
    st.divider()
    st.balloons()
    st.success("🎉 모든 도장을 모으셨습니다! 아래 양식을 작성하여 응모하세요.")
    
    with st.form("entry_form"):
        st.subheader("🎟️ 추첨 응모함")
        name = st.text_input("이름")
        student_id = st.text_input("학번")
        phone = st.text_input("연락처")
        submit_button = st.form_submit_button("응모하기")
        
        if submit_button:
            if name and student_id and phone:
                # 여기에 나중에 Google Sheets 연동 코드를 넣으면 됩니다.
                st.info(f"{name}님, 응모 데이터 전송 중... (현재는 테스트 모드입니다)")
            else:
                st.error("모든 정보를 입력해주세요.")

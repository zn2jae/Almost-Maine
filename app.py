import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="공연 홍보 도장판", layout="centered")

# 2. 구글 시트 연결 초기화
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 세션 상태 초기화
if 'stamps' not in st.session_state:
    st.session_state.stamps = [False, False, False, False]

if 'selected_mission' not in st.session_state:
    st.session_state.selected_mission = None

# --- 앱 UI ---
st.title("🎭 공연 홍보 디지털 도장판")
st.info("4개의 도장을 모두 모으면 추첨 응모가 가능합니다!")

# 4. 도장 현황판 (미션 선택)
st.subheader("📍 미션을 선택하세요")
cols = st.columns(4)

for i in range(4):
    with cols[i]:
        img_path = "images/stamp_filled.png" if st.session_state.stamps[i] else "images/stamp_empty.png"
        st.image(img_path, use_container_width=True)
        if not st.session_state.stamps[i]:
            if st.button(f"미션 {i+1}", key=f"btn_{i}"):
                st.session_state.selected_mission = i
        else:
            st.write("✅ 완료!")

st.divider()

# ... (상단 설정 및 도장 현황판 코드는 그대로 유지) ...

# 5. 선택된 미션 인터랙션 영역
if st.session_state.selected_mission is not None:
    m_idx = st.session_state.selected_mission
    
    if st.button("❌ 미션 창 닫기"):
        st.session_state.selected_mission = None
        st.rerun()

    # 미션 1 (기존 유지)
    if m_idx == 0:
        st.markdown("### 🎫 미션 1: 온라인 퀴즈")
        ans1 = st.text_input("공연의 주인공 이름은?", key="input_q1")
        if st.button("제출하기", key="sub1"):
            if ans1 == "정답1": # 실제 정답으로 수정
                st.session_state.stamps[0] = True
                st.session_state.selected_mission = None
                st.rerun()
            else:
                st.error("틀렸습니다! 다시 입력해주세요.")

    # 미션 2 (보완됨)
    elif m_idx == 1:
        st.markdown("### 🎫 미션 2: 온라인 퀴즈")
        st.write("공연 포스터나 공지사항을 잘 확인해보세요!")
        ans2 = st.text_input("공연이 열리는 요일은 언제인가요?", key="input_q2")
        if st.button("제출하기", key="sub2"):
            if ans2 == "목요일": # 실제 정답으로 수정
                st.session_state.stamps[1] = True
                st.session_state.selected_mission = None
                st.success("두 번째 도장 획득!")
                st.rerun()
            else:
                st.error("오답입니다. 포스터를 다시 확인해볼까요?")

    # 미션 3 (보완됨)
    elif m_idx == 2:
        st.markdown("### 🎫 미션 3: 배우 상호작용")
        st.write("교내에서 '배우' 명찰을 단 사람을 찾아 첫 번째 시크릿 코드를 물어보세요!")
        code1 = st.text_input("첫 번째 시크릿 코드 입력", type="password", key="input_c1")
        if st.button("확인", key="sub3"):
            if code1 == "acting123": # 배우가 알려줄 암호로 수정
                st.session_state.stamps[2] = True
                st.session_state.selected_mission = None
                st.success("세 번째 도장 획득!")
                st.rerun()
            else:
                st.error("코드가 일치하지 않습니다.")

    # 미션 4 (기존 유지)
    elif m_idx == 3:
        st.markdown("### 🎫 미션 4: 배우 상호작용")
        st.write("마지막 배우를 찾아 최종 암호를 입력하세요!")
        code2 = st.text_input("최종 암호 입력", type="password", key="input_c2")
        if st.button("확인", key="sub4"):
            if code2 == "finalshow": # 실제 암호로 수정
                st.session_state.stamps[3] = True
                st.session_state.selected_mission = None
                st.rerun()
            else:
                st.error("최종 암호가 틀렸습니다.")

# ... (하단 응모 섹션 코드는 그대로 유지) ...
# 6. 최종 응모 섹션 (Google Sheets 실시간 저장)
if all(st.session_state.stamps):
    st.divider()
    st.balloons()
    st.success("🎉 모든 도장을 모으셨습니다! 아래 양식을 작성하여 응모하세요.")
    
    with st.form("entry_form"):
        st.subheader("🎟️ 추첨 응모함")
        name = st.text_input("이름")
        sid = st.text_input("학번")
        phone = st.text_input("연락처")
        submit_button = st.form_submit_button("응모하기")
        
        if submit_button:
            if name and sid and phone:
                try:
                    # 1. 기존 데이터 읽기
                    df = conn.read(ttl=0) 
                    
                    # 2. 새 데이터 행 만들기
                    new_data = pd.DataFrame([{"이름": name, "학번": sid, "연락처": phone}])
                    
                    # 3. 데이터 합치기
                    updated_df = pd.concat([df, new_data], ignore_index=True)
                    
                    # 4. 시트에 업데이트
                    conn.update(data=updated_df)
                    
                    st.success(f"{name}님, 응모가 완료되었습니다! 감사합니다.")
                except Exception as e:
                    st.error(f"오류가 발생했습니다: {e}")
            else:
                st.error("모든 정보를 입력해주세요.")

import streamlit as st

# 페이지 설정
st.set_page_config(page_title="동아리 공연 온라인 도장판", layout="centered")

# 세션 상태 초기화 (도장 획득 여부 저장)
if 'stamps' not in st.session_state:
    st.session_state.stamps = [False, False, False, False]

st.title("🎭 공연 홍보 온라인 도장판")
st.info("4개의 도장을 모두 모아 추첨 응모에 참여하세요!")

# 도장 현황판 시각화
cols = st.columns(4)
for i in range(4):
    with cols[i]:
        if st.session_state.stamps[i]:
            # 도장을 획득했을 때 (images 폴더 내 stamp_filled.png 사용)
            # 이미지가 없다면 텍스트로 대체 표시
            st.success(f"도장 {i+1} 획득!")
            # st.image("images/stamp_filled.png") # 이미지 준비 후 주석 해제
        else:
            # 도장 획득 전 (images 폴더 내 stamp_empty.png 사용)
            st.warning(f"미션 {i+1}")
            # st.image("images/stamp_empty.png") # 이미지 준비 후 주석 해제

st.divider()

# --- 미션 섹션 ---

# 미션 1 & 2: 온라인 퀴즈
st.subheader("💻 온라인 퀴즈 미션")

# 퀴즈 1
if not st.session_state.stamps[0]:
    q1 = st.text_input("퀴즈 1: 우리 공연의 제목은 무엇일까요?", key="q1")
    if st.button("정답 확인", key="b1"):
        if q1 == "공연제목": # 실제 정답으로 수정하세요
            st.session_state.stamps[0] = True
            st.rerun()
        else:
            st.error("틀렸습니다! 다시 생각해보세요.")

# 퀴즈 2
if st.session_state.stamps[0] and not st.session_state.stamps[1]:
    q2 = st.text_input("퀴즈 2: 동아리 방 번호는 몇 번일까요?", key="q2")
    if st.button("정답 확인", key="b2"):
        if q2 == "101": # 실제 정답으로 수정하세요
            st.session_state.stamps[1] = True
            st.rerun()

# 미션 3 & 4: 오프라인 배우 상호작용
st.subheader("🏃 오프라인 배우 미션")
st.write("교내를 돌아다니는 배우를 찾아 비밀코드를 물어보세요!")

# 오프라인 미션 1
if st.session_state.stamps[1] and not st.session_state.stamps[2]:
    code1 = st.text_input("배우가 알려준 첫 번째 코드를 입력하세요", type="password")
    if st.button("코드 확인 1"):
        if code1 == "배우이름1": # 실제 배우가 알려줄 정답
            st.session_state.stamps[2] = True
            st.rerun()

# 오프라인 미션 2
if st.session_state.stamps[2] and not st.session_state.stamps[3]:
    code2 = st.text_input("배우가 알려준 두 번째 코드를 입력하세요", type="password")
    if st.button("코드 확인 2"):
        if code2 == "대박공연": # 실제 배우가 알려줄 정답
            st.session_state.stamps[3] = True
            st.rerun()

# --- 최종 응모 섹션 ---
if all(st.session_state.stamps):
    st.balloons()
    st.success("🎉 모든 도장을 다 모으셨습니다! 추첨 응모가 가능합니다.")
    
    with st.form("entry_form"):
        st.subheader("🎟️ 추첨 응모함")
        name = st.text_input("이름")
        student_id = st.text_input("학번")
        phone = st.text_input("연락처")
        submit_button = st.form_submit_button("응모하기")
        
        if submit_button:
            if name and student_id and phone:
                # 여기서 데이터를 저장하는 로직(Google Sheets 등)을 추가할 수 있습니다.
                st.write(f"{name}님, 응모가 완료되었습니다! 공연장에서 만나요!")
            else:
                st.error("모든 정보를 입력해주세요.")

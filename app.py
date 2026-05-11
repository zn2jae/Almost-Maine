# 현재 사용자가 어떤 미션을 선택했는지 저장하는 상태 추가
if 'selected_mission' not in st.session_state:
    st.session_state.selected_mission = None

st.divider()

# --- 스탬프 선택 섹션 ---
st.subheader("📍 미션을 선택하세요")
cols = st.columns(4)

for i in range(4):
    with cols[i]:
        # 도장 상태에 따른 이미지 표시 (이미 배포하신 images 폴더 기준)
        img_path = "images/stamp_filled.png" if st.session_state.stamps[i] else "images/stamp_empty.png"
        st.image(img_path, use_container_width=True)
        
        # 미션 선택 버튼
        if not st.session_state.stamps[i]:
            if st.button(f"미션 {i+1} 도전", key=f"btn_{i}"):
                st.session_state.selected_mission = i
        else:
            st.write("✅ 완료!")

st.divider()

# --- 선택된 미션 인터랙션 영역 ---
if st.session_state.selected_mission is not None:
    m_idx = st.session_state.selected_mission
    
    if m_idx == 0:
        st.info("🎫 미션 1: 온라인 퀴즈")
        ans1 = st.text_input("공연의 주인공 이름은?")
        if st.button("제출하기"):
            if ans1 == "홍길동": # 정답 수정
                st.session_state.stamps[0] = True
                st.session_state.selected_mission = None # 미션창 닫기
                st.rerun()
                
    elif m_idx == 1:
        st.info("🎫 미션 2: 온라인 퀴즈")
        ans2 = st.text_input("공연이 열리는 장소는?")
        if st.button("제출하기"):
            if ans2 == "강당": # 정답 수정
                st.session_state.stamps[1] = True
                st.session_state.selected_mission = None
                st.rerun()

    elif m_idx == 2:
        st.info("🎫 미션 3: 배우 상호작용")
        st.write("배우를 찾아 '첫 번째 암호'를 입력하세요!")
        code1 = st.text_input("시크릿 코드 입력", type="password")
        if st.button("확인"):
            if code1 == "1234": # 암호 수정
                st.session_state.stamps[2] = True
                st.session_state.selected_mission = None
                st.rerun()

    elif m_idx == 3:
        st.info("🎫 미션 4: 배우 상호작용")
        st.write("마지막 배우를 찾아 '두 번째 암호'를 입력하세요!")
        code2 = st.text_input("최종 암호 입력", type="password")
        if st.button("확인"):
            if code2 == "5678": # 암호 수정
                st.session_state.stamps[3] = True
                st.session_state.selected_mission = None
                st.rerun()
else:
    st.write("위의 버튼을 눌러 미션을 시작하세요.")

# --- 응모 섹션은 동일하게 유지 (모든 도장이 True일 때만 나타남) ---

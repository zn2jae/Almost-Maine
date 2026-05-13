import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="Almost, Maine 도장판", layout="centered")

# 2. 구글 시트 연결 초기화
conn = st.connection("gsheets", type=GSheetsConnection)

# 3. 세션 상태 초기화
if 'stamps' not in st.session_state:
    st.session_state.stamps = [False, False]

if 'selected_mission' not in st.session_state:
    st.session_state.selected_mission = None

# --- 앱 UI ---
st.title("🎭 Almost, Maine 도장판")
st.info("도장을 모두 모으고 추첨 응모를 해보세요!")

# 4. 도장 현황판 (미션 선택)
st.subheader("📍 진행하고 싶은 미션을 선택하세요")
cols = st.columns(2)

for i in range(2):
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
import random

# --- [추가] 퀴즈 데이터 정의 ---
# 미션 1 문제 리스트
if 'q1_pool' not in st.session_state:
    st.session_state.q1_pool = [
        {"q": "배우가 무대 위에서 각본(희곡)에 따라 인물이나 사건을 말과 동작으로 연기하여 관객에게 직접 보여주는 무대 예술을 무엇이라 할까요?", "a": ["연극"]},
        {"q": "오늘날 타인에게 비치는 외적인격이나 사회적 가면을 뜻하는 말로, 고대 그리스 연극에서 배우가 쓰던 가면에서 유래된 말은?", "a": ["페르소나"]},
        {"q": "연극의 3요소는 무엇일까요?\n(힌트: 연기하는 OO, 그것을 보는 OO, 배우가 보는 OO)", "a": ["배우, 관객, 희곡", "배우, 관객, 대본"]},
        {"q": "경상국립대학교 공연분과 연극 동아리의 이름은?", "a": ["경상극예술연구회", "경상극회"]},
        {"q": "이번 5월, 저희 동아리에서 올리는 공연의 이름은?", "a": ["올모스트 메인", "almost, maine", "almost maine" "올모스트, 메인"]}
    ]

# 미션 2 문제 리스트
if 'q2_pool' not in st.session_state:
    st.session_state.q2_pool = [
        {"q": "다른 사람을 진심으로 애틋하게 그리워하고 열렬히 좋아하며 온 마음과 정성을 다해 자신의 모든 걸 내어 줄 수 있는 감정을 무엇이라 하나요?", "a": ["사랑"]},
        {"q": "우리말로 '거의'라는 뜻을 가진 영어 단어는?", "a": ["올모스트", "almost"]},
        {"q": "보통 추운 지역에서 발견되는 천문학적 기상현상을 무엇이라 하나요?", "a": ["오로라"]},
        {"q": "프로포즈를 위해 상대에게 건네는 '이것'은 무엇일까요?\n(힌트: 악세서리)", "a": ["반지"]},
        {"q": "친구 사이, 우리는 연인이 될 수 있다?\n(힌트: 자유로운 의견을 적어주세요 ^^)", "a": ["FREE_PASS"]} # 자유 답변용 키워드
    ]

# 각 미션별 랜덤 문제 선택 상태 관리
if 'm1_question' not in st.session_state:
    st.session_state.m1_question = random.choice(st.session_state.q1_pool)
if 'm2_question' not in st.session_state:
    st.session_state.m2_question = random.choice(st.session_state.q2_pool)

# --- 미션 인터랙션 영역 ---
if st.session_state.selected_mission is not None:
    m_idx = st.session_state.selected_mission
    
    if st.button("❌ 미션 창 닫기"):
        st.session_state.selected_mission = None
        st.rerun()

    # 상시 표시 힌트 문구
    if m_idx in [0, 1]:
        st.caption("💡 퀴즈의 답을 모르겠다면? 주변의 배우들을 찾아 힌트를 얻어보세요!")

    # 미션 1: 랜덤 온라인 퀴즈
    if m_idx == 0:
        st.markdown("### 🎫 미션 1: 연극 상식 퀴즈")
        current_q = st.session_state.m1_question
        st.write(f"**Q. {current_q['q']}**")
        ans1 = st.text_input("답변 입력", key="input_q1").strip()
        
        if st.button("제출하기", key="sub1"):
            if any(correct_ans in ans1.lower() for correct_ans in [a.lower() for a in current_q['a']]):
                st.session_state.stamps[0] = True
                st.session_state.selected_mission = None
                st.success("첫 번째 도장 획득!")
                st.rerun()
            else:
                st.error("오답입니다. 다시 시도하거나 배우에게 힌트를 얻으세요!")

   # 미션 2: 랜덤 온라인 퀴즈 (자유 답변 포함 및 시트2 업데이트)
    elif m_idx == 1:
        st.markdown("### 🎫 미션 2: 공연 관련 퀴즈")
        current_q = st.session_state.m2_question
        st.write(f"**Q. {current_q['q']}**")
        ans2 = st.text_input("답변 입력", key="input_q2").strip()
        
        if st.button("제출하기", key="sub2"):
            # 1. 자유 답변 문제(FREE_PASS)인 경우
            if "FREE_PASS" in current_q['a']:
                if not ans2:
                    st.warning("의견을 한 글자라도 적어주세요!")
                else:
                    try:
                        from datetime import datetime
                        # 시트2의 기존 데이터를 읽어옵니다 (캐시 없이 실시간)
                        existing_opinions = conn.read(worksheet="시트2", ttl=0)
                        
                        # 새 의견 데이터 생성
                        new_opinion = pd.DataFrame([{
                            "시간": datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
                            "의견": ans2
                        }])
                        
                        # 기존 데이터 아래에 새 의견 추가
                        updated_opinions = pd.concat([existing_opinions, new_opinion], ignore_index=True)
                        
                        # 시트2 전체를 업데이트 (에러 방지)
                        conn.update(worksheet="시트2", data=updated_opinions)
                        
                        st.session_state.stamps[1] = True
                        st.session_state.selected_mission = None
                        st.success("소중한 의견 감사합니다! 두 번째 도장 획득!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"의견 저장 중 오류가 발생했습니다: {e}")
            
            # 2. 일반 퀴즈 문제인 경우
            elif any(correct_ans in ans2.lower() for correct_ans in [a.lower() for a in current_q['a']]):
                st.session_state.stamps[1] = True
                st.session_state.selected_mission = None
                st.success("정답입니다! 두 번째 도장 획득!")
                st.rerun()
            else:
                st.error("오답입니다. 다시 시도해 보세요!")
    

# --- 6. 최종 응모 섹션 (안전한 데이터 업데이트 방식) ---
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
                    # 1. 기존 '시트1'의 데이터를 실시간으로 읽어옵니다.
                    # ttl=0은 캐시를 사용하지 않고 즉시 읽어오라는 뜻입니다.
                    existing_data = conn.read(worksheet="시트1", ttl=0)
                    
                    # 2. 새 응모자 정보를 데이터프레임으로 만듭니다.
                    new_entry = pd.DataFrame([{"이름": name, "학번": sid, "연락처": phone}])
                    
                    # 3. 기존 데이터와 새 데이터를 합칩니다.
                    updated_df = pd.concat([existing_data, new_entry], ignore_index=True)
                    
                    # 4. 합쳐진 전체 데이터를 '시트1'에 덮어씁니다. (이게 가장 확실합니다)
                    conn.update(worksheet="시트1", data=updated_df)
                    
                    st.success(f"{name}님, 응모가 성공적으로 완료되었습니다!")
                except Exception as e:
                    st.error(f"데이터 전송 중 오류가 발생했습니다: {e}")
            else:
                st.error("모든 정보를 입력해주세요.")

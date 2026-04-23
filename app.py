import streamlit as st
import numpy as np

# 1. 페이지 설정 및 다크/라이트 모드 대응을 위한 반응형 설정
st.set_page_config(
    page_title="10 만들기 게임",
    layout="wide",  # 반응형을 위해 wide 모드 사용
    initial_sidebar_state="collapsed"
)

# 2. 커스텀 CSS: 버튼 디자인, 반응형 크기, 저작권 표기 등
st.markdown("""
    <style>
    /* 전체 배경 및 폰트 */
    .main { background-color: transparent; }
    
    /* 숫자 버튼 디자인 - 다크/라이트 모드 모두 잘 보이도록 설정 */
    div.stButton > button {
        width: 100%;
        aspect-ratio: 1 / 1; /* 정사각형 유지 */
        font-size: 1.5rem !important;
        font-weight: bold !important;
        border-radius: 12px;
        transition: all 0.2s;
        border: 2px solid #4A90E2;
    }
    
    /* 반응형 폰트 조절 (모바일 우선) */
    @media (max-width: 600px) {
        div.stButton > button { font-size: 1.2rem !important; margin: 2px; }
    }

    /* 저작권 표기 스타일 */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(0,0,0,0.05);
        color: gray;
        text-align: center;
        padding: 10px;
        font-size: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. JavaScript: 전체화면 및 뒤로가기 방지 확인창
st.components.v1.html("""
    <script>
    // 전체화면 함수
    window.toggleFullScreen = function() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen();
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }

    // 뒤로가기/새로고침 방지 확인창
    window.onbeforeunload = function() {
        return "게임 중이신가요? 변경사항이 저장되지 않을 수 있습니다.";
    };
    </script>
    """, height=0)

# 세션 상태 관리
if 'board' not in st.session_state:
    st.session_state.board = np.random.randint(1, 10, size=(5, 8)) # 가로로 긴 형태 (태블릿/PC 고려)
    st.session_state.selected = []
    st.session_state.score = 0

# 로직 함수들
def reset_game():
    st.session_state.board = np.random.randint(1, 10, size=(5, 8))
    st.session_state.selected = []
    st.session_state.score = 0

# 상단 헤더 영역
col1, col2 = st.columns([3, 1])
with col1:
    st.title("🔢 합쳐서 10!")
with col2:
    if st.button("🖥️ 전체화면", use_container_width=True):
        st.components.v1.html("<script>window.parent.document.documentElement.requestFullscreen();</script>", height=0)

st.subheader(f"현재 점수: {st.session_state.score}점")

# 게임 보드 (반응형 그리드)
rows, cols_count = st.session_state.board.shape
for r in range(rows):
    cols = st.columns(cols_count)
    for c in range(cols_count):
        num = st.session_state.board[r, c]
        if num == 0:
            cols[c].button(" ", key=f"empty_{r}_{c}", disabled=True)
            continue
            
        is_selected = (r, c) in st.session_state.selected
        btn_label = f"{num}"
        
        if cols[c].button(btn_label, key=f"btn_{r}_{c}", type="primary" if is_selected else "secondary"):
            if (r, c) not in st.session_state.selected:
                st.session_state.selected.append((r, c))
                current_sum = sum(st.session_state.board[p] for p in st.session_state.selected)
                
                if current_sum == 10:
                    st.toast("정답! 10 완성 🎯")
                    st.session_state.score += 10
                    for p in st.session_state.selected:
                        st.session_state.board[p] = 0
                    st.session_state.selected = []
                    st.rerun()
                elif current_sum > 10:
                    st.toast("10을 넘었어요! 다시 선택하세요 ❌")
                    st.session_state.selected = []
                    st.rerun()

# 하단 메뉴
st.write("---")
if st.button("🔄 게임 초기화"):
    reset_game()
    st.rerun()

# 5. 저작권 표기 (푸터)
st.markdown('<div class="footer">© 2026 AI-ON교과연구회. All Rights Reserved.</div>', unsafe_allow_html=True)

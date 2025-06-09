import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import platform

# 한글 폰트 설정
if platform.system() == 'Windows':
    plt.rc('font', family='Malgun Gothic')
elif platform.system() == 'Darwin':  # macOS
    plt.rc('font', family='AppleGothic')
else:  # Linux (Streamlit Cloud 포함)
    plt.rc('font', family='NanumGothic')

# 마이너스 깨짐 방지
matplotlib.rcParams['axes.unicode_minus'] = False

# -----------------------------
# 1. 데이터 입력
# -----------------------------
st.title("희토류 수입 차단 시뮬레이션 (한국 기준)")

# 예시 수입 데이터 (톤 단위)
data = {
    '국가': ['중국', '독일', '남아프리카', '미국', '일본'],
    '수입량': [100.5, 3.5, 0.91, 0.23, 0.17]
}
df = pd.DataFrame(data)

# 전체 수입량
total_import = df['수입량'].sum()

# -----------------------------
# 2. 사용자 입력 (차단할 국가 선택)
# -----------------------------
st.subheader("🚫 차단할 수입국 선택")
blocked_country = st.selectbox("수출을 차단한 국가를 선택하세요", df['국가'])

# 대체 공급 가능 비율 입력
replacement_rate = st.slider("📦 대체 공급 가능 비율 (%)", 0, 100, 30)

# -----------------------------
# 3. 시뮬레이션 결과 계산
# -----------------------------
blocked_amount = df[df['국가'] == blocked_country]['수입량'].values[0]
replaced_amount = blocked_amount * (replacement_rate / 100)
new_total_import = total_import - blocked_amount + replaced_amount
reduction_percent = (total_import - new_total_import) / total_import * 100

# -----------------------------
# 4. 결과 출력
# -----------------------------
st.markdown(f"""
### 📊 시뮬레이션 결과
- 차단된 국가: **{blocked_country}**
- 차단된 수입량: **{blocked_amount} 톤**
- 대체 공급된 수량: **{replaced_amount:.1f} 톤**
- 최종 수입량: **{new_total_import:.1f} 톤**  
- 💥 전체 수입량 감소율: **{reduction_percent:.1f}%**
""")

# -----------------------------
# 5. 시각화 (Before / After)
# -----------------------------
st.subheader("📉 수입량 변화 시각화")
before = pd.DataFrame({
    '구분': ['기존 총수입'],
    '수입량': [total_import]
})
after = pd.DataFrame({
    '구분': ['시뮬레이션 후'],
    '수입량': [new_total_import]
})
compare_df = pd.concat([before, after])

fig, ax = plt.subplots()
ax.bar(compare_df['구분'], compare_df['수입량'], color=['skyblue', 'salmon'])
ax.set_ylabel('수입량 (톤)')
st.pyplot(fig)
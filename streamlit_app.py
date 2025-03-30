# 필요한 라이브러리 임포트 | Import required libraries
import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
from sklearn.utils import resample
from sklearn.linear_model import LinearRegression
import time
from visualization import display_visualization

# 페이지 설정 | Page configuration
st.set_page_config(
    page_title="회귀 계수 추정 방법 비교 | Regression Coefficient Estimation Comparison",
    page_icon="📊",
    layout="wide"
)

# Custom CSS 로드 | Load custom CSS
with open('.streamlit/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# 제목 | Title
st.title("회귀 계수 추정 방법 비교")
st.title("Regression Coefficient Estimation Comparison")

st.markdown("""
이 앱은 부트스트랩, 몬테카를로, 베이지안 방법을 사용하여 회귀 계수를 추정하고 비교합니다.
This app estimates and compares regression coefficients using Bootstrap, Monte Carlo, and Bayesian methods.
""")

# 사이드바 컨트롤 | Sidebar controls
st.sidebar.header("파라미터 설정 | Parameter Settings")

# 데이터 생성 파라미터 | Data Generation Parameters
st.sidebar.subheader("데이터 생성 파라미터 | Data Generation Parameters")
true_slope = st.sidebar.slider("실제 기울기 | True Slope", min_value=1.0, max_value=10.0, value=3.0, step=0.1)
true_intercept = st.sidebar.slider("실제 절편 | True Intercept", min_value=0.0, max_value=10.0, value=5.0, step=0.1)
noise_level = st.sidebar.slider("노이즈 수준 | Noise Level", min_value=0.0, max_value=10.0, value=2.0, step=0.1)
n_samples = st.sidebar.slider("샘플 수 | Sample Size", min_value=50, max_value=1000, value=100, step=10)

# 몬테카를로 시뮬레이션 파라미터 | Monte Carlo Simulation Parameters
st.sidebar.subheader("부트스트랩/몬테카를로 파라미터 | Bootstrap/Monte Carlo Parameters")
n_iterations = st.sidebar.slider("반복 횟수 | Number of Iterations", min_value=100, max_value=5000, value=1000, step=100)

# 데이터 생성 | Data Generation
np.random.seed(42)
x = np.linspace(0, 10, n_samples)
y = true_slope * x + true_intercept + np.random.normal(0, noise_level, x.size)

# 진행 상태 표시 | Progress display
progress_bar = st.progress(0)
status_text = st.empty()

# 1. 부트스트랩 ------------------------------------------------------
status_text.text("부트스트랩 분석 중... | Running Bootstrap analysis...")
bootstrap_coefs = []
for i in range(n_iterations):
    x_resampled, y_resampled = resample(x, y)
    model = LinearRegression().fit(x_resampled.reshape(-1,1), y_resampled)
    bootstrap_coefs.append(model.coef_[0])
    progress_bar.progress((i + 1) / (n_iterations * 3))

# 2. 몬테카를로 ------------------------------------------------------
status_text.text("몬테카를로 분석 중... | Running Monte Carlo analysis...")
monte_carlo_coefs = []
for i in range(n_iterations):
    new_x = np.random.uniform(0, 10, n_samples)
    new_y = true_slope * new_x + true_intercept + np.random.normal(0, noise_level, new_x.size)
    model = LinearRegression().fit(new_x.reshape(-1,1), new_y)
    monte_carlo_coefs.append(model.coef_[0])
    progress_bar.progress((i + n_iterations + 1) / (n_iterations * 3))

# 3. 베이지안 회귀 ----------------------------------------------------
status_text.text("베이지안 회귀 분석 중... | Running Bayesian regression analysis...")
X = np.vstack([x, np.ones(len(x))]).T
theta_hat = np.linalg.inv(X.T@X) @ X.T@y
sigma_sq = np.sum((y - X@theta_hat)**2)/(len(x)-2)
bayesian_coefs = np.random.normal(theta_hat[0], 
                                 np.sqrt(sigma_sq), 
                                 n_iterations)
progress_bar.progress(1.0)
status_text.text("분석 완료! | Analysis complete!")

# 결과 표시 | Display results
# 통계적 요약 | Statistical Summary
st.subheader("통계적 요약 | Statistical Summary")
stats_df = pd.DataFrame({
    'Method': ['Bootstrap', 'Monte Carlo', 'Bayesian'],
    'Mean': [np.mean(bootstrap_coefs), np.mean(monte_carlo_coefs), np.mean(bayesian_coefs)],
    'Std': [np.std(bootstrap_coefs), np.std(monte_carlo_coefs), np.std(bayesian_coefs)],
    'True Value': [true_slope, true_slope, true_slope]
})
st.dataframe(stats_df.style.format({
    'Mean': '{:.4f}',
    'Std': '{:.4f}',
    'True Value': '{:.4f}'
}))

# 데이터프레임 생성 | Create DataFrame
df = pd.DataFrame({
    'Method': ['Bootstrap'] * n_iterations + ['Monte Carlo'] * n_iterations + ['Bayesian'] * n_iterations,
    'Coefficient': np.concatenate([bootstrap_coefs, monte_carlo_coefs, bayesian_coefs])
})

# 시각화 표시 | Display visualization
display_visualization(df, true_slope, n_iterations)

# About 버튼 및 팝업 | About button and popup
with st.expander("About | 소개", expanded=False):
    with open("intro.md", "r", encoding="utf-8") as f:
        st.markdown(f.read())


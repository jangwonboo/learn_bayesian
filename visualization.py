import streamlit as st
import numpy as np
import pandas as pd
import altair as alt
import logging
import os
from datetime import datetime
from config import (
    DEBUG_MODE, SHOW_COMMENTS, LOG_LEVEL, LOGGING_CONFIG,
    CODE_BLOCKS, conditional_block
)

# 로깅 설정 | Logging configuration
@conditional_block('show_logging')
def setup_logging():
    """로깅 설정을 초기화합니다 | Initialize logging configuration"""
    if not LOGGING_CONFIG['enabled']:
        return None
        
    # 로그 디렉토리 생성 | Create log directory
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # 로그 파일명 설정 | Set log filename
    log_filename = f'logs/visualization_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'
    
    # 로거 설정 | Configure logger
    logger = logging.getLogger('visualization')
    logger.setLevel(getattr(logging, LOG_LEVEL))
    
    # 파일 핸들러 설정 | Configure file handler
    if LOGGING_CONFIG['file_logging']:
        file_handler = logging.FileHandler(log_filename, encoding='utf-8')
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    
    # 콘솔 핸들러 설정 | Configure console handler
    if LOGGING_CONFIG['console_logging']:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, LOG_LEVEL))
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
    
    return logger

# 로거 초기화 | Initialize logger
logger = setup_logging()

@conditional_block('show_debug_code')
def log_debug(message):
    """Debug 로깅을 위한 헬퍼 함수 | Helper function for debug logging"""
    if DEBUG_MODE and logger:
        logger.debug(message)

@conditional_block('show_logging')
def log_info(message):
    """Info 로깅을 위한 헬퍼 함수 | Helper function for info logging"""
    if logger:
        logger.info(message)

@conditional_block('show_visualization_code')
def create_visualization(df, true_slope, n_iterations):
    """
    Create visualization for regression coefficient estimation methods.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the coefficient estimates
    true_slope : float
        True slope value for reference line
    n_iterations : int
        Number of iterations used in the analysis
    """
    log_info("시각화 생성 시작 | Starting visualization creation")
    log_debug(f"입력 데이터 크기 | Input data size: {len(df)}")
    log_debug(f"실제 기울기 값 | True slope value: {true_slope}")
    log_debug(f"반복 횟수 | Number of iterations: {n_iterations}")

    # 공통 x축과 y축 범위 설정 | Set common x and y axis ranges
    all_coefs = df['Coefficient'].values
    x_min, x_max = min(all_coefs) - 0.1, max(all_coefs) + 0.1

    # y축 최대값 계산 개선 | Improved y-axis maximum calculation
    # 각 방법별로 히스토그램 빈도 계산 | Calculate histogram frequencies for each method
    bins = np.linspace(x_min, x_max, 31)  # 30 bins
    bootstrap_hist, _ = np.histogram(df[df['Method'] == 'Bootstrap']['Coefficient'], bins=bins)
    monte_carlo_hist, _ = np.histogram(df[df['Method'] == 'Monte Carlo']['Coefficient'], bins=bins)
    bayesian_hist, _ = np.histogram(df[df['Method'] == 'Bayesian']['Coefficient'], bins=bins)

    y_max = max([
        np.max(bootstrap_hist),
        np.max(monte_carlo_hist),
        np.max(bayesian_hist)
    ]) * 1.1  # 여유 공간 추가 | Add margin

    # 상세 로깅 추가 | Add detailed logging
    log_debug("=== 히스토그램 빈도 통계 | Histogram Frequency Statistics ===")
    log_debug(f"부트스트랩 최대 빈도 | Bootstrap max frequency: {np.max(bootstrap_hist)}")
    log_debug(f"몬테카를로 최대 빈도 | Monte Carlo max frequency: {np.max(monte_carlo_hist)}")
    log_debug(f"베이지안 최대 빈도 | Bayesian max frequency: {np.max(bayesian_hist)}")
    log_debug(f"계산된 y축 최대값 | Calculated y-axis maximum: {y_max:.2f}")

    # display df
    log_debug(f"df: {df}")
    log_debug(f"x축 범위 | x-axis range: [{x_min:.4f}, {x_max:.4f}]")
    log_debug(f"y축 최대값 | y-axis maximum: {y_max:.2f}")

    # 기본 차트 설정 | Base chart settings
    log_info("기본 차트 설정 중 | Setting up base chart")
    base = alt.Chart(df).encode(
        x=alt.X('Coefficient:Q', 
                bin=alt.Bin(maxbins=30, extent=[x_min, x_max]),  # extent 추가 | Add extent
                title='기울기(θ1) | Slope(θ1)',
                scale=alt.Scale(domain=[x_min, x_max])),
        y=alt.Y('count():Q', 
                title='빈도 | Frequency',
                scale=alt.Scale(domain=[0, y_max], nice=True)),  # nice=True 추가 | Add nice=True
        tooltip=['count():Q']
    ).properties(
        width=400,
        height=300
    )

    # 실제값을 나타내는 수직선 생성 | Create vertical line for true value
    log_info("참조선 생성 중 | Creating reference line")
    rule = alt.Chart(pd.DataFrame({'x': [true_slope]})).mark_rule(
        color='red',
        strokeDash=[5, 5],
        strokeWidth=2
    ).encode(
        x='x:Q',
        tooltip=[alt.Tooltip('x:Q', title='실제값 | True Value')]
    )

    # 각 방법별 차트 생성 | Create charts for each method
    log_info("각 방법별 차트 생성 중 | Creating charts for each method")
    
    bootstrap_chart = base.mark_bar(opacity=0.7, color='#1f77b4').transform_filter(
        alt.datum.Method == 'Bootstrap'
    )
    log_debug("부트스트랩 차트 생성 완료 | Bootstrap chart created")

    monte_carlo_chart = base.mark_bar(opacity=0.7, color='#ff7f0e').transform_filter(
        alt.datum.Method == 'Monte Carlo'
    )
    log_debug("몬테카를로 차트 생성 완료 | Monte Carlo chart created")

    bayesian_chart = base.mark_bar(opacity=0.7, color='#2ca02c').transform_filter(
        alt.datum.Method == 'Bayesian'
    )
    log_debug("베이지안 차트 생성 완료 | Bayesian chart created")

    # 차트를 수평으로 결합 | Combine charts horizontally
    log_info("차트 결합 중 | Combining charts")
    final_chart = alt.hconcat(
        bootstrap_chart + rule,
        monte_carlo_chart + rule,
        bayesian_chart + rule,
        spacing=20
    ).configure_view(
        stroke=None
    ).configure_axis(
        labelFontSize=12,
        titleFontSize=14
    ).configure_title(
        fontSize=16,
        anchor='middle'
    )

    log_info("시각화 생성 완료 | Visualization creation completed")
    return final_chart

@conditional_block('show_visualization_code')
def display_visualization(df, true_slope, n_iterations):
    """
    Display the visualization with description.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        DataFrame containing the coefficient estimates
    true_slope : float
        True slope value for reference line
    n_iterations : int
        Number of iterations used in the analysis
    """
    log_info("시각화 표시 시작 | Starting visualization display")
    
    st.subheader("시각화 | Visualization")
    
    # Create and display the chart
    chart = create_visualization(df, true_slope, n_iterations)
    st.altair_chart(chart, use_container_width=True)
    log_info("차트 표시 완료 | Chart display completed")

    # Add chart description
    if SHOW_COMMENTS:
        st.markdown("""
        ### 차트 설명 | Chart Description

        각 히스토그램은 해당 방법으로 추정된 회귀 계수의 분포를 보여줍니다.
        Each histogram shows the distribution of regression coefficients estimated by each method.

        - **파란색**: 부트스트랩 방법 | Blue: Bootstrap method
        - **주황색**: 몬테카를로 방법 | Orange: Monte Carlo method
        - **초록색**: 베이지안 방법 | Green: Bayesian method
        - **빨간 점선**: 실제 기울기 값 | Red dashed line: True slope value
        """)
    log_info("차트 설명 표시 완료 | Chart description display completed") 
# 회귀 계수 추정 방법 비교 시각화 | Regression Coefficient Estimation Comparison Visualization

이 프로젝트는 부트스트랩, 몬테카를로, 베이지안 방법을 사용하여 회귀 계수를 추정하고 비교하는 시각화 도구입니다.
This project is a visualization tool that compares regression coefficient estimation methods using Bootstrap, Monte Carlo, and Bayesian approaches.

## 주요 기능 | Key Features

- 부트스트랩, 몬테카를로, 베이지안 방법을 사용한 회귀 계수 추정
  Regression coefficient estimation using Bootstrap, Monte Carlo, and Bayesian methods
- 실시간 시각화 및 비교
  Real-time visualization and comparison
- 인터랙티브 파라미터 조정
  Interactive parameter adjustment
- 상세한 통계 요약
  Detailed statistical summary

## 설치 방법 | Installation

1. 저장소 클론 | Clone the repository:
```bash
git clone https://github.com/jangwonboo/learn_bayesian.git
cd learn_bayesian
```

2. 가상환경 생성 및 활성화 | Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. 필요한 패키지 설치 | Install required packages:
```bash
pip install -r requirements.txt
```

## 사용 방법 | Usage

1. Streamlit 앱 실행 | Run the Streamlit app:
```bash
streamlit run streamlit_app.py
```

2. 웹 브라우저에서 앱 열기 | Open the app in your web browser:
```
http://localhost:8501
```

3. 사이드바에서 파라미터 조정 | Adjust parameters in the sidebar:
   - 실제 기울기 | True Slope
   - 실제 절편 | True Intercept
   - 노이즈 수준 | Noise Level
   - 샘플 수 | Sample Size
   - 반복 횟수 | Number of Iterations

## 분석 방법 | Analysis Methods

### 1. 부트스트랩 | Bootstrap
- 원본 데이터에서 반복적으로 리샘플링하여 추정치의 분포를 생성
  Generate distribution of estimates through repeated resampling from original data
- 데이터의 불확실성을 직접적으로 반영
  Directly reflect data uncertainty

### 2. 몬테카를로 | Monte Carlo
- 새로운 데이터를 생성하여 추정치의 분포를 생성
  Generate distribution of estimates by creating new data
- 모델의 일반화 성능을 평가
  Evaluate model generalization performance

### 3. 베이지안 | Bayesian
- 사전 분포를 가정하고 데이터를 통해 사후 분포를 계산
  Calculate posterior distribution through data assuming prior distribution
- 불확실성을 확률적으로 표현
  Express uncertainty probabilistically

## 라이선스 | License

이 프로젝트는 MIT 라이선스를 따릅니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details. 
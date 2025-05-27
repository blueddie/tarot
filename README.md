# 🔮 타로 카드 점술 웹 애플리케이션

AI 기반 타로 카드 점술을 제공하는 웹 애플리케이션입니다. 사용자가 질문을 선택하고 카드를 뽑으면 AI가 카드를 해석하여 점술 결과를 제공합니다.

## ✨ 주요 기능

- **질문 선택**: 미리 준비된 10가지 질문 중 선택 가능
- **카드 선택**: 인터랙티브한 카드 선택 인터페이스
- **카드 방향**: 정방향/역방향 설정 가능
- **AI 해석**: LLM 모델을 통한 개인화된 카드 해석
- **반응형 디자인**: 모바일 및 데스크톱 지원
- **실시간 공유**: ngrok을 통한 외부 접근 가능

## 🛠️ 기술 스택

- **Python**: 3.12.7
- **Backend**: FastAPI
- **Frontend**: HTML, CSS, JavaScript, Jinja2 템플릿
- **AI Model**: OpenAI LLM Model
- **서버**: Uvicorn
- **터널링**: ngrok

## 📁 프로젝트 구조

```
hy2/
├── main.py                 # FastAPI 메인 애플리케이션
├── requirements.txt        # Python 의존성
├── README.md              # 프로젝트 문서
├── models/
│   └── model.py           # LLM 모델 클래스
├── templates/             # HTML 템플릿
│   ├── main.html          # 메인 페이지
│   ├── questions.html     # 질문 선택 페이지
│   ├── card_selection.html # 카드 선택 페이지
│   └── result.html        # 결과 페이지
└── static/               # 정적 파일
    ├── css/              # 스타일시트
    ├── js/               # JavaScript 파일
    ├── images/           # 일반 이미지
    └── card_images/      # 타로 카드 이미지
```

## 🚀 설치 및 실행

### 1. 저장소 클론

```bash
git clone <repository-url>
cd hy2
```

### 2. Python 버전 확인

Python 3.12.7 이상이 필요합니다:
```bash
python --version
```

### 3. 가상환경 생성 (권장)

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate     # Windows
```

### 4. 의존성 설치

```bash
pip install -r requirements.txt
```

### 5. 애플리케이션 실행

```bash
python main.py
```

실행 후 콘솔에 표시되는 ngrok Public URL을 통해 외부에서도 접근할 수 있습니다.

## 📱 사용 방법

1. **메인 페이지**: 애플리케이션 시작
2. **질문 선택**: 10가지 미리 준비된 질문 중 하나 선택
3. **카드 선택**:
   - 뒤집힌 카드들 중 3장 선택
   - 각 카드를 클릭하여 정방향/역방향 설정
4. **결과 확인**: AI가 해석한 카드의 의미와 종합 해석 확인

## 🎯 API 엔드포인트

- `GET /`: 메인 페이지
- `GET /questions`: 질문 선택 페이지
- `GET /select-cards`: 카드 선택 페이지
- `GET /result`: 점술 결과 페이지

## 🔧 설정

### ngrok 설정

애플리케이션은 자동으로 ngrok 터널을 생성하여 외부 접근을 허용합니다. ngrok 계정이 필요할 수 있습니다.

### 카드 이미지

`static/card_images/` 디렉토리에 타로 카드 이미지 파일들을 배치해야 합니다. 파일명은 `.png` 형식이어야 하며, `back_card.png`는 카드 뒷면 이미지로 사용됩니다.

## 🤖 AI 모델

이 애플리케이션은 `models/model.py`에 정의된 커스텀 LLM 모델을 사용합니다. 모델은 다음 정보를 바탕으로 해석을 제공합니다:

- 사용자 질문
- 선택된 3장의 카드
- 각 카드의 방향 (정방향/역방향)
- 카드의 순서

## 🎨 커스터마이징

### 질문 추가/수정

`main.py`의 `questions_page` 함수에서 질문 목록을 수정할 수 있습니다.

### 스타일 변경

`static/css/` 디렉토리의 CSS 파일을 수정하여 디자인을 변경할 수 있습니다.

### 카드 해석 로직

`models/model.py`에서 AI 모델의 해석 로직을 수정할 수 있습니다.

## 🐛 문제 해결

### 일반적인 문제들

1. **카드 이미지가 표시되지 않는 경우**

   - `static/card_images/` 디렉토리에 이미지 파일이 있는지 확인
   - 파일 확장자가 `.png`인지 확인
2. **AI 해석이 작동하지 않는 경우**

   - `models/model.py`의 LLM 모델 설정 확인
   - 네트워크 연결 상태 확인
3. **ngrok 연결 문제**

   - ngrok 계정 설정 확인
   - 방화벽 설정 확인


---

⭐

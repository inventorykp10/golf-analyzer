# Golf Scorecard Analyzer - Proxy Server

이 서버는 골프 스코어카드 이미지를 분석하여 코스 정보를 자동으로 추출하는 프록시 서버입니다.

## 기능

- 스코어카드 이미지 업로드
- Google Gemini AI를 사용한 자동 분석
- 코스 정보 추출 (이름, 위치, Par, 거리, Stroke Index)

## 환경 변수 설정

Render.com에서 다음 환경 변수를 설정해야 합니다:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## API 엔드포인트

### POST /api/scorecard

스코어카드 이미지를 분석합니다.

**Request Body:**
```json
{
  "base64Data": "base64_encoded_image_data",
  "mimeType": "image/jpeg"
}
```

**Response:**
```json
{
  "name": "Course Name",
  "location": "City",
  "holes": 18,
  "par": [4, 4, 3, ...],
  "distances_blue": [365, 348, ...],
  "distances_white": [350, 335, ...],
  "stroke_index": [5, 11, 7, ...]
}
```

## 로컬 개발

```bash
# 의존성 설치
npm install

# 환경 변수 설정 (.env 파일 생성)
GEMINI_API_KEY=your_key_here

# 서버 실행
npm start
```

## Render 배포

1. GitHub에 코드 푸시
2. Render.com에서 Web Service 생성
3. 저장소 연결
4. Environment 탭에서 GEMINI_API_KEY 설정
5. 자동 배포

## 보안

⚠️ **중요:** API 키를 절대 코드에 직접 입력하지 마세요!
- 항상 환경 변수를 사용하세요
- .gitignore에 .env 파일이 포함되어 있는지 확인하세요
- GitHub에 API 키가 노출되지 않도록 주의하세요

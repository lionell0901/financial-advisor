# 중장년층 금융 조언 AI 프로젝트

Railway $5 요금제를 활용한 경량 RAG 기반 금융 조언 시스템

## 프로젝트 개요
- **대상 사용자**: 50-60대 중장년층
- **목적**: 이해하기 쉬운 금융 조언 제공
- **기술 스택**: FastAPI, SQLite, Google Gemini API
- **배포 환경**: Railway ($5/월 요금제)

## 개발 단계
- **Phase 1**: 기본 FastAPI + 하드코딩 데이터 (현재 단계)
- **Phase 2**: SQLite + 간단한 검색
- **Phase 3**: 외부 LLM API 연동
- **Phase 4**: RAG 엔진 완성

## 실행 방법
```bash
# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt

# 개발 서버 실행
python main.py
```

## API 엔드포인트
- `GET /`: 서비스 정보
- `POST /advice`: 금융 조언 요청
- `GET /health`: 서비스 상태 확인
- `GET /admin/stats`: 시스템 통계
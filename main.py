"""
중장년층을 위한 금융 조언 AI 시스템
Railway $5 요금제 제약사항을 고려한 경량 FastAPI 구현

Phase 1: 하드코딩된 금융 지식으로 시작
Phase 2: SQLite DB로 확장 예정
Phase 3: 외부 LLM API 연동 예정
"""
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from config import settings
import logging
from datetime import datetime
from typing import List, Optional
import os

# === 로깅 설정 ===
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# === FastAPI 앱 생성 ===
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Railway에서 실행되는 경량 RAG 기반 금융 조언 시스템",
    docs_url="/docs" if settings.DEBUG else None,  # 프로덕션에서는 docs 숨김
    redoc_url="/redoc" if settings.DEBUG else None
)

# === 정적 파일 서빙 설정 ===
# 정적 파일 디렉토리가 존재하는지 확인하고 마운트
static_dir = os.path.join(os.getcwd(), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# === 데이터 모델 정의 ===
class QuestionRequest(BaseModel):
    """금융 질문 요청 모델"""
    text: str = Field(..., min_length=5, max_length=200, description="금융 관련 질문")
    user_id: Optional[str] = Field("anonymous", description="사용자 식별자 (선택사항)")
    age_group: Optional[str] = Field("50-60대", description="연령대 (선택사항)")

class AdviceResponse(BaseModel):
    """금융 조언 응답 모델"""
    advice: str = Field(..., description="금융 조언 내용")
    confidence: float = Field(..., ge=0.0, le=1.0, description="응답 신뢰도")
    sources: List[str] = Field(..., description="정보 출처")
    keywords: List[str] = Field(..., description="관련 키워드")
    timestamp: str = Field(..., description="응답 생성 시간")
    disclaimer: str = Field(..., description="면책 조항")

# === 중장년층 금융 지식 데이터베이스 (하드코딩) ===
# Phase 2에서 SQLite로 이전 예정
FINANCIAL_KNOWLEDGE = {
    "예금": {
        "advice": """예금은 원금이 100% 보장되는 가장 안전한 금융상품입니다. 

📌 주요 특징:
• 예금자보호법에 의해 1인당 5천만원까지 보호
• 현재 시중은행 정기예금 금리: 연 3.0~3.5% 내외
• 중도해지시 약정금리보다 낮은 금리 적용

💡 중장년층 추천사항:
• 생활비 6개월분은 입출금이 자유로운 적금에 보관
• 목돈은 1~2년 정기예금으로 안전하게 운용
• 금리 변동 대비 단계별 만기 분산 고려""",
        
        "keywords": ["안전", "원금보장", "예금자보호", "정기예금", "적금"],
        "related_topics": ["적금", "금리", "안전투자"],
        "confidence": 0.95
    },
    
    "적금": {
        "advice": """적금은 매월 일정 금액을 저축하여 목돈을 마련하는 상품입니다.

📌 주요 특징:
• 매월 10만원~50만원 정도 납입 (상품별 상이)
• 복리 효과로 단순 저축보다 유리
• 중도해지시 약정금리 하향 적용

💡 중장년층 활용법:
• 은퇴자금 마련용으로 5년 이상 장기 적금 활용
• 자녀 교육비, 결혼자금 등 목적자금 마련
• 연금저축과 병행하여 세제혜택 극대화

⚠️ 주의사항: 중도해지시 금리 손실이 크므로 여유자금으로만 가입""",
        
        "keywords": ["목돈마련", "복리효과", "장기저축", "정기적립"],
        "related_topics": ["예금", "연금저축", "목표설정"],
        "confidence": 0.90
    },
    
    "연금": {
        "advice": """연금은 은퇴 후 안정적인 노후생활을 위한 필수 준비입니다.

📌 연금의 종류:
• 국민연금: 의무가입, 평균 월 55만원 정도 수령
• 개인연금(연금저축): 세액공제 연 400만원까지
• 퇴직연금(DC형/DB형): 직장 통해 가입

💡 중장년층 전략:
• 50대: 개인연금 추가납입으로 절세 + 노후준비
• 연금저축펀드보다 연금저축보험이 원금보장 측면에서 안전
• 국민연금 임의계속가입으로 수령액 증대 고려

📊 권장 비중: 안전자산(예적금) 70% + 연금상품 30%""",
        
        "keywords": ["노후준비", "세액공제", "개인연금", "국민연금", "퇴직연금"],
        "related_topics": ["세금", "은퇴계획", "안전투자"],
        "confidence": 0.92
    },
    
    "투자": {
        "advice": """중장년층 투자는 '안전성'을 최우선으로 해야 합니다.

📌 기본 원칙:
• 원금 손실 위험이 있는 투자는 여유자금으로만
• 전체 자산의 20~30%를 넘지 않도록 제한
• 단기 수익보다 장기 안정성 추구

💡 추천 투자처:
• 국고채, 회사채 등 채권형 펀드
• 배당주 중심의 안정적인 주식
• 리츠(REITs) - 부동산 간접투자

⚠️ 피해야 할 투자:
• 고위험 파생상품, 선물거래
• 원금보장 안 되는 구조화상품
• 이해하지 못하는 복잡한 상품""",
        
        "keywords": ["안전투자", "분산투자", "채권펀드", "배당주", "리츠"],
        "related_topics": ["위험관리", "자산배분", "포트폴리오"],
        "confidence": 0.85
    },
    
    "세금": {
        "advice": """중장년층은 절세를 통해 실질소득을 늘릴 수 있습니다.

📌 주요 절세 방법:
• 연금저축 세액공제: 연 400만원까지 16.5% 공제
• 퇴직연금 세액공제: 연 700만원까지 추가 공제
• 청약통장: 연 240만원까지 소득공제

💡 실전 절세팁:
• 의료비 공제: 총급여의 3% 초과분 공제
• 신용카드 소득공제: 총급여의 25% 초과 사용분
• 기부금 공제: 정치후원금, 종교단체 기부

📊 50대 맞벌이 기준 연간 절세효과: 50~100만원 가능""",
        
        "keywords": ["세액공제", "소득공제", "연금저축", "의료비공제", "절세"],
        "related_topics": ["연금", "재무계획", "소득관리"],
        "confidence": 0.88
    },
    
    "부동산": {
        "advice": """중장년층 부동산 투자는 신중한 접근이 필요합니다.

📌 현재 시장 상황 (2024년 기준):
• 고금리로 인한 매수심리 위축
• 지역별 격차 심화 (수도권 vs 지방)
• 전세시장 불안정성 지속

💡 중장년층 부동산 전략:
• 실거주 목적이 우선, 투자는 부차적으로 고려
• 대출 비중 최소화 (총 자산 대비 40% 이하)
• 유지비용 (세금, 관리비) 충분히 고려

⚠️ 주의사항: 
• 노후자금을 부동산에 과도하게 집중 금지
• 유동성 부족 문제 심각하게 고려""",
        
        "keywords": ["부동산투자", "실거주", "대출비중", "유동성", "세금"],
        "related_topics": ["자산배분", "위험관리", "유동성관리"],
        "confidence": 0.80
    }
}

# === 면책 조항 ===
DISCLAIMER = """
⚠️ 면책 조항: 본 조언은 일반적인 정보 제공 목적으로, 개인의 구체적인 재무상황을 반영하지 않습니다. 
실제 투자 결정 전에는 반드시 전문가와 상담하시기 바랍니다.
"""

# === 유틸리티 함수 ===
def find_best_match(question: str) -> tuple:
    """질문에 가장 적합한 금융 주제 찾기"""
    question_lower = question.lower()
    best_match = None
    best_confidence = 0.0
    
    # 키워드 기반 매칭 (Phase 2에서 더 정교한 검색으로 개선 예정)
    for topic, data in FINANCIAL_KNOWLEDGE.items():
        match_score = 0.0
        
        # 주제명 직접 매칭
        if topic in question_lower:
            match_score += 0.8
        
        # 키워드 매칭
        for keyword in data["keywords"]:
            if keyword.lower() in question_lower:
                match_score += 0.3
        
        # 관련 주제 매칭
        for related in data["related_topics"]:
            if related.lower() in question_lower:
                match_score += 0.2
        
        if match_score > best_confidence:
            best_confidence = match_score
            best_match = topic
    
    return best_match, min(best_confidence, 1.0)

# === API 엔드포인트 ===
@app.get("/")
def read_root():
    """웹 인터페이스 또는 API 정보 제공"""
    # 정적 파일이 있으면 웹 인터페이스 제공
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    
    # 정적 파일이 없으면 기존 JSON 응답
    return {
        "message": f"{settings.APP_NAME}에 오신 것을 환영합니다!",
        "version": settings.VERSION,
        "environment": settings.ENVIRONMENT,
        "description": "중장년층을 위한 쉬운 금융 조언 서비스",
        "available_endpoints": {
            "POST /advice": "금융 조언 요청",
            "GET /health": "서비스 상태 확인",
            "GET /admin/stats": "시스템 통계",
            "GET /topics": "사용 가능한 금융 주제 목록"
        },
        "usage_example": {
            "endpoint": "POST /advice",
            "request": {"text": "예금 상품 추천해주세요", "user_id": "user123"},
            "description": "예금, 적금, 연금, 투자, 세금, 부동산 등에 대해 질문하세요"
        }
    }

@app.post("/advice", response_model=AdviceResponse)
def get_financial_advice(request: QuestionRequest):
    """금융 조언 제공 엔드포인트"""
    logger.info(f"금융 상담 요청 - 사용자: {request.user_id}, 질문: {request.text[:50]}...")
    
    try:
        # 최적 매칭 금융 주제 찾기
        best_topic, confidence = find_best_match(request.text)
        
        if best_topic and confidence >= settings.CONFIDENCE_THRESHOLD:
            # 매칭된 주제로 조언 제공
            topic_data = FINANCIAL_KNOWLEDGE[best_topic]
            
            return AdviceResponse(
                advice=topic_data["advice"],
                confidence=min(confidence * topic_data["confidence"], 1.0),
                sources=[f"금융 기초지식: {best_topic}", "한국은행", "금융감독원"],
                keywords=topic_data["keywords"],
                timestamp=datetime.now().isoformat(),
                disclaimer=DISCLAIMER
            )
        else:
            # 기본 안내 응답
            return AdviceResponse(
                advice="""구체적인 금융 상품이나 상황을 말씀해주시면 더 정확한 조언을 드릴 수 있습니다.

📌 질문 가능한 주제:
• 예금/적금: "안전한 예금 상품 추천해주세요"
• 연금: "50대 연금 준비 방법이 궁금해요"  
• 투자: "중장년층 투자 방법 알려주세요"
• 세금: "연말정산 절세 방법이 있나요"
• 부동산: "지금 집을 사도 될까요"

💡 구체적인 상황(나이, 자산규모, 목표 등)을 함께 알려주시면 더 맞춤형 조언이 가능합니다.""",
                
                confidence=0.5,
                sources=["일반 금융 가이드"],
                keywords=["금융기초", "상담안내"],
                timestamp=datetime.now().isoformat(),
                disclaimer=DISCLAIMER
            )
            
    except Exception as e:
        logger.error(f"조언 생성 중 오류 발생: {str(e)}")
        raise HTTPException(status_code=500, detail="조언 생성 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.")

@app.get("/health")
def health_check():
    """서비스 상태 확인"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "environment": settings.ENVIRONMENT,
        "version": settings.VERSION,
        "services": {
            "database": "ready",  # Phase 2에서 실제 DB 연결 체크로 변경
            "knowledge_base": f"{len(FINANCIAL_KNOWLEDGE)} topics loaded",
            "memory_usage": "optimal"  # Phase 4에서 실제 메모리 모니터링 추가
        }
    }

@app.get("/topics")
def get_available_topics():
    """사용 가능한 금융 주제 목록"""
    topics = {}
    for topic, data in FINANCIAL_KNOWLEDGE.items():
        topics[topic] = {
            "keywords": data["keywords"],
            "related_topics": data["related_topics"],
            "example_question": f"{topic}에 대해 알려주세요"
        }
    
    return {
        "total_topics": len(FINANCIAL_KNOWLEDGE),
        "topics": topics,
        "usage_tip": "위 키워드들을 포함해서 질문하시면 더 정확한 답변을 받으실 수 있습니다."
    }

@app.get("/admin/stats")
def get_system_stats():
    """시스템 통계 정보 (관리자용)"""
    return {
        "knowledge_base": {
            "total_topics": len(FINANCIAL_KNOWLEDGE),
            "topics": list(FINANCIAL_KNOWLEDGE.keys()),
            "avg_confidence": sum(data["confidence"] for data in FINANCIAL_KNOWLEDGE.values()) / len(FINANCIAL_KNOWLEDGE)
        },
        "system_info": settings.get_api_info(),
        "performance": {
            "cache_ttl": settings.CACHE_TTL,
            "max_advice_length": settings.MAX_ADVICE_LENGTH,
            "confidence_threshold": settings.CONFIDENCE_THRESHOLD
        },
        "health_status": "operational"
    }

# === 메인 실행부 ===
if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"{settings.APP_NAME} 시작 중...")
    logger.info(f"환경: {settings.ENVIRONMENT}")
    logger.info(f"디버그 모드: {settings.DEBUG}")
    
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower()
    )
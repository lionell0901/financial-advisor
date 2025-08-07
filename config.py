"""
환경변수 관리 및 설정 모듈
Railway $5 요금제 제약사항을 고려한 설정 관리
"""
import os
from dotenv import load_dotenv

# .env 파일 로드 (프로젝트 루트에서)
load_dotenv()

class Settings:
    """애플리케이션 설정 클래스"""
    
    # === 기본 애플리케이션 설정 ===
    APP_NAME = "중장년층 금융조언 AI"
    VERSION = "0.1.0"
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT = os.getenv("ENVIRONMENT", "development")
    
    # === 서버 설정 ===
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))
    
    # === API 키 설정 (보안 중요!) ===
    # 현재는 주석 처리, Phase 3에서 활성화
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
    
    # === 캐시 및 성능 설정 (Railway 2GB RAM 고려) ===
    CACHE_TTL = 3600  # 1시간 캐시 (메모리 절약)
    MAX_CACHE_SIZE = 100  # 최대 캐시 항목 수
    
    # === 금융 조언 설정 ===
    MAX_ADVICE_LENGTH = 500  # 중장년층을 위한 간결한 설명
    CONFIDENCE_THRESHOLD = 0.7  # 응답 신뢰도 임계값
    
    # === 로깅 설정 ===
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    def __init__(self):
        """설정 초기화 및 검증"""
        # Phase 1에서는 기본 설정만 검증
        # Phase 3에서 API 키 필수 검증 추가 예정
        pass
    
    def get_db_path(self) -> str:
        """데이터베이스 파일 경로 (Phase 2에서 사용)"""
        return os.path.join(os.getcwd(), "financial_advisor.db")
    
    def is_production(self) -> bool:
        """프로덕션 환경 여부 확인"""
        return self.ENVIRONMENT.lower() == "production"
    
    def get_api_info(self) -> dict:
        """API 정보 반환 (디버깅/관리용)"""
        return {
            "app_name": self.APP_NAME,
            "version": self.VERSION,
            "environment": self.ENVIRONMENT,
            "debug_mode": self.DEBUG,
            "host": self.HOST,
            "port": self.PORT
        }

# 전역 설정 인스턴스
settings = Settings()
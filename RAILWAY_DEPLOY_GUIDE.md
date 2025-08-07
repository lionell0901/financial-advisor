# Railway 배포 가이드

## 1. 사전 준비
- [Railway](https://railway.app) 회원가입 및 로그인
- GitHub 계정 연결 준비

## 2. Git 저장소 업로드
현재 로컬 프로젝트를 GitHub에 업로드해야 합니다.

### GitHub에서 새 저장소 생성
1. GitHub에서 `financial-advisor` 저장소 생성 (Private 또는 Public)
2. 로컬에서 원격 저장소 연결:

```bash
git remote add origin https://github.com/YOUR_USERNAME/financial-advisor.git
git branch -M main
git push -u origin main
```

## 3. Railway 배포 단계

### Step 1: 새 프로젝트 생성
- Railway 대시보드에서 "New Project" 클릭
- "Deploy from GitHub repo" 선택
- `financial-advisor` 저장소 선택

### Step 2: 환경변수 설정
Railway 프로젝트 설정에서 다음 환경변수 추가:
```
ENVIRONMENT=production
DEBUG=False
PORT=8000
```

### Step 3: 배포 완료 대기
- 자동으로 빌드 및 배포 진행
- 5-10분 후 완료
- 제공된 URL로 접속 확인

## 4. 배포 후 테스트

### 기본 동작 확인
```bash
# 서비스 상태 확인
curl https://your-app-name.railway.app/health

# API 테스트
curl -X POST "https://your-app-name.railway.app/advice" \
  -H "Content-Type: application/json" \
  -d '{"text": "예금 상품 추천해주세요"}'
```

### 브라우저 테스트
- `https://your-app-name.railway.app/` - 서비스 정보
- `https://your-app-name.railway.app/docs` - API 문서 (개발용)
- `https://your-app-name.railway.app/topics` - 사용 가능한 주제 목록

## 5. 예상 리소스 사용량 (Railway $5 플랜)
- **메모리**: 50-100MB (2GB 한계 내)
- **CPU**: 낮은 사용률 (정적 지식베이스)
- **디스크**: 50MB 미만
- **네트워크**: 요청량에 따라 변동

## 6. 모니터링 포인트
- `/health` 엔드포인트로 서비스 상태 확인
- `/admin/stats`로 시스템 정보 모니터링
- Railway 대시보드에서 리소스 사용량 확인

## 7. 문제 해결
### 배포 실패시
1. 로그 확인: Railway 대시보드 > Deployments > 최신 배포 로그 확인
2. 환경변수 확인: 필수 변수들이 설정되었는지 확인
3. 파일 확인: requirements.txt, Procfile 등이 올바른지 확인

### 메모리 초과시
1. `CACHE_TTL` 늘려서 메모리 사용량 감소
2. `MAX_CACHE_SIZE` 줄여서 캐시 크기 제한
3. 불필요한 로그 레벨 조정

## 8. 다음 단계 (Phase 2)
배포 성공 후 다음 기능들을 단계적으로 추가:
- SQLite 데이터베이스 연동
- 검색 기능 개선
- 사용자 질문 로깅
- 성능 모니터링

---

**⚠️ 주의사항**: 
- API 키 등 민감 정보는 절대 코드에 포함하지 말고 환경변수로 관리
- 프로덕션 환경에서는 DEBUG=False로 설정
- Railway $5 플랜의 리소스 한계를 항상 고려
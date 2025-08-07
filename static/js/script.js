// 토스 스타일 JavaScript - 중장년층 친화적 UX

document.addEventListener('DOMContentLoaded', function() {
    // DOM 요소들
    const questionInput = document.getElementById('questionInput');
    const askButton = document.getElementById('askButton');
    const charCount = document.getElementById('charCount');
    const answerSection = document.getElementById('answerSection');
    const answerContent = document.getElementById('answerContent');
    const confidenceScore = document.getElementById('confidenceScore');
    const sourcesInfo = document.getElementById('sourcesInfo');
    const quickButtons = document.querySelectorAll('.quick-btn');
    const topicCards = document.querySelectorAll('.topic-card');

    // 상태 관리
    let isLoading = false;

    // 입력 텍스트 실시간 업데이트
    questionInput.addEventListener('input', function() {
        const length = this.value.length;
        charCount.textContent = length;
        
        // 버튼 활성화/비활성화
        askButton.disabled = length < 5 || length > 200 || isLoading;
        
        // 글자 수 색상 변경
        if (length > 180) {
            charCount.style.color = '#FF4757'; // 빨간색
        } else if (length > 150) {
            charCount.style.color = '#FF6B00'; // 주황색
        } else {
            charCount.style.color = '#9CA3AF'; // 기본 회색
        }
    });

    // Enter 키로 질문하기 (Shift+Enter는 줄바꿈)
    questionInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            if (!askButton.disabled) {
                handleAskQuestion();
            }
        }
    });

    // 질문하기 버튼 클릭
    askButton.addEventListener('click', handleAskQuestion);

    // 빠른 질문 버튼들
    quickButtons.forEach(button => {
        button.addEventListener('click', function() {
            const question = this.dataset.question;
            questionInput.value = question;
            questionInput.dispatchEvent(new Event('input'));
            
            // 부드럽게 스크롤
            questionInput.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
            
            // 잠시 후 질문 실행
            setTimeout(() => {
                if (!askButton.disabled) {
                    handleAskQuestion();
                }
            }, 500);
        });
    });

    // 주제 카드 클릭
    topicCards.forEach(card => {
        card.addEventListener('click', function() {
            const title = this.querySelector('.topic-title').textContent;
            const examples = {
                '예금/적금': '안전한 예금 상품 추천해주세요',
                '연금': '50대 연금 준비 방법 알려주세요',
                '투자': '중장년층 안전한 투자 방법이 궁금해요',
                '세금': '세금 절약 방법 알려주세요',
                '부동산': '지금 부동산 투자해도 될까요',
                '재무설계': '중장년층 재무설계 방법 알려주세요'
            };
            
            const question = examples[title] || `${title}에 대해 알려주세요`;
            questionInput.value = question;
            questionInput.dispatchEvent(new Event('input'));
            
            // 입력창으로 스크롤
            questionInput.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'center' 
            });
        });
    });

    // 질문 처리 함수
    async function handleAskQuestion() {
        const question = questionInput.value.trim();
        if (!question || question.length < 5 || isLoading) return;

        try {
            setLoadingState(true);
            
            const response = await fetch('/advice', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    text: question,
                    user_id: 'web_user_' + Date.now(),
                    age_group: '50-60대'
                })
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            displayAnswer(data);
            
        } catch (error) {
            console.error('Error:', error);
            displayError();
        } finally {
            setLoadingState(false);
        }
    }

    // 로딩 상태 설정
    function setLoadingState(loading) {
        isLoading = loading;
        askButton.disabled = loading || questionInput.value.length < 5;
        
        const buttonText = askButton.querySelector('.button-text');
        const spinner = askButton.querySelector('.loading-spinner');
        
        if (loading) {
            buttonText.textContent = '답변 준비 중...';
            spinner.style.display = 'block';
            askButton.style.cursor = 'not-allowed';
        } else {
            buttonText.textContent = '💬 질문하기';
            spinner.style.display = 'none';
            askButton.style.cursor = 'pointer';
        }
    }

    // 답변 표시
    function displayAnswer(data) {
        // 신뢰도 점수 표시
        const confidence = Math.round(data.confidence * 100);
        confidenceScore.textContent = confidence;
        
        // 신뢰도에 따른 배지 색상 변경
        const badge = document.querySelector('.confidence-badge');
        if (confidence >= 80) {
            badge.style.backgroundColor = '#00D563'; // 초록색
        } else if (confidence >= 60) {
            badge.style.backgroundColor = '#FF6B00'; // 주황색
        } else {
            badge.style.backgroundColor = '#FF4757'; // 빨간색
        }

        // 답변 내용 표시 (마크다운 스타일 파싱)
        const formattedAdvice = formatAdviceText(data.advice);
        answerContent.innerHTML = formattedAdvice;

        // 출처 정보 표시
        sourcesInfo.textContent = data.sources.join(', ');

        // 답변 섹션 표시
        answerSection.style.display = 'block';
        
        // 부드럽게 스크롤
        answerSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });

        // 성공 피드백 (햅틱 피드백 시뮬레이션)
        if (navigator.vibrate) {
            navigator.vibrate(50);
        }
    }

    // 에러 표시
    function displayError() {
        answerContent.innerHTML = `
            <div style="text-align: center; padding: 2rem; color: #FF4757;">
                <h4>⚠️ 일시적인 오류가 발생했습니다</h4>
                <p>잠시 후 다시 시도해주세요.</p>
                <p style="font-size: 14px; color: #9CA3AF; margin-top: 1rem;">
                    문제가 지속되면 페이지를 새로고침해주세요.
                </p>
            </div>
        `;
        
        confidenceScore.textContent = '-';
        sourcesInfo.textContent = '오류 발생';
        
        answerSection.style.display = 'block';
        answerSection.scrollIntoView({ 
            behavior: 'smooth', 
            block: 'start' 
        });
    }

    // 답변 텍스트 포매팅 (마크다운 스타일)
    function formatAdviceText(text) {
        return text
            // 볼드 텍스트
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            // 이탤릭 텍스트
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            // 제목 (📌, 💡 등으로 시작)
            .replace(/^(📌|💡|⚠️|📊)\s*(.+)$/gm, '<h4>$1 $2</h4>')
            // 리스트 아이템 (• 로 시작)
            .replace(/^•\s*(.+)$/gm, '<li>$1</li>')
            // 리스트 감싸기
            .replace(/(<li>.*<\/li>)/gs, function(match) {
                return '<ul>' + match + '</ul>';
            })
            // 줄바꿈
            .replace(/\n\n/g, '</p><p>')
            .replace(/\n/g, '<br>')
            // 문단 감싸기
            .replace(/^(.)/gm, '<p>$1')
            .replace(/(.)\n?$/gm, '$1</p>')
            // 중복 문단 태그 정리
            .replace(/<p><\/p>/g, '')
            .replace(/<p>(<h4>)/g, '$1')
            .replace(/(<\/h4>)<\/p>/g, '$1')
            .replace(/<p>(<ul>)/g, '$1')
            .replace(/(<\/ul>)<\/p>/g, '$1');
    }

    // 페이지 로드 시 입력창에 포커스
    questionInput.focus();
    
    // 스크롤 시 헤더 그림자 효과
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        const header = document.querySelector('.header');
        
        if (scrollTop > 100) {
            header.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        } else {
            header.style.boxShadow = 'none';
        }
        
        lastScrollTop = scrollTop;
    });

    // 성능 최적화: 디바운스 함수
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // 입력 최적화 (디바운스 적용)
    const debouncedInput = debounce(function() {
        // 추가 입력 처리 로직이 필요한 경우
    }, 300);

    questionInput.addEventListener('input', debouncedInput);
});
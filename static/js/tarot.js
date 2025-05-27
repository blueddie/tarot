// 타로 카드 해석 결과를 가져오는 함수
async function getTarotReading(selectedCards) {
    try {
        const response = await fetch('http://localhost:8000/tarot', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                질문: selectedCards.question,
                카드_1: {
                    카드: selectedCards.card1.name,
                    방향: selectedCards.card1.direction
                },
                카드_2: {
                    카드: selectedCards.card2.name,
                    방향: selectedCards.card2.direction
                },
                카드_3: {
                    카드: selectedCards.card3.name,
                    방향: selectedCards.card3.direction
                }
            })
        });

        if (!response.ok) {
            throw new Error('API 호출 중 오류가 발생했습니다');
        }

        const result = await response.json();
        
        // 결과를 화면에 표시
        displayTarotResult(result);
        
    } catch (error) {
        console.error('Error:', error);
        alert('타로 카드 해석 중 오류가 발생했습니다.');
    }
}

// 타로 카드 결과를 화면에 표시하는 함수
function displayTarotResult(result) {
    const resultContainer = document.getElementById('tarot-result');
    if (!resultContainer) return;

    // 로딩 표시
    resultContainer.innerHTML = '<div class="loading">해석 중...</div>';

    try {
        resultContainer.innerHTML = `
            <div class="result-section">
                <h3>과거의 해석</h3>
                <p>${result.카드_1_해석}</p>
            </div>
            <div class="result-section">
                <h3>현재의 해석</h3>
                <p>${result.카드_2_해석}</p>
            </div>
            <div class="result-section">
                <h3>미래의 해석</h3>
                <p>${result.카드_3_해석}</p>
            </div>
            <div class="result-section">
                <h3>종합 해석</h3>
                <p>${result.종합_해석}</p>
            </div>
        `;
    } catch (error) {
        console.error('결과 표시 중 오류:', error);
        resultContainer.innerHTML = '<div class="error">해석 결과를 표시하는 중 오류가 발생했습니다.</div>';
    }
}

// 타로 카드 선택 완료 후 결과 요청
function requestTarotReading() {
    // 입력값 검증
    const question = document.getElementById('question').value;
    if (!question) {
        alert('질문을 입력해주세요.');
        return;
    }

    const card1 = document.querySelector('[data-position="1"]');
    const card2 = document.querySelector('[data-position="2"]');
    const card3 = document.querySelector('[data-position="3"]');

    if (!card1.dataset.cardName || !card2.dataset.cardName || !card3.dataset.cardName) {
        alert('모든 카드를 선택해주세요.');
        return;
    }

    const selectedCards = {
        question: question,
        card1: {
            name: card1.dataset.cardName,
            direction: card1.dataset.direction || '정방향'
        },
        card2: {
            name: card2.dataset.cardName,
            direction: card2.dataset.direction || '정방향'
        },
        card3: {
            name: card3.dataset.cardName,
            direction: card3.dataset.direction || '정방향'
        }
    };

    getTarotReading(selectedCards);
}

// 타로 카드 목록
const tarotCards = [
    "The Fool", "The Magician", "The High Priestess", "The Empress", "The Emperor",
    "The Hierophant", "The Lovers", "The Chariot", "Strength", "The Hermit",
    "Wheel of Fortune", "Justice", "The Hanged Man", "Death", "Temperance",
    "The Devil", "The Tower", "The Star", "The Moon", "The Sun",
    "Judgement", "The World"
];

// 페이지 로드 시 카드 선택 UI 초기화
document.addEventListener('DOMContentLoaded', function() {
    initializeCardSelection();
});

// 카드 선택 UI 초기화
function initializeCardSelection() {
    const cardSlots = document.querySelectorAll('.card-slot');
    
    cardSlots.forEach(slot => {
        // 카드 선택 버튼 추가
        const selectButton = document.createElement('button');
        selectButton.textContent = '카드 선택';
        selectButton.className = 'card-select-button';
        selectButton.onclick = () => showCardSelection(slot);
        
        // 방향 선택 버튼 추가 (카드 선택 후 표시)
        const directionButton = document.createElement('button');
        directionButton.textContent = '방향 전환';
        directionButton.className = 'direction-button';
        directionButton.style.display = 'none';
        directionButton.onclick = () => toggleCardDirection(slot);
        
        slot.appendChild(selectButton);
        slot.appendChild(directionButton);
    });
}

// 카드 선택 모달 표시
function showCardSelection(slot) {
    const modal = document.createElement('div');
    modal.className = 'card-selection-modal';
    
    const modalContent = document.createElement('div');
    modalContent.className = 'modal-content';
    
    const closeButton = document.createElement('button');
    closeButton.textContent = '×';
    closeButton.className = 'close-button';
    closeButton.onclick = () => modal.remove();
    
    modalContent.appendChild(closeButton);
    
    // 카드 목록 생성
    tarotCards.forEach(cardName => {
        const cardButton = document.createElement('button');
        cardButton.textContent = cardName;
        cardButton.onclick = () => {
            selectCard(slot, cardName);
            modal.remove();
        };
        modalContent.appendChild(cardButton);
    });
    
    modal.appendChild(modalContent);
    document.body.appendChild(modal);
}

// 카드 선택
function selectCard(slot, cardName) {
    slot.dataset.cardName = cardName;
    slot.dataset.direction = '정방향';
    
    // 카드 이미지나 이름 표시
    const cardDisplay = document.createElement('div');
    cardDisplay.className = 'selected-card';
    cardDisplay.textContent = cardName;
    
    // 기존 선택된 카드가 있다면 제거
    const existingCard = slot.querySelector('.selected-card');
    if (existingCard) {
        existingCard.remove();
    }
    
    // 방향 버튼 표시
    const directionButton = slot.querySelector('.direction-button');
    directionButton.style.display = 'block';
    
    // 선택 버튼 숨기기
    const selectButton = slot.querySelector('.card-select-button');
    selectButton.style.display = 'none';
    
    slot.insertBefore(cardDisplay, slot.firstChild);
}

// 카드 방향 전환
function toggleCardDirection(slot) {
    const currentDirection = slot.dataset.direction;
    slot.dataset.direction = currentDirection === '정방향' ? '역방향' : '정방향';
    
    // 방향 표시 업데이트
    const cardDisplay = slot.querySelector('.selected-card');
    if (cardDisplay) {
        cardDisplay.classList.toggle('reversed');
    }
} 
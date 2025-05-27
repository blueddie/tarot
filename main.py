from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pyngrok import ngrok
import random
import os
import json
from typing import List
from pydantic import BaseModel
from models.model import LLMModel

class Card:
    def __init__(self, name: str, is_reversed: bool, position: int):
        self.name = name
        self.is_reversed = is_reversed
        self.position = position  # 카드 순서 추가

app = FastAPI()

# 정적 파일과 템플릿 설정
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# LLM 모델 인스턴스 생성
llm_model = LLMModel()

@app.get("/", response_class=HTMLResponse)
async def main_page(request: Request):
    return templates.TemplateResponse(
        "main.html",
        {"request": request}
    )

@app.get("/questions", response_class=HTMLResponse)
async def questions_page(request: Request):
    questions = [
        "현재 나의 전반적인 상황은 어떤가요?",
        "내 연애는 어떻게 될까요?",
        "내 진로는 어떻게 될까요?",
        "오늘 하루는 어떨까요?",
        "내가 지금 가장 집중해야 할 것은 무엇인가요?",
        "나의 숨겨진 재능이나 잠재력은 무엇인가요?",
        "현재 나를 둘러싼 인간관계는 어떤가요?",
        "내 금전운과 재정 상황은 어떻게 될까요?",
        "오늘 누군가와 만날 가능성이 있을까요?",
        "내가 지금 가장 피해야 할 것은 무엇인가요?"
    ]
    return templates.TemplateResponse(
        "questions.html",
        {"request": request, "questions": questions}
    )

@app.get("/select-cards", response_class=HTMLResponse)
async def select_cards(request: Request, question: str):
    # card_images 디렉토리에서 카드 파일 목록을 가져옴
    card_files = [f for f in os.listdir("static/card_images") 
                 if f.endswith('.png') and f != 'back_card.png']
    # 카드를 랜덤하게 섞음
    random.shuffle(card_files)
    
    return templates.TemplateResponse(
        "card_selection.html",
        {
            "request": request, 
            "cards": card_files,
            "question": question
        }
    )

@app.get("/result", response_class=HTMLResponse)
async def show_result(
    request: Request,
    question: str,
    cards: str,  # JSON string: [{"name": "card.png", "is_reversed": true, "position": 1}, ...]
):
    try:
        cards_data = json.loads(cards)
        # position 순서대로 정렬
        cards_data.sort(key=lambda x: x["position"])
        cards_list = [Card(card["name"], card["is_reversed"], card["position"]) for card in cards_data]
        
        # LLM 입력용 데이터 생성
        llm_input_data = {
            "질문": question,
            "카드 1": {
                "카드": cards_list[0].name.replace('.png', '').replace('_', ' ').title(),
                "방향": "역방향" if cards_list[0].is_reversed else "정방향"
            },
            "카드 2": {
                "카드": cards_list[1].name.replace('.png', '').replace('_', ' ').title(),
                "방향": "역방향" if cards_list[1].is_reversed else "정방향"
            },
            "카드 3": {
                "카드": cards_list[2].name.replace('.png', '').replace('_', ' ').title(),
                "방향": "역방향" if cards_list[2].is_reversed else "정방향"
            }
        }
        
        # LLM 모델 호출
        result = llm_model.get_answer(json.dumps(llm_input_data, ensure_ascii=False))
        interpretation = json.loads(result)
        
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "question": question,
                "cards": cards_list,
                "interpretation": interpretation
            }
        )
    except Exception as e:
        print(f"Error in show_result: {str(e)}")
        # 에러 발생 시 기본 해석 제공
        default_interpretation = {
            "카드_1_해석": "카드 해석을 불러오는 중 오류가 발생했습니다.",
            "카드_2_해석": "카드 해석을 불러오는 중 오류가 발생했습니다.",
            "카드_3_해석": "카드 해석을 불러오는 중 오류가 발생했습니다.",
            "종합_해석": "해석을 불러오는 중 오류가 발생했습니다. 다시 시도해주세요."
        }
        
        cards_data = json.loads(cards)
        cards_data.sort(key=lambda x: x["position"])
        cards_list = [Card(card["name"], card["is_reversed"], card["position"]) for card in cards_data]
        
        return templates.TemplateResponse(
            "result.html",
            {
                "request": request,
                "question": question,
                "cards": cards_list,
                "interpretation": default_interpretation
            }
        )

if __name__ == "__main__":
    import uvicorn
    # ngrok 터널 설정
    ngrok_tunnel = ngrok.connect(8000)
    print('Public URL:', ngrok_tunnel.public_url)
    uvicorn.run(app, host="127.0.0.1", port=8000) 
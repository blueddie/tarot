from openai import OpenAI
from dotenv import load_dotenv
import os
import json
from datetime import datetime
load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


class LLMModel:

    def __init__(self):
        self.client = OpenAI(api_key=openai_api_key)
        self.input_data = None

        self.system_prompt = f"""
        당신은 숙련된 타로카드 점술가입니다.
        사용자의 질문에 대해 타로카드를 사용하여 점술을 진행합니다.
        타로카드는 총 22장이며, 전체 카드 구성입니다.
        타로 카드는 순서와 방향이 있습니다.
        순서는 카드 1은 과거를, 카드 2는 현재를, 카드 3은 미래를 의미합니다.
        방향은 정방향과 역방향이 있으니 방향을 고려하여 해석합니다.

        카드의 해석은 항상 긍정적일 필요는 없습니다.
        각 카드의 의미는 질문에 따라 다르게 해석합니다.
        
        [타로카드 전체 구성]
        0. The Fool            - 바보
        1. The Magician        - 마법사
        2. The High Priestess  - 여교황
        3. The Empress         - 여제
        4. The Emperor         - 황제
        5. The Hierophant      - 교황
        6. The Lovers          - 연인
        7. The Chariot         - 전차
        8. Strength            - 힘
        9. The Hermit          - 은둔자
        10. Wheel of Fortune    - 운명의 수레바퀴
        11. Justice             - 정의
        12. The Hanged Man      - 매달린 남자
        13. Death               - 죽음
        14. Temperance          - 절제
        15. The Devil           - 악마
        16. The Tower           - 탑
        17. The Star            - 별
        18. The Moon            - 달
        19. The Sun             - 태양
        20. Judgement           - 심판
        21. The World           - 세계

        카드 해석에는 카드의 한글 이름을 사용합니다.

        [아웃풋 포맷]
        출력은 단일 JSON 객체여야 합니다.
        {{
            "카드_1_해석": "과거를 나타내는 첫 번째 카드에 대한 자세한 해석",
            "카드_2_해석": "현재를 나타내는 두 번째 카드에 대한 자세한 해석",
            "카드_3_해석": "미래를 나타내는 세 번째 카드에 대한 자세한 해석",
            "종합_해석": "세 카드의 의미를 종합한 전체적인 해석과 조언"
        }}

        각 카드의 해석은 다음을 포함해야 합니다:
        1. 카드의 기본적인 의미
        2. 카드의 방향(정/역)에 따른 특별한 의미
        3. 질문자의 상황에 맞는 구체적인 해석
        4. 실질적인 조언이나 주의사항

        종합 해석은 다음을 포함해야 합니다:
        1. 세 카드의 전체적인 흐름 분석
        2. 질문자의 상황에 대한 통찰
        3. 미래를 위한 구체적인 조언
        4. 주의해야 할 점이나 활용할 수 있는 기회
        """


        self.model_name = "gpt-4o"

    def get_answer(self, input_data):

        self.input_data_source = input_data

        
        # 입력 데이터로 user_prompt 업데이트
        user_prompt = f"""
            제가 고른 질문과 카드는 다음과 같습니다.
           {self.input_data_source}

           타로카드 점술 결과를 출력해주세요.
        """

        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": self.system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=1.0
        )

        answer_json = response.choices[0].message.content

        return answer_json

from fastapi import FastAPI, Request, Form
# from fastapi.responses import RedirectResponse
# from database.connection import conn
from routes.users import user_router
from routes.events import event_router

import random

import uvicorn

from database.connection import Settings

app = FastAPI()
settings = Settings()

# 라우트 등록
app.include_router(user_router, prefix="/user") # test에서 /user/signin 으로 쓰는 이유
app.include_router(event_router, prefix="/event")

# CORS 설정
from fastapi.middleware.cors import CORSMiddleware

origins = ["*"] # 허용할 domain

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

# # huggingface - gradio
# from gradio_client import Client
# HF_MODEL = "KimSHine/Scenario_Koalpaca_5.8B-lora"

# client = Client(HF_MODEL)

# gradio - test
from gradio_client import Client

# client = Client("abidlabs/en2fr")

HF_MODEL = "skang187/yeollm_test"

client = Client(HF_MODEL)

def make_scenario(instruction, input_summary):
    
    result = client.predict(instruction, input_summary, api_name="/predict")
    return result

# # DB 연결
# @app.on_event("startup")
# # def on_startup():
# #     conn()
# async def init_db():
#     await settings.initialize_database()

from fastapi.templating import Jinja2Templates

# html fastapi 전송방법

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):    
    return templates.TemplateResponse("home.html",{"request":request})

@app.get("/scenario")
async def scenario_page(request: Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.post("/scenario/generate")
async def generate_scenario(request : Request):
    form_data = await request.form()
    
    selected_value = form_data.get('written_type')
    given_summary = form_data.get('input_summary')
    
    print(selected_value, given_summary)
    
    results_label : tuple[str] = ("YEOLLM", "TextDavinci-003", "GPT3.5")
    results_content : tuple[str]= make_scenario(selected_value, given_summary)
    
    results = [(k,v) for k,v in zip(results_label, results_content)]
    
    print(results)
    
    # shuffle
    random.shuffle(results)
    
    answer : dict = {
        results[0][0] : results[0][1],
        results[1][0] : results[1][1],
        results[2][0] : results[2][1],
    }
    
    return answer



# uvicorn.run() 으로 지정 포트에서 애플리케이션 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
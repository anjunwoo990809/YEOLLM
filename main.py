from fastapi import FastAPI, Request
import random
import uvicorn
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from gradio_client import Client
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# CORS 설정
# https://stackoverflow.com/questions/65191061/fastapi-cors-middleware-not-working-with-get-method/65994876#65994876
origins = [
    "*"
]

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins = origins,
        allow_credentials = True,
        allow_methods = ["*"],
        allow_headers = ["*"],
    )
]
app = FastAPI(middleware=middleware)

HF_MODEL = 'skang187/yeollm' #"skang187/yeollm"

client = Client(HF_MODEL)

def make_scenario(selected_value : str, input_summary):
    
    result = client.predict(selected_value, input_summary, api_name="/predict")
    return result

# html fastapi 전송방법
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):    
    return templates.TemplateResponse("yeollm_start.html",{"request":request})

@app.get("/scenario")
async def scenario_page(request: Request):
    return templates.TemplateResponse("yeollm_model.html",{"request":request})

generate_text = []

@app.post("/scenario/generate")
async def generate_scenario(request : Request):
    form_data = await request.form()
    
    selected_value = form_data.get('written_type')
    given_summary = form_data.get('input_summary')
    
    print(selected_value, given_summary)
    
    results_label : tuple[str] = ("YEOLLM", "TextDavinci-003", "GPT3.5")
    results_content = make_scenario(selected_value, given_summary)
    
    results = [(k,v) for k,v in zip(results_label, results_content)]
    
    print(results)
    
    # shuffle
    random.shuffle(results)
    
    answer : list = [
        (results[0][0] , results[0][1].lstrip().split("\n")),
        (results[1][0] , results[1][1].lstrip().split("\n")),
        (results[2][0] , results[2][1].lstrip().split("\n"))
    ]
    generate_text.append(answer)
    return answer

from fastapi.responses import HTMLResponse

@app.get("/result", response_class=HTMLResponse)
@app.post("/result", response_class=HTMLResponse)
async def scenario_result(request: Request):
    return templates.TemplateResponse("yeollm_result.html", {"request": request, "generate_text": generate_text})


# uvicorn.run() 으로 지정 포트에서 애플리케이션 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
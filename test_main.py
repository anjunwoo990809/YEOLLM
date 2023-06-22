from gradio_client import Client

# client = Client("abidlabs/en2fr")

HF_MODEL = "skang187/yeollm_test"

client = Client(HF_MODEL)

def make_scenario(instruction, input_summary):
    
    result = client.predict(instruction, input_summary, api_name="/predict")
    return result

if __name__ == "__main__":
    print("printing")
    print(make_scenario("역사 대본 만들어줘",
        "준우는 오늘 점심을 너무 많이 먹어서 세정이에게 약을 사달라고 부탁했다."))
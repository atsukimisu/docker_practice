from fastapi import FastAPI

from request import RequestModel

app = FastAPI()

@app.get("/hello")
async def greetings():
    return {
        "message": "Hello World."
    }

@app.post("/echo/")
async def parrot_response(request_data: RequestModel):
    input_message = request_data.message
    response_content = {
        "content": input_message
        }
    return response_content

@app.get("/hoge")
async def loadfile(file):
    with open('hoge.txt') as h:
        h.seek(0)
        text = h.read()
    return {
        "content": text
    }
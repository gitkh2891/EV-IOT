import time
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, WebSocket, Request
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random

app = FastAPI()
templates = Jinja2Templates(directory="templates")

#define message handling
async def server_handle_message(message, ws):
    if(message=="webon"):
        await ws.send_text("Start button clicked")
        print("front end request turn on")

    elif(message=="weboff"):
        await ws.send_text("Stop button clicked")
        print("front end request turn off")

    elif(message=="report"):
        num=round((random.random())*100)
        await ws.send_text(str(num))
        print(str(num))
        print("front end request random number")

    elif(message=="charger preparing"):
        await ws.send_text("confirm preparing")
        print("server confirm that charger is preparing and updates frontend")

    elif(message=="charger request auth"):
        await ws.send_text("auth request accepted")
        print("server accepts auth request")

    elif(message=="start transaction request"):
        await ws.send_text("transaction request confirmed")
        print("server confirms transaction request")   

    elif(message=="charger charging"):
        await ws.send_text("confirm charging")
        print("server confirm that charger is charging and updates frontend")

    else:
        await ws.send_text(message)
        print("no amendments to msg")


@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    # Render the HTML template
    return templates.TemplateResponse("index.html", {"request" : request})

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await server_handle_message(data,websocket)
        
        print("server parsed message")          
        #await websocket.send_text(data)

     
# start the server
if __name__ == "__main__":
    clients = []
    uvicorn.run(app, host="127.0.0.1", port=80, ws_ping_interval=600, ws_ping_timeout=60)

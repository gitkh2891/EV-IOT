import time
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi import FastAPI, WebSocket, Request
import uvicorn
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
import random
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# define connection manager class
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


#create the manager class to manage all connections 
manager = ConnectionManager()


#define message handling
async def server_handle_message(message, ws):
    if(message=="webon"):
        await ws.send_text("start")
        print("front end request start")

    elif(message=="weboff"):
        await ws.send_text("stop")
        print("front end request stop")

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

# http endpoints

# Render the HTML template for internal testing UI
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):

    return templates.TemplateResponse("index.html", {"request" : request})


# http endpoint that invokes the Manager class and broadcast a "start" meesage with charger_id to all connected clients
# invoke with example: send a POST request to http://localhost/start?id=123 

@app.post('/start')
async def start(request: Request):
    charger_id = request.query_params["id"]
    await manager.broadcast(str(charger_id)+"start")
    return ("Start message broadcasted to clients") 


# similar http endpoint for sending "stop" message

@app.post('/stop')
async def start(request: Request):
    charger_id = request.query_params["id"]
    await manager.broadcast(str(charger_id)+"stop")
    return ("Stop message broadcasted to clients") 



# websocket endpoint

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    while True:
        
        data = await websocket.receive_text()
        await manager.broadcast(data)

        print("server parsed message")          


# original ws endpoint without use of manager class

@app.websocket("/ws2")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await server_handle_message(data,websocket)
        
        print("server parsed message")          

# start the server
if __name__ == "__main__":
    clients = []
    uvicorn.run(app, host="127.0.0.1", port=80, ws_ping_interval=600, ws_ping_timeout=60)
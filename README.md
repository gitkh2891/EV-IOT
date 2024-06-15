The files uploaed here are meant for mid-term prep and are correct as at 15th Jun 2024.

The server.py file represents the "backend" central server and is meant to be hosted in the cloud.
This script sets up a simple WebSocket server on localhost and deploys 2 FastAPI endpoints: 
- 1 websocket endpoint "/ws" serving the WebSocket server
- 1 http endpoint "/" serving the index.html which is a simple html front-end to test the WebSocket connection and simplified message handling logic of the server script, based on high-level OCPP 1.6J sequence diagram.   

The index.html should be stored in a "tenmplates" folder for static files, in accordance to the standard folder structure for FastAPI.

The client.py is supposed to be running in a Raspberry Pi.
Message handling logic is not implemented yet.


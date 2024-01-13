from flask import Flask, render_template
from flask_socketio import SocketIO
from threading import Thread
import json
import websocket
from flask_cors import CORS
import time

app = Flask(__name__)
CORS(app, origins="http://localhost:3000")
# Update the SocketIO initialization with the correct path
socketio = SocketIO(app, cors_allowed_origins="http://localhost:3000", path='/socket.io')

exchange_ws_url = "ws://localhost:8765"
last_timestamp = None
total_changes = 0
ws = None  # Declare ws as a global variable

def on_message(ws, message):
    global last_timestamp, total_changes

    data = json.loads(message)
    print(f"WebSocket Connection Opened.")
    print(f"Symbol: BTC-USD\nInterval: {data['Interval']} seconds\nTotal Changes: {data['Total_Changes']}")
    print(f"Speed: {data['Speed']} changes per second")
    print(f"Velocity: {data['Velocity']} (c/s*)\n")
    # print(socketio)
    socketio.emit('orderbook_update', data)
    # print(data)
    # if 'bids' in data and 'asks' in data:
       
    #     timestamp = data['time']

    #     if last_timestamp:
    #         time_diff = timestamp - last_timestamp
    #         changes_per_second = 1 / time_diff
    #         total_changes += random.randint(100, 200)

    #         # Check if the WebSocket connection is open before emitting data
    #         if ws and ws.sock and ws.sock.connected:
    #             socketio.emit('orderbook_update', {
    #                 'total_changes': total_changes,
    #                 'speed': changes_per_second,
    #                 'velocity': total_changes - changes_per_second
    #             })

    #             print(f"WebSocket Connection Opened.")
    #             print(f"Symbol: BTC-USD\nInterval: {time_diff} seconds\nTotal Changes: {total_changes}")
    #             print(f"Speed: {changes_per_second:.2f} changes per second")
    #             print(f"Velocity: {total_changes - changes_per_second:.2f} (c/s*)\n")
    #         else:
    #             print("WebSocket Connection is closed.")

    #     last_timestamp = timestamp
        
def on_close(ws, close_status_code, close_msg):
    print("WebSocket Connection Closed.")

def on_open(ws):
    print("WebSocket Connection Opened.")
    subscribe_msg = {
    "type": "subscribe",
    "product_ids": [
        "BTC-USD"
    ],
    "channels": [
        "full"
    ],
   
    "timestamp": str(time.time())
}
    ws.send(json.dumps(subscribe_msg))
    
            
@socketio.on('request_orderbook_update')
def handle_request_orderbook_update():
    global ws
    # Check if the WebSocket connection is already open
    if not ws or (ws and not getattr(ws, 'sock', None) or not ws.sock.connected):
        ws = websocket.WebSocketApp(exchange_ws_url, on_message=on_message, on_error=on_error)
        ws.on_open = on_open
        socketio.start_background_task(target=ws.run_forever)
    else:
        print("WebSocket Connection is already open.")

def on_error(ws, error):
    print(error)


def run_websocket():
    global ws
    ws = websocket.WebSocketApp(exchange_ws_url, on_message=on_message, on_error=on_error)
    ws.on_open = on_open

    # Instead of ws.run_forever(), use socketio.start_background_task
    socketio.start_background_task(target=ws.run_forever)

    # socketio.run(app, debug=True, use_reloader=False)
    socketio.run(app, debug=True, use_reloader=False)

if __name__ == "__main__":
    socket_thread = Thread(target=run_websocket)
    socket_thread.start()

    # Start Flask app with Socket.IO on port 8000
    

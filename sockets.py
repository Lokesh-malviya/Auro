import asyncio
import json
import websockets
import random
import time

async def fake_order_book(websocket, path):
    total_changes = 0
    last_timestamp = None

    while True:
        time.sleep(3)  # Adjust the interval
        total_changes += random.randint(100, 200)

        current_timestamp = time.time()

        if last_timestamp:
            time_diff = current_timestamp - last_timestamp
            changes_per_second = (total_changes - last_timestamp) / time_diff
            velocity = total_changes - changes_per_second

            # Create the fake data similar to the provided format
            fake_data = {
                'Symbol': 'BTC-USD',
                'Interval': f'{time_diff:.2f} seconds',
                'Total_Changes': total_changes,
                'Speed': f'{changes_per_second:.2f} changes per second',
                'Velocity': f'{velocity:.2f} (c/s*)'
            }

            # Send the fake data to connected clients
            await websocket.send(json.dumps(fake_data))

        last_timestamp = current_timestamp

async def start_mock_server():
    server = await websockets.serve(fake_order_book, "localhost", 8765)

    print("Mock WebSocket Server Started")

    # Keep the event loop running
    await server.wait_closed()

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_mock_server())

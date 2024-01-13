
// src/App.js
import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';
import { Line } from 'react-chartjs-2';

const socket = io('http://localhost:5000', { transports: ['websocket'], path: '/socket.io' });

function App() {
  const [orderbook, setOrderbook] = useState({
    total_changes: 0,
    speed: 0,
    velocity: 0,
    data: [], // Added data array to store changes per second over time
  });

  useEffect(() => {
    socket.on('orderbook_update', (data) => {
      setOrderbook(data);
    });

    socket.emit('request_orderbook_update');

    // return () => {
    //   socket.disconnect();
    // };
  }, []);

  const chartData = {
    labels: orderbook.data.map((_, index) => index), // Use index as labels for the index axis
    datasets: [
      {
        label: 'Changes Per Second',
        data: orderbook.data,
        fill: false,
        borderColor: 'rgba(75,192,192,1)',
        borderWidth: 2,
      },
    ],
  };

  return (
    <div className="App">
      <h1>Orderbook Velocity Tracker</h1>
      <p>Changes per Second: {orderbook.speed.toFixed(2)}</p>
      {/* <Line data={chartData} options={{ maintainAspectRatio: false }} /> */}
    </div>
  );
}

export default App;

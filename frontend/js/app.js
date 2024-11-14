let chart;
let temperatureData = [];
let humidityData = [];

const chartOptions = {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: 'Sensor Data',
            data: [],
            borderColor: 'rgb(75, 192, 192)',
            tension: 0.1
        }]
    },
    options: {
        responsive: true,
        scales: {
            y: {
                beginAtZero: true
            }
        },
        animation: {
            duration: 0 // Disable animation for better performance
        }
    }
};

function initChart() {
    const ctx = document.getElementById('sensorChart').getContext('2d');
    chart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Temperature (°C)',
                    data: [],
                    borderColor: 'rgb(255, 99, 132)',
                    backgroundColor: 'rgba(255, 99, 132, 0.5)',
                    yAxisID: 'temperature'
                },
                {
                    label: 'Humidity (%)',
                    data: [],
                    borderColor: 'rgb(53, 162, 235)',
                    backgroundColor: 'rgba(53, 162, 235, 0.5)',
                    yAxisID: 'humidity'
                }
            ]
        },
        options: chartOptions
    });
}

function handleSensorData(data) {
    const timestamp = new Date(data.timestamp).toLocaleTimeString();
    
    if (data.topic.includes('temperature')) {
        temperatureData.push({ timestamp, value: data.value });
        if (temperatureData.length > 50) temperatureData.shift();
    } else if (data.topic.includes('humidity')) {
        humidityData.push({ timestamp, value: data.value });
        if (humidityData.length > 50) humidityData.shift();
    }

    updateChart();
    updateDebugInfo();
}

function updateChart() {
    if (!chart) return;
    
    const labels = temperatureData.map(d => d.timestamp);
    chart.data.labels = labels;
    chart.data.datasets[0].data = temperatureData.map(d => d.value);
    chart.data.datasets[1].data = humidityData.map(d => d.value);
    chart.update();
}

function updateDebugInfo() {
    document.getElementById('debugInfo').textContent = 
        `Temperature points: ${temperatureData.length} | Humidity points: ${humidityData.length}`;
}

function initializeApp() {
    initChart();
    const socket = socketService.connect();

    socket.on('new_data', (message) => {
        console.log('Sensor data received: ', message);
        handleSensorData(message);
    });
}

document.addEventListener('DOMContentLoaded', initializeApp);
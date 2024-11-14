const config = {
    API_URL: 'http://localhost:5000',
    SOCKET_OPTIONS: {
        transports: ['websocket', 'polling'],
        path: '/socket.io/',
        reconnection: true,
        reconnectionDelay: 1000,
        reconnectionDelayMax: 5000,
        reconnectionAttempts: Infinity
    }
};
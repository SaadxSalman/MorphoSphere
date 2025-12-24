import express from 'express';
import { createServer } from 'http';
import { Server } from 'socket.io';
import mongoose from 'mongoose';

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, { cors: { origin: "*" } });

// MongoDB Connection
mongoose.connect(process.env.MONGO_URI || '');

io.on('connection', (socket) => {
    console.log('Core-Engine Linked 🔗');
    socket.on('telemetry', (data) => {
        // Broadcast to Dashboard
        io.emit('live-update', data);
    });
});

httpServer.listen(5000, () => console.log('Brain-API on port 5000'));
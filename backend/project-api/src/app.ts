import dotenv from 'dotenv';
dotenv.config();

import express from 'express';
import cors from 'cors';

import workflowRoutes from './routes/workflow.routes';
import { errorHandler } from './middlewares/error.middleware';

const app = express();
app.use(express.json());

app.use(cors({
    origin: process.env.CORS_ORIGIN || '*',
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
}));

app.use('/api', workflowRoutes);

app.use(errorHandler);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`API server started at port ${PORT}`);
});
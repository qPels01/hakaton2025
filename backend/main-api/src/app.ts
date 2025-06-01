import express from 'express';
import authRouter from './routes/authRoutes';
import testRouter from './routes/userRoutes';
import formRoutes from './routes/formRoutes';
import userRoutes from './routes/userRoutes';
import teamRoutes from './routes/teamRoutes';
import developerRoutes from './routes/developerRoutes';
import taskRoutes from './routes/taskRoutes';
import {processData} from './controllers/workflow.controller';
import cors from "cors";

const app = express();

app.use(cors({
    origin: process.env.CORS_ORIGIN || '*',
    credentials: true,
    methods: ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
    allowedHeaders: ['Content-Type', 'Authorization'],
}));

app.use(express.json());

app.use('/api/auth', authRouter);
app.use('/api/user', testRouter);
app.use('/api/teams', teamRoutes);
app.use('/api/developers', developerRoutes);
app.use('/api/tasks', taskRoutes);
app.use('/api/forms', formRoutes);
app.use('/api/users', userRoutes);

app.use('/api/process', processData);

export default app;

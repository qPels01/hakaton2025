import express from 'express';
import authRouter from './routes/authRoutes';
import testRouter from './routes/userRoutes';
import formRoutes from './routes/formRoutes';
import userRoutes from './routes/userRoutes';
import teamRoutes from './routes/teamRoutes';
import developerRoutes from './routes/developerRoutes';
import taskRoutes from './routes/taskRoutes';
import cors from "cors";

const app = express();

app.use(cors({
  origin: [
    "http://localhost:3000",
    "http://127.0.0.1:5500",
  ],
  credentials: true 
}));
app.use(express.json());

app.use('/api/auth', authRouter);
app.use('/api/user', testRouter);
app.use('/api/teams', teamRoutes);
app.use('/api/developers', developerRoutes);
app.use('/api/tasks', taskRoutes);
app.use('/api/forms', formRoutes);
app.use('/api/users', userRoutes);

export default app;

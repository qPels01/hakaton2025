import express from 'express';
import authRouter from './routes/authRoutes';
import testRouter from './routes/userRoutes';
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

export default app;

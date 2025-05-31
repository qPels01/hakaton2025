import express from 'express';
import authRouter from './routes/authRoutes';
import testRouter from './routes/testRoutes'

const app = express();
app.use(express.json());

app.use('/api/auth', authRouter);
app.use('/api/user', testRouter);

export default app;

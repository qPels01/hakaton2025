import express from 'express';
import userRoutes from './routes/user.routes';
import teamRoutes from './routes/team.routes';

const app = express();
app.use(express.json());

app.use('/users', userRoutes);
app.use('/teams', teamRoutes);

export default app;
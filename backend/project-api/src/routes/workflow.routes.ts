import { Router } from 'express';
import { processData } from '../controllers/workflow.controller';

const router = Router();

router.post('/process', processData);

export default router;
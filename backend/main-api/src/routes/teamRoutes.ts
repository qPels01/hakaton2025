import { Router } from 'express';
import { authMiddleware } from '../middlewares/authMiddleware';
import { adminMiddleware } from "../middlewares/adminMiddleware";
import {
  getAllTeams, getTeamById, createTeam, deleteTeam
} from '../controllers/teamController';

const router = Router();

router.get('/', authMiddleware, getAllTeams);
router.get('/:id',authMiddleware, getTeamById);
router.post('/', authMiddleware, createTeam);
router.delete('/:id', authMiddleware,deleteTeam);

export default router;
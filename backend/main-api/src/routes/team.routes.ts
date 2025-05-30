// src/routes/team.routes.ts
import { Router } from "express";
import * as teamController from "../controllers/team.controller";

const router = Router();

router.get("/", teamController.getTeams);
router.post("/", teamController.createTeam);
router.get("/:id", teamController.getTeamById);
router.put("/:id", teamController.updateTeam);
router.delete("/:id", teamController.deleteTeam);

export default router;
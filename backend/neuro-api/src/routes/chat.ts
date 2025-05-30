import { Router } from "express";
import { chatWithGPT } from "../controllers/chatController";

const router = Router();

router.post("/chat", chatWithGPT);

export default router;
import { Request, Response, NextFunction } from 'express';
import { askChatGPT } from '../services/openai';

export const chatWithGPT = async (
  req: Request,
  res: Response,
  next: NextFunction
): Promise<void> => {
    try {
        const { messages } = req.body;
        if (!Array.isArray(messages)) {
            res.status(400).json({ error: 'messages should be an array' });
            return;
        }
        const apiKey = process.env.OPENAI_API_KEY ?? '';
        if (!apiKey) throw new Error('OPENAI_API_KEY is not configured');
        const completion = await askChatGPT(messages, apiKey);
        res.json(completion);
    } catch (error) {
        next(error);
    }
};
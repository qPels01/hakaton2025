import fs from 'fs';
import path from 'path';

export enum PromptStage {
  STAGE1 = 'stage1',
  STAGE2 = 'stage2',
  REVIEW = 'review',
}

const cache: Partial<Record<PromptStage, string>> = {};

export async function getPromptAsync(stage: PromptStage): Promise<string> {
  if (cache[stage]) {
    return cache[stage] as string;
  }

  const promptsDir = path.resolve(__dirname, '../prompts');
  const filePath = path.join(promptsDir, `${stage}.txt`);
  try {
    const text = await fs.promises.readFile(filePath, 'utf-8');
    cache[stage] = text;
    return text;
  } catch (err) {
    throw new Error(`Prompt file not found: ${filePath}`);
  }
}
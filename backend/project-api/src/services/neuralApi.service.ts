import axios from 'axios';
import { NeuralApiRequestPayload } from '../types/neuralApi.types';
import { getPromptAsync, PromptStage } from '../config/prompts';

const endpoint = process.env.NEURO_ENDPOINT as string;

if (!endpoint) {
  throw new Error('NEURO_ENDPOINT environment variable not set');
}

export async function callNeuralApi(systemPrompt: string, userMessage: string): Promise<any> {
  const payload: NeuralApiRequestPayload = {
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userMessage }
    ]
  };
  const response = await axios.post(endpoint, payload,{
    timeout:30000
  });
  if (!response.data) throw new Error('Neural API error');
  return response.data;
}


export async function callNeuralApiStage1(input: string) {
  const prompt = await getPromptAsync(PromptStage.STAGE1);
  return await callNeuralApi(prompt, input);
}

export async function callNeuralApiStage2(input: any) {
    const prompt = await getPromptAsync(PromptStage.STAGE2);
  return await callNeuralApi(prompt, input);
}

export async function callNeuralApiReview(input: any) {
      const prompt = await getPromptAsync(PromptStage.REVIEW);
  return await callNeuralApi(prompt, input);
}
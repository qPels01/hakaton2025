// types/neuralApi.types.ts
export interface NeuralApiMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

export interface NeuralApiRequestPayload {
  messages: NeuralApiMessage[];
}
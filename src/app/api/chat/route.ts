import { createOpenAI } from '@ai-sdk/openai';
import { streamText } from 'ai';

export const maxDuration = 30;

// Setup custom provider untuk connect ke 9router lokal
const customProvider = createOpenAI({
  baseURL: 'http://localhost:20128/v1',
  apiKey: process.env.NINEROUTER_API_KEY || 'sk-4081c7ffcc504100bd772f915f06822a', // Gunakan key dummy jika env tidak ada
});

export async function POST(req: Request) {
  const { messages } = await req.json();

  const result = await streamText({
    model: customProvider('WSL_PRAY') as any,
    messages,
    system: "You are an elite, premium AI Productivity Assistant named PrayChatBot created for Boss PRAY. You communicate professionally yet confidently. Your layout outputs are always clean. You help the user dominate tasks, debug code, and plan strategies efficiently. If asked who you are, state that you are PrayChatBot powered by 9Router WSL_PRAY model.",
  });

  return result.toDataStreamResponse();
}

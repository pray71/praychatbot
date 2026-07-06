import { google } from '@ai-sdk/google';
import { streamText } from 'ai';

// Next.js config biar API route-nya jalan di Edge Runtime (lebih kenceng)
export const runtime = 'edge';

export async function POST(req: Request) {
  // Ambil pesan dari request (history percakapan)
  const { messages } = await req.json();

  // Panggil Gemini menggunakan ai-sdk
  const result = await streamText({
    // Bos bisa ganti ke 'gemini-1.5-flash' kalo mau lebih cepet & murah
    model: google('gemini-1.5-pro-latest') as any,
    system: "Kamu adalah asisten AI PRAYCHATBOT, yang cerdas, menggunakan bahasa gaul yang santai. Kamu memanggil user dengan sebutan 'Bos'.",
    messages,
  });

  // Lempar kembali stream response-nya ke UI
  return result.toTextStreamResponse();
}

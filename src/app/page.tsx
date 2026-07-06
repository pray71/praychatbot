'use client';

import { Chat } from '@/components/Chat';
import { ThemeProvider } from '@/components/theme-provider';
import { SessionProvider } from 'next-auth/react';

export default function Home() {
  return (
    <ThemeProvider
      attribute="class"
      defaultTheme="system"
      enableSystem
      disableTransitionOnChange
    >
      <SessionProvider>
        <Chat />
      </SessionProvider>
    </ThemeProvider>
  );
}

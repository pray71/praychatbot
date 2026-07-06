'use client';

import { useChat } from '@ai-sdk/react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Send, User, Bot, Sparkles } from 'lucide-react';

export function Chat() {
  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: '/api/chat',
  });

  return (
    <main className="flex min-h-screen flex-col bg-background selection:bg-primary/30 text-foreground relative overflow-hidden">
      {/* Background gradients */}
      <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-primary/20 blur-[100px] pointer-events-none" />
      <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-accent/20 blur-[100px] pointer-events-none" />

      {/* Header */}
      <nav className="sticky top-0 z-50 flex items-center justify-between p-4 backdrop-blur-md bg-background/60 border-b border-border/50">
        <div className="flex items-center gap-2">
          <div className="relative flex h-9 w-9 items-center justify-center rounded-lg bg-primary/10 border border-primary/20">
            <Sparkles className="h-5 w-5 text-primary" />
          </div>
          <h1 className="text-xl font-bold tracking-tight">PrayChatBot</h1>
        </div>
        <div className="flex items-center gap-3">
          <Button variant="ghost" size="sm" className="hidden sm:flex">Features</Button>
          <Button variant="default" size="sm" className="rounded-full shadow-lg hover:shadow-primary/20 transition-all">
            Upgrade Pro
          </Button>
        </div>
      </nav>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col items-center p-4 sm:p-6 w-full max-w-4xl mx-auto h-[calc(100vh-140px)]">
        {messages.length === 0 ? (
          <div className="flex-1 flex items-center justify-center w-full">
            <Card className="w-full border-none shadow-none bg-transparent">
              <CardHeader className="text-center">
                <CardTitle className="text-4xl sm:text-5xl font-extrabold tracking-tight bg-gradient-to-br from-foreground to-foreground/60 bg-clip-text text-transparent pb-2">
                  Welcome back, Boss.
                </CardTitle>
                <CardDescription className="text-lg text-muted-foreground mt-4 max-w-xl mx-auto">
                  I'm your premium AI productivity assistant powered by 9Router. How can I help you dominate your tasks today?
                </CardDescription>
              </CardHeader>
              <CardContent className="flex flex-wrap justify-center gap-3 mt-8">
                {["Draft a crypto article", "Help me debug a script", "Plan my week"].map((suggestion) => (
                  <Button 
                    key={suggestion} 
                    variant="outline" 
                    className="rounded-full bg-background/50 backdrop-blur-sm border-border/50 hover:bg-muted"
                    onClick={() => handleInputChange({ target: { value: suggestion } } as any)}
                  >
                    {suggestion}
                  </Button>
                ))}
              </CardContent>
            </Card>
          </div>
        ) : (
          <ScrollArea className="flex-1 w-full pr-4 pb-4">
            <div className="flex flex-col gap-6">
              {messages.map((m) => (
                <div key={m.id} className={`flex gap-4 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {m.role !== 'user' && (
                    <Avatar className="h-8 w-8 mt-1 border border-primary/20 shrink-0">
                      <div className="flex h-full w-full items-center justify-center bg-primary/10">
                        <Bot className="h-4 w-4 text-primary" />
                      </div>
                    </Avatar>
                  )}
                  
                  <div className={`rounded-2xl px-5 py-3 max-w-[85%] sm:max-w-[75%] ${
                    m.role === 'user' 
                      ? 'bg-primary text-primary-foreground ml-auto' 
                      : 'bg-muted/50 backdrop-blur-md border border-border/50 shadow-sm'
                  }`}>
                    <div className="prose prose-sm dark:prose-invert max-w-none break-words whitespace-pre-wrap">
                      {m.content}
                    </div>
                  </div>

                  {m.role === 'user' && (
                    <Avatar className="h-8 w-8 mt-1 shrink-0">
                      <AvatarFallback className="bg-secondary"><User className="h-4 w-4" /></AvatarFallback>
                    </Avatar>
                  )}
                </div>
              ))}
              {isLoading && (
                <div className="flex gap-4 justify-start">
                  <Avatar className="h-8 w-8 mt-1 border border-primary/20 shrink-0">
                    <div className="flex h-full w-full items-center justify-center bg-primary/10">
                      <Bot className="h-4 w-4 text-primary" />
                    </div>
                  </Avatar>
                  <div className="rounded-2xl px-5 py-3 bg-muted/50 backdrop-blur-md border border-border/50 shadow-sm flex items-center gap-2">
                    <div className="w-2 h-2 rounded-full bg-primary/50 animate-bounce" />
                    <div className="w-2 h-2 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: '0.2s' }} />
                    <div className="w-2 h-2 rounded-full bg-primary/50 animate-bounce" style={{ animationDelay: '0.4s' }} />
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>
        )}

        {/* Input Area */}
        <div className="w-full mt-auto pt-4 relative">
          <form 
            onSubmit={handleSubmit} 
            className="relative flex items-center w-full bg-background/60 backdrop-blur-xl border border-border/60 p-2 rounded-3xl shadow-[0_0_40px_-15px_rgba(0,0,0,0.3)]"
          >
            <Input
              value={input}
              onChange={handleInputChange}
              placeholder="Message your AI..."
              className="flex-1 border-none bg-transparent shadow-none focus-visible:ring-0 text-base px-4"
              disabled={isLoading}
            />
            <Button 
              type="submit" 
              size="icon" 
              disabled={isLoading || !input.trim()}
              className="rounded-full h-10 w-10 shrink-0"
            >
              <Send className="h-4 w-4 ml-0.5" />
            </Button>
          </form>
          <div className="text-center mt-3 text-xs text-muted-foreground/60">
            AI can make mistakes. Consider verifying important information.
          </div>
        </div>
      </div>
    </main>
  );
}

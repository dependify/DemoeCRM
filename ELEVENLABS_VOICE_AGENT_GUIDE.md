# ElevenLabs Voice Agent Implementation Guide

> **Complete guide for implementing ElevenLabs Conversational AI Voice Agent in React applications**

---

## Overview

This document provides a complete, replicable implementation of the ElevenLabs Voice Agent widget for React applications. The implementation uses the **public agent mode**, which requires only an Agent ID and no API keys on the client side.

### Key Features
- 🎤 **Voice Mode**: Real-time voice conversation with WebRTC
- 💬 **Text Mode**: Text-based chat as fallback
- 📝 **Live Transcription**: Shows user and agent messages in real-time
- 🎨 **Animated UI**: Smooth animations with Framer Motion
- 📱 **Responsive**: Works on desktop and mobile

---

## Prerequisites

### 1. ElevenLabs Account Setup
1. Create an account at [ElevenLabs](https://elevenlabs.io)
2. Go to [Agents Platform](https://elevenlabs.io/app/agents)
3. Create a new agent or use an existing one
4. Copy your **Agent ID** (format: `agent_xxxxxxxxxxxxxxxxxxxx`)

### 2. Agent Configuration
Your agent must be set as **public** (no authentication required) for client-side connection.

---

## File Structure

```
src/
├── components/
│   └── voice-agent/
│       └── VoiceAgentButton.tsx    # Main voice agent component
├── components/ui/                   # Shadcn UI components (Button, Input)
├── hooks/
│   └── use-toast.ts                 # Toast notification hook
└── components/layout/
    └── Layout.tsx                   # Where VoiceAgentButton is mounted
```

---

## Installation

### Step 1: Install Dependencies

```bash
npm install @elevenlabs/react framer-motion lucide-react
```

### Step 2: Install UI Components (if using Shadcn)

```bash
npx shadcn-ui@latest add button input
```

---

## Configuration

### Agent ID
Replace the agent ID with your own:

```typescript
const ELEVENLABS_AGENT_ID = "agent_2601kfx2xrd5emmbts6ss7m5146j";
```

### Quick Questions (Optional)
Customize the quick question buttons:

```typescript
const QUICK_QUESTIONS = [
  { icon: GraduationCap, text: "What are the admission requirements?" },
  { icon: BookOpen, text: "Tell me about the courses offered" },
  { icon: Calendar, text: "When is the next session?" },
  { icon: HelpCircle, text: "How do I apply?" },
];
```

---

## Complete Component Code

### File: `src/components/voice-agent/VoiceAgentButton.tsx`

```tsx
import { useState, useCallback, useRef, useEffect } from "react";
import { useConversation } from "@elevenlabs/react";
import { motion, AnimatePresence } from "framer-motion";
import { Mic, MicOff, X, Loader2, MessageCircle, Send, Keyboard, GraduationCap, BookOpen, Calendar, HelpCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useToast } from "@/hooks/use-toast";

// ============================================
// CONFIGURATION - Replace with your Agent ID
// ============================================
const ELEVENLABS_AGENT_ID = "agent_2601kfx2xrd5emmbts6ss7m5146j";

// Quick question buttons (customize as needed)
const QUICK_QUESTIONS = [
  { icon: GraduationCap, text: "What are the admission requirements?" },
  { icon: BookOpen, text: "Tell me about the courses offered" },
  { icon: Calendar, text: "When is the next session?" },
  { icon: HelpCircle, text: "How do I apply?" },
];

export function VoiceAgentButton() {
  // ============================================
  // STATE
  // ============================================
  const [isOpen, setIsOpen] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [mode, setMode] = useState<"voice" | "text">("voice");
  const [textInput, setTextInput] = useState("");
  const [isSending, setIsSending] = useState(false);
  const [transcripts, setTranscripts] = useState<{ role: "user" | "agent"; text: string }[]>([]);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { toast } = useToast();

  // ============================================
  // ELEVENLABS SDK HOOK
  // ============================================
  const conversation = useConversation({
    onConnect: () => {
      console.log("Connected to voice agent");
      setIsConnecting(false);
    },
    onDisconnect: () => {
      console.log("Disconnected from voice agent");
      setIsConnecting(false);
    },
    onMessage: (message: any) => {
      console.log("Voice agent message:", message);
      // Handle user transcription
      if (message.type === "user_transcript" && message.user_transcription_event?.user_transcript) {
        setTranscripts(prev => [...prev, {
          role: "user",
          text: message.user_transcription_event.user_transcript
        }]);
      }
      // Handle agent response
      else if (message.type === "agent_response" && message.agent_response_event?.agent_response) {
        setTranscripts(prev => [...prev, {
          role: "agent",
          text: message.agent_response_event.agent_response
        }]);
      }
    },
    onError: (error) => {
      console.error("Voice agent error:", error);
      setIsConnecting(false);
      toast({
        variant: "destructive",
        title: "Voice Agent Error",
        description: "There was a problem connecting to the voice agent. Please try again.",
      });
    },
  });

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [transcripts]);

  // ============================================
  // VOICE CONVERSATION HANDLERS
  // ============================================
  const startConversation = useCallback(async () => {
    setIsConnecting(true);
    setTranscripts([]);

    try {
      // Request microphone permission
      await navigator.mediaDevices.getUserMedia({ audio: true });

      // For public agents, connect directly with agentId - no token needed!
      await conversation.startSession({
        agentId: ELEVENLABS_AGENT_ID,
        connectionType: "webrtc",
      });

    } catch (error) {
      console.error("Failed to start conversation:", error);
      setIsConnecting(false);
      toast({
        variant: "destructive",
        title: "Connection Failed",
        description: error instanceof Error ? error.message : "Failed to connect to voice agent.",
      });
    }
  }, [conversation, toast]);

  const stopConversation = useCallback(async () => {
    await conversation.endSession();
  }, [conversation]);

  // ============================================
  // TEXT MESSAGE HANDLERS
  // ============================================
  const sendTextMessage = useCallback(async (messageOverride?: string) => {
    const messageToSend = messageOverride || textInput.trim();
    if (!messageToSend || isSending) return;

    if (!messageOverride) setTextInput("");
    setIsSending(true);
    setTranscripts(prev => [...prev, { role: "user", text: messageToSend }]);

    try {
      // If not connected, start a session first
      if (conversation.status === "disconnected") {
        await conversation.startSession({
          agentId: ELEVENLABS_AGENT_ID,
          connectionType: "webrtc",
        });
        // Wait a bit for connection to establish
        await new Promise(resolve => setTimeout(resolve, 500));
      }

      // Send message using the SDK
      if (conversation.status === "connected") {
        conversation.sendUserMessage(messageToSend);
      }
    } catch (error) {
      console.error("Failed to send message:", error);
      toast({
        variant: "destructive",
        title: "Message Failed",
        description: "Couldn't send your message. Please try again.",
      });
    } finally {
      setIsSending(false);
    }
  }, [textInput, isSending, conversation, toast]);

  const handleQuickQuestion = (question: string) => {
    sendTextMessage(question);
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendTextMessage();
    }
  };

  const toggleOpen = () => {
    if (isOpen && conversation.status === "connected") {
      stopConversation();
    }
    setIsOpen(!isOpen);
  };

  // ============================================
  // RENDER
  // ============================================
  return (
    <>
      {/* Floating Button */}
      <motion.div
        className="fixed bottom-24 right-8 z-50"
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ delay: 1, type: "spring", stiffness: 200 }}
      >
        <Button
          onClick={toggleOpen}
          size="lg"
          className={`rounded-full w-14 h-14 shadow-lg transition-all duration-300 ${
            conversation.status === "connected"
              ? "bg-green-500 hover:bg-green-600"
              : "bg-amber-500 hover:bg-amber-600"
          }`}
        >
          <AnimatePresence mode="wait">
            {isOpen ? (
              <motion.div
                key="close"
                initial={{ rotate: -90, opacity: 0 }}
                animate={{ rotate: 0, opacity: 1 }}
                exit={{ rotate: 90, opacity: 0 }}
              >
                <X className="h-6 w-6" />
              </motion.div>
            ) : (
              <motion.div
                key="mic"
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                exit={{ scale: 0 }}
              >
                <MessageCircle className="h-6 w-6" />
              </motion.div>
            )}
          </AnimatePresence>
        </Button>

        {/* Pulse effect when connected */}
        {conversation.status === "connected" && (
          <span className="absolute inset-0 rounded-full bg-green-500/30 animate-ping" />
        )}
      </motion.div>

      {/* Voice Agent Panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: "spring", stiffness: 300, damping: 30 }}
            className="fixed bottom-44 right-8 z-50 w-80 max-w-[calc(100vw-4rem)] bg-white dark:bg-gray-900 border border-gray-200 dark:border-gray-700 rounded-2xl shadow-xl overflow-hidden"
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-amber-500 to-orange-500 text-white p-4">
              <h3 className="font-semibold text-lg">AI Assistant</h3>
              <p className="text-sm text-white/80">
                Ask me anything
              </p>
            </div>

            {/* Mode Toggle */}
            <div className="px-4 pt-4">
              <div className="flex gap-1 p-1 bg-gray-100 dark:bg-gray-800 rounded-lg">
                <button
                  onClick={() => setMode("voice")}
                  className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                    mode === "voice"
                      ? "bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm"
                      : "text-gray-500 hover:text-gray-700"
                  }`}
                >
                  <Mic className="h-4 w-4" />
                  Voice
                </button>
                <button
                  onClick={() => setMode("text")}
                  className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-md text-sm font-medium transition-colors ${
                    mode === "text"
                      ? "bg-white dark:bg-gray-700 text-gray-900 dark:text-white shadow-sm"
                      : "text-gray-500 hover:text-gray-700"
                  }`}
                >
                  <Keyboard className="h-4 w-4" />
                  Text
                </button>
              </div>
            </div>

            {/* Content */}
            <div className="p-4 space-y-4">
              {/* Status (Voice mode only) */}
              {mode === "voice" && (
                <div className="flex items-center gap-2 text-sm">
                  <div
                    className={`w-2 h-2 rounded-full ${
                      conversation.status === "connected"
                        ? "bg-green-500"
                        : "bg-gray-400"
                    }`}
                  />
                  <span className="text-gray-500">
                    {conversation.status === "connected"
                      ? conversation.isSpeaking
                        ? "Speaking..."
                        : "Listening..."
                      : "Ready to connect"}
                  </span>
                </div>
              )}

              {/* Transcripts / Messages */}
              {transcripts.length > 0 && (
                <div className="max-h-48 overflow-y-auto space-y-2 text-sm">
                  {transcripts.map((t, i) => (
                    <div
                      key={i}
                      className={`p-2 rounded-lg ${
                        t.role === "user"
                          ? "bg-blue-100 dark:bg-blue-900/30 text-gray-900 dark:text-white ml-4"
                          : "bg-amber-100 dark:bg-amber-900/30 text-gray-900 dark:text-white mr-4"
                      }`}
                    >
                      <span className="font-medium text-xs text-gray-500 block mb-1">
                        {t.role === "user" ? "You" : "Assistant"}
                      </span>
                      {t.text}
                    </div>
                  ))}
                  <div ref={messagesEndRef} />
                </div>
              )}

              {/* Voice Mode Controls */}
              {mode === "voice" && (
                <>
                  {conversation.status === "disconnected" ? (
                    <Button
                      onClick={startConversation}
                      disabled={isConnecting}
                      className="w-full bg-amber-500 hover:bg-amber-600 text-white"
                    >
                      {isConnecting ? (
                        <>
                          <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                          Connecting...
                        </>
                      ) : (
                        <>
                          <Mic className="mr-2 h-4 w-4" />
                          Start Voice Chat
                        </>
                      )}
                    </Button>
                  ) : (
                    <Button
                      onClick={stopConversation}
                      variant="destructive"
                      className="w-full"
                    >
                      <MicOff className="mr-2 h-4 w-4" />
                      End Conversation
                    </Button>
                  )}
                  <p className="text-xs text-gray-500 text-center">
                    {conversation.status === "connected"
                      ? "Speak naturally. I'll respond when you pause."
                      : "Click to speak with our AI assistant"}
                  </p>
                </>
              )}

              {/* Text Mode Controls */}
              {mode === "text" && (
                <>
                  <div className="flex gap-2">
                    <Input
                      value={textInput}
                      onChange={(e) => setTextInput(e.target.value)}
                      onKeyDown={handleKeyPress}
                      placeholder="Type your message..."
                      disabled={isSending}
                      className="flex-1"
                    />
                    <Button
                      onClick={() => sendTextMessage()}
                      disabled={isSending || !textInput.trim()}
                      size="icon"
                      className="bg-amber-500 hover:bg-amber-600 text-white"
                    >
                      {isSending ? (
                        <Loader2 className="h-4 w-4 animate-spin" />
                      ) : (
                        <Send className="h-4 w-4" />
                      )}
                    </Button>
                  </div>
                </>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
```

---

## Usage

### Mount in Layout Component

```tsx
// src/components/layout/Layout.tsx
import { VoiceAgentButton } from "@/components/voice-agent/VoiceAgentButton";

export function Layout({ children }) {
  return (
    <div>
      {children}
      <VoiceAgentButton />
    </div>
  );
}
```

---

## API Reference

### ElevenLabs SDK Methods

| Method | Description |
|--------|-------------|
| `conversation.startSession({ agentId, connectionType })` | Start voice session |
| `conversation.endSession()` | End current session |
| `conversation.sendUserMessage(text)` | Send text message to agent |
| `conversation.status` | Current status: `"connected"` or `"disconnected"` |
| `conversation.isSpeaking` | Whether agent is currently speaking |

### SDK Callbacks

| Callback | Description |
|----------|-------------|
| `onConnect` | Called when WebRTC connection established |
| `onDisconnect` | Called when connection ends |
| `onMessage` | Called for each message (user transcript or agent response) |
| `onError` | Called when an error occurs |

### Message Types

```typescript
// User transcript
{
  type: "user_transcript",
  user_transcription_event: {
    user_transcript: "User's spoken words"
  }
}

// Agent response
{
  type: "agent_response",
  agent_response_event: {
    agent_response: "Agent's reply text"
  }
}
```

---

## Customization

### Styling
The component uses Tailwind CSS. Modify the classes to match your design system.

### Colors
Replace these color classes:
- `bg-amber-500` → Your primary color
- `bg-green-500` → Connected state color
- `bg-blue-100` → User message background
- `bg-amber-100` → Agent message background

### Position
Change the floating button position:
```tsx
className="fixed bottom-24 right-8 z-50"
// Change to: bottom-8, left-8, etc.
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Microphone access denied" | Ensure HTTPS or localhost; check browser permissions |
| "Connection failed" | Verify Agent ID is correct and agent is public |
| "No audio" | Check browser audio permissions and volume |

### Browser Requirements
- **Chrome 74+** (recommended)
- **Firefox 66+**
- **Safari 14.1+**
- **Edge 79+**

---

## Security Notes

> ⚠️ **Important**: This implementation uses **public agent mode**. The Agent ID is exposed in client-side code. For private agents requiring authentication, you need a backend to generate signed URLs.

### For Private Agents (with authentication)
If your agent requires authentication, you'll need:

```typescript
// Backend endpoint to get signed URL
app.get("/api/voice/token", async (req, res) => {
  const response = await fetch(
    `https://api.elevenlabs.io/v1/convai/conversation/get_signed_url?agent_id=${AGENT_ID}`,
    {
      headers: {
        "xi-api-key": process.env.ELEVENLABS_API_KEY, // Keep secret!
      },
    }
  );
  const data = await response.json();
  res.json({ signedUrl: data.signed_url });
});
```

---

## Resources

- [ElevenLabs Agents Platform](https://elevenlabs.io/docs/agents-platform/overview)
- [React SDK Documentation](https://elevenlabs.io/docs/conversational-ai/libraries/react)
- [Agent Configuration](https://elevenlabs.io/app/agents)

---

## Version Info

| Package | Version |
|---------|---------|
| `@elevenlabs/react` | ^0.13.0 |
| `framer-motion` | ^10.x |
| `lucide-react` | ^0.x |

---

*Last updated: February 2026*

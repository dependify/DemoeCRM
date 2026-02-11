# ElevenLabs Voice Agent Setup Guide

## Understanding the Voice Connection URL

The URL you shared is the **LiveKit WebSocket connection URL** that ElevenLabs uses for voice conversations:

```
https://livekit.rtc.elevenlabs.io/rtc/v1/validate?access_token=eyJhbGciOiJIUzI1Ni...
```

### What this URL contains:

1. **Server**: `livekit.rtc.elevenlabs.io` - ElevenLabs' real-time communication server
2. **JWT Token**: The long string after `access_token=` is a JSON Web Token containing:
   - Room ID: `room_agent_2601kfx2xrd5emmbts6ss7m5146j_conv_9901kgpfh953f4qr18zdhrkp8gjt`
   - User ID: `user_agent_2601kfx2xrd5emmbts6ss7m5146j_conv_9901kgpfh953f4qr18zdhrkp8gjt`
   - Permissions (canPublish, canSubscribe, canPublishData)
   - Expiration time (exp: 1770281918 = about 15 minutes)
   - Metadata

3. **Agent ID**: `agent_2601kfx2xrd5emmbts6ss7m5146j` - Your DUSOM voice agent

## How Voice Connection Works

### Architecture:
```
┌─────────────┐      ┌──────────────┐      ┌─────────────────┐
│   Browser   │ ←──→ │   Backend    │ ←──→ │  ElevenLabs API │
│  (React)    │      │  (Node.js)   │      │  (LiveKit RTC)  │
└─────────────┘      └──────────────┘      └─────────────────┘
       │                     │                      │
       │ 1. Request token    │                      │
       │ ──────────────────> │                      │
       │                     │ 2. Get signed URL    │
       │                     │ ──────────────────>  │
       │                     │                      │
       │                     │ 3. Return signed URL │
       │                     │ <──────────────────  │
       │                     │                      │
       │ 4. Connect WebRTC   │                      │
       │ <────────────────────────────────────────> │
```

### Steps to Connect:

1. **Request Token**: Frontend calls `POST /api/voice/token` with `agent_id`
2. **Backend Proxies**: Backend calls ElevenLabs API with your API key
3. **Get Signed URL**: ElevenLabs returns a JWT-signed WebSocket URL (like the one you shared)
4. **WebRTC Connection**: Frontend uses the signed URL to connect directly to LiveKit server

## The Problem

Your API key `sk_3c4f17f77fa4b9165fc8e6b65e27d01f70753d08a1de4ca0` is **invalid or revoked**.

Error from ElevenLabs:
```json
{
  "detail": {
    "status": "api_key_not_verifiable",
    "message": "400: {'status': 'invalid_api_key', 'message': 'API key is invalid'}"
  }
}
```

## Solution

### Step 1: Get a New API Key

1. Go to https://elevenlabs.io
2. Sign in to your account
3. Go to **Profile Settings** → **API Keys**
4. Create a new API key
5. Copy the new key (starts with `sk_...`)

### Step 2: Update Backend Environment

In your backend server, set the environment variable:

```bash
# On Windows PowerShell:
$env:ELEVENLABS_API_KEY="sk_your_new_api_key_here"

# On Linux/Mac:
export ELEVENLABS_API_KEY="sk_your_new_api_key_here"
```

Or update the `.env` file in the backend directory:
```
ELEVENLABS_API_KEY=sk_your_new_api_key_here
ELEVENLABS_AGENT_ID=agent_2601kfx2xrd5emmbts6ss7m5146j
```

### Step 3: Restart Backend

```bash
cd backend
npm run build
npm start
```

### Step 4: Test Connection

```bash
# Test the voice token endpoint
curl -X POST http://localhost:3001/api/voice/token \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent_2601kfx2xrd5emmbts6ss7m5146j"}'
```

You should get a response like:
```json
{
  "token": "wss://livekit.rtc.elevenlabs.io/rtc/v1/validate?access_token=eyJhbGci...",
  "signed_url": "wss://livekit.rtc.elevenlabs.io/rtc/v1/validate?access_token=eyJhbGci..."
}
```

## Current Behavior (Without Valid API Key)

The voice agent currently works in **fallback mode**:
- Voice mode: Disabled (shows "Unavailable")
- Text mode: Uses predefined responses for common questions
- Fallback responses work for:
  - "What are the admission requirements?"
  - "Tell me about the courses offered"
  - "When is the next session?"
  - "How do I apply?"

## Alternative: Direct ElevenLabs API Call (Not Recommended for Production)

You could also call ElevenLabs directly from the frontend, but this **exposes your API key**:

```typescript
// ⚠️ DON'T DO THIS IN PRODUCTION
const response = await fetch(
  `https://api.elevenlabs.io/v1/convai/conversation/get_signed_url?agent_id=${agentId}`,
  {
    headers: { 'xi-api-key': 'sk_your_api_key' } // API key visible in browser!
  }
);
```

**Always use the backend proxy** to keep your API key secure.

## Summary

Yes, that URL format is correct! It's a LiveKit WebSocket URL with a JWT token. To fix the voice agent:

1. Get a new API key from ElevenLabs
2. Update the `ELEVENLABS_API_KEY` environment variable
3. Restart the backend
4. Voice mode will then work properly

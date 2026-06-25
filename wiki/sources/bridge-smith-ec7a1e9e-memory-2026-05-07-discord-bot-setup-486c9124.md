---
pageType: source
id: source.bridge.smith-ec7a1e9e.memory-2026-05-07-discord-bot-setup-486c9124
title: "Memory Bridge (smith): 2026-05-07-discord-bot-setup"
sourceType: memory-bridge
sourcePath: /Users/Jeff/Smith/memory/2026-05-07-discord-bot-setup.md
bridgeRelativePath: memory/2026-05-07-discord-bot-setup.md
bridgeWorkspaceDir: /Users/Jeff/Smith
bridgeAgentIds:
  - smith
status: active
updatedAt: 2026-05-07T04:26:00.743Z
---

# Memory Bridge (smith): 2026-05-07-discord-bot-setup

## Bridge Source
- Workspace: `/Users/Jeff/Smith`
- Relative path: `memory/2026-05-07-discord-bot-setup.md`
- Kind: `markdown`
- Agents: smith
- Updated: 2026-05-07T04:26:00.743Z

## Content
````markdown
# Session: 2026-05-07 11:25:56 GMT+7

- **Session Key**: agent:main:telegram:direct:8611951691
- **Session ID**: ced509b9-0a51-4a34-8898-3f13a8fcd3b0
- **Source**: telegram

## Conversation Summary

user: hey, i want to set up you in a discord server so i can communicate with you there. please walk me through getting you in as a bot in discord so i can communicate with you
assistant: 

sure, let's get this set up! discord integration with openclaw is handled through the gateway config. here's the walkthrough:

## Step 1: Create a Discord Bot

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Click **"New Application"** → give it a name (e.g. "OpenClaw")
3. On the left sidebar, click **"Bot"**
4. Click **"Add Bot"** → confirm
5. Under the bot token section, click **"Reset Token"** and copy/save the token (you'll need this)

## Step 2: Configure OpenClaw with the Bot Token

Once you have your bot token, I'll need to add it to the gateway config. You can do this with the gateway tool:

```bash
openclaw gateway config patch channels.discord.botToken "YOUR_DISCORD_BOT_TOKEN"
```

## Step 3: Enable Message Content Intent

1. In the Discord Developer Portal, go to your bot → **"Bot"** page
2. Scroll to **"Privileged Gateway Intents"**
3. Enable **"Message Content Intent"** (required for reading messages)

## Step 4: Generate an Invite Link

1. Go to **"OAuth2" → "URL Generator"**
2. Check these scopes: `bot`, `applications.commands`
3. For permissions, check at minimum:
   - `Send Messages`
   - `Read Message History`
   - `Use Slash Commands` (optional but recommended)
4. Copy the generated URL and open it to add the bot to your server

## Step 5: Restart the Gateway

After patching the config, restart:

```bash
openclaw gateway restart
```

---

**Once you've created the bot and have the token**, paste it here and I'll help you patch the config and get everything running. make sure to grab that token before moving on! 🤙
user: check my openclaw.json out that json format synth text error or not
assistant: 

ok so here's the deal:

**The current openclaw.json is valid JSON, but it's TRUNCATED.**

- Current file size: **1,583 bytes** 
- Most recent backup size: **13,914 bytes**

The file got cut down to only 1,583 bytes, which is why Python now says it's valid JSON — the truncated version happens to be syntactically correct, but it's missing a ton of config including your discord settings.

Let me check what's actually in the truncated version vs the full backup:


````

## Notes
<!-- openclaw:human:start -->
<!-- openclaw:human:end -->

## Related
<!-- openclaw:wiki:related:start -->
- No related pages yet.
<!-- openclaw:wiki:related:end -->

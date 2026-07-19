User Info: **Name**: Best Wuttipong · Thai name: วุฒิพงษ์ · goes by Jeff · Email: bed.wuttipong@gmail.com · Hotmail: bed.wuttipong@hotmail.com · Discord: best.wuttipong (id: 1313876113776312391) · **Work email**: wuttipong.t@flexpak.co.th
§
Personal Preferences: lowercase, emojis, casual. Bear Notes (grizzly CLI at /opt/homebrew/bin/grizzly). Workspace: no symlinks, ~/Smith directly.
§
Jeff prefers English for task lists and work content. Company data stays in chat only — never save externally.
§
Smith's GitHub repo is PRIVATE. Repo: github.com/bwuttipong/smith (https, master branch). Don't propose making it public. Don't suggest sharing URLs to it externally without explicit ask. Commits and pushes are fine — it's a personal workspace, just not for public eyes.
§
Antigravity: Jeff's work Windows laptop (remote execution env, NOT an AI model). Has its own Hermes instance. Provider keys: Xiaomi MiMo in OpenClaw config.
§
End-of-day ritual: git add -A && git commit -m "date summary" && git push on BOTH Smith (Mac/Hermes) and OpenClaw (Antigravity/Windows) when Jeff says good night.
§
Work: TPN & TPK Flexpak (Thung Hua Sinn Group). VB.NET + SQL Server. Slack #projects. Notion: ~/.openclaw/.env. พี่วัชรพงศ์ at TPK. Weekly report: Thai HTML via AgentMail (always use `html` field, inline CSS only), subject: "อัปเดตประจำสัปดาห์: ... (สัปดาห์สิ้นสุด DD MMM YYYY)"
§
Company: TPN/TPK. NO internet on work laptop. Blocks AI platforms. Photos→vision workaround. Phone for external checks.
§
Agent OS: ~/Workspaces/agentos — Next.js dashboard (localhost:3737). Process toasts: draggable, % progress, error+retry, manual dismiss. Apollo timeout: 5min. Skill: building-agent-os.
§
qmd install ~/.local/lib/node_modules/@tobilu/qmd. Two Nodes: /usr/local/bin/node v24 ABI137 (modules built for it) vs /opt/homebrew/bin/node v26 ABI147. qmd runtime=`env node` → bg/cron/Apollo can drift to v26, making `qmd embed` crash (NODE_MODULE_VERSION 137 vs 147, exit 1), not silent. Fix: rebuild better-sqlite3+sqlite-vec with /usr/local/bin/npm in that path + pin bin/qmd CLI child to /usr/local/bin/node.
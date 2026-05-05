# 🛠️ BotConsole v2.0

**BotConsole** is a high-performance, terminal-based management wizard for Discord bots. It provides a sleek, professional CLI interface to interact with, manage, and (if necessary) neutralize Discord servers with surgical precision.

Designed for developers who want a "home page" for their bot without needing a web dashboard, BotConsole runs entirely in your terminal.

---

## 🚀 Features

### 📡 Live Communication
*   **Live Chat:** Intercept and send messages in any text channel in real-time.
*   **Emoji Support:** Automatically parses and sends custom server emojis.
*   **History Sync:** View recent message history upon entering a channel.

### 🆔 Identity Management
*   **Profile Override:** Change the bot's username and avatar (via URL) instantly.
*   **Presence Control:** Set custom activities (Playing, Streaming, Listening, Watching).

### 🔧 Server Administration
*   **Structural Injection:** Create channels, categories, and roles on the fly.
*   **Member Intel:** View member lists and execute kicks or bans.
*   **Audit Recon:** View real-time audit logs to see who is doing what.

### ⚠️ Advanced Tools (The Void Protocol)
*   **Channel Ghosting:** Instantly purge all message history from a specific stream.
*   **Server Nuke:** Wipes all channels/branding and rebrands the server.
*   **FULL DESTROY:** A "scorched earth" protocol that mass-bans members, locks down permissions, wipes the server, and injects 50+ channels with a custom ASCII nuke payload and @everyone mentions.

---

## 🛠️ Installation

### 1. Prerequisites
*   **Python 3.10+**
*   **A Discord Bot Token** (with all Privileged Gateway Intents enabled).

### 2. Setup
Clone or download the script and install the required libraries:

```bash
pip install discord.py rich questionary aiohttp
```

### 3. Execution
Run the console from your terminal:

```bash
python3 discord_dash.py
```

---

## 🛡️ Security & Safety

*   **Code Confirmation:** Destructive actions require a randomly generated security code to prevent accidental execution.
*   **Local Session:** BotConsole does not store your token. It must be provided at the start of each session for maximum security.
*   **Permission Check:** Ensure your bot has the **Administrator** permission for advanced tools to function correctly.

---

## ⚖️ Legal & Disclaimer

**BotConsole** is intended for administrative use and server management testing. Using this tool to maliciously disrupt communities or violate the [Discord Terms of Service](https://discord.com/static/terms/2023-03-27_terms_of_service.pdf) may result in the termination of your bot account and your Discord developer account. Use responsibly.

---

*“Welcome to the silence.”*

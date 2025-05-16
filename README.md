# Discord Admin Bot - *Mobi the Moderator*

Created by: **Alec Gomez**

**Mobi Bot is a dedicated Discord bot designed to enhance moderation and community management within Discord servers. Built with Python, Mobi Bot offers automated content moderation, including link approval mechanisms and bad word filtering, to help maintain a safe and welcoming environment for all community members.**

## Features

The following **features** are completed:

- [x] **Automated Bad Word Filtering: Automatically detects and deletes messages containing predefined inappropriate words, helping maintain the server's content policy.**
- [x] **Link Approval System: Monitors messages for links and either holds them for moderator approval or automatically deletes them based on the server's current settings.**
- [x] **Dynamic Toggle System: Allows administrators to dynamically toggle the link approval system on or off, providing flexibility in content management according to the server's needs.**

The following **future** features are planned:

- [ ] **Whitelisting Links is a work in progress.**

## Commands

👋 Here are all the available commands for Mobi Bot:

### 🌟 General Commands
| Command | Description |
|---------|-------------|
| `!hello` | Say hello to Mobi! A friendly way to check if the bot is active |
| `!help`  | Display all available commands and their descriptions |

### 🛡️ Moderator Commands
| Command | Description |
|---------|-------------|
| `!approve <user_id>` | Approve a pending link from a user. The original link will be reposted in the channel |

### ⚡ Admin Commands
| Command | Description |
|---------|-------------|
| `!words add <word>` | Add a word to the profanity filter list |
| `!words remove <word>` | Remove a word from the profanity filter list |
| `!link_approval on/off` | Toggle the link approval system on or off |

## Project Structure

The project is organized into several key components:
```
discord-bot/
│
├── src/                        # Source code directory
│   ├── main.py                 # Main bot file
│   ├── badwords_manager.py     # Manages the bad words list
│   └── link_manager.py         # Manages links and toggle state
│
├── data/                       # Data files directory for persistence
│   ├── toggle_state.json       # Stores the toggle state for link approval
│   ├── pending_links.json      # Stores links pending approval
│   └── badwords.json           # Stores the list of bad words
|   └── whitelist.json          # Implementing Whitelist to allow words
│
└── README.md                   # This file
```

## Video Walkthrough

Here's a walkthrough of implemented user stories:

<img src='public\assets\walkthrough.gif' title='Video Walkthrough' width='' alt='Video Walkthrough' />

GIF created with ezgif

## 📝 Notes

- The bot automatically filters messages containing banned words
- Links are held for moderator approval when link approval is enabled
- Moderators receive notifications when new links need approval
- All settings and data are persistently stored in JSON files

## License

    Copyright 2025 Alec Gomez

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
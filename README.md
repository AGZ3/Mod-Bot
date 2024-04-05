Mobi Bot

Mobi Bot is a dedicated Discord bot designed to enhance moderation and community management within Discord servers. Built with Python, Mobi Bot offers automated content moderation, including link approval mechanisms and bad word filtering, to help maintain a safe and welcoming environment for all community members.

Features

Automated Bad Word Filtering: Automatically detects and deletes messages containing predefined inappropriate words, helping maintain the server's content policy.
Link Approval System: Monitors messages for links and either holds them for moderator approval or automatically deletes them based on the server's current settings.
Dynamic Toggle System: Allows administrators to dynamically toggle the link approval system on or off, providing flexibility in content management according to the server's needs.

Project Structure

The project is organized into several key components:

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
│
├── .env                        # Environment variables (e.g., DISCORD_KEY)
├── requirements.txt            # Python package dependencies
└── README.md                   # This file

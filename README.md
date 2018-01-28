# QuoteBot

![Example 01](https://my.mixtape.moe/ihmkev.png)    
![Example 02](https://my.mixtape.moe/sexrnz.png)

Tired of hitting the 50 message limit for pins? Use QuoteBot to save all your favorite memories!

### [Click here to add QuoteBot to your server!](https://discordapp.com/oauth2/authorize?client_id=403644354591326218&scope=bot&permissions=117760)

### Usage

**Note:** `m` denotes a mention of the bot, i.e. `@QuoteBot#6976`.

- `m quote <message ID> [message ID ...]`: Quotes one or more messages from the current channel.
- `m quote from <channel mention> <message ID> [message ID ...]`: Quotes one or more messages from the mentioned channel.
- `m unquote <message ID> [message ID ..]`: Unquotes a message. (ID must be from the quote channel.)
- `m qc set <channel mention>` [**admin only**]: Sets the channel quotes are embedded in.
- `m qc get`: Prints a mention of the current quote channel to chat.
- `m invite`: Prints a URL to invite the bot to your server.
- `m stats`: Displays QuoteBot's statistics.
- `m ping`: Pong! Easy check to make sure QuoteBot is working.
- `m reload [cog name] [cog name ...]`: Reloads specified cogs or all cogs if none are specified.

### Enabling Developer Mode in Discord

You need to enable developer mode to be able to copy message IDs. Here's how:

1. Click on "User Settings."
2. Click on "Appearance."
3. Scroll down to "Advanced."
4. Click the switch next to "Developer Mode."

Now you can copy message IDs. When you hover your mouse over a message, click the three dots to the right (long press on mobile). An option called "Copy ID" should show up. Click it!

### Setup

1. Clone the repo with `git clone <url> [folder]`.
2. Install requirements with `pip[3] install -r requirements.txt`.
3. Install discord.py v1.0.0a with `python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py`
4. Copy `config_default.json` to `config.json` and enter your bot token.
5. Run the bot with `python[3] quotebot.py`.

### v1.0 Roadmap

- [x] Make `quote` command available to bot owner and admins.
- [x] Update `quote` command to add reactions from original messages.
- [x] Add `invite` command.
- [x] Write help documentation for `help` command.
- [x] If quoting a message with just a URL to an image, embed the image.
- [x] Give quoted message embeds a footer with date, time, and channel.
- [x] Add `print` statements for invites, database manipulation, errors.
- [x] Add instructions for enabling Discord Developer Mode to `README.md`.

### v2.0 Roadmap

**R&D of these features will begin if/when the bot has joined 500 guilds.**

_Most of these features are theoretical and may or may not be implemented._

- [ ] Refactor from `commands.Bot` to `commands.AutoShardedBot`.
- [ ] Implement cross-guild quoting.
- [ ] Add SQL server functionality.
- [ ] Add more fields to the `guilds` table so stats can show "top" servers.
- [ ] Implement relational table to keep track of specific quoted messages.
- [ ] Save and attach files to quote message instead of URLs.

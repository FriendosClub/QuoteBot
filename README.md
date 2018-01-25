# QuoteBot

Tired of hitting the 50 message limit for pins? Use QuoteBot to save all your favorite memories!

### [Click here to add QuoteBot to your server!](https://discordapp.com/oauth2/authorize?client_id=403644354591326218&scope=bot&permissions=117760)

### Usage

**Note:** `m` denotes a mention of the bot, i.e. `@QuoteBot#6976`.

- `m quote <message ID> [message ID ...]`: Quotes one or more messages from the current channel.
- `m quote from <channel mention> <message ID> [message ID ...]`: Quotes one or more messages from the mentioned channel.
- `m qc set <channel mention>` [**admin only**]: Sets the channel quotes are embedded in.
- `m qc get`: Prints a mention of the current quote channel to chat.
- `m stats`: Displays QuoteBot's statistics.
- `m ping`: Pong! Easy check to make sure QuoteBot is working.

### Setup

1. Clone the repo with `git clone <url> [folder]`.
2. Install requirements with `pip[3] install -r requirements.txt`.
3. Copy `config_default.json` to `config.json` and enter your bot token.
4. Run the bot with `python[3] quotebot.py`.

### v1.0 Roadmap

- [x] Make command `qc set` admin-only.
- [x] Update `quote` command to take an arbitrary number of message IDs.
- [x] Add `quote` subcommand so users can specify a channel.
- [x] Update the `stats` command to display global stats as an embed.
- [x] Update `quote` command to handle non-image attachments.
- [x] Update `quote` command to handle up to 10 attachments.
- [ ] ~~Update `quote` command to handle embeds (e.g. YouTube videos).~~
- [x] Implement `unquote` command.
- [x] Create a more verbose `on_ready` message.
- [ ] If quoting a message with just a URL to an image, embed the image.
- [ ] Add logging for invites, database manipulation, errors.
- [ ] Update command help/usage and documentation.
- [ ] Implement DMing of help to users who request it.
- [ ] Add instructions for enabling Discord Developer Mode to `README.md`.

### v2.0 Roadmap

**R&D of these features will begin if/when the bot has joined 500 guilds.**

_Most of these features are theoretical and may or may not be implemented._

- [ ] Refactor from `commands.Bot` to `commands.AutoShardedBot`.
- [ ] Implement cross-guild quoting.
- [ ] Add SQL server functionality.
- [ ] Add more fields to the `guilds` table so stats can show "top" servers.
- [ ] Implement relational table to keep track of specific quoted messages.
- [ ] Save and attach files to quote message instead of URLs.

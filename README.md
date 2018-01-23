# QuoteBot

Tired of hitting the 50 message limit for pins? Use QuoteBot to save all your favorite memories!

### [Click here to add QuoteBot to your server!](https://discordapp.com/oauth2/authorize?client_id=403644354591326218&scope=bot&permissions=117760)

### Usage

**Note:** `m` denotes a mention of the bot, i.e. `@QuoteBot#6976`

- `m quote <message ID>`: Quotes a message from the current channel.
- `m quote <message ID> [channel mention]` [**currently broken**]: Quotes a message from the mentioned channel.
- `m stats`: Displays QuoteBot's statistics.
- `m qc set <channel mention>` [**admin only**]: Sets the channel quotes are embedded in.
- `m qc get`: Prints a mention of the current quote channel to chat.
- `m ping`: Pong! Easy check to make sure QuoteBot is working.

### Setup

1. Clone the repo with `git clone <url> [folder]`.
2. Install requirements with `pip[3] install -r requirements.txt`.
3. Copy `config_default.json` to `config.json` and enter your bot token.
4. Run the bot with `python[3] quotebot.py`.

### To-Do

- [ ] Write help/usage documentation
- [ ] Add instructions for enabling Discord Developer Mode to `README.md`.
- [x] Make command `qc set` admin-only.
- [ ] Update the `stats` command to display global stats as well.
- [x] Update `quote` command to take an arbitrary number of message IDs.
- [x] Add `quote` subcommand so users can specify a channel.
- [ ] Update `quote` command to handle non-image attachments.
- [ ] Update `quote` command to handle up to 10 attachments.
- [ ] Implement `unquote` command.
- [ ] ~~Implement a `create_quote_channel` (admin only) command.~~
- [ ] Add SQL server functionality.
- [ ] More testing and bugfixes.

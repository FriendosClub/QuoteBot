"""Summary
"""
import sqlite3


class DBHelper():
    """Simple helper class to abstract SQlite I/O

    Attributes:
        file (str): The sqlite database, i.e. `quotebot.db`.
    """
    def __init__(self, db_file: str):
        """Default constructor.

        Args:
            db_file (str): The sqlite database, i.e. `quotebot.db`.
        """
        self.file = db_file

        # Debugging
        print('Initializing database...')

        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS guilds
                       (guild_id INTEGER NOT NULL UNIQUE,
                        quote_channel INTEGER NOT NULL,
                        quote_count INTEGER NOT NULL DEFAULT 0 CHECK(quote_count >= 0),
                        PRIMARY KEY(guild_id))''')
        conn.commit()
        conn.close()

    def get_quote_channel(self, guild_id: int) -> int:
        """Retrieve the ID of the channel for posting quotes.

        Args:
            guild_id (int): ID of the specific guild.

        Returns:
            int: The quote channel ID. Returns `None` if no entry is present.
        """
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        cursor.execute('SELECT quote_channel FROM guilds WHERE guild_id=?',
                       (guild_id,))
        # Guild IDs/entries are unique, so there will be zero or one results.
        result = cursor.fetchone()

        conn.close()

        if not result:
            return None
        else:
            # Return the only item in the tuple
            return result[0]

    def set_quote_channel(self, guild_id: int, channel_id: int) -> bool:
        """Inserts or updates the required information for a guild.

        Args:
            guild_id (int): The ID of the guild.
            channel_id (int): The ID of the quote channel.

        Returns:
            bool: True if the insert/update succeeded, False otherwise.
        """
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        result = False

        q = '''INSERT OR REPLACE INTO guilds (guild_id, quote_channel, quote_count)
               VALUES (?, ?, (SELECT quote_count FROM guilds WHERE guild_id=?))'''

        # TODO: Implement error handling for this query (CHECK fail, etc.)
        cursor.execute(q, (guild_id, channel_id, guild_id))
        result = True

        conn.commit()
        conn.close()
        return result

    def update_quote_count(self, guild_id: int, amount: int = 1):
        """Updates the number of quotes the bot has stored for a guild.
           Defaults to incrementing by one.

        Args:
            guild_id (int): Which guild's quote count to modify.
            amount (int, optional): The desired delta.
        """
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        # TODO: Implement error handling
        cursor.execute('''UPDATE guilds SET quote_count = quote_count + ?
                          WHERE guild_id = ?''', (amount, guild_id))

        conn.commit()
        conn.close()

    def get_quote_count(self, guild_id: int) -> int:
        """Fetches the number of messages quoted for a guild.

        Args:
            guild_id (int): Which guild to fetch the statistic for.

        Returns:
            int: The number of messages quoted.
        """
        conn = sqlite3.connect(self.file)
        cursor = conn.cursor()

        cursor.execute('''SELECT quote_count FROM guilds
                          WHERE guild_id=?''', (guild_id,))

        guild_quote_count = cursor.fetchone()

        conn.close()

        if guild_quote_count is None:
            guild_quote_count = 0

        return guild_quote_count[0]

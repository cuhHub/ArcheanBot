# // ---------------------------------------------------------------------
# // ------- [Models] Waitee
# // ---------------------------------------------------------------------

"""
A model representing a user waiting for the server to reach a certain player count
Repo: https://github.com/cuhHub/ArcheanBot

---

Copyright (C) 2024 Cuh4

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

# ---- // Imports
from __future__ import annotations

import peewee
import discord
import time
from bot import Bot

from . import proxy

# ---- // Main
class Waitee(peewee.Model):
    """
    A model representing a user waiting for the server to reach a certain player count
    """

    user_id = peewee.IntegerField()
    wants_player_count = peewee.IntegerField()
    fallback_channel_id = peewee.IntegerField()
    start_time = peewee.FloatField(default = time.time)
    
    class Meta:
        database = proxy
        
    @classmethod
    def wait_for_count(cls, user: discord.User, player_count: int, channel: discord.TextChannel) -> Waitee:
        """
        Creates a Waitee record for the provided user.

        Args:
            user (discord.User): The user to create a Waitee record for.
            player_count (int): The player count to wait for.
            channel (discord.TextChannel): The channel to send the reminder to if sending via DMs didn't work.

        Returns:
            Waitee: The created Waitee record.
        """
        
        return cls.create(
            user_id = user.id,
            wants_player_count = player_count,
            fallback_channel_id = channel.id
        )
        
    async def get_user(self, bot: Bot) -> discord.User|None:
        """
        Returns the user associated with the Waitee record.

        Args:
            bot (Bot): The bot to use for retrieving the user.

        Returns:
            discord.User|None: The user associated with the Waitee record, or None if not found.
        """     
        
        try:
            return bot.get_user(self.user_id) or await bot.fetch_user(self.user_id)
        except:
            return
        
    async def get_fallback_channel(self, bot: Bot) -> discord.TextChannel|None:
        """
        Returns the fallback channel associated with the Waitee record.

        Args:
            bot (Bot): The bot to use for retrieving the channel.

        Returns:
            discord.TextChannel|None: The fallback channel associated with the Waitee record, or None if not found.
        """     
        
        try:
            return bot.get_channel(self.fallback_channel_id) or await bot.fetch_channel(self.fallback_channel_id)
        except:
            return
        
    @classmethod
    def get_waitee(cls, user: discord.User) -> Waitee|None:
        """
        Returns the Waitee record for the provided user.

        Args:
            user (discord.User): The user to retrieve the Waitee record for.

        Returns:
            Waitee|None: The Waitee record for the user, or None if not found.
        """        

        try:
            return cls.get(user_id = user.id)
        except peewee.DoesNotExist:
            return
        
    @classmethod
    def get_waitees_for_player_count(cls, player_count: int) -> list[Waitee]:
        """
        Returns a list of Waitees waiting for the server to reach the provided player count.

        Args:
            player_count (int): The player count to check against.

        Returns:
            list[Waitee]: The list of waitees.
        """        

        try:
            return list(cls.select().where(cls.wants_player_count == player_count).execute())
        except peewee.DoesNotExist:
            return []
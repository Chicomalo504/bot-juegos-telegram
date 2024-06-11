#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from bot_base import BotBase
from .hangman import HangManGame 
from utils.errors import ModelError

class BotTelegramAhorcado(BotBase):
    def __init__(self):
        super(BotTelegramAhorcado, self).__init__(__file__)

    def name(self):
        return 'Ahorcado'

    def generate_game_state(self, user_id):
        self.users_data[str(user_id)] = HangManGame()
        #self.data_manager.save_info(self.users_data)

    def get_game(self, user_id: int):
        return self.users_data[str(user_id)]
    
    async def play(self, update, context):
        user_id = self.get_user_id(update)
        bot = context.bot
        self.generate_game_state(user_id)
        await self.send_message(bot, user_id, "Ingrese una letra como mensaje para jugar:")
        await self.send_message(bot, user_id, self.get_game(user_id).template())

    async def answer_message(self, update, context):
        letter = update.message.text.upper()
        bot = context.bot
        user_id = update.message.chat_id
        game = self.get_game(user_id)

        async def try_letter():
            game.try_letter(letter)
            await self.send_message(bot, user_id, game.template())
            if game.lost():
                await self.send_message(bot, user_id, "Has perdido\nLa palabra era: {}".format(game.word()))
        
            if game.won():
                await self.send_message(bot, user_id, "Felicitaciones, hasta ganado!.")

        if not game.is_finished():
            await self.process_user_action(bot, user_id, try_letter)
            #self.data_manager.save_info(self.users_data)
        else:
            await self.game_finished_message(bot, user_id)

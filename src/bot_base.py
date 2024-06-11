#!/usr/bin/env/ python3
# -*- coding: utf-8 -*-

import os
from bot_telegram import BotTelegram
from utils.data_manager import DataManager
from utils.errors import ModelError


class BotBase(BotTelegram):

    def __init__(self, file):
        self.data_manager = DataManager(os.path.dirname(file))
        self.users_data = self.data_manager.generate_info(dict())

    def is_inline_game(self):
        return False

    def do_not_understand_message(self):
        return "Disculpa, no entiendo tu mensaje."

    async def game_finished_message(self, bot, user_id):
        await self.send_message(bot, user_id, "El juego ya terminó. Utiliza /juegos para comenzar uno nuevo.")

    async def answer_message(self, update, context):
        usuario = self.get_user_id(update)
        bot = context.bot
        await self.send_message(bot, usuario, self.do_not_understand_message())

    async def answer_button(self, update, context):
        usuario = self.get_user_id(update)
        bot = context.bot
        await self.send_message(bot, usuario, self.do_not_understand_message())

    async def process_user_action(self, bot, user_id, callback):
        try:
           await callback()
        except ModelError as error:
            await self.send_message(bot, user_id, error.message)
        except:
            await self.send_message(bot, user_id, "Ocurrió un error inesperado, por favor intenta nuevamente")
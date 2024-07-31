#!/usr/bin/env/python3
# -*- coding: utf-8 -*-
from telegram_bot import BotTelegram
from games.Hangman.hangman_bot import BotTelegramAhorcado
from games.Mastermind.bot_mastermind import BotMastermind
from games.Minesweeper.minesweeper_bot import BotBuscaminas
from games.TicTacToe.tictactoe_bot import BotTicTacToe
from games.TicTacToe_MultiPlayer.inline_tictactoe_bot import BotTaTeTiInLine
from games.RockPaperScissor.rock_paper_scissor_bot import BotRockPaperScissor
from games.RockPaperScissor.rock_paper_scissor_multiplayer_bot import BotRockPaperScissorMultiplayer
from utils.data_manager import DataManager
from telegram import InputTextMessageContent, InlineQueryResultArticle
from uuid import uuid4

import os

# Para crear boton en telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

bot_mastermind = BotMastermind()
bot_tictactoe = BotTicTacToe()
bot_ahorcado = BotTelegramAhorcado()
bot_buscaminas = BotBuscaminas()
bot_rps = BotRockPaperScissor()
bot_tateti_inline = BotTaTeTiInLine()
bot_rps_multiplayer = BotRockPaperScissorMultiplayer()
from internationalization import set_translator

class GamesTelegramBot(BotTelegram):
    def __init__(self, name, token):
        BotTelegram.__init__(self, name, token)
        self.game_catalog = {bot_ahorcado.name(): bot_ahorcado,
                                   bot_buscaminas.name(): bot_buscaminas,                                   bot_mastermind.name(): bot_mastermind,
                                   bot_tictactoe.name(): bot_tictactoe,
                                   bot_tateti_inline.name(): bot_tateti_inline,
                                   bot_rps.name(): bot_rps,
                                   bot_rps_multiplayer.name(): bot_rps_multiplayer
                                   }
        
        self.data_manager = DataManager(os.path.abspath(''))
        self.user_data = self.data_manager.generate_info(dict())
    
    # TO-DO: We should re check how this is done
    def change_translator(self, new_translator):
        super().change_translator(new_translator)
        for game in self.game_catalog.values():
            game.change_translator(new_translator)
    
    @set_translator
    async def start(self, update, context):
        bot = context.bot
        user_id = self.get_user_id(update)
        user_name = update.message.chat.first_name
        self.user_data[str(user_id)] = {"juego_actual": None, "estado": {}}
        self.data_manager.save_info(self.user_data)
        message = self._("Hello *{}*, welcome to classic games bot. Use /games to show the available games").format(user_name) + ".\n\n"
        message += self._("There are also some multiplayer games. To play them, you have to write `@juegos_clasicos_bot play` on your friend's chat.") + "\n\n"
        message += self._("A list with the available games will be shown, then select the game that you want to play.")
        await self.send_message(bot, user_id, message, 'markdown')

    @set_translator
    async def display_games(self, update, context):
        games = [[InlineKeyboardButton(game.name(), callback_data=game.name())] for game in
                    self.game_catalog.values() if not game.is_inline_game()]
        await update.message.reply_text(self._("Available games are:"), reply_markup=InlineKeyboardMarkup(games))

    def get_inline_game_by_query_data(self, query_data):
        if (query_data in ['tijera', 'piedra', 'papel']):
            return bot_rps_multiplayer.name()
        else:
            return bot_tateti_inline.name()

    @set_translator
    async def display_inline_games(self, update, context):
        inline_games = []
        for bot_game in self.game_catalog.values():
            if bot_game.is_inline_game():
                inline_message_id = uuid4()
                inline_games.append(InlineQueryResultArticle(
                    id=inline_message_id,
                    title=bot_game.name(),
                    input_message_content=InputTextMessageContent(self._("Let's play to: {}").format(bot_game.name())),
                    reply_markup=bot_game.generate_inline_markup()))
        self.data_manager.save_info(self.user_data)

        await update.inline_query.answer(inline_games)
    
    @set_translator
    async def select_game(self, update, context):
        selected_game = update.callback_query.data
        user = self.get_user_id(update)
        bot = context.bot
        self.user_data[str(user)] = {"juego_actual": selected_game}
        self.data_manager.save_info(self.user_data)

        await self.send_message(bot, user, self._("You chose to play {}. To change the game, you can use /games again") \
                            .format(selected_game))

        await self.game_catalog[selected_game].play(update, context)

    @set_translator
    async def answer_button_by_game(self, update, context):
        if not update.callback_query.inline_message_id:
            user = self.get_user_id(update)
            current_game = self.user_data[str(user)]["juego_actual"]
            await self.game_catalog[current_game].answer_button(update, context)
        else:
            game_name = self.get_inline_game_by_query_data(update.callback_query.data)
            await self.game_catalog[game_name].answer_button(update, context)
    
    @set_translator
    async def answer_message_by_game(self, update, context):
        user_id = self.get_user_id(update)
        current_game = self.user_data[str(user_id)]["juego_actual"]
        await self.game_catalog[current_game].answer_message(update, context)


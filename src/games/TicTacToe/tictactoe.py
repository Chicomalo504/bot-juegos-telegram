import json
from utils.errors import ModelError
# Ta Te Ti

import random


class TicTacToeGame:
	def __init__(self) -> None:
		self.board = [" " for i in range(9)]
		self.game_finished = False

	def to_json(self):
		return json.dumps(self.__dict__)

	@classmethod
	def from_json(cls, json_str):
			data = json.loads(json_str)
			game = cls()
			game.board = data['board']
			game.game_finished = data['game_finished']
			return game
	
	def finished(self):
		return self.game_finished

	def is_winner(self, symbol):
		# Dado un board y la letra de un jugador, devuelve True (verdadero) si el mismo ha ganado.
		# Utilizamos reempplazamos board por ta y letra por le para no escribir tanto
		board = self.board
		return ((board[6] == symbol and board[7] == symbol and board[8] == symbol) or  # horizontal superior
				(board[3] == symbol and board[4] == symbol and board[5] == symbol) or  # horizontal medio
				(board[0] == symbol and board[1] == symbol and board[2] == symbol) or  # horizontal inferior
				(board[6] == symbol and board[3] == symbol and board[0] == symbol) or  # verticual izquierda
				(board[7] == symbol and board[4] == symbol and board[1] == symbol) or  # vertical medio
				(board[8] == symbol and board[5] == symbol and board[2] == symbol) or  # vertical derecha
				(board[6] == symbol and board[4] == symbol and board[2] == symbol) or  # diagonal
				(board[8] == symbol and board[4] == symbol and board[0] == symbol))  # diagonal


	def duplicate_game(self):
		# Duplica la lista del board y devuelve el duplicado
		game = AgainstComputerTicTacToe()
		game.board = self.board[:]
		game.player_symbol = self.player_symbol
		game.computer_symbol = self.computer_symbol
		return game


	def is_empty_cell(self, cell):
		return self.board[cell] == " "


	def find_random_cell_from(self, cell_options):
		# Devuelve una jugada válida en el board de la lista recibida.
		# Devuelve None si no hay ninguna jugada válida.

		possible_choices = []
		for cell in cell_options:
			if self.is_empty_cell(cell):
				possible_choices.append(cell)

		if len(possible_choices) != 0:
			return random.choice(possible_choices)



	def is_full_board(self):
		# D evuelve True si cada espacio del board fue ocupado, caso contrario devuelve False.
		for cell in range(9):
			if self.is_empty_cell(cell):
				return False
		return True
	
	def mark_cell(self, symbol, cell):
		if (self.is_empty_cell(cell)):
			self.board[cell] = symbol
			if self.is_winner(symbol) or self.is_full_board():
				self.game_finished = True
		else:
			raise ModelError("Esa casilla ya está ocupada, por favor elige otra.")
	

class AgainstComputerTicTacToe(TicTacToeGame):
	 
	def __init__(self):
			super(AgainstComputerTicTacToe, self).__init__()
			self.player_symbol = ''
			self.computer_symbol = ''
	
	@classmethod
	def from_json(cls, json_str):
			data = json.loads(json_str)
			game = cls()
			game.board = data['board']
			game.game_finished = data['game_finished']
			game.player_symbol = data['player_symbol']
			game.computer_symbol = data['computer_symbol']
			return game
	
	def started(self):
		return self.player_symbol != ''
	
	def get_players_symbols(self, player_symbol):
		if player_symbol.upper() == 'X':
			self.player_symbol = 'X'
			self.computer_symbol = 'O'
		elif player_symbol.upper() == 'O':
			self.player_symbol = 'O'
			self.computer_symbol = 'X'
		else:
				raise ModelError("Símbolo incorrecto, por favor elige X o O")
	
	def computer_plays_first(self):
		return self.computer_symbol == 'X'
  
	def make_computer_movement(self):

		# Aquí está nuestro algoritmo para nuestra IA (Inteligencia Artificial) del TATETI
		# Primero, verifica si podemos ganar en la próxima jugada.
		for cell in range(9):
			copy = self.duplicate_game()
			if copy.is_empty_cell(cell):
					copy.mark_cell(self.computer_symbol, cell)
					if copy.is_winner(self.computer_symbol):
							self.mark_cell(self.computer_symbol, cell)
							return

		# Verifica si el jugador podría ganar en su próxima jugada, y lo bloquea.
		for cell in range(9):
			copy = self.duplicate_game()
			if copy.is_empty_cell(cell):
				copy.mark_cell(self.player_symbol, cell)
				if copy.is_winner(self.player_symbol):
					self.mark_cell(self.computer_symbol, cell)
					return
		
		copy = self.duplicate_game()
		# Intenta ocupar una de las esquinas de estar libre.
		cell = self.find_random_cell_from([0, 2, 6, 8])
		if cell != None:
				self.mark_cell(self.computer_symbol, cell)
				return

		# De estar libre, intenta ocupar el centro.
		if self.is_empty_cell(4):
				self.mark_cell(self.computer_symbol, 4)
				return

		# Ocupa alguno de los lados.
		cell = self.find_random_cell_from([1, 3, 5, 7])
		self.mark_cell(self.computer_symbol, cell)
	
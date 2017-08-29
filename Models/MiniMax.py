import sys 
import copy
from random import randint
from Models.Tabuleiro import Tabuleiro


class MiniMax:

	def __init__(self, jogador1, jogador2):
		self.jogador1 = jogador1
		self.jogador2 = jogador2
		self.isRunning = False

	def start(self, profundidade, tabuleiro):
		self.isRunning = True
		self.count = 0
		# tabuleiroCopia = Tabuleiro(15, 15)
		# tabuleiroCopia.setEstadoAtual(tabuleiro.getEstadoAtual())
		jogada = self.run(profundidade, tabuleiro, self.jogador1, -1*sys.maxsize, sys.maxsize)
		print("Pontuacao : " + str(jogada[0]) + "Linha : " + str(jogada[1]) + "Coluna : " + str(jogada[2]))
		return jogada

	def run(self, profundidade, tabuleiro, jogador, alpha, beta):
		proximasJogadas = tabuleiro.gerarPossiveisJogadas()
		pontuacao = 0
		jogadaLinha = -1
		jogadaColuna = -1
		print(" MINIMAX RUNNING - Profundidade : " + str(profundidade))
		# print(tabuleiro.getEstadoAtual())
		if(len(proximasJogadas) == 0 or profundidade == 0):
			pontuacao = self.avaliacao(tabuleiro)
			self.count = self.count + 1
			print("MINIMAX TERMINOU : " + str(self.count))
			return [pontuacao, jogadaLinha, jogadaColuna]
		else:
			for jogada in proximasJogadas:

				tabuleiro.getEstadoAtual()[jogada[0]][jogada[1]] = jogador.getPeca()

				if jogador is self.jogador1:
					pontuacao = self.run(profundidade-1, tabuleiro, self.jogador2, alpha, beta)[0]

					if pontuacao > alpha:
						alpha = pontuacao
						jogadaLinha = jogada[0]
						jogadaColuna = jogada[1]
				else:
					pontuacao = self.run(profundidade-1, tabuleiro, self.jogador1, alpha, beta)[0]

					if pontuacao < beta:
						beta = pontuacao
						jogadaLinha = jogada[0]
						jogadaColuna = jogada[1]

				tabuleiro.getEstadoAtual()[jogada[0]][jogada[1]] = 0
				if alpha >= beta:
					break

			param = alpha if jogador is self.jogador1 else beta		
			return [param, jogadaLinha, jogadaColuna]

	def avaliacaoTeste(self):
		p1 = randint(1, 9) * 100
		p2 = randint(1, 9) * 100

		return p1 - p2

	def avaliacao(self, tabuleiro):
		# print("Executando a avaliacao")
		self.pontuacao = [5, 10, 5000, 10000, 5000000, 10000000, 1000000000]
		scoreAvaliacaoPorLinha = self.avaliacaoPorLinha(tabuleiro)
		scoreAvaliacaoPorColuna = self.avaliacaoPorColuna(tabuleiro)
		score = scoreAvaliacaoPorLinha + scoreAvaliacaoPorColuna	
		# print("Avaliacao Linha : " + str(scoreAvaliacaoPorLinha)+ " Avaliacao Coluna : " + str(scoreAvaliacaoPorColuna)+ "Avaliacao Total : " + str(score))
		return score

	# avalia o tabuleiro em suas linhas
	def avaliacaoPorLinha(self, tabuleiro):
		# print("avaliacao linha")
		linha = 0
		estados = tabuleiro.getEstadoAtual()
		scoreP1 = 0
		scoreP2 = 0
		espacoVazio = 0
		# avaliando por linhas
		for row in estados:
			coluna = 0
			
			while coluna < len(row):
				
				if row[coluna] == 0:
					espacoVazio = 1					
					coluna = coluna + 1
					# print("Espaco vazio : coluna : " + str(coluna))					
					continue				
				# avaliando as pecas do jogador1
				# tem uma peca
				if row[coluna].getDono() is self.jogador1:
					if coluna+1 < len(row):

						# a casa seguinte esta vazia	
						if row[coluna + 1] == 0:
							espacoVazio = 1
							coluna = coluna + 1
						# tem duas pecas

						elif row[coluna+1].getDono() is self.jogador1:
							# print("JOGADOR 1")
							if coluna+2 < len(row):
								
								# tem duas pecas e a casa seguinte esta vazia
								if row[coluna + 2] == 0:	
									# ja tem um espaco vazio, entao sao dois espacos vazios
									if espacoVazio == 1:
										scoreP1 = scoreP1 + self.pontuacao[1]
										coluna = coluna + 2
									# so tem um espaco vazio	
									else:
										scoreP1 = scoreP1 + self.pontuacao[0]
										espacoVazio = 1	
										coluna = coluna + 2

								# tem tres pecas
								elif row[coluna+2].getDono() is self.jogador1:

									if coluna+3 < len(row):

										# tem tres pecas e a casa seguinte esta vazia	
										if row[coluna + 3] == 0:
											# ja tem um espaco vazio, entao sao dois espacos vazios
											if espacoVazio == 1:
												scoreP1 = scoreP1 + self.pontuacao[3]
												coluna = coluna + 3
											# so tem um espaco vazio	
											else:
												scoreP1 = scoreP1 + self.pontuacao[2]
												espacoVazio = 1	
												coluna = coluna + 3	

										# tem quatro pecas
										elif row[coluna+3].getDono() is self.jogador1:
											
											if coluna+4 < len(row):

												# tem quatro pecas e a casa seguinte esta vazia	
												if row[coluna+4] == 0:
													# ja tem um espaco vazio, entao sao dois espacos vazios
													if espacoVazio == 1:
														scoreP1 = scoreP1 + self.pontuacao[5]
														coluna = coluna + 4
													# so tem um espaco vazio	
													else:
														scoreP1 = scoreP1 + self.pontuacao[4]
														espacoVazio = 1	
														coluna = coluna + 4	
												# tem 5 pecas
												elif row[coluna+4].getDono() is self.jogador1:
													scoreP1 = scoreP1 + self.pontuacao[6]
													espacoVazio = 0
													coluna = coluna + 5

												# tem quatro pecas e a seguinte eh do oponente	
												elif row[coluna+4].getDono() is self.jogador2:
													espacoVazio = 0
													coluna = coluna + 4

											# tem quatro pecas no canto do tabuleiro e tem um espaco vazio		
											elif espacoVazio == 1:
												scoreP1 = scoreP1 + self.pontuacao[4]
												espacoVazio = 0
												coluna = coluna + 4	

											# tem quatro pecas no canto do tabuleiro e nao tem espaco vazio	
											else:	
												coluna = coluna + 4

										# tem tres pecas e a seguinte eh do oponente			
										elif row[coluna+3].getDono() is self.jogador2:
											espacoVazio = 0 
											coluna = coluna + 3											

									# tem tres pecas no canto do tabuleiro e tem um espaco vazio				
									elif espacoVazio == 1:
										scoreP1 = scoreP1 + self.pontuacao[2]
										espacoVazio = 0
										coluna = coluna + 3	

									# tem tres pecas no canto do tabuleiro e nao tem espaco vazio	
									else:
										coluna = coluna + 3

								# tem duas pecas e a peca seguinte eh do oponente						
								elif row[coluna+2].getDono() is self.jogador2:
									coluna = coluna + 2
									espacoVazio = 0
								
							# duas pecas no canto do tabuleiro e tem um espaco vazio					
							elif espacoVazio == 1:
								scoreP1 = scoreP1 + self.pontuacao[0]
								espacoVazio = 0
								coluna = coluna + 2

							# duas pecas no canto do tabuleiro e nao tem espacos vazios
							else:
								coluna = coluna + 2	

						# a peca seguinte eh do oponente							
						elif row[coluna+1].getDono() is self.jogador2:
							coluna = coluna + 1	

					# ultima casa da linha							
					else:
						coluna = coluna + 1
							
				# avaliando as pecas do jogador2
				# tem uma peca			
				elif row[coluna].getDono() is self.jogador2:
					# print("JOGADOR 2")
					if coluna+1 < len(row):
						# a casa seguinte esta vazia	
						if row[coluna+1] == 0 :
							espacoVazio = 1
							coluna = coluna + 1

						# tem duas pecas
						elif row[coluna+1].getDono() is self.jogador2:

							if coluna+2 < len(row):

								# tem duas pecas e a casa seguinte esta vazia
								if row[coluna+2] == 0:	
									# ja tem um espaco vazio, entao sao dois espacos vazios
									if espacoVazio == 1:
										scoreP2 = scoreP2 + self.pontuacao[1]
										coluna = coluna + 2
									# so tem um espaco vazio	
									else:
										scoreP2 = scoreP2 + self.pontuacao[0]
										espacoVazio = 1	
										coluna = coluna + 2

								# tem tres pecas
								elif row[coluna+2].getDono() is self.jogador2:

									if coluna+3 < len(row):

										# tem tres pecas e a casa seguinte esta vazia	
										if row[coluna+3] == 0:
											# ja tem um espaco vazio, entao sao dois espacos vazios
											if espacoVazio == 1:
												scoreP2 = scoreP2 + self.pontuacao[3]
												coluna = coluna + 3
											# so tem um espaco vazio	
											else:
												scoreP2 = scoreP2 + self.pontuacao[2]
												espacoVazio = 1	
												coluna = coluna + 3		

										# tem quatro pecas
										elif row[coluna+3].getDono() is self.jogador2:
											
											if coluna+4 < len(row):

												# tem quatro pecas e a casa seguinte esta vazia	
												if row[coluna+4] == 0:
													# ja tem um espaco vazio, entao sao dois espacos vazios
													if espacoVazio == 1:
														scoreP2 = scoreP2 + self.pontuacao[5]
														coluna = coluna + 4
													# so tem um espaco vazio	
													else:
														scoreP2 = scoreP2 + self.pontuacao[4]
														espacoVazio = 1	
														coluna = coluna + 4
												# tem 5 pecas
												elif row[coluna+4].getDono() is self.jogador2:
													scoreP2 = scoreP2 + self.pontuacao[6]
													espacoVazio = 0
													coluna = coluna + 4

												# tem quatro pecas e a seguinte eh do oponente	
												elif row[coluna+4].getDono() is self.jogador1:
													espacoVazio = 0
													coluna = coluna + 4														

											# tem quatro pecas no canto do tabuleiro e tem um espaco vazio		
											elif espacoVazio == 1:
												scoreP2 = scoreP2 + self.pontuacao[4]
												espacoVazio = 0
												coluna = coluna + 4	

											# tem quatro pecas no canto do tabuleiro e nao tem espaco vazio	
											else:	
												coluna = coluna + 4

										# tem tres pecas e a seguinte eh do oponente			
										elif row[coluna+3].getDono() is self.jogador1:
											espacoVazio= 0 
											coluna = coluna + 3
										
									# tem tres pecas no canto do tabuleiro e tem um espaco vazio				
									elif espacoVazio == 1:
										scoreP2 = scoreP2 + self.pontuacao[2]
										espacoVazio = 0
										coluna = coluna + 3	

									# tem tres pecas no canto do tabuleiro e nao tem espaco vazio	
									else:
										coluna = coluna + 3

								# tem duas pecas e a peca seguinte eh do oponente						
								elif row[coluna+2].getDono() is self.jogador1:
									coluna = coluna + 2
									espacoVazio = 0
								
							# duas pecas no canto do tabuleiro e tem um espaco vazio					
							elif espacoVazio == 1:
								scoreP2 = scoreP2 + self.pontuacao[0]
								espacoVazio = 0
								coluna = coluna + 2

							# duas pecas no canto do tabuleiro e nao tem espacos vazios
							else:
								coluna = coluna + 2	

						# a peca seguinte eh do oponente							
						elif row[coluna+1].getDono() is self.jogador1:
							coluna = coluna + 1

					# ultima casa da linha		
					else:
						coluna = coluna + 1					
			linha = linha + 1

		return scoreP1 - scoreP2

	# avalia o tabuleiro em suas colunas	
	def avaliacaoPorColuna(self, tabuleiro):
		# print("avaliacao coluna")
		coluna = 0
		estados = tabuleiro.getEstadoAtual()
		scoreP1C = 0
		scoreP2C = 0
		espacoVazio = 0
		# avaliando por coluna
		while coluna < len(estados[0]):
			linha = 0
			# print("Tamanho Coluna: " + str(len(estados[0])))
			while linha < len(estados):
				# print("Tamanho Coluna: " + str(len(estados)))
				if estados[linha][coluna] == 0:
					espacoVazio = 1					
					linha = linha + 1
					# print("Espaco vazio : Linha : " + str(linha))					
					continue				
				# avaliando as pecas do jogador1
				# tem uma peca
				# print(estados[linha][coluna].getDono())
				if estados[linha][coluna].getDono() is self.jogador1:
					if linha+1 < len(estados):

						# a casa seguinte esta vazia	
						if estados[linha+1][coluna] == 0:
							espacoVazio = 1
							linha = linha + 1
						# tem duas pecas

						elif estados[linha+1][coluna].getDono() is self.jogador1:

							if linha+2 < len(estados):
								
								# tem duas pecas e a casa seguinte esta vazia
								if estados[linha+2][coluna] == 0:	
									# ja tem um espaco vazio, entao sao dois espacos vazios
									if espacoVazio == 1:
										scoreP1C = scoreP1C + self.pontuacao[1]
										linha = linha + 2
									# so tem um espaco vazio	
									else:
										scoreP1C = scoreP1C + self.pontuacao[0]
										espacoVazio = 1	
										linha = linha + 2

								# tem tres pecas
								elif estados[linha+2][coluna].getDono() is self.jogador1:

									if linha+3 < len(estados):

										# tem tres pecas e a casa seguinte esta vazia	
										if estados[linha+3][coluna] == 0:
											# ja tem um espaco vazio, entao sao dois espacos vazios
											if espacoVazio == 1:
												scoreP1C = scoreP1C + self.pontuacao[3]
												linha = linha + 3
											# so tem um espaco vazio	
											else:
												scoreP1C = scoreP1C + self.pontuacao[2]
												espacoVazio = 1	
												linha = linha + 3	

										# tem quatro pecas
										elif estados[linha+3][coluna].getDono() is self.jogador1:
											
											if linha+4 < len(estados):

												# tem quatro pecas e a casa seguinte esta vazia	
												if estados[linha+4][coluna] == 0:
													# ja tem um espaco vazio, entao sao dois espacos vazios
													if espacoVazio == 1:
														scoreP1C = scoreP1C + self.pontuacao[5]
														linha = linha + 4
													# so tem um espaco vazio	
													else:
														scoreP1C = scoreP1C + self.pontuacao[4]
														espacoVazio = 1	
														linha = linha + 4	
												# tem 5 pecas
												elif estados[linha+4][coluna].getDono() is self.jogador1:
													scoreP1C = scoreP1C + self.pontuacao[6]
													espacoVazio = 0
													linha = linha + 5

												# tem quatro pecas e a seguinte eh do oponente	
												elif estados[linha+4][coluna].getDono() is self.jogador2:
													espacoVazio = 0
													linha = linha + 4

											# tem quatro pecas no canto do tabuleiro e tem um espaco vazio		
											elif espacoVazio == 1:
												scoreP1C = scoreP1C + self.pontuacao[4]
												espacoVazio = 0
												linha = linha + 4	

											# tem quatro pecas no canto do tabuleiro e nao tem espaco vazio	
											else:	
												linha = linha + 4

										# tem tres pecas e a seguinte eh do oponente			
										elif estados[linha+3][coluna].getDono() is self.jogador2:
											espacoVazio = 0 
											linha = linha + 3											

									# tem tres pecas no canto do tabuleiro e tem um espaco vazio				
									elif espacoVazio == 1:
										scoreP1C = scoreP1C + self.pontuacao[2]
										espacoVazio = 0
										linha = linha + 3	

									# tem tres pecas no canto do tabuleiro e nao tem espaco vazio	
									else:
										linha = linha + 3

								# tem duas pecas e a peca seguinte eh do oponente						
								elif estados[linha+2][coluna].getDono() is self.jogador2:
									linha = linha + 2
									espacoVazio = 0
								
							# duas pecas no canto do tabuleiro e tem um espaco vazio					
							elif espacoVazio == 1:
								scoreP1C = scoreP1C + self.pontuacao[0]
								espacoVazio = 0
								linha = linha + 2

							# duas pecas no canto do tabuleiro e nao tem espacos vazios
							else:
								linha = linha + 2	

						# a peca seguinte eh do oponente							
						elif estados[linha+1][coluna].getDono() is self.jogador2:
							linha = linha + 1
					# ultima casa da coluna								
					else:
						linha = linha + 1
							
				# avaliando as pecas do jogador2
				# tem uma peca			
				elif estados[linha][coluna].getDono() is self.jogador2:
					
					if linha+1 < len(estados):
						# a casa seguinte esta vazia	
						if estados[linha+1][coluna] == 0 :
							espacoVazio = 1
							linha = linha + 1
							
						# tem duas pecas
						elif estados[linha+1][coluna].getDono() is self.jogador2:

							if linha+2 < len(estados):

								# tem duas pecas e a casa seguinte esta vazia
								if estados[linha+2][coluna] == 0:	
									# ja tem um espaco vazio, entao sao dois espacos vazios
									if espacoVazio == 1:
										scoreP2C = scoreP2C + self.pontuacao[1]
										linha = linha + 2
									# so tem um espaco vazio	
									else:
										scoreP2C = scoreP2C + self.pontuacao[0]
										espacoVazio = 1	
										linha = linha + 2

								# tem tres pecas
								elif estados[linha+2][coluna].getDono() is self.jogador2:

									if linha+3 < len(estados):

										# tem tres pecas e a casa seguinte esta vazia	
										if estados[linha+3][coluna] == 0:
											# ja tem um espaco vazio, entao sao dois espacos vazios
											if espacoVazio == 1:
												scoreP2C = scoreP2C + self.pontuacao[3]
												linha = linha + 3
											# so tem um espaco vazio	
											else:
												scoreP2C = scoreP2C + self.pontuacao[2]
												espacoVazio = 1	
												linha = linha + 3		

										# tem quatro pecas
										elif estados[linha+3][coluna].getDono() is self.jogador2:
											
											if linha+4 < len(estados):

												# tem quatro pecas e a casa seguinte esta vazia	
												if estados[linha+4][coluna] == 0:
													# ja tem um espaco vazio, entao sao dois espacos vazios
													if espacoVazio == 1:
														scoreP2C = scoreP2C + self.pontuacao[5]
														linha = linha + 4
													# so tem um espaco vazio	
													else:
														scoreP2C = scoreP2C + self.pontuacao[4]
														espacoVazio = 1	
														linha = linha + 4
												# tem 5 pecas
												elif estados[linha+4][coluna].getDono() is self.jogador2:
													scoreP2C = scoreP2C + self.pontuacao[6]
													espacoVazio = 0
													linha = linha + 4

												# tem quatro pecas e a seguinte eh do oponente	
												elif estados[linha+4][coluna].getDono() is self.jogador1:
													espacoVazio = 0
													linha = linha + 4														

											# tem quatro pecas no canto do tabuleiro e tem um espaco vazio		
											elif espacoVazio == 1:
												scoreP2C = scoreP2C + self.pontuacao[4]
												espacoVazio = 0
												linha = linha + 4	

											# tem quatro pecas no canto do tabuleiro e nao tem espaco vazio	
											else:	
												linha = linha + 4

										# tem tres pecas e a seguinte eh do oponente			
										elif estados[linha+3][coluna].getDono() is self.jogador1:
											espacoVazio= 0 
											linha = linha + 3
										
									# tem tres pecas no canto do tabuleiro e tem um espaco vazio				
									elif espacoVazio == 1:
										scoreP2C = scoreP2C + self.pontuacao[2]
										espacoVazio = 0
										linha = linha + 3	

									# tem tres pecas no canto do tabuleiro e nao tem espaco vazio	
									else:
										linha = linha + 3

								# tem duas pecas e a peca seguinte eh do oponente						
								elif estados[linha+2][coluna].getDono() is self.jogador1:
									linha = linha + 2
									espacoVazio = 0
								
							# duas pecas no canto do tabuleiro e tem um espaco vazio					
							elif espacoVazio == 1:
								scoreP2C = scoreP2C + self.pontuacao[0]
								espacoVazio = 0
								linha = linha + 2

							# duas pecas no canto do tabuleiro e nao tem espacos vazios
							else:
								linha = linha + 2	

						# a peca seguinte eh do oponente							
						elif estados[linha+1][coluna].getDono() is self.jogador1:
							linha = linha + 1
					# ultima casa da coluna
					else:
						linha = linha + 1
											
			coluna = coluna + 1

		return scoreP1C - scoreP2C				
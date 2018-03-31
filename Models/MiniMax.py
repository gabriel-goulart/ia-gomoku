import sys 
import copy
from random import randint
from Models.Tabuleiro import Tabuleiro


class MiniMax:

	def __init__(self, jogador1, jogador2):
		self.jogador1 = jogador1
		self.jogador2 = jogador2

	# inicia os parametros usados no algoritmo
	def start(self, profundidade, tabuleiro, linha):
		self.limitLinha = linha
		self.countIteracoes = 0
		self.pontuacao = [5, 10, 5000, 10000, 5000000, 10000000, 1000000000]
		# tabuleiroCopia = Tabuleiro(15, 15)
		# tabuleiroCopia.setEstadoAtual(tabuleiro.getEstadoAtual())
		jogada = self.run(profundidade, tabuleiro, self.jogador1, -1*sys.maxsize, sys.maxsize)
		# print("Pontuacao : " + str(jogada[0]) + "Linha : " + str(jogada[1]) + "Coluna : " + str(jogada[2]))
		print(" MINIMAX - Iteracoes : " + str(self.countIteracoes))
		return jogada

	# execucao do algoritmo			
	def run(self, profundidade, tabuleiro, jogador, alpha, beta):
		proximasJogadas = tabuleiro.gerarPossiveisJogadas(self.limitLinha)
		pontuacao = 0
		jogadaLinha = -1
		jogadaColuna = -1
		self.countIteracoes = self.countIteracoes + 1
		# print(tabuleiro.getEstadoAtual())
		if(len(proximasJogadas) == 0 or profundidade == 0):
			pontuacao = self.avaliacao(tabuleiro)
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

	# realiza a avaliacao do tabuleiro
	def avaliacao(self, tabuleiro):
		# print("Executando a avaliacao")
		
		scoreAvaliacaoPorLinha = self.avaliacaoPorLinha(tabuleiro)
		scoreAvaliacaoPorColuna = self.avaliacaoPorColuna(tabuleiro)
		scoreAvaliacaoPorDiagonal = self.avaliacaoPorDiagonal(tabuleiro)
		score = scoreAvaliacaoPorLinha + scoreAvaliacaoPorColuna + scoreAvaliacaoPorDiagonal	
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
									
									scoreP1 = scoreP1 + self.pontuacao[espacoVazio]
									coluna = coluna + 2
									# so tem um espaco vazio
									if espacoVazio == 0:
										espacoVazio = 1	

								# tem tres pecas
								elif row[coluna+2].getDono() is self.jogador1:

									if coluna+3 < len(row):

										# tem tres pecas e a casa seguinte esta vazia	
										if row[coluna + 3] == 0:
											# ja tem um espaco vazio, entao sao dois espacos vazios
											coluna = coluna + 3	
											scoreP1 = scoreP1 + self.pontuacao[espacoVazio + 2]
											# so tem um espaco vazio	
											if espacoVazio == 0:
												espacoVazio = 1

										# tem quatro pecas
										elif row[coluna+3].getDono() is self.jogador1:
											
											if coluna+4 < len(row):

												# tem quatro pecas e a casa seguinte esta vazia	
												if row[coluna+4] == 0:
													# ja tem um espaco vazio, entao sao dois espacos vazios
													coluna = coluna + 4
													scoreP1 = scoreP1 + self.pontuacao[espacoVazio + 4]
													# so tem um espaco vazio	
													if espacoVazio == 0:
														espacoVazio = 1
													
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
											# soma na coluna ja foi feita na linha depois do elif
										
												

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
									# soma da coluna ja foi feita na linha depois do elif
										

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
							# soma da coluna ja feita na linha depois do elif
								

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

									scoreP2 = scoreP2 + self.pontuacao[espacoVazio]
									coluna = coluna + 2

									if espacoVazio == 0:
										espacoVazio = 1

								# tem tres pecas
								elif row[coluna+2].getDono() is self.jogador2:

									if coluna+3 < len(row):

										# tem tres pecas e a casa seguinte esta vazia	
										if row[coluna+3] == 0:
											# ja tem um espaco vazio, entao sao dois espacos vazios
											coluna = coluna + 3
											scoreP2 = scoreP2 + self.pontuacao[espacoVazio + 2]
											# so tem um espaco vazio	
											if espacoVazio == 0:
												espacoVazio = 1	

										# tem quatro pecas
										elif row[coluna+3].getDono() is self.jogador2:
											
											if coluna+4 < len(row):

												# tem quatro pecas e a casa seguinte esta vazia	
												if row[coluna+4] == 0:
													# ja tem um espaco vazio, entao sao dois espacos vazios
													coluna = coluna + 4
													scoreP2 = scoreP2 + self.pontuacao[espacoVazio + 4]
													if espacoVazio == 0:
														espacoVazio = 1	
														# so tem um espaco vazio	

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
											# soma da coluna ja feita depois do elif	

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
									# soma da coluna ja feita antes do elif

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
							# soma da coluna ja feita depois do elif

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
									scoreP1C = scoreP1C + self.pontuacao[espacoVazio]
									linha = linha + 2
									# so tem um espaco vazio	
									if espacoVazio == 0:
										espacoVazio = 1	
									
								# tem tres pecas
								elif estados[linha+2][coluna].getDono() is self.jogador1:

									if linha+3 < len(estados):

										# tem tres pecas e a casa seguinte esta vazia	
										if estados[linha+3][coluna] == 0:
											# ja tem um espaco vazio, entao sao dois espacos vazios
											scoreP1C = scoreP1C + self.pontuacao[espacoVazio + 2]
											linha = linha + 3	
											# so tem um espaco vazio	
											if espacoVazio == 0:
												espacoVazio = 1	
											
										# tem quatro pecas
										elif estados[linha+3][coluna].getDono() is self.jogador1:
											
											if linha+4 < len(estados):

												# tem quatro pecas e a casa seguinte esta vazia	
												if estados[linha+4][coluna] == 0:
													# ja tem um espaco vazio, entao sao dois espacos vazios
													scoreP1C = scoreP1C + self.pontuacao[espacoVazio + 4]
													linha = linha + 4
													# so tem um espaco vazio	
													if espacoVazio == 0:
														espacoVazio = 1	
														
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
											# soma ja feita 2 linhas acima

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
									# soma ja feita 2 linhas acima

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
							# soma ja feita 2 linhas acima

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
									scoreP2C = scoreP2C + self.pontuacao[espacoVazio + 1]
									linha = linha + 2
									# so tem um espaco vazio	
									if espacoVazio == 0:
										espacoVazio = 1	
									
								# tem tres pecas
								elif estados[linha+2][coluna].getDono() is self.jogador2:

									if linha+3 < len(estados):

										# tem tres pecas e a casa seguinte esta vazia	
										if estados[linha+3][coluna] == 0:
											# ja tem um espaco vazio, entao sao dois espacos vazios
											scoreP2C = scoreP2C + self.pontuacao[espacoVazio + 2]
											linha = linha + 3
											# so tem um espaco vazio	
											if espacoVazio == 0:
												espacoVazio = 1	
											
										# tem quatro pecas
										elif estados[linha+3][coluna].getDono() is self.jogador2:
											
											if linha+4 < len(estados):

												# tem quatro pecas e a casa seguinte esta vazia	
												if estados[linha+4][coluna] == 0:
													# ja tem um espaco vazio, entao sao dois espacos vazios
													scoreP2C = scoreP2C + self.pontuacao[espacoVazio + 4]
													linha = linha + 4
													# so tem um espaco vazio	
													if espacoVazio == 0:
														espacoVazio = 1	
													
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
											# soma ja feita 2 linhas acima

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
									# soma ja feita 2 linhas acima

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
							# soma ja feita 2 linhas acima

						# a peca seguinte eh do oponente							
						elif estados[linha+1][coluna].getDono() is self.jogador1:
							linha = linha + 1
					# ultima casa da coluna
					else:
						linha = linha + 1
											
			coluna = coluna + 1

		return scoreP1C - scoreP2C		


	# avaliando o tabuleiro pelas diagonais	
	def avaliacaoPorDiagonal(self, tabuleiro):
		linha = 0
		coluna = 4
		diagonalControle = 5
		estados = tabuleiro.getEstadoAtual()
		scoreP1D = 0
		scoreP2D = 0
		espacoVazio = 0	

		# diagonal topo-esquerda ( / )
		while diagonalControle < len(estados[0]):
			if diagonalControle > len(estados[0]):
				break
			# print("Controle diagonal : " + str(diagonalControle))	
			if estados[linha][coluna] == 0:

				if linha >= diagonalControle:
					espacoVazio = 0
					linha = 0
					coluna = diagonalControle
					diagonalControle = diagonalControle + 1
					# print("Controle Vazio diagonal : " + str(diagonalControle))
				else:
					espacoVazio = 1
					linha = linha +1
					coluna = coluna -1
				continue

			elif estados[linha][coluna].getDono() is self.jogador1:

				if linha+1 < diagonalControle and coluna -1 > 0:

					# a casa esta vazia
					if estados[linha+1][coluna-1] == 0:
						espacoVazio = 1
						linha = linha +1
						coluna = coluna -1
						continue
					# tem duas pecas em sequencia	
					elif estados[linha+1][coluna-1].getDono() is self.jogador1:

						if linha+2 < diagonalControle and coluna -2 > 0:

							if estados[linha+2][coluna-2] == 0:
								if espacoVazio == 1:
									scoreP1D = scoreP1D + self.pontuacao[1]
								else:
									scoreP1D = scoreP1D + self.pontuacao[0]

								espacoVazio = 1
								linha = linha +2
								coluna = coluna -2
								continue
							
							# tem tres pecas em sequencia
							elif estados[linha+2][coluna-2].getDono() is self.jogador1:

								if linha+3 < diagonalControle and coluna -3 > 0:

									if estados[linha+3][coluna-3] == 0:
										
										if espacoVazio == 1:											 
											scoreP1D = scoreP1D + self.pontuacao[3]
										else:
											scoreP1D = scoreP1D + self.pontuacao[2]

										espacoVazio = 1
										linha = linha +3
										coluna = coluna -3
										continue

									# tem quatro pecas em sequencia
									elif estados[linha+3][coluna-3].getDono() is self.jogador1:

										if linha+4 < diagonalControle and coluna -4 > 0:

											if estados[linha+4][coluna-4] == 0:
												if espacoVazio == 1:											 
													scoreP1D = scoreP1D + self.pontuacao[5]
												else:
													scoreP1D = scoreP1D + self.pontuacao[4]

												espacoVazio = 1
												linha = linha +4
												coluna = coluna -4
												continue

											# tem 5 pecas
											elif estados[linha+4][coluna-4].getDono() is self.jogador1:
												espacoVazio = 0
												linha = linha +4
												coluna = coluna -4
												scoreP1D = scoreP1D + self.pontuacao[6]
											else:
												if espacoVazio == 1:
													scoreP1D = scoreP1D + self.pontuacao[4]
													espacoVazio = 0
												linha = linha +4
												coluna = coluna -4	
										# fim do tabuleiro	
										else:
											if espacoVazio == 1:
												scoreP1D = scoreP1D + self.pontuacao[4]
												espacoVazio = 0
											linha = 0
											coluna = diagonalControle
											diagonalControle = diagonalControle + 1
									else:
										if espacoVazio == 1:
											scoreP1D = scoreP1D + self.pontuacao[2]
											espacoVazio = 0
										linha = linha +3
										coluna = coluna -3		
								# fim do tabuleiro	
								else:
									if espacoVazio == 1:
										scoreP1D = scoreP1D + self.pontuacao[2]
										espacoVazio = 0
									linha = 0
									coluna = diagonalControle
									diagonalControle = diagonalControle + 1

							else:
								if espacoVazio == 1:
									scoreP1D = scoreP1D + self.pontuacao[0]
									espacoVazio = 0
								linha = linha +2
								coluna = coluna -2	
						# fim do tabuleiro	
						else:
							if espacoVazio == 1:
								scoreP1D = scoreP1D + self.pontuacao[0]
								espacoVazio = 0
							linha = 0
							coluna = diagonalControle
							diagonalControle = diagonalControle + 1
					else:
						linha = linha +1
						coluna = coluna -1	

				# terminou o processamento da coluna		
				else:
					linha = 0
					coluna = diagonalControle
					diagonalControle = diagonalControle + 1	

			# peca do jogador 2		
			else:
				if linha+1 < diagonalControle and coluna -1 > 0:

					# a casa esta vazia
					if estados[linha+1][coluna-1] == 0:
						espacoVazio = 1
						linha = linha +1
						coluna = coluna -1
						continue
					# tem duas pecas em sequencia	
					elif estados[linha+1][coluna-1].getDono() is self.jogador2:

						if linha+2 < diagonalControle and coluna -2 > 0:

							if estados[linha+2][coluna-2] == 0:
								if espacoVazio == 1:
									scoreP2D = scoreP2D + self.pontuacao[1]
								else:
									scoreP2D = scoreP2D + self.pontuacao[0]

								espacoVazio = 1
								linha = linha +2
								coluna = coluna -2
								continue
							
							# tem tres pecas em sequencia
							elif estados[linha+2][coluna-2].getDono() is self.jogador2:

								if linha+3 < diagonalControle and coluna -3 > 0:

									if estados[linha+3][coluna-3] == 0:
										
										if espacoVazio == 1:											 
											scoreP2D = scoreP2D + self.pontuacao[3]
										else:
											scoreP2D = scoreP2D + self.pontuacao[2]

										espacoVazio = 1
										linha = linha +3
										coluna = coluna -3
										continue

									# tem quatro pecas em sequencia
									elif estados[linha+3][coluna-3].getDono() is self.jogador2:

										if linha+4 < diagonalControle and coluna -4 > 0:

											if estados[linha+4][coluna-4] == 0:
												if espacoVazio == 1:											 
													scoreP2D = scoreP2D + self.pontuacao[5]
												else:
													scoreP2D = scoreP2D + self.pontuacao[4]

												espacoVazio = 1
												linha = linha +4
												coluna = coluna -4
												continue

											# tem 5 pecas
											elif estados[linha+4][coluna-4].getDono() is self.jogador2:
												espacoVazio = 0
												linha = linha +4
												coluna = coluna -4
												scoreP2D = scoreP2D + self.pontuacao[6]
											else:
												if espacoVazio == 1:
													scoreP2D = scoreP2D + self.pontuacao[4]
													espacoVazio = 0
												linha = linha +4
												coluna = coluna -4	
										# fim do tabuleiro	
										else:
											if espacoVazio == 1:
												scoreP2D = scoreP2D + self.pontuacao[4]
												espacoVazio = 0
											linha = 0
											coluna = diagonalControle
											diagonalControle = diagonalControle + 1	
									else:
										if espacoVazio == 1:
											scoreP2D = scoreP2D + self.pontuacao[2]
											espacoVazio = 0
										linha = linha +3
										coluna = coluna -3		
								# fim do tabuleiro	
								else:
									if espacoVazio == 1:
										scoreP2D = scoreP2D + self.pontuacao[2]
										espacoVazio = 0
									linha = 0
									coluna = diagonalControle
									diagonalControle = diagonalControle + 1	

							else:
								if espacoVazio == 1:
									scoreP2D = scoreP2D + self.pontuacao[0]
									espacoVazio = 0
								linha = linha +2
								coluna = coluna -2	
						# fim do tabuleiro	
						else:
							if espacoVazio == 1:
								scoreP2D = scoreP2D + self.pontuacao[0]
								espacoVazio = 0
							linha = 0
							coluna = diagonalControle
							diagonalControle = diagonalControle + 1	
					else:
						linha = linha +1
						coluna = coluna -1	

				# terminou o processamento da coluna		
				else:
					linha = 0
					coluna = diagonalControle
					diagonalControle = diagonalControle + 1	


		###### diagonal topo-direita ( \ ) ##############
		linha = 0
		coluna = 10
		diagonalControle = 11
		linhaControle = 4
		espacoVazio = 0
		while diagonalControle > 0:
			
			# print("Controle diagonal : " + str(diagonalControle))	
			if estados[linha][coluna] == 0:

				if linha >= linhaControle:
					espacoVazio = 0
					linha = 0
					diagonalControle = diagonalControle - 1
					linhaControle = linhaControle +1
					coluna = diagonalControle -1
					
					# print("Controle Vazio diagonal : " + str(diagonalControle))
				else:
					espacoVazio = 1
					linha = linha +1
					coluna = coluna +1
				continue

			elif estados[linha][coluna].getDono() is self.jogador1:

				if linha+1 < linhaControle and coluna +1 < len(estados[0]):

					# a casa esta vazia
					if estados[linha+1][coluna+1] == 0:
						espacoVazio = 1
						linha = linha +1
						coluna = coluna +1
						continue
					# tem duas pecas em sequencia	
					elif estados[linha+1][coluna+1].getDono() is self.jogador1:

						if linha+2 < linhaControle and coluna +2 < len(estados[0]):

							if estados[linha+2][coluna+2] == 0:
								if espacoVazio == 1:
									scoreP1D = scoreP1D + self.pontuacao[1]
								else:
									scoreP1D = scoreP1D + self.pontuacao[0]

								espacoVazio = 1
								linha = linha +2
								coluna = coluna +2
								continue
							
							# tem tres pecas em sequencia
							elif estados[linha+2][coluna+2].getDono() is self.jogador1:

								if linha+3 < linhaControle and coluna +3 < len(estados[0]):

									if estados[linha+3][coluna+3] == 0:
										
										if espacoVazio == 1:											 
											scoreP1D = scoreP1D + self.pontuacao[3]
										else:
											scoreP1D = scoreP1D + self.pontuacao[2]

										espacoVazio = 1
										linha = linha +3
										coluna = coluna +3
										continue

									# tem quatro pecas em sequencia
									elif estados[linha+3][coluna+3].getDono() is self.jogador1:

										if linha+4 < linhaControle and coluna +4 < len(estados[0]):

											if estados[linha+4][coluna+4] == 0:
												if espacoVazio == 1:											 
													scoreP1D = scoreP1D + self.pontuacao[5]
												else:
													scoreP1D = scoreP1D + self.pontuacao[4]

												espacoVazio = 1
												linha = linha +4
												coluna = coluna +4
												continue

											# tem 5 pecas
											elif estados[linha+4][coluna+4].getDono() is self.jogador1:
												espacoVazio = 0
												linha = linha +4
												coluna = coluna +4
												scoreP1D = scoreP1D + self.pontuacao[6]
											else:
												if espacoVazio == 1:
													scoreP1D = scoreP1D + self.pontuacao[4]
													espacoVazio = 0
												linha = linha +4
												coluna = coluna +4	
										# fim do tabuleiro	
										else:
											if espacoVazio == 1:
												scoreP1D = scoreP1D + self.pontuacao[4]
												espacoVazio = 0
											linha = 0
											diagonalControle = diagonalControle - 1
											coluna = diagonalControle -1
											linhaControle = linhaControle +1
											
									else:
										if espacoVazio == 1:
											scoreP1D = scoreP1D + self.pontuacao[2]
											espacoVazio = 0
										linha = linha +3
										coluna = coluna +3		
								# fim do tabuleiro	
								else:
									if espacoVazio == 1:
										scoreP1D = scoreP1D + self.pontuacao[2]
										espacoVazio = 0
									linha = 0
									diagonalControle = diagonalControle - 1
									coluna = diagonalControle -1
									linhaControle = linhaControle +1

							else:
								if espacoVazio == 1:
									scoreP1D = scoreP1D + self.pontuacao[0]
									espacoVazio = 0
								linha = linha +2
								coluna = coluna +2	
						# fim do tabuleiro	
						else:
							if espacoVazio == 1:
								scoreP1D = scoreP1D + self.pontuacao[0]
								espacoVazio = 0
							linha = 0
							diagonalControle = diagonalControle - 1
							coluna = diagonalControle -1
							linhaControle = linhaControle +1
					else:
						linha = linha +1
						coluna = coluna +1	

				# terminou o processamento da coluna		
				else:
					linha = 0
					diagonalControle = diagonalControle - 1
					coluna = diagonalControle -1
					linhaControle = linhaControle +1

			# peca do jogador 2		
			else:
				if linha+1 < linhaControle and coluna -1 < len(estados[0]):

					# a casa esta vazia
					if estados[linha+1][coluna+1] == 0:
						espacoVazio = 1
						linha = linha +1
						coluna = coluna +1
						continue
					# tem duas pecas em sequencia	
					elif estados[linha+1][coluna+1].getDono() is self.jogador2:

						if linha+2 < linhaControle and coluna +2 < len(estados[0]):

							if estados[linha+2][coluna+2] == 0:
								if espacoVazio == 1:
									scoreP2D = scoreP2D + self.pontuacao[1]
								else:
									scoreP2D = scoreP2D + self.pontuacao[0]

								espacoVazio = 1
								linha = linha +2
								coluna = coluna +2
								continue
							
							# tem tres pecas em sequencia
							elif estados[linha+2][coluna+2].getDono() is self.jogador2:

								if linha+3 < linhaControle and coluna +3 < len(estados[0]):

									if estados[linha+3][coluna+3] == 0:
										
										if espacoVazio == 1:											 
											scoreP2D = scoreP2D + self.pontuacao[3]
										else:
											scoreP2D = scoreP2D + self.pontuacao[2]

										espacoVazio = 1
										linha = linha +3
										coluna = coluna +3
										continue

									# tem quatro pecas em sequencia
									elif estados[linha+3][coluna+3].getDono() is self.jogador2:

										if linha+4 < linhaControle and coluna +4 < len(estados[0]):

											if estados[linha+4][coluna+4] == 0:
												if espacoVazio == 1:											 
													scoreP2D = scoreP2D + self.pontuacao[5]
												else:
													scoreP2D = scoreP2D + self.pontuacao[4]

												espacoVazio = 1
												linha = linha +4
												coluna = coluna +4
												continue

											# tem 5 pecas
											elif estados[linha+4][coluna+4].getDono() is self.jogador2:
												espacoVazio = 0
												linha = linha +4
												coluna = coluna +4
												scoreP2D = scoreP2D + self.pontuacao[6]
											else:
												if espacoVazio == 1:
													scoreP2D = scoreP2D + self.pontuacao[4]
													espacoVazio = 0
												linha = linha +4
												coluna = coluna +4	
										# fim do tabuleiro	
										else:
											if espacoVazio == 1:
												scoreP2D = scoreP2D + self.pontuacao[4]
												espacoVazio = 0
											linha = 0
											diagonalControle = diagonalControle - 1
											coluna = diagonalControle -1
											linhaControle = linhaControle +1
									else:
										if espacoVazio == 1:
											scoreP2D = scoreP2D + self.pontuacao[2]
											espacoVazio = 0
										linha = linha +3
										coluna = coluna +3		
								# fim do tabuleiro	
								else:
									if espacoVazio == 1:
										scoreP2D = scoreP2D + self.pontuacao[2]
										espacoVazio = 0
									linha = 0
									diagonalControle = diagonalControle - 1
									coluna = diagonalControle -1
									linhaControle = linhaControle +1

							else:
								if espacoVazio == 1:
									scoreP2D = scoreP2D + self.pontuacao[0]
									espacoVazio = 0
								linha = linha +2
								coluna = coluna +2	
						# fim do tabuleiro	
						else:
							if espacoVazio == 1:
								scoreP2D = scoreP2D + self.pontuacao[0]
								espacoVazio = 0
							linha = 0
							diagonalControle = diagonalControle - 1
							coluna = diagonalControle -1
							linhaControle = linhaControle +1
					else:
						linha = linha +1
						coluna = coluna +1	

				# terminou o processamento da coluna		
				else:
					linha = 0
					diagonalControle = diagonalControle - 1
					coluna = diagonalControle -1
					linhaControle = linhaControle +1


		###### diagonal base-esquerda( \ ) ##############
		linha = 14
		coluna = 4
		diagonalControle = 5
		linhaControle = 10
		espacoVazio = 0	

		while diagonalControle < len(estados[0]):
			if diagonalControle > len(estados[0]):
				break
			# print("Controle diagonal : " + str(diagonalControle))	
			if estados[linha][coluna] == 0:

				if linha < linhaControle:
					espacoVazio = 0
					linha = 14
					coluna = diagonalControle
					diagonalControle = diagonalControle + 1
					# print("Controle Vazio diagonal : " + str(diagonalControle))
				else:
					espacoVazio = 1
					linha = linha -1
					coluna = coluna -1
				continue

			elif estados[linha][coluna].getDono() is self.jogador1:

				if linha-1 > linhaControle and coluna -1 > 0:

					# a casa esta vazia
					if estados[linha-1][coluna-1] == 0:
						espacoVazio = 1
						linha = linha -1
						coluna = coluna -1
						continue
					# tem duas pecas em sequencia	
					elif estados[linha-1][coluna-1].getDono() is self.jogador1:

						if linha-2 > linhaControle and coluna -2 > 0:

							if estados[linha-2][coluna-2] == 0:
								if espacoVazio == 1:
									scoreP1D = scoreP1D + self.pontuacao[1]
								else:
									scoreP1D = scoreP1D + self.pontuacao[0]

								espacoVazio = 1
								linha = linha -2
								coluna = coluna -2
								continue
							
							# tem tres pecas em sequencia
							elif estados[linha-2][coluna-2].getDono() is self.jogador1:

								if linha-3 > linhaControle and coluna -3 > 0:

									if estados[linha-3][coluna-3] == 0:
										
										if espacoVazio == 1:											 
											scoreP1D = scoreP1D + self.pontuacao[3]
										else:
											scoreP1D = scoreP1D + self.pontuacao[2]

										espacoVazio = 1
										linha = linha -3
										coluna = coluna -3
										continue

									# tem quatro pecas em sequencia
									elif estados[linha-3][coluna-3].getDono() is self.jogador1:

										if linha-4 > linhaControle and coluna -4 > 0:

											if estados[linha-4][coluna-4] == 0:
												if espacoVazio == 1:											 
													scoreP1D = scoreP1D + self.pontuacao[5]
												else:
													scoreP1D = scoreP1D + self.pontuacao[4]

												espacoVazio = 1
												linha = linha -4
												coluna = coluna -4
												continue

											# tem 5 pecas
											elif estados[linha-4][coluna-4].getDono() is self.jogador1:
												espacoVazio = 0
												linha = linha -4
												coluna = coluna -4
												scoreP1D = scoreP1D + self.pontuacao[6]
											else:
												if espacoVazio == 1:
													scoreP1D = scoreP1D + self.pontuacao[4]
													espacoVazio = 0
												linha = linha -4
												coluna = coluna -4	
										# fim do tabuleiro	
										else:
											if espacoVazio == 1:
												scoreP1D = scoreP1D + self.pontuacao[4]
												espacoVazio = 0
											linha = 14
											coluna = diagonalControle
											diagonalControle = diagonalControle + 1
									else:
										if espacoVazio == 1:
											scoreP1D = scoreP1D + self.pontuacao[2]
											espacoVazio = 0
										linha = linha -3
										coluna = coluna -3		
								# fim do tabuleiro	
								else:
									if espacoVazio == 1:
										scoreP1D = scoreP1D + self.pontuacao[2]
										espacoVazio = 0
									linha = 14
									coluna = diagonalControle
									diagonalControle = diagonalControle + 1

							else:
								if espacoVazio == 1:
									scoreP1D = scoreP1D + self.pontuacao[0]
									espacoVazio = 0
								linha = linha -2
								coluna = coluna -2	
						# fim do tabuleiro	
						else:
							if espacoVazio == 1:
								scoreP1D = scoreP1D + self.pontuacao[0]
								espacoVazio = 0
							linha = 14
							coluna = diagonalControle
							diagonalControle = diagonalControle + 1
					else:
						linha = linha -1
						coluna = coluna -1	

				# terminou o processamento da coluna		
				else:
					linha = 14
					coluna = diagonalControle
					diagonalControle = diagonalControle + 1	

			# peca do jogador 2		
			else:
				if linha-1 > linhaControle and coluna -1 > 0:

					# a casa esta vazia
					if estados[linha-1][coluna-1] == 0:
						espacoVazio = 1
						linha = linha -1
						coluna = coluna -1
						continue
					# tem duas pecas em sequencia	
					elif estados[linha-1][coluna-1].getDono() is self.jogador2:

						if linha-2 > linhaControle and coluna -2 > 0:

							if estados[linha-2][coluna-2] == 0:
								if espacoVazio == 1:
									scoreP2D = scoreP2D + self.pontuacao[1]
								else:
									scoreP2D = scoreP2D + self.pontuacao[0]

								espacoVazio = 1
								linha = linha -2
								coluna = coluna -2
								continue
							
							# tem tres pecas em sequencia
							elif estados[linha-2][coluna-2].getDono() is self.jogador2:

								if linha-3 > linhaControle and coluna -3 > 0:

									if estados[linha-3][coluna-3] == 0:
										
										if espacoVazio == 1:											 
											scoreP2D = scoreP2D + self.pontuacao[3]
										else:
											scoreP2D = scoreP2D + self.pontuacao[2]

										espacoVazio = 1
										linha = linha -3
										coluna = coluna -3
										continue

									# tem quatro pecas em sequencia
									elif estados[linha-3][coluna-3].getDono() is self.jogador2:

										if linha-4 > linhaControle and coluna -4 > 0:

											if estados[linha-4][coluna-4] == 0:
												if espacoVazio == 1:											 
													scoreP2D = scoreP2D + self.pontuacao[5]
												else:
													scoreP2D = scoreP2D + self.pontuacao[4]

												espacoVazio = 1
												linha = linha -4
												coluna = coluna -4
												continue

											# tem 5 pecas
											elif estados[linha-4][coluna-4].getDono() is self.jogador2:
												espacoVazio = 0
												linha = linha -4
												coluna = coluna -4
												scoreP2D = scoreP2D + self.pontuacao[6]
											else:
												if espacoVazio == 1:
													scoreP2D = scoreP2D + self.pontuacao[4]
													espacoVazio = 0
												linha = linha -4
												coluna = coluna -4	
										# fim do tabuleiro	
										else:
											if espacoVazio == 1:
												scoreP2D = scoreP2D + self.pontuacao[4]
												espacoVazio = 0
											linha = 14
											coluna = diagonalControle
											diagonalControle = diagonalControle + 1	
									else:
										if espacoVazio == 1:
											scoreP2D = scoreP2D + self.pontuacao[2]
											espacoVazio = 0
										linha = linha -3
										coluna = coluna -3		
								# fim do tabuleiro	
								else:
									if espacoVazio == 1:
										scoreP2D = scoreP2D + self.pontuacao[2]
										espacoVazio = 0
									linha = 14
									coluna = diagonalControle
									diagonalControle = diagonalControle + 1	

							else:
								if espacoVazio == 1:
									scoreP2D = scoreP2D + self.pontuacao[0]
									espacoVazio = 0
								linha = linha -2
								coluna = coluna -2	
						# fim do tabuleiro	
						else:
							if espacoVazio == 1:
								scoreP2D = scoreP2D + self.pontuacao[0]
								espacoVazio = 0
							linha = 14
							coluna = diagonalControle
							diagonalControle = diagonalControle + 1	
					else:
						linha = linha -1
						coluna = coluna -1	

				# terminou o processamento da coluna		
				else:
					linha = 14
					coluna = diagonalControle
					diagonalControle = diagonalControle + 1	

		
		###### diagonal base-esquerda ( / ) ##############
		linha = 14
		coluna = 10
		diagonalControle = 11
		linhaControle = 10
		espacoVazio = 0
		while diagonalControle > 0:
			
			if estados[linha][coluna] == 0:

				if linha <= linhaControle:
					espacoVazio = 0
					linha = 14
					diagonalControle = diagonalControle - 1
					linhaControle = linhaControle -1
					coluna = diagonalControle -1
					
				else:
					espacoVazio = 1
					linha = linha -1
					coluna = coluna +1
				continue

			elif estados[linha][coluna].getDono() is self.jogador1:

				if linha-1 > linhaControle and coluna +1 < len(estados[0]):

					# a casa esta vazia
					if estados[linha-1][coluna+1] == 0:
						espacoVazio = 1
						linha = linha -1
						coluna = coluna +1
						continue
					# tem duas pecas em sequencia	
					elif estados[linha-1][coluna+1].getDono() is self.jogador1:

						if linha-2 > linhaControle and coluna +2 < len(estados[0]):

							if estados[linha-2][coluna+2] == 0:
								if espacoVazio == 1:
									scoreP1D = scoreP1D + self.pontuacao[1]
								else:
									scoreP1D = scoreP1D + self.pontuacao[0]

								espacoVazio = 1
								linha = linha -2
								coluna = coluna +2
								continue
							
							# tem tres pecas em sequencia
							elif estados[linha-2][coluna+2].getDono() is self.jogador1:

								if linha-3 > linhaControle and coluna +3 < len(estados[0]):

									if estados[linha-3][coluna+3] == 0:
										
										if espacoVazio == 1:											 
											scoreP1D = scoreP1D + self.pontuacao[3]
										else:
											scoreP1D = scoreP1D + self.pontuacao[2]

										espacoVazio = 1
										linha = linha -3
										coluna = coluna +3
										continue

									# tem quatro pecas em sequencia
									elif estados[linha-3][coluna+3].getDono() is self.jogador1:

										if linha-4 > linhaControle and coluna +4 < len(estados[0]):

											if estados[linha-4][coluna+4] == 0:
												if espacoVazio == 1:											 
													scoreP1D = scoreP1D + self.pontuacao[5]
												else:
													scoreP1D = scoreP1D + self.pontuacao[4]

												espacoVazio = 1
												linha = linha -4
												coluna = coluna +4
												continue

											# tem 5 pecas
											elif estados[linha-4][coluna+4].getDono() is self.jogador1:
												espacoVazio = 0
												linha = linha -4
												coluna = coluna +4
												scoreP1D = scoreP1D + self.pontuacao[6]
											else:
												if espacoVazio == 1:
													scoreP1D = scoreP1D + self.pontuacao[4]
													espacoVazio = 0
												linha = linha -4
												coluna = coluna +4	
										# fim do tabuleiro	
										else:
											if espacoVazio == 1:
												scoreP1D = scoreP1D + self.pontuacao[4]
												espacoVazio = 0
											linha = 14
											diagonalControle = diagonalControle - 1
											coluna = diagonalControle -1
											linhaControle = linhaControle -1
											
									else:
										if espacoVazio == 1:
											scoreP1D = scoreP1D + self.pontuacao[2]
											espacoVazio = 0
										linha = linha -3
										coluna = coluna +3		
								# fim do tabuleiro	
								else:
									if espacoVazio == 1:
										scoreP1D = scoreP1D + self.pontuacao[2]
										espacoVazio = 0
									linha = 14
									diagonalControle = diagonalControle - 1
									coluna = diagonalControle -1
									linhaControle = linhaControle -1

							else:
								if espacoVazio == 1:
									scoreP1D = scoreP1D + self.pontuacao[0]
									espacoVazio = 0
								linha = linha -2
								coluna = coluna +2	
						# fim do tabuleiro	
						else:
							if espacoVazio == 1:
								scoreP1D = scoreP1D + self.pontuacao[0]
								espacoVazio = 0
							linha = 14
							diagonalControle = diagonalControle - 1
							coluna = diagonalControle -1
							linhaControle = linhaControle -1
					else:
						linha = linha -1
						coluna = coluna +1	

				# terminou o processamento da coluna		
				else:
					linha = 14
					diagonalControle = diagonalControle - 1
					coluna = diagonalControle -1
					linhaControle = linhaControle -1

			# peca do jogador 2		
			else:
				if linha-1 > linhaControle and coluna -1 < len(estados[0]):

					# a casa esta vazia
					if estados[linha-1][coluna+1] == 0:
						espacoVazio = 1
						linha = linha -1
						coluna = coluna +1
						continue
					# tem duas pecas em sequencia	
					elif estados[linha-1][coluna+1].getDono() is self.jogador2:

						if linha-2 > linhaControle and coluna +2 < len(estados[0]):

							if estados[linha-2][coluna+2] == 0:
								if espacoVazio == 1:
									scoreP2D = scoreP2D + self.pontuacao[1]
								else:
									scoreP2D = scoreP2D + self.pontuacao[0]

								espacoVazio = 1
								linha = linha -2
								coluna = coluna +2
								continue
							
							# tem tres pecas em sequencia
							elif estados[linha-2][coluna+2].getDono() is self.jogador2:

								if linha-3 > linhaControle and coluna +3 < len(estados[0]):

									if estados[linha-3][coluna+3] == 0:
										
										if espacoVazio == 1:											 
											scoreP2D = scoreP2D + self.pontuacao[3]
										else:
											scoreP2D = scoreP2D + self.pontuacao[2]

										espacoVazio = 1
										linha = linha -3
										coluna = coluna +3
										continue

									# tem quatro pecas em sequencia
									elif estados[linha-3][coluna+3].getDono() is self.jogador2:

										if linha-4 > linhaControle and coluna +4 < len(estados[0]):

											if estados[linha-4][coluna+4] == 0:
												if espacoVazio == 1:											 
													scoreP2D = scoreP2D + self.pontuacao[5]
												else:
													scoreP2D = scoreP2D + self.pontuacao[4]

												espacoVazio = 1
												linha = linha -4
												coluna = coluna +4
												continue

											# tem 5 pecas
											elif estados[linha-4][coluna+4].getDono() is self.jogador2:
												espacoVazio = 0
												linha = linha -4
												coluna = coluna +4
												scoreP2D = scoreP2D + self.pontuacao[6]
											else:
												if espacoVazio == 1:
													scoreP2D = scoreP2D + self.pontuacao[4]
													espacoVazio = 0
												linha = linha -4
												coluna = coluna +4	
										# fim do tabuleiro	
										else:
											if espacoVazio == 1:
												scoreP2D = scoreP2D + self.pontuacao[4]
												espacoVazio = 0
											linha = 14
											diagonalControle = diagonalControle - 1
											coluna = diagonalControle -1
											linhaControle = linhaControle -1
									else:
										if espacoVazio == 1:
											scoreP2D = scoreP2D + self.pontuacao[2]
											espacoVazio = 0
										linha = linha -3
										coluna = coluna +3		
								# fim do tabuleiro	
								else:
									if espacoVazio == 1:
										scoreP2D = scoreP2D + self.pontuacao[2]
										espacoVazio = 0
									linha = 14
									diagonalControle = diagonalControle - 1
									coluna = diagonalControle -1
									linhaControle = linhaControle -1

							else:
								if espacoVazio == 1:
									scoreP2D = scoreP2D + self.pontuacao[0]
									espacoVazio = 0
								linha = linha -2
								coluna = coluna +2	
						# fim do tabuleiro	
						else:
							if espacoVazio == 1:
								scoreP2D = scoreP2D + self.pontuacao[0]
								espacoVazio = 0
							linha = 14
							diagonalControle = diagonalControle - 1
							coluna = diagonalControle -1
							linhaControle = linhaControle -1
					else:
						linha = linha -1
						coluna = coluna +1	

				# terminou o processamento da coluna		
				else:
					linha = 14
					diagonalControle = diagonalControle - 1
					coluna = diagonalControle -1
					linhaControle = linhaControle -1						
		
		# print("Pontuacao p1 diagonal : " + str(scoreP1D))
		# print("Pontuacao p2 diagonal : " + str(scoreP2D))
		return scoreP1D - scoreP2D			
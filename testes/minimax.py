from functools import reduce
import random

class CPU:
    # dificuldades de jogo do bot
    DIFICULDADE_FACIL = 0
    DIFICULDADE_MEDIA = 1
    DIFICULDADE_DIFICIL = 2
    DIFICULDADE_EXTREMA = 3

    # probabilidade de cada lance dependendo da dificuldade do bot
    probabilidades = {
        DIFICULDADE_FACIL: {
            1: 20, 
            0: 20, 
            -1: 60
        },
        DIFICULDADE_MEDIA: {
            1: 55, 
            0: 20, 
            -1: 5
        },
        DIFICULDADE_DIFICIL: {
            1: 90, 
            0: 5, 
            -1: 5
        },
        DIFICULDADE_EXTREMA: {
            1: 98, 
            0: 1, 
            -1: 1
        }
    }

    def __init__(self, identificador: int, oponente: int, dificuldade = DIFICULDADE_MEDIA):
        self.identificador = identificador # identificador de qual jogador/simbolo a IA é
        self.identificador_oponente = oponente
        self.dificuldade = dificuldade
        self.print_debug = False

    def get_lances_disponiveis(self, tabuleiro):
        lances = []
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == 0:  # == 0 significa célula vazia
                    lances.append((i, j))

        return lances

    def get_score_de_fim_de_partida(self, vencedor):
        if vencedor == self.identificador:
            return +1
        if vencedor == self.identificador_oponente:
            return -1
        return 0

    def escolher_proximo_lance(self, tabuleiro):

        # salvar quais são os lances diponíveis na posição
        lances_validos = self.get_lances_disponiveis(tabuleiro)

        if len(lances_validos) == 0:
            raise ValueError("O bot não tem lances válidos na posição. Não chame-o nesses casos.")

        # calcula a pontuação de cada lance
        scores = [0] * len(lances_validos)

        for i in range(len(lances_validos)):
            lin, col = lances_validos[i]
            tabuleiro[lin][col] = self.identificador # realiza o lance do bot
            scores[i] = self.min(tabuleiro, lin, col)

            tabuleiro[lin][col] = 0 # desfaz o lance
        
        ## escolhe o lance dependendo da dificuldade do bot

        resultados = list(set(scores)) # remove os repetidos
        pesos = [CPU.probabilidades[self.dificuldade][i] for i in resultados]
        escolha = random.choices(resultados, weights=pesos)[0]
        
        # pega os lances com o mesmo score
        lances_com_score_escolhido = [lances_validos[i] for i in range(len(lances_validos)) if scores[i] == escolha]

        # escolhe um lance aleatório dentro os disponíveis
        lance_jogado = random.choice(lances_com_score_escolhido)
        
        return lance_jogado

    def min(self, tabuleiro, line, column):
        # lances da posição
        lances = self.get_lances_disponiveis(tabuleiro)

        # se a partida acabou, retorna o vencedor
        resultado = self.get_vencedor_da_posicao(tabuleiro)
        if len(lances) == 0 or resultado != 0:
            return self.get_score_de_fim_de_partida(resultado)

        # calcula a pontuação de cada lance
        scores = [0] * len(lances)

        for i in range(len(lances)):
            lin, col = lances[i]
            tabuleiro[lin][col] = self.identificador_oponente # realiza o lance do oponente
            scores[i] = self.max(tabuleiro, lin, col)

            #if scores[i] == -1: # otimização
            #    return -1       # se achou um caminho ótimo, pare a busca

            tabuleiro[lin][col] = 0 # desfaz o lance

        return min(scores)

    def max(self, tabuleiro, line, column):
        # lances da posição
        lances = self.get_lances_disponiveis(tabuleiro)

        # se a partida acabou, retorna o vencedor
        resultado = self.get_vencedor_da_posicao(tabuleiro)
        if len(lances) == 0 or resultado != 0:
            return self.get_score_de_fim_de_partida(resultado)

        # calcula a pontuação de cada lance
        scores = [0] * len(lances)

        for i in range(len(lances)):
            lin, col = lances[i]
            tabuleiro[lin][col] = self.identificador # realiza o lance do bot
            scores[i] = self.min(tabuleiro, lin, col)

            #if scores[i] == 1:  # otimização
            #    return 1        # se achou um caminho ótimo, pare a busca

            tabuleiro[lin][col] = 0 # desfaz o lance

        return max(scores)

    @staticmethod
    def get_vencedor_da_posicao(tabuleiro):
        vencedor = 0 # ninguém

        # usa o operador binário & (AND) para verificar se existe 3 símbolos iguais em sequência
        # e acumula o resultado de tudo com o operador binário | (OR)
        for i in range(3): vencedor |= reduce(lambda x, y: x & y, tabuleiro[i])
        for j in range(3): vencedor |= reduce(lambda x, y: x & y, [tabuleiro[i][j] for i in range(3)])
        vencedor |= reduce(lambda x, y: x & y, [tabuleiro[i][i] for i in range(3)])
        vencedor |= reduce(lambda x, y: x & y, [tabuleiro[i][2-i] for i in range(3)])

        return vencedor

if __name__ == '__main__':
    cpu = CPU(identificador=1, oponente=2)

    tab = [
        [1, 2, 0],
        [1, 1, 0],
        [2, 0, 2]
    ]

    print(cpu.escolher_proximo_lance(tab))
    #print(cpu.get_vencedor_da_posicao(tab))

    pass
from functools import reduce

class CPU:
    def __init__(self, identificador: int, oponente: int):
        self.identificador = identificador # identificador de qual jogador/simbolo a IA é
        self.identificador_oponente = oponente
        self.print_debug = False

    def get_lances_disponiveis(self, tabuleiro):
        lances = []
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == 0:  # 0 significa célula vazia
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
        escolha = self.get_lances_disponiveis(tabuleiro)

        if len(escolha) == 0:
            raise ValueError("O bot não tem lances na posição. Não chame-o nesses casos.")

        # calcula a pontuação de cada lance
        scores = [0] * len(escolha)

        for i in range(len(escolha)):
            lin, col = escolha[i]
            tabuleiro[lin][col] = self.identificador # realiza o lance do bot
            scores[i] = self.min(tabuleiro, lin, col)
            tabuleiro[lin][col] = 0 # desfaz o lance

        print(f'{escolha =}\n{scores =}')

        return escolha[scores.index(max(scores))]

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
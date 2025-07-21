from functools import reduce

class CPU:
    def __init__(self, identificador: int):
        self.identificador = identificador # identificador de qual jogador/simbolo a IA é
        self.print_debug = False

    def escolher_proximo_lance(self, tabuleiro):

        # salvar quais são os lances diponíveis na posição
        lances = []
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == 0: # 0 significa célula vazia
                    lances.append((i, j))

        # não há nenhum lance
        if len(lances) == 0:
            return -1, -1

        ### Algoritmo minimax

        if self.print_debug: print('\nEscolher proximo lance')
        if self.print_debug: print(f'Tabuleiro: {tabuleiro}')
        if self.print_debug: print(f'Lances: {lances}')
        scores = []
        for idx, lance in enumerate(lances):
            i, j = lance
            if self.print_debug: print(f'\nEscolher proximo lance: Fazendo o lance {lance}')
            tabuleiro[i][j] = self.identificador # faz o lance
            scores.append(self.min(lances, tabuleiro, len(lances) - 1, 1)) # calcula a pontuação (-1, 0 ou +1)
            tabuleiro[i][j] = self.identificador # desfaz o lance
            if self.print_debug: print(f'\nEscolher proximo lance: Score do lance {lance} = {scores[-1]}')

        if self.print_debug: print(f'--- Escolhendo o proximo lance')
        p = (lambda lan, scr: [f'{lan[x]}: {scr[x]}' for x in range(len(lan))])(lances, scores)
        if self.print_debug: print(f'Lances: {p}')

        res = scores.index(max(scores)) # retorna o lance com a melhor pontuação
        return lances[res]

    def min(self, lances, tabuleiro, lances_restantes, tabulacao):
        venc = self.get_vencedor_da_posicao(tabuleiro)

        if self.print_debug: print(f'\n{"  "*tabulacao}Funcao min')
        if self.print_debug: print(f'{"  "*tabulacao}Tabuleiro: {tabuleiro}')
        if self.print_debug: print(f'{"  "*tabulacao}Venc: {venc}')
        if self.print_debug: print(f'{"  "*tabulacao}Lances: {lances}, lances_restantes = {lances_restantes}')
        if venc == self.identificador: return 1 # o bot ganhou
        if venc != 0: return -1 # o outro jogador ganhou
        if lances_restantes == 0: return 0 # empatou

        scores = []
        for idx, lance in enumerate(lances):
            i, j = lance
            if tabuleiro[i][j]: # a célula está preenchida
                scores.append(100) # coloca um score pequeno para ser desconsiderado
                if self.print_debug: print(f'{"  "*tabulacao}funcao min: {lance} ocupado')
                continue
            if self.print_debug: print(f'\n{"  "*tabulacao}Função min: Fazendo o lance {lance}')
            tabuleiro[i][j] = self.identificador % 2 + 1
            scores.append(self.max(lances, tabuleiro, lances_restantes - 1, tabulacao + 1))
            tabuleiro[i][j] = 0

        if self.print_debug: print(f'{"  "*tabulacao}--- Função min | tabuleiro: {tabuleiro}')
        p = (lambda lan, scr: [f'{lan[x]}: {scr[x]}' for x in range(len(lan))])(lances, scores)
        if self.print_debug: print(f'{"  "*tabulacao}Lances: {p}')

        return min(scores)

    def max(self, lances, tabuleiro, lances_restantes, tabulacao):
        venc = self.get_vencedor_da_posicao(tabuleiro)

        if self.print_debug: print(f'\n{"  "*tabulacao}Funcao max')
        if self.print_debug: print(f'{"  "*tabulacao}Tabuleiro: {tabuleiro}')
        if self.print_debug: print(f'{"  "*tabulacao}Venc: {venc}')
        if self.print_debug: print(f'{"  "*tabulacao}Lances: {lances}, lances_restantes = {lances_restantes}')
        if venc == self.identificador: return 1  # o bot ganhou
        if venc != 0: return -1  # o outro jogador ganhou
        if lances_restantes == 0: return 0  # empatou

        scores = []
        for idx, lance in enumerate(lances):
            i, j = lance
            if tabuleiro[i][j]:  # a célula está preenchida
                scores.append(-100) # coloca um score grande para ser desconsiderado
                if self.print_debug: print(f'{"  "*tabulacao}funcao max: {lance} ocupado')
                continue
            if self.print_debug: print(f'\n{"  "*tabulacao}Função max: Fazendo o lance {lance}')
            tabuleiro[i][j] = self.identificador # faz o lance
            scores.append(self.min(lances, tabuleiro, lances_restantes - 1, tabulacao + 1)) # calcula a pontuação (-1, 0 ou +1)
            tabuleiro[i][j] = 0 # desfaz o lance

        if self.print_debug: print(f'{"  "*tabulacao}--- Função max | tabuleiro: {tabuleiro}')
        p = (lambda lan, scr: [f'{lan[x]}: {scr[x]}' for x in range(len(lan))])(lances, scores)
        if self.print_debug: print(f'{"  "*tabulacao}Lances: {p}')

        return max(scores)

    def get_vencedor_da_posicao(self, tabuleiro):
        vencedor = 0 # ninguém

        # usa o operador binário & (AND) para verificar se existe 3 símbolos iguais em sequência
        # e acumula o resultado de tudo com o operador binário | (OR)
        for i in range(3): vencedor |= reduce(lambda x, y: x & y, tabuleiro[i])
        for j in range(3): vencedor |= reduce(lambda x, y: x & y, [tabuleiro[i][j] for i in range(3)])
        vencedor |= reduce(lambda x, y: x & y, [tabuleiro[i][i] for i in range(3)])
        vencedor |= reduce(lambda x, y: x & y, [tabuleiro[i][2-i] for i in range(3)])

        return vencedor

if __name__ == '__main__':
    cpu = CPU(identificador=2)

    tab = [
        [0, 1, 1],
        [0, 0, 0],
        [0, 0, 0]
    ]

    print(cpu.escolher_proximo_lance(tab))
    #print(cpu.get_vencedor_da_posicao(tab))

    pass
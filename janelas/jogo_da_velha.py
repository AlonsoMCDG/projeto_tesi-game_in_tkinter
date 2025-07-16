import tkinter as tk
from tkinter import messagebox


class TelaJogoDaVelha(tk.Frame):
    ### Constantes
    _SEM_VENCEDOR = 0
    JOGADOR_1 = 1  # 01b
    JOGADOR_2 = 2  # 10b
    EMPATE = 4
    SIMBOLOS_JOGADORES = [' ', 'X', 'O']

    def __init__(self, master):
        super().__init__(master)
        self.janela = master
        self.config(width=700, height=500)
        self.pack(fill='both', expand=True)
        self.jogador_com_a_vez = TelaJogoDaVelha.JOGADOR_1
        self.vencedor = TelaJogoDaVelha._SEM_VENCEDOR # ninguém

        ### Frame com o nome do jogador 2 (oponente) (no topo da tela)
        # a-fazer

        ### Frame com o nome do jogador 1 (atual) (no inferior da tela)
        # a-fazer

        ### Frame com o grid 3x3 no centro
        self.frmGridJogo = FrameGridJogo(self, self)
        self.frmGridJogo.pack()

        ### Frame com opcoes de configuracao na lateral direita
        FrameConfiguracoes(self).pack()

    def passar_a_vez(self):
        # passa a vez para o proximo jogador
        if self.jogador_com_a_vez == TelaJogoDaVelha.JOGADOR_1:
            self.jogador_com_a_vez = TelaJogoDaVelha.JOGADOR_2
        else:
            self.jogador_com_a_vez = TelaJogoDaVelha.JOGADOR_1

    def jogo_rolando(self):
        return self.vencedor == TelaJogoDaVelha._SEM_VENCEDOR

    def alterar_vencedor(self, vencedor):
        self.vencedor = vencedor


class FrameGridJogo(tk.Frame):
    def __init__(self, master, controlador):
        super().__init__(master)
        print('master de grid:', self.master)
        self.controlador = controlador

        # widgets de botões do grid
        self.botoes_grid = []

        self.posicoes_grid = [[0]*3 for i in range(3)] # matriz com os símbolos em cada célula do grid

        for linha in range(3):
            for coluna in range(3):
                btn = tk.Button(self,
                                width=1,
                                height=1,
                                padx=40,
                                pady=15,
                                relief="solid",
                                font=("Arial", 40),
                                # text=f'({linha}, {coluna})',
                                )

                # definindo atributos personalizados pros botoes
                btn.posicao = (linha, coluna)  # define um atributo com a linha e coluna de onde o botao se encontra
                btn.valor_preenchido = ' '  # qual valor está preenchido no botão ('X', 'O' ou nenhum)

                btn.config(command=lambda b=btn: self.realizar_jogada(b))
                self.botoes_grid.append(btn)  # adiciona aa lista de botoes

                btn.grid(row=linha, column=coluna, sticky='nswe')  # coloca o botao no frame

    def realizar_jogada(self, btn):
        vez = self.controlador.jogador_com_a_vez
        if self.controlador.jogo_rolando() and self.celula_esta_vazia(btn):
            simbolo = TelaJogoDaVelha.SIMBOLOS_JOGADORES[vez]
            btn.config(text=simbolo)
            btn.valor_preenchido = simbolo

            linha, coluna = btn.posicao
            self.posicoes_grid[linha][coluna] = vez

            if self.checar_se_jogo_acabou():
                return

            self.controlador.passar_a_vez()

    def checar_se_jogo_acabou(self):
        #01, 10, 01
        #01, 01, 10
        #10, 01, 10

        bt = self.botoes_grid
        g = self.posicoes_grid

        ### Linhas:
        for l in range(3):
            res = g[l][0] & g[l][1] & g[l][2]

            # Checa se (e quem) venceu
            if self._ha_vencedor(res):
                self.destacar_botoes(
                    bt[self.linha_e_coluna_para_indice(l, 0)],
                    bt[self.linha_e_coluna_para_indice(l, 1)],
                    bt[self.linha_e_coluna_para_indice(l, 2)],
                )
                return True

        ### Colunas:
        for c in range(3):
            res = g[0][c] & g[1][c] & g[2][c]

            # Checa se (e quem) venceu
            if self._ha_vencedor(res):
                self.destacar_botoes(
                    bt[self.linha_e_coluna_para_indice(0, c)],
                    bt[self.linha_e_coluna_para_indice(1, c)],
                    bt[self.linha_e_coluna_para_indice(2, c)],
                )
                return True

        ### Diagonais:

        # principal
        res = g[0][0] & g[1][1] & g[2][2]
        # Checa se (e quem) venceu
        if self._ha_vencedor(res):
            self.destacar_botoes(
                bt[self.linha_e_coluna_para_indice(0, 0)],
                bt[self.linha_e_coluna_para_indice(1, 1)],
                bt[self.linha_e_coluna_para_indice(2, 2)],
            )
            return True

        # secundaria
        res = g[0][2] & g[1][1] & g[2][0]
        # Checa se (e quem) venceu
        if self._ha_vencedor(res):
            self.destacar_botoes(
                bt[self.linha_e_coluna_para_indice(0, 2)],
                bt[self.linha_e_coluna_para_indice(1, 1)],
                bt[self.linha_e_coluna_para_indice(2, 0)],
            )
            return True

        ### Empate
        soma = 0
        for i in range(3):
            for j in range(3):
                soma += g[i][j]
        if soma == 13: # todas as posicoes estao preenchidas
            print("Empate!!")
            self.controlador.alterar_vencedor(TelaJogoDaVelha.EMPATE)
            self.destacar_botoes(*bt)
            return True

        # Ninguém venceu ainda
        return False

    @staticmethod
    def linha_e_coluna_para_indice(linha, coluna, num_linhas=3, num_colunas=3):
        return linha * num_colunas + coluna

    @staticmethod
    def destacar_botoes(*botoes):
        for btn in botoes:
            btn.config(bg='red')

    def _ha_vencedor(self, validagem):
        if validagem == TelaJogoDaVelha.JOGADOR_1:
            print("Jogador 1 venceu")
            self.controlador.alterar_vencedor(TelaJogoDaVelha.JOGADOR_1)
            return True

        if validagem == TelaJogoDaVelha.JOGADOR_2:
            print("Jogador 2 venceu")
            self.controlador.alterar_vencedor(TelaJogoDaVelha.JOGADOR_2)
            return True

        return False

    @staticmethod
    def celula_esta_vazia(btn):
        return btn.valor_preenchido == ' '

class FrameConfiguracoes(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        print('master de configuracoes:', self.master)


if __name__ == '__main__':
    gui = tk.Tk()
    #gui.geometry('500x300')
    TelaJogoDaVelha(gui)

    gui.mainloop()
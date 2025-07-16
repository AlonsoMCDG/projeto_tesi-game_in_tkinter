import tkinter as tk

### Constantes
_JOGADOR_1 = 1 # 01b
_JOGADOR_2 = 2 # 10b
_SIMBOLOS_JOGADORES = [' ', 'X', 'O']

class TelaJogoDaVelha(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.janela = master
        self.config(width=700, height=500)
        self.pack(fill='both', expand=True)
        self.jogador_com_a_vez = _JOGADOR_1
        self.vencedor = 0 # ninguém

        ### Frame com o nome do jogador 2 (oponente) (no topo da tela)

        ### Frame com o nome do jogador 1 (atual) (no inferior da tela)

        ### Frame com o grid 3x3 no centro
        self.frm_grid = tk.Frame(self)
        self.frm_grid.pack()

        # Cria uma matriz 3x3 para guardar os simbolos em cada posicao do grid
        self.posicoes_grid = [[0]*3 for i in range(3)]


        # widgets de botões do grid
        self.botoes_grid = []

        for linha in range(3):
            for coluna in range(3):
                btn = tk.Button(self.frm_grid,
                                width=1,
                                height=1,
                                padx=40,
                                pady=15,
                                relief="solid",
                                font=("Arial", 40),
                                #text=f'({linha}, {coluna})',
                                )

                # definindo atributos personalizados pros botoes
                btn.posicao = (linha, coluna) # define um atributo com a linha e coluna da celula
                btn.valor_preenchido = ' ' # qual valor está preenchido no botão ('X', 'O' ou nenhum)

                btn.config(command = lambda b=btn: self.realizar_jogada(b))
                self.botoes_grid.append(btn) # adiciona aa lista de botoes

                btn.grid(row=linha, column=coluna, sticky='nswe') # coloca o botao no frame

        # Coloca os botoes no grame usando o gerenciador grid
        # for i, btn in enumerate(self.botoes_grid):
        #     linha = i // 3
        #     coluna = i % 3
        #     print(btn, btn.cget("text"))
        #
        #     btn.grid(row=linha, column=coluna, sticky='nswe')

        print(self.posicoes_grid)

        ### Frame com opcoes de configuracao na lateral direita

    def realizar_jogada(self, btn):

        if self.vencedor == 0 and btn.valor_preenchido == ' ':
            simbolo = _SIMBOLOS_JOGADORES[self.jogador_com_a_vez]
            btn.config(text=simbolo)
            btn.valor_preenchido = simbolo

            linha, coluna = btn.posicao
            self.posicoes_grid[linha][coluna] = self.jogador_com_a_vez

            if self.checar_vitoria():
                return

            # passa a vez para o proximo jogador
            if self.jogador_com_a_vez == _JOGADOR_1:
                self.jogador_com_a_vez = _JOGADOR_2
            else:
                self.jogador_com_a_vez = _JOGADOR_1




    def checar_vitoria(self):
        #01, 10, 01
        #01, 01, 10
        #10, 01, 10

        g = self.posicoes_grid
        alguem_venceu = False

        print("-----")
        print(self.posicoes_grid)
        # linhas:
        for l in range(3):
            res = g[l][0] & g[l][1] & g[l][2]

            print(f'Linha {l}: {res}')
            print(g[l][0], g[l][1], g[l][2])

            if res == _JOGADOR_1:
                print("JOgador 1 venceu")
                self.vencedor = _JOGADOR_1
                return True

            if res == _JOGADOR_2:
                print("JOgador 2 venceu")
                self.vencedor = _JOGADOR_2
                return True

        # colunas
        return False

if __name__ == '__main__':
    gui = tk.Tk()
    #gui.geometry('500x300')
    TelaJogoDaVelha(gui)

    gui.mainloop()
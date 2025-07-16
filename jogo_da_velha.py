import tkinter as tk

### Constantes
_JOGADOR_1 = 0
_JOGADOR_2 = 1
_SIMBOLOS_JOGADORES = ['X', 'O']

class TelaJogoDaVelha(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.janela = master
        self.config(width=700, height=500)
        self.pack(fill='both', expand=True)
        self.jogador_com_a_vez = _JOGADOR_1

        ### Frame com o nome do jogador 2 (oponente) (no topo da tela)

        ### Frame com o nome do jogador 1 (atual) (no inferior da tela)

        ### Frame com o grid 3x3 no centro
        self.frm_grid = tk.Frame(self)
        self.frm_grid.pack()

        # Cria uma matriz 3x3 para guardar os simbolos em cada posicao do grid
        self.posicoes_grid = [[' ']*3]*3

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

        if btn.valor_preenchido == ' ':
            simbolo = _SIMBOLOS_JOGADORES[self.jogador_com_a_vez]
            btn.config(text=simbolo)
            btn.valor_preenchido = simbolo
            self.jogador_com_a_vez = (self.jogador_com_a_vez + 1) % 2 # passa a vez para o proximo jogador



if __name__ == '__main__':
    gui = tk.Tk()
    #gui.geometry('500x300')
    TelaJogoDaVelha(gui)

    gui.mainloop()
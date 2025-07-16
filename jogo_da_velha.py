import tkinter as tk

### Constantes
_JOGADOR_1 = 0
_JOGADOR_2 = 1

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
        self.botoes_grid = [
            [
                tk.Button(self.frm_grid,
                          width=1,
                          height=1,
                          padx=40,
                          pady=40,
                          relief="solid",
                          text=f'({linha}, {coluna})')
                for coluna in range(3)
            ] for linha in range(3)
        ]

        # Coloca os botoes no grame usando o gerenciador grid
        for line, row in enumerate(self.botoes_grid):
            for column, btn in enumerate(row):
                print(btn, btn.cget("text"))
                btn.grid(row=line, column=column, sticky='nswe')

        print(self.posicoes_grid)

        # Frame com opcoes de configuracao na lateral direita


if __name__ == '__main__':
    gui = tk.Tk()
    #gui.geometry('500x300')
    TelaJogoDaVelha(gui)

    gui.mainloop()
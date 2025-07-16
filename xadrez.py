import tkinter as tk


class TelaXadrez(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.janela = master
        self.janela.geometry("750x500")

        # Frame com informações da partida e opções de configurações
        # no lado direito da tela, ocupando todo o espaço vertical
        # - Oferecer empate
        # - Desistir
        # - Mudar cor do tabuleiro
        # etc.
        self.frame_configuracoes = tk.Frame(self)
        self.frame_configuracoes.pack(side='right', fill='y', expand=True)
        tk.Label(self.frame_configuracoes,
                 text='Configurações',
                 bg='red'
                 ).pack()

        # Frame com as informações do oponente na parte superior
        self.frame_oponente = tk.Frame(self)
        self.frame_oponente.pack(side='top', fill='x', expand=True)
        tk.Label(self.frame_oponente,
                 text='Oponente',
                 bg='blue'
                 ).pack()

        # Frame com as informações do jogador na parte inferior
        self.frame_jogador = tk.Frame(self)
        self.frame_jogador.pack(side='bottom', fill='x', expand=True)
        tk.Label(self.frame_jogador,
                 text='Jogador',
                 bg='green'
                 ).pack()

        # Frame com o tabuleiro na parte esquerda
        self.frame_tabuleiro = tk.Frame(self)
        self.frame_tabuleiro.pack(fill='both', expand=True)
        tk.Label(self.frame_tabuleiro,
                 text='Tabuleiro',
                 bg='yellow'
                 ).pack()

        self.pack(fill='both', expand=True)


if __name__ == '__main__':
    gui = tk.Tk()
    TelaXadrez(gui)
    gui.mainloop()
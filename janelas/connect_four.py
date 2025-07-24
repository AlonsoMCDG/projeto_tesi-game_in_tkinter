import tkinter as tk
from functools import reduce
from tkinter import ttk
from tkinter import messagebox
from wsgiref.util import request_uri
import random


class TelaConnectFour(tk.Frame):
    ### Constantes
    SEM_VENCEDOR = 0
    JOGADOR_1 = 1  # 01b
    JOGADOR_2 = 2  # 10b
    EMPATE = 4
    SIMBOLOS_JOGADORES = [' ', 'X', 'O']
    CORES_JOGADORES = ['blue', '#ff0000', '#ffff00']

    def __init__(self, master):
        super().__init__(master)
        master.resizable(False, False)
        master.title('Connect 4')
        
        self._jogador_com_a_vez = tk.IntVar(value=TelaConnectFour.JOGADOR_1)
        self.vencedor = TelaConnectFour.SEM_VENCEDOR # ninguém
        self.vitorias = {
            TelaConnectFour.EMPATE: tk.IntVar(value=0),
            TelaConnectFour.JOGADOR_1: tk.IntVar(value=0),
            TelaConnectFour.JOGADOR_2: tk.IntVar(value=0)
        }

        ### Frame com opcoes de configuracao na lateral direita
        self.frmConfiguracoes = FrameConfiguracoes(self)
        self.frmConfiguracoes.pack(side='right', fill='both', expand=True)
        self.frmConfiguracoes.pack_propagate(False)

        ### Frame com o nome do jogador 2 (oponente) (no topo da tela)
        # a-fazer

        ### Frame com o nome do jogador 1 (atual) (no inferior da tela)
        # a-fazer

        ### Frame com o grid 3x3 no centro
        self.frmGridJogo = FrameGridJogo(self, 6, 7)
        self.frmGridJogo.pack(padx=10, pady=10, fill='both', expand=True)

    def passar_a_vez(self):
        if self._jogador_com_a_vez.get() == TelaConnectFour.JOGADOR_1:
            self._jogador_com_a_vez.set(TelaConnectFour.JOGADOR_2)
        else:
            self._jogador_com_a_vez.set(TelaConnectFour.JOGADOR_1)

    def jogo_rolando(self):
        return self.vencedor == TelaConnectFour.SEM_VENCEDOR

    def definir_vencedor(self, novo_vencedor):
        self.vencedor = novo_vencedor
    
    def finalizar_jogo(self, resultado):
        self.definir_vencedor(resultado)
        self.incrementar_vitoria_para_o_jogador(resultado)
        self.avisar_fim_de_jogo()

    def get_vencedor(self):
        return self.vencedor

    def get_jogador_com_a_vez(self):
        return self._jogador_com_a_vez.get()

    def get_vitorias_do_jogador(self, jogador):
        return self.vitorias[jogador].get()

    def set_vitorias_do_jogador(self, jogador, vitorias):
        if vitorias >= 0:
            self.vitorias[jogador].set(vitorias)

    def incrementar_vitoria_para_o_jogador(self, jogador):
        self.vitorias[jogador].set(self.vitorias[jogador].get() + 1)

    def add_trace_callback(self, callback):
        self._jogador_com_a_vez.trace_add('write', callback)

    def reiniciar_partida(self):
        self.frmGridJogo.iniciar_nova_partida()
        self._jogador_com_a_vez.set(TelaConnectFour.JOGADOR_1)
        self.vencedor = TelaConnectFour.SEM_VENCEDOR

    def avisar_fim_de_jogo(self):
        texto = ('Empate!' if self.vencedor == TelaConnectFour.EMPATE
                 else f'Jogador {self.vencedor} venceu!')
        
        print('Fim de jogo!', texto)

        messagebox.showinfo('Fim de jogo!', texto)
    
    def get_cor_jogador_com_a_vez(self):
        cor = TelaConnectFour.CORES_JOGADORES[self.get_jogador_com_a_vez()]
        return cor

class FrameGridJogo(tk.Frame):
    def __init__(self, master: TelaConnectFour, LINHAS: int, COLUNAS: int):
        super().__init__(master)
        self.controlador = master
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.LINHAS = LINHAS
        self.COLUNAS = COLUNAS

        # widgets de botões do grid
        self.botoes_grid = []

        # valores em cada posição do grid
        self.valores_grid = []

        self.iniciar_nova_partida()
    
    def zerar_valores_grid(self, linhas, colunas):
        self.valores_grid = [[0] * colunas for l in range(linhas)]

    def inserir_botoes(self, linhas, colunas):
        self.botoes_grid = [[None] * colunas for i in range(linhas)]
        for linha in range(linhas):
            for coluna in range(colunas):
                btn = tk.Button(self.frame,
                                width=1,
                                height=1,
                                padx=25,
                                pady=20,
                                relief="solid",
                                font=("Arial", 10),
                                #text=f'({linha}, {coluna})',
                                )

                btn.config(command=lambda but=btn, col=coluna: self.on_click(but, col))
                btn.bind('<Enter>', lambda event, col=coluna: self.on_enter(event, col))
                btn.bind('<Leave>', lambda event, col=coluna: self.on_leave(event, col))

                self.botoes_grid[linha][coluna] = btn  # adiciona o botão aa lista de botoes

                btn.grid(row=linha, column=coluna, sticky='nswe')  # coloca o botao no frame
    
    def on_click(self, botao_clicado, coluna):
        if self.controlador.jogo_rolando():

            # procura uma posição livre na coluna
            linha = self.get_topo_coluna(coluna)

            if linha != -1:
                self.realizar_jogada(linha, coluna)

    def realizar_jogada(self, linha, coluna):
        self.atualizar_posicao_grid(linha, coluna, self.controlador.get_jogador_com_a_vez())
        self.controlador.passar_a_vez()
        if not self.checar_condicoes_de_fim_de_jogo():
            self.on_enter(None, coluna) # atualiza a cor da célula no topo
    
    def atualizar_posicao_grid(self, linha, coluna, novo_valor):
        # define a cor da célula
        cor = self.controlador.get_cor_jogador_com_a_vez()
        self.atualizar_cor_da_celula_no_topo_da_coluna(coluna, cor)
        self.botoes_grid[linha][coluna].config(activebackground=cor)

        self.valores_grid[linha][coluna] = novo_valor

    def on_enter(self, e, coluna):
        if self.controlador.jogo_rolando():
            cor = self.controlador.get_cor_jogador_com_a_vez()
            cor = self.escurecer_cor(cor)
            linha = self.get_topo_coluna(coluna)
            if linha != -1:
                self.atualizar_cor_da_celula_no_topo_da_coluna(coluna, cor)

    def on_leave(self, e, coluna):
        if self.controlador.jogo_rolando():
            linha = self.get_topo_coluna(coluna)
            if linha != -1:
                self.atualizar_cor_da_celula_no_topo_da_coluna(coluna, '#f0f0f0')
    
    def atualizar_cor_da_celula_no_topo_da_coluna(self, coluna, nova_cor=-1):
        if nova_cor == -1: self.controlador.get_cor_jogador_com_a_vez(0) # valor padrão
        linha = self.get_topo_coluna(coluna)
        self.botoes_grid[linha][coluna].config(bg=nova_cor)
    
    # retorna a célula livre no topo da coluna
    def get_topo_coluna(self, coluna):
        linha = self.LINHAS - 1
        while linha >= 0:
            if self.valores_grid[linha][coluna] == 0:
                return linha
            linha -= 1
        return linha

    def escurecer_cor(self, cor, fator=0.6):
        return '#' + ''.join(f'{int(int(cor[i:i+2], 16) * fator):02x}' for i in (1, 3, 5))

    def checar_condicoes_de_fim_de_jogo(self):
        g = self.valores_grid # grid do jogo
        vencedor = 0 # ninguém ainda

        # checa horizontalmente
        for l in range(self.LINHAS):
            for c in range(self.COLUNAS - 3):
                seq = g[l][c] & g[l][c + 1] & g[l][c + 2] & g[l][c + 3]
                if seq != 0: # alguém fez uma sequência
                    vencedor = seq
                    break
            if vencedor != 0:
                break
        
        if vencedor == 0:
            # checa verticalmente
            for c in range(self.COLUNAS):
                for l in range(self.LINHAS - 3):
                    seq = g[l][c] & g[l + 1][c] & g[l + 2][c] & g[l + 3][c]
                    if seq != 0: # alguém fez uma sequência
                        vencedor = seq
                        break
                if vencedor != 0:
                    break
        
        if vencedor == 0:
            # checa diagonal secundária
            for l in range(3, self.LINHAS):
                for c in range(self.COLUNAS - 3):
                    seq = g[l][c] & g[l - 1][c + 1] & g[l - 2][c + 2] & g[l - 3][c + 3]
                    if seq != 0: # alguém fez uma sequência
                        vencedor = seq
                        break
                if vencedor != 0:
                    break
        
        if vencedor == 0:
            # checa diagonal principal
            for l in range(self.LINHAS - 3):
                for c in range(self.COLUNAS - 3):
                    seq = g[l][c] & g[l + 1][c + 1] & g[l + 2][c + 2] & g[l + 3][c + 3]
                    if seq != 0: # alguém fez uma sequência
                        vencedor = seq
                        break
                if vencedor != 0:
                    break
        
        if vencedor != 0:
            # alguém venceu
            self.controlador.finalizar_jogo(vencedor)
            return True
        
        ## se ninguém venceu, pode haver empate
        espacos_livres = sum([linha.count(0) for linha in self.valores_grid])

        if espacos_livres == 0:
            # empatou
            self.controlador.finalizar_jogo(TelaConnectFour.EMPATE)
            return True

        return False # o jogo não acabou

    def iniciar_nova_partida(self):
        self.inserir_botoes(self.LINHAS, self.COLUNAS)
        self.zerar_valores_grid(self.LINHAS, self.COLUNAS)

class FrameConfiguracoes(tk.Frame):
    def __init__(self, master: TelaConnectFour):
        super().__init__(master, bg='#336633', width=300)
        self.controlador = master

        # Divide a tela em 3 linhas de tamanho igual/parecido
        for i in range(3):
            self.rowconfigure(i, weight=1)
        self.columnconfigure(0, weight=1)

        ### Seção Partida

        cor_fundo = '#456456'
        frm_partida = tk.Frame(self, width=200, bg=cor_fundo)
        frm_partida.grid(row=0, column=0, sticky='nsew')#pack(fill='both', expand=True)

        tk.Label(frm_partida, text='Partida').pack(pady=5)
        ttk.Separator(frm_partida, orient='horizontal').pack(fill='x', padx=10, pady=5)

        container_vez = tk.Frame(frm_partida)
        container_vez.pack()
        self.strvar_vez_jogador = tk.StringVar(value='x')
        self.controlador.add_trace_callback(self.atualizar_label_vez_jogador)
        tk.Label(container_vez,
                 text='Vez:').pack(side='left')
        
        self.frmCorJogadorVez = f = tk.Frame(container_vez,
                 bg=self.controlador.get_cor_jogador_com_a_vez(),
                 width=30,
                 height=30
                 )
        f.pack()
        f.pack_propagate(False)

        cor_fundo = '#567567'
        frm_vitorias = tk.Frame(self, width=200, bg=cor_fundo)
        frm_vitorias.grid(row=1, column=0, sticky='nsew')

        tk.Label(frm_vitorias, text='Vitórias').pack(pady=5)
        ttk.Separator(frm_vitorias, orient='horizontal').pack(fill='x', padx=10, pady=5)

        container_vitorias = tk.Frame(frm_vitorias)
        container_vitorias.pack(fill='both', expand=True, padx=10, pady=10)

        container_vitorias.columnconfigure(0, weight=1)
        container_vitorias.columnconfigure(1, weight=1)

        tk.Label(container_vitorias, text='Jogador 1').grid(row=0, column=0)
        tk.Label(container_vitorias,
                 width=3,
                 textvariable=self.controlador.vitorias[TelaConnectFour.JOGADOR_1],
                 font=("TkDefaultFont", 50)
                 ).grid(row=1, column=0)

        tk.Label(container_vitorias, text='Jogador 2').grid(row=0, column=1)
        tk.Label(container_vitorias,
                 width=3,
                 textvariable=self.controlador.vitorias[TelaConnectFour.JOGADOR_2],
                 font=("TkDefaultFont", 50)
                 ).grid(row=1, column=1)

        ### Seção Opcoes

        cor_fundo = '#678678'
        frm_opcoes = tk.Frame(self, width=200, bg=cor_fundo)
        frm_opcoes.grid(row=2, column=0, sticky='nsew')

        tk.Label(frm_opcoes, text='Opções').pack(pady=5)
        ttk.Separator(frm_opcoes, orient='horizontal').pack(fill='x', padx=10, pady=5)

        container_opcoes = tk.Frame(frm_opcoes)
        container_opcoes.pack()

        tk.Button(container_opcoes,
                  text='Reiniciar partida',
                  command=self.controlador.reiniciar_partida
                  ).pack(ipadx=20, ipady=20)

        tk.Canvas(self, width=300, height=1).grid()

    def atualizar_label_vez_jogador(self, *args):
        vez = self.controlador.get_jogador_com_a_vez()
        simbolo = self.controlador.SIMBOLOS_JOGADORES[vez]
        self.strvar_vez_jogador.set(simbolo)

        self.frmCorJogadorVez.config(bg=self.controlador.get_cor_jogador_com_a_vez())


if __name__ == '__main__':
    gui = tk.Tk()
    gui.resizable(False, False)
    #gui.geometry('500x300')
    TelaConnectFour(gui).pack()

    gui.mainloop()
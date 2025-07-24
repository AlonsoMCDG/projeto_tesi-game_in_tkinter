import tkinter as tk
from tkinter import ttk
from classes.BaseTelaJogo import BaseTelaJogo
import random
from enum import Enum

class TelaCampoMinado(BaseTelaJogo, tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        master.title('Campo Minado')

        self.tamanho_grid = (10, 10)

        self.frmConfiguracoes = FrameConfiguracoes(self)
        self.frmConfiguracoes.pack(side='right')#, fill='both', expand=True)

        self.frmGridJogo = FrameGridJogo(self, *self.tamanho_grid, )
        self.frmGridJogo.pack()

        print('vish')
    
    def reiniciar_partida(self):
        super().reiniciar_partida()
        self.frmGridJogo.iniciar_nova_partida()


class FrameGridJogo(tk.Frame):
    def __init__(self, master: TelaCampoMinado, LINHAS: int, COLUNAS: int, largura=500, altura=500):
        super().__init__(master)
        self.controlador = master
        self.frame = tk.Frame(self)
        self.frame.pack()
        self.LINHAS = LINHAS
        self.COLUNAS = COLUNAS
        self.LARGURA = largura
        self.ALTURA = altura
        self.numero_de_minas = 8

        self.HOVER = 0
        self.cores = {
            'padrão': "#f0f0f0",
            'hover': "#98bec0",
            'escondida': "#014e96",
            'revelada': "#bbffff",
            'vazia': "#8dc2c2",
            'mina': "#ff0000",
        }

        # widgets de botões do grid
        self.botoes_grid = []

        # valores em cada posição do grid
        self.valores_grid = []

        self.iniciar_nova_partida()
    
    def zerar_valores_grid(self, linhas, colunas):
        self.valores_grid = [
            [
                {
                    'visivel': False,
                    'tem_mina': False,
                    'contador': 0
                }
                for coluna in range(colunas)
            ]
            for linha in range(linhas)
        ]

    def inserir_botoes(self, linhas, colunas):
        self.botoes_grid = [[None] * colunas for i in range(linhas)]

        altura_celula = self.ALTURA / self.LINHAS
        largura_celula = self.LARGURA / self.COLUNAS
        
        for linha in range(linhas):
            for coluna in range(colunas):
                cell = tk.Frame(self.frame,
                                name=f'{linha}:{coluna}',
                                width=altura_celula,
                                height=largura_celula,
                                bg=self.cores['escondida'],
                                highlightbackground='black',
                                highlightthickness=1,
                                )

                label = tk.Label(cell, 
                                 name=f'{linha}:{coluna}',
                                 bg=self.cores['escondida'],
                                #  text=f'{self.valores_grid[linha][coluna]['contador']}',
                                 )
                label.place(x=0, y=0, relwidth=1, relheight=1)

                cell.grid_propagate(False)
                cell.grid(row=linha, column=coluna)

                label.bind('<Enter>', lambda event, c=label: self.on_enter(event, c))
                label.bind('<Leave>', lambda event, c=label: self.on_leave(event, c))
                label.bind('<Button-1>', lambda event, c=label: self.on_click(event, c))

                self.botoes_grid[linha][coluna] = label
    
    def sortear_posicoes_minas(self):
        pos = [(lin, col) for lin in range(self.LINHAS) for col in range(self.COLUNAS)]
        com_minas = random.sample(pos, self.numero_de_minas)

        for pos in com_minas:
            l, c = pos
            self.valores_grid[l][c]['tem_mina'] = True
            self.valores_grid[l][c]['contador'] = -1

            # soma +1 para o contador de minas dos vizinhos
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= l + i < self.LINHAS and 0 <= c + j < self.COLUNAS:
                        if not self.valores_grid[l + i][c + j]['tem_mina']:
                            self.valores_grid[l + i][c + j]['contador'] += 1
        
    def on_click(self, botao_clicado, celula):
        if self.controlador.jogo_rolando():
            linha, coluna = map(int, celula.winfo_name().split(':'))
            self.realizar_jogada(linha, coluna)

    def realizar_jogada(self, linha, coluna):
        self.propagar_revelacao(linha, coluna)
        self.controlador.passar_a_vez()
        self.checar_condicoes_de_fim_de_jogo()
    
    def propagar_revelacao(self, linha, coluna):
        if 0 <= linha < self.LINHAS and 0 <= coluna < self.COLUNAS: # está dentro da tabela

            # print('revelando', linha, coluna)
            celula = self.valores_grid[linha][coluna]
            
            if celula['visivel']: # já está revelado
                return
            
            self.revelar_celula(linha, coluna)

            if not celula['tem_mina'] and celula['contador'] == 0:
                # revela os vizinhos se a célula está vazia
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        self.propagar_revelacao(linha + i, coluna + j)
    
    def revelar_celula(self, linha, coluna):
        celula = self.valores_grid[linha][coluna]
        celula['visivel'] = True
        texto = 'X' if celula['tem_mina'] else f'{celula["contador"]}'
        self.botoes_grid[linha][coluna].config(text=texto)

        cor = self.cores['vazia']
        if celula['contador'] != 0:
            cor = self.cores['revelada']
        if celula['tem_mina']:
            cor = self.cores['mina']
        
        self.botoes_grid[linha][coluna].config(bg=cor)
        
    
    def atualizar_posicao_grid(self, linha, coluna, novo_valor):
        # define a cor da célula
        cor = self.controlador.get_cor_jogador_com_a_vez()
        self.atualizar_cor_da_celula(coluna, cor)
        self.botoes_grid[linha][coluna].config(activebackground=cor)

        self.valores_grid[linha][coluna] = novo_valor

    def on_enter(self, e, celula: tk.Frame):
        if self.controlador.jogo_rolando():
            linha, coluna = map(int, celula.winfo_name().split(':'))
            if not self.valores_grid[linha][coluna]['visivel']:
                celula.config(bg=self.cores['hover'])

    def on_leave(self, e, celula):
        if self.controlador.jogo_rolando():
            linha, coluna = map(int, celula.winfo_name().split(':'))
            if not self.valores_grid[linha][coluna]['visivel']:
                celula.config(bg=self.cores['escondida'])
    
    def atualizar_cor_da_celula(self, coluna, nova_cor=-1):
        pass


    def escurecer_cor(self, cor, fator=0.6):
        return '#' + ''.join(f'{int(int(cor[i:i+2], 16) * fator):02x}' for i in (1, 3, 5))

    def checar_condicoes_de_fim_de_jogo(self):
        g = self.valores_grid # grid do jogo
        vencedor = 0 # ninguém ainda

        return False # o jogo não acabou

    def iniciar_nova_partida(self):
        self.zerar_valores_grid(self.LINHAS, self.COLUNAS)
        self.sortear_posicoes_minas()
        self.inserir_botoes(self.LINHAS, self.COLUNAS)
    
    class Estados(Enum):
        ESCONDIDO = 0
        


class FrameConfiguracoes(tk.Frame):
    def __init__(self, master: TelaCampoMinado):
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
        tk.Label(container_vez,
                 text='Vez:').pack(side='left')
        
        self.frmCorJogadorVez = f = tk.Frame(container_vez,
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
                 textvariable=self.controlador.vitorias[TelaCampoMinado.JOGADOR_1],
                 font=("TkDefaultFont", 50)
                 ).grid(row=1, column=0)

        tk.Label(container_vitorias, text='Jogador 2').grid(row=0, column=1)
        tk.Label(container_vitorias,
                 width=3,
                 textvariable=self.controlador.vitorias[TelaCampoMinado.JOGADOR_2],
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
        pass


if __name__ == '__main__':
    gui = tk.Tk()
    TelaCampoMinado(gui).pack()
    gui.mainloop()
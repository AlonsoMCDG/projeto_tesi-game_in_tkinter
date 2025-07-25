import tkinter as tk
from functools import reduce
from tkinter import ttk
from tkinter import messagebox
from wsgiref.util import request_uri
import random


class TelaJogoDaVelha(tk.Frame):
    ### Constantes
    SEM_VENCEDOR = 0
    JOGADOR_1 = 1  # 01b
    JOGADOR_2 = 2  # 10b
    EMPATE = 4
    SIMBOLOS_JOGADORES = [' ', 'X', 'O']

    def __init__(self, master):
        super().__init__(master)
        master.resizable(False, False)
        master.title('Jogo da Velha')
        self.janela = master
        self._jogador_com_a_vez = tk.IntVar(value=TelaJogoDaVelha.JOGADOR_1)
        #self.jogador_com_a_vez = TelaJogoDaVelha.JOGADOR_1
        self.vencedor = TelaJogoDaVelha.SEM_VENCEDOR # ninguém
        self.vitorias = {
            TelaJogoDaVelha.JOGADOR_1: tk.IntVar(value=0),
            TelaJogoDaVelha.JOGADOR_2: tk.IntVar(value=0)
        }
        self.CPU = CPU(identificador=self.JOGADOR_2, oponente=self.JOGADOR_1) # bot para jogar no lugar do jogador 2

        ### Frame com opcoes de configuracao na lateral direita
        self.frmConfiguracoes = FrameConfiguracoes(self)
        self.frmConfiguracoes.pack(side='right', fill='both', expand=True)
        self.frmConfiguracoes.pack_propagate(False)

        ### Frame com o nome do jogador 2 (oponente) (no topo da tela)
        # a-fazer

        ### Frame com o nome do jogador 1 (atual) (no inferior da tela)
        # a-fazer

        ### Frame com o grid 3x3 no centro
        self.frmGridJogo = FrameGridJogo(self)
        self.frmGridJogo.pack(padx=10, pady=10, fill='both', expand=True)

    def passar_a_vez(self):
        # passa a vez para o proximo jogador
        if self._jogador_com_a_vez.get() == TelaJogoDaVelha.JOGADOR_1:
            self._jogador_com_a_vez.set(TelaJogoDaVelha.JOGADOR_2)

            # se o jogo acabou, não tenta chamar o bot
            if self.vencedor != self.SEM_VENCEDOR:
                return

            tabuleiro = self.frmGridJogo.posicoes_grid.copy() # tabuleiro do jogo
            jogada = self.CPU.escolher_proximo_lance(tabuleiro) # escolhe próxima jogada
            indice_botao = self.frmGridJogo.linha_e_coluna_para_indice(jogada[0], jogada[1])
            btn = self.frmGridJogo.botoes_grid[indice_botao] # botão na posição da jogada


            self.frmGridJogo.realizar_jogada(btn) # realiza a jogada
        else:
            self._jogador_com_a_vez.set(TelaJogoDaVelha.JOGADOR_1)

    def jogo_rolando(self):
        return self.vencedor == TelaJogoDaVelha.SEM_VENCEDOR

    def alterar_vencedor(self, vencedor):
        self.vencedor = vencedor

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
        self.frmGridJogo.reiniciar_partida()
        self._jogador_com_a_vez.set(TelaJogoDaVelha.JOGADOR_1)
        self.alterar_vencedor(TelaJogoDaVelha.SEM_VENCEDOR)

class FrameGridJogo(tk.Frame):
    def __init__(self, master: TelaJogoDaVelha):
        super().__init__(master)
        print('master de grid:', self.master)
        self.controlador = master
        self.frame = tk.Frame(self)
        self.frame.pack()

        # widgets de botões do grid
        self.botoes_grid = []

        self.posicoes_grid = self.nova_matriz_de_posicoes() # matriz com os símbolos em cada célula do grid

        self.inserir_botoes()

    def inserir_botoes(self):
        self.botoes_grid = []
        for linha in range(3):
            for coluna in range(3):
                btn = tk.Button(self.frame,
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
        vez = self.controlador.get_jogador_com_a_vez()
        if self.controlador.jogo_rolando() and self.celula_esta_vazia(btn):
            simbolo = TelaJogoDaVelha.SIMBOLOS_JOGADORES[vez]
            btn.config(text=simbolo)
            btn.valor_preenchido = simbolo

            linha, coluna = btn.posicao
            self.posicoes_grid[linha][coluna] = vez

            if self.checar_se_jogo_acabou():
                if self.controlador.get_vencedor() != TelaJogoDaVelha.EMPATE:
                    self.controlador.incrementar_vitoria_para_o_jogador(self.controlador.get_vencedor())
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
            print("Fim de jogo: Empate!!")
            self.controlador.alterar_vencedor(TelaJogoDaVelha.EMPATE)
            self.destacar_botoes(*bt)
            return True

        # Ninguém venceu ainda
        return False

    def reiniciar_partida(self):
        self.inserir_botoes()
        self.posicoes_grid = self.nova_matriz_de_posicoes()

    @staticmethod
    def nova_matriz_de_posicoes():
        mat = [[0]*3 for i in range(3)]
        #print(f'Nova matriz: {mat}')
        return mat

    @staticmethod
    def linha_e_coluna_para_indice(linha, coluna, num_linhas=3, num_colunas=3):
        return linha * num_colunas + coluna

    @staticmethod
    def destacar_botoes(*botoes):
        for btn in botoes:
            btn.config(bg='red')

    def _ha_vencedor(self, validagem):
        if validagem == TelaJogoDaVelha.JOGADOR_1:
            print("Fim de jogo: Jogador 1 venceu")
            self.controlador.alterar_vencedor(TelaJogoDaVelha.JOGADOR_1)
            return True

        if validagem == TelaJogoDaVelha.JOGADOR_2:
            print("Fim de jogo: Jogador 2 venceu")
            self.controlador.alterar_vencedor(TelaJogoDaVelha.JOGADOR_2)
            return True

        return False

    @staticmethod
    def celula_esta_vazia(btn):
        return btn.valor_preenchido == ' '

class FrameConfiguracoes(tk.Frame):
    def __init__(self, master: TelaJogoDaVelha):
        super().__init__(master, bg='#336633', width=300)
        print('master de configuracoes:', self.master)
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
        tk.Label(container_vez,
                 textvariable=self.strvar_vez_jogador,
                 font=("TkDefaultFont", 50)).pack()

        ### Seção Vitorias

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
                 textvariable=self.controlador.vitorias[TelaJogoDaVelha.JOGADOR_1],
                 font=("TkDefaultFont", 50)
                 ).grid(row=1, column=0)

        tk.Label(container_vitorias, text='Jogador 2').grid(row=0, column=1)
        tk.Label(container_vitorias,
                 width=3,
                 textvariable=self.controlador.vitorias[TelaJogoDaVelha.JOGADOR_2],
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
    gui = tk.Tk()
    gui.resizable(False, False)
    #gui.geometry('500x300')
    TelaJogoDaVelha(gui).pack()

    gui.mainloop()
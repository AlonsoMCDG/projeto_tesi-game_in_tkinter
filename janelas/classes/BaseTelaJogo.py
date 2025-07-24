import tkinter as tk
from tkinter import messagebox

class BaseTelaJogo(tk.Frame):
    ### Constantes
    SEM_VENCEDOR = 0
    JOGADOR_1 = 1  # 01b
    JOGADOR_2 = 2  # 10b
    EMPATE = 4

    def __init__(self, master):
        super().__init__(master)
        master.resizable(False, False)
        self._jogador_com_a_vez = tk.IntVar(value=BaseTelaJogo.JOGADOR_1)

        self.vencedor = BaseTelaJogo.SEM_VENCEDOR
        self.vitorias = {
            BaseTelaJogo.EMPATE: tk.IntVar(value=0),
            BaseTelaJogo.JOGADOR_1: tk.IntVar(value=0),
            BaseTelaJogo.JOGADOR_2: tk.IntVar(value=0)
        }

    def passar_a_vez(self):
        if self._jogador_com_a_vez.get() == BaseTelaJogo.JOGADOR_1:
            self._jogador_com_a_vez.set(BaseTelaJogo.JOGADOR_2)
        else:
            self._jogador_com_a_vez.set(BaseTelaJogo.JOGADOR_1)

    def jogo_rolando(self):
        return self.vencedor == BaseTelaJogo.SEM_VENCEDOR

    def definir_vencedor(self, novo_vencedor):
        self.vencedor = novo_vencedor
    
    def finalizar_jogo(self, resultado):
        self.definir_vencedor(resultado)
        self.incrementar_vitoria_para_o_jogador(resultado)
        self.avisar_fim_de_jogo()
    
    def get_vencedor(self):
        return self.vencedor
    
    def alterar_vencedor(self, vencedor):
        self.vencedor = vencedor

    def get_jogador_com_a_vez(self):
        return self._jogador_com_a_vez.get()

    def get_vitorias_do_jogador(self, jogador):
        return self.vitorias[jogador].get()

    def set_vitorias_do_jogador(self, jogador, vitorias):
        if vitorias >= 0:
            self.vitorias[jogador].set(vitorias)

    def incrementar_vitoria_para_o_jogador(self, jogador):
        self.vitorias[jogador].set(self.vitorias[jogador].get() + 1)

    def avisar_fim_de_jogo(self):
        texto = ('Empate!' if self.vencedor == BaseTelaJogo.EMPATE
                 else f'Jogador {self.vencedor} venceu!')
        
        print('Fim de jogo!', texto)

        messagebox.showinfo('Fim de jogo!', texto)

    def reiniciar_partida(self):
        self._jogador_com_a_vez.set(BaseTelaJogo.JOGADOR_1)
        self.alterar_vencedor(BaseTelaJogo.SEM_VENCEDOR)
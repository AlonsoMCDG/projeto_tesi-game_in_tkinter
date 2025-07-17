import tkinter as tk

from jogo_da_velha import TelaJogoDaVelha
from letreiro import Letreiro

class Tela(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.frm_lista_de_jogos = tk.Frame(self)
        self.frm_lista_de_jogos.columnconfigure(0, weight=1)
        self.frm_lista_de_jogos.columnconfigure(1, weight=1)
        self.frm_lista_de_jogos.pack(fill='both', expand=True, padx=10)

        self.frames_jogos = [
            self.novo_frame(master=self.frm_lista_de_jogos,
                            titulo='Letreiro',
                            descricao='Teste de um letreiro',
                            jogo=Letreiro
                            ),
            self.novo_frame(master=self.frm_lista_de_jogos,
                            titulo='Jogo da Velha',
                            descricao='Jogue o jogo da velha',
                            jogo=TelaJogoDaVelha
                            )
        ]

        for i, frm in enumerate(self.frames_jogos):
            frm.grid(row=i // 2, column=i % 2, sticky='nswe')


    def novo_frame(self, master, titulo: str, descricao: str, jogo):
        frm = tk.LabelFrame(master, text=titulo)

        tk.Label(frm, text=descricao).pack()
        tk.Button(frm,
                  text='Jogar',
                  height=3,
                  width=15,
                  command=lambda tela=jogo: self.abrir_tela(jogo, titulo)
                  ).pack()

        return frm

    def abrir_tela(self, alvo, titulo):
        tela = tk.Toplevel(self)
        tela.title(titulo)
        alvo(tela).pack()

        pass

if __name__ == '__main__':
    gui = tk.Tk()
    gui.geometry('600x500')
    gui.title("Central de Jogos")
    gui.resizable(False, False)
    
    Tela(gui).pack(fill='both', expand=True)
    gui.mainloop()
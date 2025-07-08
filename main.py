import tkinter as tk


class Tela:
    def __init__(self, master):
        self.janela = master
        self.janela.geometry("750x500")

        self.animation_string = """CADÊ O PIX? """
        self.canvas_animation_active = True
        self.animation_visible_chars_length = 30 # Quantos caracteres são visíveis na animação
        self.animation_index = 0 # Qual é o caractere inicial atual

        # TextWidget com função de "Canvas" para guardar a animação
        self.txt_canvas = tk.Text(self.janela,
                                  height=1,
                                  width=self.animation_visible_chars_length,
                                  font=("Courier New", 150),
                                  relief="flat",
                                  state="disabled")
        self.txt_canvas.pack()

        # Botão de animação
        self.lbl_btn_animacao = tk.StringVar()
        self.lbl_btn_animacao.set(f'{"Desativar" if self.canvas_animation_active else "Ativar"} animação')
        self.btn_animacao = tk.Button(self.janela,
                                      textvariable=self.lbl_btn_animacao,
                                      command=self.mudar_status_animacao)
        self.btn_animacao.pack()

        self.animar_canvas() # Inicia a animação do letreiro

    def mudar_status_animacao(self):
        self.canvas_animation_active = not self.canvas_animation_active # Ativa ou Desativa a animação
        self.animar_canvas() # Chama a função de animação

        # Atualiza a label do botão de ativar/desativar animação
        self.lbl_btn_animacao.set(f'{"Desativar" if self.canvas_animation_active else "Ativar"} animação')

    def animar_canvas(self):
        if self.canvas_animation_active:
            len_anim_string = len(self.animation_string)
            visible_chars = self.animation_visible_chars_length
            loops = max(0, (self.animation_index + visible_chars) // len_anim_string - 1)
            end_index = (self.animation_index + visible_chars) % len_anim_string

            after = self.animation_string[self.animation_index: min(self.animation_index + visible_chars, len(self.animation_string))]
            before = self.animation_string[:end_index]

            # A]B[CD
            texto = after + (self.animation_string * loops) + before

            #texto += f"\n\nloops: {loops}\nafter: {after}\nbefore: {before}\nlen_texto: {len(texto)}"

            self.txt_canvas.config(state="normal")
            self.txt_canvas.delete("1.0", tk.END)
            self.txt_canvas.insert(tk.END, texto)
            self.txt_canvas.config(state="disabled")

            self.animation_index = (self.animation_index + 1) % len(self.animation_string)

            self.janela.after(500, self.animar_canvas)

gui = tk.Tk()
Tela(gui)
gui.mainloop()
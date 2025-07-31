import tkinter as tk
import random
import math

class TelaSlotMachine(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#d7da32")
        self.master.geometry("500x480")
        self.master.config(bg="#1C1031")

        self.frm_visores = tk.Frame(self, bg='#abad29')
        self.frm_visores.pack()
        self.visores = [
            FrameVisorMachine(self.frm_visores, 
                              controle = self, 
                              numero_de_slots=4, 
                              figuras=['7', 'laranja', 'limão', 'cereja', 'diamante', 'dado', 'estrela'], 
                              cores=['#FF0000', '#00E1FF', '#0077FF', '#1CFF1C', "#DDFF1C", "#FF1CF4", "#1CFFCA"],
                              cor_inicial=i, 
                              )
            for i in range(3)
        ]

        for v in self.visores:
            v.pack(side='left', pady=15)

        self.simbolos_selecionados = 0
        self.simbolos_necessarios = 3

        self.alavanca = tk.Button(self, 
                                  text="Girar", 
                                  bg="#3FFF2E",
                                  command=self.rodar_maquina,
                                  )
        self.alavanca.pack(pady=20, ipadx=60, ipady=30)
    
    def rodar_maquina(self):
        for v in self.visores:
            v.iniciar_animacao()
        # print(self.winfo_width(), self.winfo_height())
    
    def rotina_fim_de_jogo(self):
        self.simbolos_selecionados += 1

        if self.simbolos_selecionados < self.simbolos_necessarios:
            return
        
        simbolos = [
            slot.get_figura_slot_central()[0]
            for slot in self.visores
        ]
        
        print('resultado:', simbolos)

        self.simbolos_selecionados = 0
            

class FrameVisorMachine(tk.Frame):
    # Constantes de acesso
    X = 0
    Y = 1
    
    def __init__(self, master, controle, largura=100, altura=300, cor_inicial=0, numero_de_slots=1, figuras=['7'], cores=['blue']):
        super().__init__(master)

        # Clase controle do jogo
        self.controle = controle
        
        ### Elemento canvas onde as imagens serão desenhadas
        self.canvas = tk.Canvas(self, width=largura, height=altura)
        self.canvas_largura = largura
        self.canvas_altura = altura
        self.canvas.pack()
        
        ### Dimensões dos slots
        self.slots_config = {
            'padx': 5,
            'pady': 20,
            'altura': 90,
            'largura': 90
        }

        if numero_de_slots < 1:
            numero_de_slots = 1
        
        num_min_slots_para_ocupar_o_canvas = (altura // (self.slots_config['altura'] + self.slots_config['pady'])) + 2 # (+ 2 extras)
        repeticoes =  max(numero_de_slots, num_min_slots_para_ocupar_o_canvas // numero_de_slots)
        
        ### Número/quantidade de figuras no slot
        self.numero_de_slots = numero_de_slots * repeticoes
        self.cores = cores[:numero_de_slots]
        self.figuras = figuras

        ### Variáveis de animação

        # Velocidade
        self.velocidade_y_maxima = 100
        self.velocidade_y_atual = 0
        self.fator_desaceleracao = 1

        # Controle do estado de animação
        self.animando = True

        self.espaco_ocupado_pelas_figuras = (self.slots_config['altura'] +
                                              self.slots_config['pady']) * self.numero_de_slots

        self.indice_slot_central = self.numero_de_slots // 2
        
        # posição inicial do slot central
        y_inicial = (altura - self.slots_config['altura']) / 2
        x_inicial = (largura - self.slots_config['largura']) / 2

        # posição vertical do slot central
        self.y_slot_central = y_inicial

        espaco_de_um_slot = self.slots_config['altura'] + self.slots_config['pady']

        # limite inferior onde as figuras estão limitadas
        y_minimo = y_inicial - espaco_de_um_slot * self.indice_slot_central
        self.y_minimo = y_minimo
        
        # limite inferior onde as figuras estão limitadas
        y_maximo = y_inicial + espaco_de_um_slot * (self.numero_de_slots - self.indice_slot_central)
        self.y_maximo = y_maximo
        
        
        ### Objetos dos slots

        self.coords_slots = [
            [x_inicial,                         # x
             y_minimo + espaco_de_um_slot * i]  # y
            for i in range(self.numero_de_slots)
        ]

        self.slots = [
            (lambda pos, i:
                # retorna um retângulo
                self.canvas.create_rectangle(pos[0],                                # x0
                                             pos[1],                                # y0
                                             pos[0] + self.slots_config['largura'], # x1
                                             pos[1] + self.slots_config['altura'],  # y1
                                             fill=self.cores[(cor_inicial + i) % numero_de_slots],      # cor
                                             tags=(self.figuras[(cor_inicial + i) % numero_de_slots],   # simbolo
                                                   f'slot_{i}'
                                                   )
                                             )
            )(self.coords_slots[i], i) # passa as coordenadas do slot
            for i in range(self.numero_de_slots)
        ]

        # self.iniciar_animacao()
    
    def iniciar_animacao(self):
        self.velocidade_y_atual = random.uniform(20, 220)
        self.fator_desaceleracao = 1
        self.animando = True

        self.animar()
    
    def animar(self):
        if self.animando:
            # Espaço total ocupado pelas figuras
            intervalo = self.y_maximo - self.y_minimo

            # Move cada slot
            for i in range(self.numero_de_slots):
                y_inicial = self.coords_slots[i][self.Y]

                deslocamento = (y_inicial + self.velocidade_y_atual - self.y_minimo) % intervalo
                y_fim = self.y_minimo + deslocamento

                # somar deslocamento
                novo_y = y_fim

                # define nova posição
                self.coords_slots[i][self.Y] = novo_y

                delta = y_fim - y_inicial

                # move o retangulo para a nova posição
                self.canvas.move(self.slots[i], 0, delta)
            
            # desacelera um pouco devido ao "atrito"
            if self.fator_desaceleracao > 0.01:
                self.fator_desaceleracao = self.velocidade_y_atual / 100
            self.velocidade_y_atual -= self.fator_desaceleracao

            if self.velocidade_y_atual < 3 and self.fator_desaceleracao > 0.4:
                self.fator_desaceleracao /= 2

            # Slot parou de rodar
            if self.velocidade_y_atual < 0:
                self.velocidade_y_atual = 0
                self.animando = False
                self.centralizar_slots()
                self.controle.rotina_fim_de_jogo()
            else:
                self.after(20, self.animar)
        else:
            # print('nao animando')
            pass
    
    def centralizar_slots(self):
        slot_mais_perto = -1
        menor_distancia = 999999999
        alvo = self.y_slot_central

        for i in range(self.numero_de_slots):
            distancia_ate_centro = math.fabs(alvo - self.coords_slots[i][self.Y])

            # atualiza o slot com a menor distância até o centro
            if distancia_ate_centro <= menor_distancia:
                menor_distancia = distancia_ate_centro
                slot_mais_perto = i
        
        deslocamento = alvo - self.coords_slots[slot_mais_perto][self.Y]

        # desloca todos os slots até alinhar o slot central
        for i, slot in enumerate(self.slots):
            self.coords_slots[i][self.Y] += deslocamento
            self.canvas.move(slot, 0, deslocamento)
    
    def get_id_slot_central(self):
        x = self.canvas.winfo_width() / 2
        y = self.canvas.winfo_height() / 2
        slot_central = self.canvas.find_closest(x, y)
        return slot_central
    
    def get_figura_slot_central(self):
        item = self.get_id_slot_central()
        tags = self.canvas.gettags(item)

        return tags

if __name__ == '__main__':
    gui = tk.Tk()
    TelaSlotMachine(gui).pack(ipadx=10, ipady=10)
    gui.mainloop()
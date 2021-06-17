import pygame
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                             K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_m, K_n, K_b,
                           K_ESCAPE, K_UP, K_DOWN, K_RCTRL, K_LCTRL,
                           K_SPACE, K_w, K_s, K_a, K_d, # Para o jogo funcionar com o w, a, s, d e espaço
                           K_p # Pause no botão p (ou esc)
                           )
from fundo import Fundo
from elementos import ElementoSprite
import random

from time import time
from time import sleep
import os

class Jogo:
    def __init__(self, size=(1000, 1000), fullscreen=False):
        self.elementos = {}
        pygame.init()
        self.tela = pygame.display.set_mode(size, FULLSCREEN) # Rodar em fullscreen
        self.fundo = Fundo()
        self.jogador = None
        
        self.nivel = 0
        flags = DOUBLEBUF
        if fullscreen:
            flags |= FULLSCREEN

        self.screen_size = self.tela.get_size()
        pygame.mouse.set_visible(0)
        pygame.display.set_caption('Baby Shooter')
        self.run = True
        
        self.fonte = pygame.font.Font("freesansbold.ttf", 32) # Define fonte
        
        # Define os textos do placar
        self.texto_vidas = self.fonte.render("Vidas: ", True, (0,0,0), (88,198,247))
        self.texto_pontos = self.fonte.render("Pontos: ", True, (0,0,0), (88,198,247))
        self.texto_nivel = self.fonte.render("Nível: ", True, (0,0,0), (88,198,247))
        
        # Define os "retângulos" do placar
        self.texto_vidas_rect = self.texto_vidas.get_rect()
        self.texto_pontos_rect = self.texto_vidas.get_rect()
        self.texto_nivel_rect = self.texto_vidas.get_rect()
        
        # Define a posição do placar
        self.texto_vidas_rect.center = (100,30)
        self.texto_pontos_rect.center = (100,64)
        self.texto_nivel_rect.center = (100,98)
        
        # Define a tela
        self.screen = pygame.display.get_surface()
        
        # Quantidade máima de vírus na tela
        self.quantidade_de_virus = 15
        
        # Diferença de xp entre os níveis
        self.xp_anterior = 0
        
        #Música
        pygame.mixer.music.load('Bebe.mp3') # Carrega e guarda a música que será tocada durante o jogo.
        pygame.mixer.music.play(-1) # Faz com que a música entre em loop.
        self.music = True # Faz com que a música comece a tocar
        
        #Sons
        self.derrota = pygame.mixer.Sound('Choro_do_Fim.mp3') # Som feito quando o bebê perde.        
        
    def manutencao(self):
        r = random.randint(0, self.quantidade_de_virus)
        x = random.randint(1, self.screen_size[0])
        virii = self.elementos["virii"]
        if r > (len(virii)):
            if self.nivel > 0:
                
                tipo_virus = 8 + (self.nivel * 2) # Difine um range para nascerem virus diferentes a cada nível
                if tipo_virus > 15: # Limita o range
                    tipo_virus = 15
                    
                nivel_virus = random.randint(0, tipo_virus) # Cria um range para os vírus nascerem de acordo com uma proporção pré estabelecida
                
                if nivel_virus > 13:
                    enemy = Virus([0, 0], lives = 100, speed=[0, random.randint(5,7)], image="brocolis.png")
                    size = enemy.get_size()
                    enemy.set_pos([self.jogador.get_pos()[0], 0])
                
                elif nivel_virus > 7:
                    enemy = Virus([0, 0], lives = 3, speed=[random.randint(-1,1), random.randint(3,5)], image="cenoura2.png") 
                    size = enemy.get_size()
                    enemy.set_pos([min(max(x, size[0]/2), self.screen_size[0]-size[0]/2), 0])
                
                else:
                    enemy = Virus([0, 0], speed=[random.randint(-1,1), random.randint(2,4)]) 
                    size = enemy.get_size()
                    enemy.set_pos([min(max(x, size[0]/2), self.screen_size[0]-size[0]/2), 0])
            
            else:
                enemy = Virus([0, 0])
                size = enemy.get_size()
                enemy.set_pos([min(max(x, size[0]/2), self.screen_size[0]-size[0]/2), 0])
            mesmo_lugar = pygame.sprite.spritecollide(enemy, virii, False)
            if mesmo_lugar: # Se os virus foram nascer sobrepostos, o vírus não nasce
                return
            self.elementos["virii"].add(enemy)
        
    def gera_powerup(self): # Gera um powerup novo
        pw_up = Powerup([0, 0], speed=[random.randint(-1,1), random.randint(3,5)]) # Cria o powerup, com velocidade (angulo) aleatória num certo range
        size = pw_up.get_size() # Define size igual ao tamanho do powerup
        x = random.randint(1, self.screen_size[0]) # Posição aleatoria para o powerup "nascer"
        pw_up.set_pos([min(max(x, size[0]/2), self.screen_size[0]-size[0]/2), 0]) # Define a posição do powerup, mas não deixa ele nascer fora da tela
        self.elementos["powerup"].add(pw_up) # Adiciona o powerup (sprite)

    def muda_nivel(self):
        # Verifica o xp
        xp = self.jogador.get_pontos()
        # Verifica se deve mudar o nível pra 1
        if xp >= 10 and self.nivel == 0:
            # Altera o fundo
            self.fundo = Fundo("azulejo.png")
            # Altera o nível
            self.nivel = 1
            # Adiciona mais vidas para o jogador
            self.jogador.set_lives(self.jogador.get_lives() + 3)
            self.gera_powerup() # Manda gera o powerup
            
        elif xp >= 50 and self.nivel == 1:
            self.fundo = Fundo("quadrados.png")
            self.nivel = 2
            self.jogador.set_lives(self.jogador.get_lives() + 6)
            self.xp_anterior = xp
            self.gera_powerup() # Manda gera o powerup
            
        elif (xp - self.xp_anterior) >= 50: # Confere a diferença do xp atual pra ultima troca de nível
            fundos = random.choice(["azulejo.png","quadrados.png","madeira.png"]) # Atualiza o fundo aleatóriamenta da fase 4 em diante
            self.fundo = Fundo(fundos)
            self.xp_anterior = xp
            self.nivel += 1
            self.quantidade_de_virus += 2 # Quantidade de vírus a mais que nasce a cada nível
            self.gera_powerup() # Manda gera o powerup
            
    def atualiza_elementos(self, dt):
        self.fundo.update(dt)
        for v in self.elementos.values():
            v.update(dt)

    def desenha_elementos(self):
        self.fundo.draw(self.tela)
        for v in self.elementos.values():
            v.draw(self.tela)
    
    def placar(self):
        # Gera os textos do placar
        self.texto_vidas = self.fonte.render(f"Vidas: {self.jogador.get_lives()}", True, (0,0,0), (88,198,247))
        self.texto_pontos = self.fonte.render(f"Pontos: {self.jogador.get_pontos()}", True, (0,0,0), (88,198,247))
        self.texto_nivel = self.fonte.render(f"Nível: {self.nivel}", True, (0,0,0), (88,198,247))
        # Desenha o placar
        self.screen.blit(self.texto_vidas, self.texto_vidas_rect)
        self.screen.blit(self.texto_pontos, self.texto_pontos_rect)
        self.screen.blit(self.texto_nivel, self.texto_nivel_rect)
        
    def verifica_impactos(self, elemento, list, action, powerup = 0):
        if (powerup == 1 and # Se tiver comparando colisão de powerup e...
            #isinstance(elemento, pygame.sprite.Sprite) and # Se o powerup for um sprite e...
            pygame.sprite.spritecollide(elemento, list, 1)): # Se o jogador e o powerup tiverem colidido
            poder = random.randint(1,3) # Randomiza o poder do powerup
            if poder == 1: # Se o tipo de powerup for 1
                self.jogador.set_lives(self.jogador.get_lives() + 1) # Aumenta uma vida do jogador
            elif poder >= 2: # Se o tipo de powerup for 2
                self.jogador.aumenta_tipo_arma() # Aumenta o tipo da arma
            return elemento.morto # Elimina o sprite do powerup
        
        else: # Se não for colisão de powerup, verifica as outras colisões
            if isinstance(elemento, pygame.sprite.RenderPlain):
                hitted = pygame.sprite.groupcollide(elemento, list, 1, 0)
                for v in hitted.values():
                    for o in v:
                        action(o)
                return hitted
    
            elif isinstance(elemento, pygame.sprite.Sprite):
                if pygame.sprite.spritecollide(elemento, list, 1):
                    action()
                return elemento.morto

    def acao_elemento(self):
        self.verifica_impactos(self.jogador, self.elementos["tiros_inimigo"],
                               self.jogador.alvejado)
        if self.jogador.morto:
            pygame.mixer.Sound.play(self.derrota) # Som emitido quando o bebê perde
            sleep(2)
            self.run = False
            return

        # Verifica se o personagem trombou em algum inimigo
        self.verifica_impactos(self.jogador, self.elementos["virii"],
                               self.jogador.colisao)
        if self.jogador.morto:
            pygame.mixer.Sound.play(self.derrota) # Som emitido quando o bebê perde.
            sleep(2)
            self.run = False
            return
        
        # Verifica se o personagem atingiu algum alvo.
        hitted = self.verifica_impactos(self.elementos["tiros"],
                                        self.elementos["virii"],
                                        Virus.alvejado)
        if hitted:
            som_de_colisao = pygame.mixer.Sound('Colisão_Lego_Comida.mp3') # Som feito quando uma legume colide com um brinquedo.
            som_de_colisao.play() # Ativa o som no momento do impacto.

        # Aumenta a pontos baseado no número de acertos:
        self.jogador.set_pontos(self.jogador.get_pontos() + len(hitted))
        
        # Verifica se o personagem trombou em algum powerup
        self.verifica_impactos(self.jogador, self.elementos["powerup"],
                               self.jogador.colisao, 1)

    def liga_desliga_musica(self):
        if self.music:
            pygame.mixer.music.pause() # Faz com que a música pare de tocar.
            self.music = False
        else:
            pygame.mixer.music.unpause() # Faz com que a música volte a tocar.
            self.music = True
        
    def ajusta_volume(self, av): # Controla o volume da música. av significa ajusta volume.
        volume = pygame.mixer.music.get_volume()
        volume += av
        if volume >=1:
            volume = 1
        pygame.mixer.music.set_volume(volume)

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False # Finaliza o jogo

        if event.type == KEYDOWN: # Verifica se foi pressionada uma tecla
            key = event.key
            if key in (K_LCTRL, K_RCTRL, K_SPACE):
                self.jogador.deve_atirar = 1 # Deve atirar
            elif key in (K_UP, K_w): # Agora funciona tanto na seta para cima quanto no w
                self.jogador.accel_top()
            elif key in (K_DOWN, K_s): # Agora funciona tanto na seta para baixo quanto no s
                self.jogador.accel_bottom()
            elif key in (K_RIGHT, K_d): # Agora funciona tanto na seta para a direita quanto no d
                self.jogador.accel_right()
            elif key in (K_LEFT, K_a): # Agora funciona tanto na seta para a esqueda quanto no a
                self.jogador.accel_left()
            elif key == K_m:
                self.liga_desliga_musica()
            elif key == K_b:
                self.ajusta_volume(-0.1)
            elif key == K_n:
                self.ajusta_volume(0.1)
                
        if event.type == KEYUP: # Verifica se a tecla foi solta
            key = event.key
            if key in (K_ESCAPE, K_p):
                self.inicio_pausa_fim(1) # Vai para a tela de pausa
            elif key in (K_LCTRL, K_RCTRL, K_SPACE):
                self.jogador.deve_atirar = 0 # Não deve atirar
            elif key in (K_UP, K_w):
                self.jogador.set_speed((self.jogador.get_speed()[0],0)) # A velocidade no eixo y zera
            elif key in (K_DOWN, K_s):
                self.jogador.set_speed((self.jogador.get_speed()[0],0)) # A velocidade no eixo y zera
            elif key in (K_RIGHT, K_d):
                self.jogador.set_speed((0,self.jogador.get_speed()[1])) # A velocidade no eixo x zera
            elif key in (K_LEFT, K_a):
                self.jogador.set_speed((0,self.jogador.get_speed()[1])) # A velocidade no eixo x zera
    
                
            
        self.jogador.atira(self.elementos["tiros"]) # Pede par atirar (mas atira somente se o deve_atirar for igual a 1)
    
    def inicio_pausa_fim(self, tela = 0): # Função das telas de inicio, pausa e game over
        
        if tela == 0: # Tela de inicio
            iniciar = Fundo("tela_inicio.png") # Define a imagem de fundo
            iniciar.draw(self.tela) # Desenha a tela com o fundo
            pygame.display.flip() # Renderiza a imagem
            while True: # Espera a ação do jogador
                event = pygame.event.poll() # Ultima ação (pressionar ou soltar botões)
                if event.type == KEYDOWN: # Se o botão for pressionado
                    key = event.key # Qual botão foi pressionado
                    if key == K_SPACE: # Se o botão pressionado for o espaço
                        break # Encerra o laço e inicia o jogo
            
        
        elif tela == 1: # Tela de pausa
            # Funcionalidade análogas a tela de início    
            pausa = Fundo("tela_pausa.png")
            pausa.draw(self.tela)
            pygame.display.flip()
            while True:
                event = pygame.event.poll()
                if event.type == KEYDOWN:
                    key = event.key
                    if key == K_SPACE: # Se o botão pressionado for espaço
                        break # Encerra o laço e retorna ao jogo
                    elif key in (K_ESCAPE, K_p): # Se o botão pressionado for esc ou p
                        self.run = False # Encerra o loop principal do Jogo()
                        self.sair_pela_pausa = True # Finaliza o jogo diretamente
                        break # Encerra o laço e sai totalmente do jogo
        
        elif tela == 2: # Tela de game over
            game_over = Fundo("tela_game_over.png")
            game_over.draw(self.tela)
            pygame.display.flip()
            while True:
                event = pygame.event.poll()
                if event.type == KEYDOWN:
                    key = event.key
                    if key == K_SPACE: # Se o botão pressionado for espaço
                        return True # Encerra o laço e reinicia o jogo
                    elif key in (K_ESCAPE, K_p): # Se o botão pressionado for esc ou p
                        return False # Encerra o laço e sai totalmente do jogo
         
            

    def loop(self):
        # Foi necessário colocar a definição de algumas variáveis do init aqui novamente, para funcionar o "jogar novamente"
        clock = pygame.time.Clock()
        dt = 16
        self.nivel = 0
        self.fundo = Fundo()
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador([200, 400], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain()
        self.elementos['powerup'] = pygame.sprite.RenderPlain() # Cria a chave "powerup" no dicionário
        self.inicio_pausa_fim(0) # Vai para a tela de inicio
        self.run = True # Define o jogo rodando
        self.sair_pela_pausa = False # Verifica se o jogador quer sair do jogo a partir da tela de pausa
        while self.run:
            clock.tick(1000 / dt)

            self.trata_eventos()
            self.acao_elemento()
            self.manutencao()
            
            # Atualiza Elementos
            self.atualiza_elementos(dt)
            
            # Muda o nível
            self.muda_nivel()
            
            # Desenhe no back buffer
            self.desenha_elementos()
            
            # Desenhar placar
            self.placar()
            
            pygame.display.flip()
        if self.sair_pela_pausa:
            return False
        else: 
            return self.inicio_pausa_fim(2) # Vai para a tela de game over

class Nave(ElementoSprite):
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[100, 180]):
        self.acceleration = [5, 5]
        if not image:
            image = "bebe.png"
        super().__init__(image, position, speed, new_size)
        self.set_lives(lives)
        self.limite = 10

    def get_lives(self):   
        return self.lives

    def set_lives(self, lives):
        self.lives = lives

    def colisao(self):
        self.set_lives(self.get_lives() - 1)
        if self.get_lives() <= 0:
            self.kill()

    def atira(self, lista_de_tiros, image=None):
        s = list(self.get_speed())
        s[1] *= 2
        Tiro(self.get_pos(), s, image, lista_de_tiros)

    def alvejado(self):
        self.set_lives(self.get_lives() - 1)
        if self.get_lives() <= 0:
            self.kill()
        
            

    @property
    def morto(self):
        return self.get_lives() == 0

    def accel_top(self):
        speed = self.get_speed()
        if speed[1] - self.acceleration[1] > -self.limite:
            self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def accel_bottom(self):
        speed = self.get_speed()
        if speed[1] + self.acceleration[1] < self.limite:
            self.set_speed((speed[0], speed[1] + self.acceleration[1]))

    def accel_left(self):
        speed = self.get_speed()
        if speed[0] - self.acceleration[0] > -self.limite:
            self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        speed = self.get_speed()
        if speed[0] + self.acceleration[0] < self.limite:
            self.set_speed((speed[0] + self.acceleration[0], speed[1]))


class Virus(Nave):
    def __init__(self, position, lives=1, speed=None, image=None, size=(70, 70)):
        if not image:
            image = "tomate.png"
        super().__init__(position, lives, speed, image, size)
        
class Powerup(Nave): # Nova classe de powerups (poderes extras). Herda de nave, assim como virus
    def __init__(self, position, lives=1, speed=None, image=None, size=(80, 80)):
        if not image:
            image = "chocolate.png" # Altera a imagem para a imagem de powerup
        super().__init__(position, lives, speed, image, size)

class Jogador(Nave):
    """
    A classe Player é uma classe derivada da classe GameObject.
       No entanto, o personagem não morre quando passa da borda, este só
    interrompe o seu movimento (vide update()).
       E possui experiência, que o fará mudar de nivel e melhorar seu tiro.
       A função get_pos() só foi redefinida para que os tiros não saissem da
    parte da frente da nave do personagem, por esta estar virada ao contrário
    das outras.
    """

    def __init__(self, position, lives=10, image=None, new_size=[100, 170]):
        if not image:
            image = "bebe.png"
        super().__init__(position, lives, [0, 0], image, new_size)
        self.pontos = 0 # Define os pontos começando em 0   
        
        self.deve_atirar = 0 # Define se deve ou não atirar quando chamar o método atira
        self.tempo_ultimo_tiro = 0 # Tempo do ultimo tiro
        self.tipo_tiro = 1 # Difine o tipo do tiro
        self.tempo_ultimo_powerup = 0 # Tempo da ultima vez q trocou a arma por um powerup
        
    def update(self, dt):
        move_speed = (self.speed[0] * dt / 16,
                      self.speed[1] * dt / 16)
        self.rect = self.rect.move(move_speed)

        if (self.rect.right > self.area.right):
            self.rect.right = self.area.right

        elif (self.rect.left < 0):
            self.rect.left = 0

        if (self.rect.bottom > self.area.bottom):
            self.rect.bottom = self.area.bottom

        elif (self.rect.top < 0):
            self.rect.top = 0
            
    def get_pos(self):
        return (self.rect.center[0], self.rect.top)

    def get_pontos(self):
        return self.pontos

    def set_pontos(self, pontos):
        self.pontos = pontos
    
    def aumenta_tipo_arma(self): # Função para aumentar o tipo da arma
        self.tipo_tiro += 1 # Aumenta 1 no tipo de arma
        self.tempo_ultimo_powerup = time() # Reseta o tempo para o jogador ficar com a arma especial de quando acaba de pegar powerup de arma
        
    def atira(self, lista_de_tiros, image=None):
        
        if self.deve_atirar == 1: # Verifica se realmente é para criar um novo tiro
            diferenca_tempo = time() - self.tempo_ultimo_tiro # Calcula a diferença do ultimo tiro para o momento atual
            if diferenca_tempo > 0.6: # Verifica se pode atirar pela diferença de tempo
                self.tempo_ultimo_tiro =  time() # Atualiza o tempo do ultimo tiro
                
                if self.tipo_tiro > 3: self.tipo_tiro = 3 # Limita a arma em 3
        
                p = self.get_pos()
                speeds = self.get_fire_speed(self.tipo_tiro) # Define a velocidade dos novos tiros
                for s in speeds:
                    Tiro(p, s, image, lista_de_tiros)

    def get_fire_speed(self, shots):
        speeds = []
        if time() - self.tempo_ultimo_powerup < 5: # Aciona a arma com 4 tiro se o jogador tiver ganhado um powerup de arma recentemente
            # Arma especial de quando acaba de pegar o powerup de arma (só tem duração de 5 segundos)    
            speeds += [(-1, -6)]
            speeds += [(1, -6)]
            speeds += [(-7, 0)]
            speeds += [(7, 0)]
        else: # Caso contrário, aciona a arma de acordo com a quantidade (+1) de powerups de arma que o jogador já ganhou (limite de 3)
            if shots <= 0:
                return speeds
            elif shots == 1:
                speeds += [(0, -6.5)]
            elif shots == 2:
                speeds += [(-1, -6.2)]
                speeds += [(1, -6.2)]
            elif shots >= 3: 
                speeds += [(0, -7)]
                speeds += [(-1.8, -6)]
                speeds += [(1.8, -6)]
            
        ''' # Arma descontínuada da versão (era muito forte)
        if shots == 5: 
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]
            speeds += [(-4, -2)]
            speeds += [(4, -2)]
        '''
        
        return speeds


class Tiro(ElementoSprite):
    def __init__(self, position, speed=None, image=None, list=None):
        if not image:
            image = "lego_azul.png"
        super().__init__(image, position, speed, new_size=[31, 35])
        if list is not None:
            self.add(list)


if __name__ == '__main__':
    J = Jogo() 
    continuar_jogando = True # Começar a jogar
    while continuar_jogando == True: # Verifica se o jogador quer continuar jogando depois de perder
        continuar_jogando = J.loop() # Inicia o jogo e retorna se o jogador quer jogar novamente
    pygame.quit() # Encerra o jogo

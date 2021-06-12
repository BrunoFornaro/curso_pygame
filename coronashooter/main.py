import pygame
from pygame.locals import (DOUBLEBUF,
                           FULLSCREEN,
                           KEYDOWN,
                           KEYUP,
                           K_LEFT,
                           K_RIGHT,
                           QUIT,
                           K_ESCAPE, K_UP, K_DOWN, K_RCTRL, K_LCTRL
                           )
from fundo import Fundo
from elementos import ElementoSprite
import random

from time import time
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
        pygame.display.set_caption('Corona Shooter')
        self.run = True
        
        self.fonte = pygame.font.Font("freesansbold.ttf", 32) # Define fonte
        
        # Define os textos do placar
        self.texto_vidas = self.fonte.render("Vidas: ", True, (0,255,0), (0,0,0))
        self.texto_pontos = self.fonte.render("Pontos: ", True, (0,255,0), (0,0,0))
        self.texto_nivel = self.fonte.render("Nível: ", True, (0,255,0), (0,0,0))
        
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

    def manutencao(self):
        r = random.randint(0, 10)
        x = random.randint(1, self.screen_size[0])
        virii = self.elementos["virii"]
        if r > (len(virii)):
            if self.nivel > 0:
                nivel_virus = random.randint(0, 10)
                if nivel_virus > 7:
                    enemy = Virus([0, 0], lives = 3, image="virinho_mau.png") 
                else:
                    enemy = Virus([0, 0]) 
            else:
                enemy = Virus([0, 0])
            size = enemy.get_size()
            enemy.set_pos([min(max(x, size[0]/2), self.screen_size[0]-size[0]/2), 0])
            mesmo_lugar = pygame.sprite.spritecollide(enemy, virii, False)
            if mesmo_lugar:
                return
            self.elementos["virii"].add(enemy)

    def muda_nivel(self):
        # Verifica o xp
        xp = self.jogador.get_pontos()
        # Verifica se deve mudar o nível pra 1
        if xp >= 10 and self.nivel == 0:
            # Altera o fundo
            self.fundo = Fundo("fundo2.png")
            # Altera o nível
            self.nivel = 1
            # Adiciona mais vidas para o jogador
            self.jogador.set_lives(self.jogador.get_lives() + 3)
        elif xp >= 50 and self.nivel == 1:
            self.fundo = Fundo("fundo3.png")
            self.nivel = 2
            self.jogador.set_lives(self.jogador.get_lives() + 6)

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
        self.texto_vidas = self.fonte.render(f"Vidas: {self.jogador.get_lives()}", True, (0,255,0), (0,0,0))
        self.texto_pontos = self.fonte.render(f"Pontos: {self.jogador.get_pontos()}", True, (0,255,0), (0,0,0))
        self.texto_nivel = self.fonte.render(f"Nível: {self.nivel}", True, (0,255,0), (0,0,0))
        # Desenha o placar
        self.screen.blit(self.texto_vidas, self.texto_vidas_rect)
        self.screen.blit(self.texto_pontos, self.texto_pontos_rect)
        self.screen.blit(self.texto_nivel, self.texto_nivel_rect)
        
    def verifica_impactos(self, elemento, list, action):
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
            self.run = False
            return

        # Verifica se o personagem trombou em algum inimigo
        self.verifica_impactos(self.jogador, self.elementos["virii"],
                               self.jogador.colisao)
        if self.jogador.morto:
            self.run = False
            return
        # Verifica se o personagem atingiu algum alvo.
        hitted = self.verifica_impactos(self.elementos["tiros"],
                                        self.elementos["virii"],
                                        Virus.alvejado)

        # Aumenta a pontos baseado no número de acertos:
        self.jogador.set_pontos(self.jogador.get_pontos() + len(hitted))

    def trata_eventos(self):
        event = pygame.event.poll()
        if event.type == pygame.QUIT:
            self.run = False

        if event.type == KEYDOWN: # Verifica se foi pressionada uma tecla
            key = event.key
            if key in (K_LCTRL, K_RCTRL):
                self.jogador.deve_atirar = 1 # Deve atirar
            elif key == K_UP:
                self.jogador.accel_top()
            elif key == K_DOWN:
                self.jogador.accel_bottom()
            elif key == K_RIGHT:
                self.jogador.accel_right()
            elif key == K_LEFT:
                self.jogador.accel_left()
                
        if event.type == KEYUP: # Verifica se a tecla foi solta
            key = event.key
            if key == K_ESCAPE:
                self.run = False
            elif key in (K_LCTRL, K_RCTRL):
                self.jogador.deve_atirar = 0 # Não deve atirar
            
            
        self.jogador.atira(self.elementos["tiros"]) # Pede par atirar (mas atira somente se o deve_atirar for igual a 1)
        

    def loop(self):
        clock = pygame.time.Clock()
        dt = 16
        self.elementos['virii'] = pygame.sprite.RenderPlain(Virus([120, 50]))
        self.jogador = Jogador([200, 400], 5)
        self.elementos['jogador'] = pygame.sprite.RenderPlain(self.jogador)
        self.elementos['tiros'] = pygame.sprite.RenderPlain()
        self.elementos['tiros_inimigo'] = pygame.sprite.RenderPlain()
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


class Nave(ElementoSprite):
    def __init__(self, position, lives=0, speed=[0, 0], image=None, new_size=[83, 248]):
        self.acceleration = [3, 3]
        if not image:
            image = "seringa.png"
        super().__init__(image, position, speed, new_size)
        self.set_lives(lives)

    def get_lives(self):
        return self.lives

    def set_lives(self, lives):
        self.lives = lives

    def colisao(self):
        if self.get_lives() <= 0:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    def atira(self, lista_de_tiros, image=None):
        s = list(self.get_speed())
        s[1] *= 2
        Tiro(self.get_pos(), s, image, lista_de_tiros)

    def alvejado(self):
        if self.get_lives() <= 0:
            self.kill()
        else:
            self.set_lives(self.get_lives() - 1)

    @property
    def morto(self):
        return self.get_lives() == 0

    def accel_top(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] - self.acceleration[1]))

    def accel_bottom(self):
        speed = self.get_speed()
        self.set_speed((speed[0], speed[1] + self.acceleration[1]))

    def accel_left(self):
        speed = self.get_speed()
        self.set_speed((speed[0] - self.acceleration[0], speed[1]))

    def accel_right(self):
        speed = self.get_speed()
        self.set_speed((speed[0] + self.acceleration[0], speed[1]))


class Virus(Nave):
    def __init__(self, position, lives=1, speed=None, image=None, size=(100, 100)):
        if not image:
            image = "virus.png"
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

    def __init__(self, position, lives=10, image=None, new_size=[83, 248]):
        if not image:
            image = "seringa.png"
        super().__init__(position, lives, [0, 0], image, new_size)
        self.pontos = 0
        
        self.deve_atirar = 0 # Define se deve ou não atirar quando chamar o método atira
        self.tempo_ultimo_tiro = 0 # Tempo do ultimo tiro

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

    def atira(self, lista_de_tiros, image=None):
        
        if self.deve_atirar == 1: # Verifica se realmente é para criar um novo tiro
            diferenca_tempo = time() - self.tempo_ultimo_tiro # Calcula a diferença do ultimo tiro para o momento atual
            if diferenca_tempo > 0.5: # Verifica se pode atirar pela diferença de tempo
                self.tempo_ultimo_tiro =  time() # Atualiza o tempo do ultimo tiro
                
                l = 1
                if self.pontos > 10: l = 3
                if self.pontos > 50: l = 5
        
                p = self.get_pos()
                speeds = self.get_fire_speed(l)
                for s in speeds:
                    Tiro(p, s, image, lista_de_tiros)

    def get_fire_speed(self, shots):
        speeds = []

        if shots <= 0:
            return speeds

        if shots == 1:
            speeds += [(0, -5)]

        if shots > 1 and shots <= 3:
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]

        if shots > 3 and shots <= 5:
            speeds += [(0, -5)]
            speeds += [(-2, -3)]
            speeds += [(2, -3)]
            speeds += [(-4, -2)]
            speeds += [(4, -2)]

        return speeds


class Tiro(ElementoSprite):
    def __init__(self, position, speed=None, image=None, list=None):
        if not image:
            image = "tiro.png"
        super().__init__(image, position, speed)
        if list is not None:
            self.add(list)


if __name__ == '__main__':
    J = Jogo()
    J.loop()
    pygame.quit()

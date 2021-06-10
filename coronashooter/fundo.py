import pygame
import os
from math import ceil


class Fundo:
    """
    Esta classe cria o fundo do jogo
    """

    def __init__(self, image="fundo_teste.png"):
        """
        Desenha o fundo da tela
        """
        image = os.path.join('imagens', image)
        image = pygame.image.load(image).convert()

        self.imagesize = image.get_size()
        self.pos = [0, -1 * self.imagesize[1]]
        screen = pygame.display.get_surface()
        screen_size = screen.get_size()

        w = (ceil(float(screen_size[0]) / self.imagesize[0]) + 1) * \
            self.imagesize[0]
        h = (ceil(float(screen_size[1]) / self.imagesize[1]) + 1) * \
            self.imagesize[1]

        back = pygame.Surface((w, h))

        for i in range((back.get_size()[0] // self.imagesize[0])):
            for j in range((back.get_size()[1] // self.imagesize[1])):
                back.blit(image, (i * self.imagesize[0], j * self.imagesize[1]))

        self.image = back
        self.fonte = pygame.font.Font("freesansbold.ttf", 32)
        self.texto = self.fonte.render("Pontuação\n\n.", True, (0,255,0), (0,0,0))
        self.texto_rect = self.texto.get_rect()
        self.texto_rect.center = (150,30)
        
    def update(self, dt):
        self.pos[1] += 1
        if self.pos[1] > 0:
            self.pos[1] -= self.imagesize[1]

    # update()

    def draw(self, screen, vidas=0, pontuacao=0, nivel=1):
        vidas = f"Vidas: {vidas * 'S2 '}"
        nivel = f"Nível: {nivel}"
        pontuacao = f"Pontução: {pontuacao}"
        self.texto = self.fonte.render(f"{vidas}. {nivel}. {pontuacao}", True, (0,255,0), (255,255,255))
        
        screen.blit(self.image, self.pos)
        screen.blit(self.texto, self.texto_rect)



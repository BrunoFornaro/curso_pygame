import pygame
import os
from math import ceil

class Fundo:
    """
    Esta classe cria o fundo do jogo
    """

    def __init__(self, image="madeira.png"):
        """
        Desenha o fundo da tela
        """
        image = os.path.join('imagens', image)
        image = pygame.image.load(image).convert()
        
        largura = pygame.display.get_surface().get_rect().right # Largura da tela
        altura = pygame.display.get_surface().get_rect().bottom # Altura da tela
        image = pygame.transform.scale(image, (largura, altura)) # Redimensiona a imagem do fundo para ficar do tamanho da tela
        
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

    
        


    def update(self, dt):
        self.pos[1] += 1
        if self.pos[1] > 0:
            self.pos[1] -= self.imagesize[1]

    # update()

    def draw(self, screen):
        screen.blit(self.image, self.pos)



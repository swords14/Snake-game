import pygame
import random

# Inicialização do Pygame
pygame.init()

# Definição das cores
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)

# Configurações da janela
largura_tela = 800
altura_tela = 600
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Jogo da Snake")

# Configurações da cobra
tamanho_cobra = 20
velocidade_cobra = 10

# Classe para representar a cobra
class Cobra:
    def __init__(self):
        self.tamanho = 1
        self.segmentos = [(largura_tela // 2, altura_tela // 2)]
        self.direcao = "direita"

    def mover(self):
        cabeca_x, cabeca_y = self.segmentos[0]

        if self.direcao == "direita":
            cabeca_x += tamanho_cobra
        elif self.direcao == "esquerda":
            cabeca_x -= tamanho_cobra
        elif self.direcao == "cima":
            cabeca_y -= tamanho_cobra
        elif self.direcao == "baixo":
            cabeca_y += tamanho_cobra

        self.segmentos.insert(0, (cabeca_x, cabeca_y))

        if len(self.segmentos) > self.tamanho:
            self.segmentos.pop()

    def desenhar(self):
        for segmento in self.segmentos:
            pygame.draw.rect(tela, VERDE, (segmento[0], segmento[1], tamanho_cobra, tamanho_cobra))

    def colisao(self, apple):
        return self.segmentos[0] == apple.posicao

    def colisao_borda(self):
        cabeca_x, cabeca_y = self.segmentos[0]
        return cabeca_x < 0 or cabeca_x >= largura_tela or cabeca_y < 0 or cabeca_y >= altura_tela

    def colisao_corpo(self):
        return self.segmentos[0] in self.segmentos[1:]

    def mudar_direcao(self, direcao):
        if direcao == "direita" and self.direcao != "esquerda":
            self.direcao = direcao
        elif direcao == "esquerda" and self.direcao != "direita":
            self.direcao = direcao
        elif direcao == "cima" and self.direcao != "baixo":
            self.direcao = direcao
        elif direcao == "baixo" and self.direcao != "cima":
            self.direcao = direcao

# Classe para representar a maçã
class Apple:
    def __init__(self):
        self.posicao = (random.randint(0, largura_tela - tamanho_cobra) // tamanho_cobra * tamanho_cobra,
                        random.randint(0, altura_tela - tamanho_cobra) // tamanho_cobra * tamanho_cobra)

    def desenhar(self):
        pygame.draw.rect(tela, VERMELHO, (self.posicao[0], self.posicao[1], tamanho_cobra, tamanho_cobra))

# Função principal do jogo
def jogar():
    cobra = Cobra()
    apple = Apple()

    relogio = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    cobra.mudar_direcao("direita")
                elif event.key == pygame.K_LEFT:
                    cobra.mudar_direcao("esquerda")
                elif event.key == pygame.K_UP:
                    cobra.mudar_direcao("cima")
                elif event.key == pygame.K_DOWN:
                    cobra.mudar_direcao("baixo")

        cobra.mover()

        if cobra.colisao(apple):
            cobra.tamanho += 1
            apple = Apple()

        if cobra.colisao_borda() or cobra.colisao_corpo():
            pygame.quit()
            return

        tela.fill(PRETO)
        cobra.desenhar()
        apple.desenhar()
        pygame.display.flip()

        relogio.tick(velocidade_cobra)

# Execução do jogo
jogar()


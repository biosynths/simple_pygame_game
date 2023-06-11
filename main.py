import pygame

pygame.init()
screen = pygame.display.set_mode((600, 600)) # flags=pygame.NOFRAME -без рамки
pygame.display.set_caption('Learning game')
icon = pygame.image.load('./images/icon.png')
pygame.display.set_icon(icon)

running = True

while running:
    # screen.fill((140, 65, 186))
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_0:
                screen.fill((140, 65, 186))


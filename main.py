import pygame

clock = pygame.time.Clock()

pygame.init()
left_boarder = 0
right_boarder = 1920
screen = pygame.display.set_mode((right_boarder, 1080)) # flags=pygame.NOFRAME -без рамки
pygame.display.set_caption('Learning game')
icon = pygame.image.load('./images/icon.png').convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load('./images/background.png').convert_alpha()

walk_left = [
    pygame.image.load('./images/player_left/player_left1.png').convert_alpha(),
    pygame.image.load('./images/player_left/player_left2.png').convert_alpha(),
    pygame.image.load('./images/player_left/player_left3.png').convert_alpha()
]
walk_right = [
    pygame.image.load('./images/player_right/player_right1.png').convert_alpha(),
    pygame.image.load('./images/player_right/player_right2.png').convert_alpha(),
    pygame.image.load('./images/player_right/player_right3.png').convert_alpha()
]

ghost = pygame.image.load('./images/ghost.png').convert_alpha()
ghost_list_in_game = []

player_anim_count = 0
bg_x = 0

player_speed = 15
player_x = 850
player_y = 650

is_jump = False
jump_count = 13

bg_sound = pygame.mixer.Sound('./sounds/bg_sound.mp3')
bg_sound.play(loops=True)

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 3000)

label = pygame.font.Font('./fonts/Kablammo-Regular.ttf', 72)
lose_label = label.render('Вы умерли!', False, 'Red')
restart_label = label.render('Давай по новой, всё хуйня', False, 'White')
restart_label_rect = restart_label.get_rect(topleft=(480, 780))

bullets_left = 5
bullet = pygame.image.load('./images/bullet.png').convert_alpha()
bullets = []

gameplay = True

running = True
while running:
    screen.blit(bg, (bg_x, 0))
    screen.blit(bg, (bg_x + 1920, 0))

    if gameplay:
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y), bottomright=(player_x + 170, player_y + 200))
        if ghost_list_in_game:
            for ghost_el in ghost_list_in_game:
                screen.blit(ghost, ghost_el)
                ghost_el.x -= 15

                if ghost_el.x < - 100:
                    ghost_list_in_game.remove(ghost_el)
                if player_rect.colliderect(ghost_el):
                    gameplay = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > left_boarder:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1720:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
        else:
            if jump_count >= -13:
                if jump_count > 0:
                    player_y -= (jump_count ** 2) / 2
                else:
                    player_y += (jump_count ** 2) / 2
                jump_count -= 1
            else:
                is_jump = False
                jump_count = 13

        if player_anim_count != 2:
            player_anim_count += 1
        else:
            player_anim_count = 0

        bg_x -= 5
        if bg_x == -1920:
            bg_x = 0

        if bullets:
            for el in bullets:
                screen.blit(bullet, (el.x, el.y))
                el.x += 50

                if el.x > right_boarder + 20:
                    bullets.remove(el)

                if ghost_list_in_game:
                    for g_el in ghost_list_in_game:
                        if el.colliderect(g_el):
                            ghost_list_in_game.remove(g_el)
                            bullets.remove(el)

    else:
        screen.fill('Black')
        screen.blit(lose_label, (750, 480))
        screen.blit(restart_label, restart_label_rect)

        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player_x = 850
            player_y = 650
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(right_boarder + 20, 700)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=([player_x + 100, player_y + 80])))
            bullets_left -= 1
    clock.tick(60)

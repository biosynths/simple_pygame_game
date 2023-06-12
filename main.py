import pygame
import config

clock = pygame.time.Clock()
pygame.init()

screen = pygame.display.set_mode((config.right_boarder, config.bottom_boarder)) # flags=pygame.NOFRAME -без рамки
pygame.display.set_caption(config.game_caption)
icon = pygame.image.load(config.icon_path).convert_alpha()
pygame.display.set_icon(icon)

bg = pygame.image.load(config.background_path).convert_alpha()
walk_left = []
for path in config.walk_left_path:
    walk_left.append(pygame.image.load(path).convert_alpha())
walk_right = []
for path in config.walk_right_path:
    walk_right.append(pygame.image.load(path).convert_alpha())
ghost = pygame.image.load(config.ghost_path).convert_alpha()
ghost_list_in_game = []

player_anim_count = config.start_anime_count
is_jump = config.is_jump_default
jump_count = config.jump_height
bg_x = config.start_bg_x

player_speed = config.player_speed
player_x = config.player_start_x
player_y = config.player_start_y

bg_sound = pygame.mixer.Sound(config.bg_sound_path)
bg_sound.set_volume(0.5)
bg_sound.play(loops=-1,)  # Проигрывать бесконечно

jump_sound = pygame.mixer.Sound(config.jump_sound_path)
jump_sound.set_volume(0.5)
hit_sound = pygame.mixer.Sound(config.hit_sound_path)
hit_sound.set_volume(0.5)

ghost_timer = pygame.USEREVENT + 1
pygame.time.set_timer(ghost_timer, 3000)

label = pygame.font.Font(config.label_path, 72)
lose_label = label.render(config.lose_text, False, 'Red')
restart_label = label.render(config.restart_text, False, 'White')
restart_label_rect = restart_label.get_rect(topleft=(480, 780))

label_small = pygame.font.Font(config.label_path, 60)


bullets_left = 5
bullet = pygame.image.load(config.bullet_image_path).convert_alpha()
bullets = []

gameplay = True
counter = 0
step = 0
running = True
while running:
    screen.blit(bg, (bg_x, config.top_boarder))
    screen.blit(bg, (bg_x + config.right_boarder, config.top_boarder))

    if gameplay:
        counter += 1
        step = counter // 60
        score_label = label_small.render(config.score_text + str(step), False, 'White')
        screen.blit(score_label, (50, 960))
        player_rect = walk_left[0].get_rect(topleft=(player_x, player_y), bottomright=(player_x + 170, player_y + 200))
        if ghost_list_in_game:
            for ghost_el in ghost_list_in_game:
                screen.blit(ghost, ghost_el)
                ghost_el.x -= config.ghost_speed

                if ghost_el.x < - 100:
                    ghost_list_in_game.remove(ghost_el)
                if player_rect.colliderect(ghost_el):
                    gameplay = False
                    hit_sound.play()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            screen.blit(walk_left[player_anim_count], (player_x, player_y))
        else:
            screen.blit(walk_right[player_anim_count], (player_x, player_y))

        if keys[pygame.K_LEFT] and player_x > config.left_boarder:
            player_x -= player_speed
        elif keys[pygame.K_RIGHT] and player_x < 1720:
            player_x += player_speed

        if not is_jump:
            if keys[pygame.K_UP]:
                is_jump = True
                jump_sound.play()
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

        # if player_anim_count != 2:
        #     player_anim_count += 1
        # else:
        #     player_anim_count = 0
        player_anim_count = (counter // 5) % 3

        bg_x -= 5
        if bg_x == -config.right_boarder:
            bg_x = 0

        if bullets:
            for el in bullets:
                screen.blit(bullet, (el.x, el.y))
                el.x += 50

                if el.x > config.right_boarder + 20:
                    bullets.remove(el)

                if ghost_list_in_game:
                    for g_el in ghost_list_in_game:
                        if el.colliderect(g_el):
                            ghost_list_in_game.remove(g_el)
                            bullets.remove(el)

    else:
        screen.fill('Black')
        screen.blit(score_label, (850, 700))
        screen.blit(lose_label, (750, 480))
        screen.blit(restart_label, restart_label_rect)
        mouse = pygame.mouse.get_pos()
        if restart_label_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            counter = 0
            player_x = config.player_start_x
            player_y = config.player_start_y
            is_jump = False
            jump_count = config.jump_height
            ghost_list_in_game.clear()
            bullets.clear()
            bullets_left = 5

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == ghost_timer:
            ghost_list_in_game.append(ghost.get_rect(topleft=(config.right_boarder + 20, 700)))
        if gameplay and event.type == pygame.KEYUP and event.key == pygame.K_SPACE and bullets_left > 0:
            bullets.append(bullet.get_rect(topleft=([player_x + 100, player_y + 80])))
            bullets_left -= 1
    clock.tick(60)

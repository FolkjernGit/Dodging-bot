import pygame
from logic import check_collision
from player import Player
from projectile import Projectile, random_projectile
pygame.init()

screen = pygame.display.set_mode((800, 600))

player = Player((400, 300), screen)
projectiles = []
spawn_timer = 0
spawn_delay = 20
MAX_PROJECTILES_SPEED = 5
# game loop
running = True
clock = pygame.time.Clock()

while running:
    clock.tick(144)
    
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Spawn
    spawn_timer += 1

    if spawn_timer >= spawn_delay:
        projectiles.append(
            random_projectile(player.position, screen.get_size(), MAX_PROJECTILES_SPEED)
        )
        spawn_timer = 0
    
    # update game state
    player.move(screen)
    # for ray in player.rays:
    #     ray.update(player.position, projectiles)
    for projectile in projectiles:
        projectile.update()
        if check_collision(player, projectile):
            print("HIT!")
            player.alive = False
    
    # Debugging
    print(player.get_observation(projectiles, screen, MAX_PROJECTILES_SPEED))
    player.draw_rays(screen)
    
    # draw everything
    screen.fill((30, 30, 30))
    player.draw_threat_lines(screen, projectiles)
    player.draw(screen)
    for projectile in projectiles:
        projectile.draw(screen)

    pygame.display.flip()

pygame.quit()
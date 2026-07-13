import pygame

def check_collision(player, projectile):
    player_center = player.position + pygame.Vector2(player.radius // 2, player.radius // 2)
    distance = player_center.distance_to(projectile.position)

    if distance < player.radius // 2 + projectile.radius:
        return True

    return False

def point_to_line_distance(point, line_start, line_end):

    direction = line_end - line_start
    direction = direction.normalize()

    to_point = point - line_start

    projection = to_point.dot(direction)

    if projection < 0:
        return 999999

    closest_point = line_start + direction * projection

    distance = point.distance_to(closest_point)

    return distance
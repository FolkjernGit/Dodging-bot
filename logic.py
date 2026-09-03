import pygame

def check_collision(player, projectile):

    distance = player.position.distance_to(
        projectile.position
    )

    hit_distance = (
        player.radius // 2 +
        projectile.radius // 2
    )

    if distance < hit_distance:

        if player.shielded:
            player.shielded = False
            player.shield_duration = 0
            player.shield_cooldown = 300
            player.blocked_projectiles += 1
            return False

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

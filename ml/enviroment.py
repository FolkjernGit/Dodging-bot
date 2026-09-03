import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pygame

from logic import check_collision
from player import Player
from projectile import random_projectile


class DodgeEnv:

    def __init__(self, screen):
        self.screen = screen

        # Environment
        self.player = None
        self.projectiles = []

        # Configuration
        self.max_projectile_speed = 5
        self.spawn_delay = 30
        self.max_time_alive = 3000

        # State
        self.spawn_timer = 0
        self.time_alive = 0

    # ------------------------------------------------------------------
    # Environment
    # ------------------------------------------------------------------

    def reset(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        player_position = (
            width // 2,
            height // 2
        )

        self.player = Player(
            player_position,
            self.screen
        )

        self.projectiles.clear()

        self.spawn_timer = 0
        self.time_alive = 0

        # Start with 10 projectiles
        for _ in range(10):
            self.spawn_projectile()

        return self.get_observation()

    def step(self, action):
        # Move player
        self.player.move(action, self.screen)

        # Update time
        self.time_alive += 1

        # Check maximum episode length
        if self.time_alive >= self.max_time_alive:
            return self.get_observation(), 10, True

        # Spawn new projectiles
        self.update_spawn_timer()

        # Update existing projectiles
        self.update_projectiles()

        # Remove projectiles that are far outside the screen
        self.remove_offscreen_projectiles()

        # Check collisions
        if self.check_collisions():
            return self.get_observation(), -10, True

        # Calculate reward
        reward = self.calculate_reward()

        return self.get_observation(), reward, False

    # ------------------------------------------------------------------
    # Projectiles
    # ------------------------------------------------------------------

    def spawn_projectile(self):
        projectile = random_projectile(
            self.player.position,
            self.screen.get_size(),
            self.max_projectile_speed
        )

        self.projectiles.append(projectile)

    def update_spawn_timer(self):
        self.spawn_timer += 1

        if self.spawn_timer >= self.spawn_delay:
            self.spawn_projectile()
            self.spawn_timer = 0

    def update_projectiles(self):
        for projectile in self.projectiles:
            projectile.update()

    def remove_offscreen_projectiles(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        remaining_projectiles = []

        for projectile in self.projectiles:
            x = projectile.position.x
            y = projectile.position.y

            inside_x = -50 < x < width + 50
            inside_y = -50 < y < height + 50

            if inside_x and inside_y:
                remaining_projectiles.append(projectile)

        self.projectiles = remaining_projectiles

    # ------------------------------------------------------------------
    # Collision
    # ------------------------------------------------------------------

    def check_collisions(self):
        for projectile in self.projectiles[:]:

            if not check_collision(self.player, projectile):

                continue

            if self.player.shielded:
                self.projectiles.remove(projectile)

            else:
                self.player.alive = False
                return True

        return False

    # ------------------------------------------------------------------
    # Rewards
    # ------------------------------------------------------------------

    def calculate_reward(self):
        reward = 0.1

        # Reward for blocking projectiles
        reward += self.blocked_projectile_reward()

        # Reward/penalty based on projectile distance
        reward += self.projectile_distance_reward()

        # Penalty for being near walls
        reward += self.wall_distance_reward()

        # Penalty for being near corners
        reward += self.corner_reward()

        return reward

    def blocked_projectile_reward(self):
        reward = self.player.blocked_projectiles * 0.2

        # Reset counter after giving reward
        self.player.blocked_projectiles = 0

        return reward

    def projectile_distance_reward(self):
        if len(self.projectiles) == 0:
            return 0

        closest_projectile = (
            self.player
            .get_closest_projectiles(self.projectiles, 1)[0]
        )

        distance = self.player.position.distance_to(
            closest_projectile.position
        )

        if distance < 50:
            return -0.1

        if distance < 200:
            return (distance - 50) / 150 * 0.05

        return 0

    def wall_distance_reward(self):
        width = self.screen.get_width()
        height = self.screen.get_height()

        x = self.player.position.x
        y = self.player.position.y

        wall_distance = min(
            x,
            width - x,
            y,
            height - y
        )

        if wall_distance < 50:
            return -0.1

        if wall_distance < 70:
            return -0.05

        return 0

    def corner_reward(self):
        corner_distance = 80

        width = self.screen.get_width()
        height = self.screen.get_height()

        x = self.player.position.x
        y = self.player.position.y

        near_left = x < corner_distance
        near_right = x > width - corner_distance

        near_top = y < corner_distance
        near_bottom = y > height - corner_distance

        near_horizontal_edge = near_left or near_right
        near_vertical_edge = near_top or near_bottom

        if near_horizontal_edge and near_vertical_edge:
            return -0.3

        return 0

    # ------------------------------------------------------------------
    # Observation
    # ------------------------------------------------------------------

    def get_observation(self):
        return self.player.get_observation(
            self.projectiles,
            self.screen,
            self.max_projectile_speed
        )

    # ------------------------------------------------------------------
    # Rendering
    # ------------------------------------------------------------------

    def render(self):
        self.screen.fill((0, 0, 0))

        self.draw_threat_lines()
        self.draw_shield()
        self.draw_player()
        self.draw_projectiles()

        pygame.display.flip()

    def draw_threat_lines(self):
        self.player.draw_threat_lines(
            self.screen,
            self.projectiles
        )

    def draw_shield(self):
        if not self.player.shielded:
            return

        pygame.draw.circle(
            self.screen,
            (0, 100, 255),
            self.player.position,
            self.player.radius // 2 + 5
        )

    def draw_player(self):
        pygame.draw.circle(
            self.screen,
            self.player.color,
            self.player.position,
            self.player.radius // 2
        )

    def draw_projectiles(self):
        for projectile in self.projectiles:
            pygame.draw.circle(
                self.screen,
                projectile.color,
                projectile.position,
                projectile.radius // 2
            )
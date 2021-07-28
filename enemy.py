import pygame
import math
import os
from settings import PATH, GREEN, RED, PATH2

pygame.init()
ENEMY_IMAGE = pygame.image.load(os.path.join("images", "enemy.png"))


class Enemy:
    # set path default
    def __init__(self, path=PATH):
        self.width = 40
        self.height = 50
        self.image = pygame.transform.scale(ENEMY_IMAGE, (self.width, self.height))
        self.health = 5
        self.max_health = 10
        self.path = path
        self.path_index = 0
        self.move_count = 0
        self.stride = 1
        self.x, self.y = self.path[0]

    def draw(self, win):
        # draw enemy
        win.blit(self.image, (self.x - self.width // 2, self.y - self.height // 2))
        # draw enemy health bar
        self.draw_health_bar(win)

    def draw_health_bar(self, win):
        """
        Draw health bar on an enemy
        :param win: window
        :return: None
        """
        pygame.draw.rect(win, RED,
                         (self.x - self.width // 2.5, self.y - self.height // 2, self.max_health * 3, 4))
        pygame.draw.rect(win, GREEN,
                         (self.x - self.width // 2.5, self.y - self.height // 2, self.health * 3, 4))

    def move(self):
        """
        Enemy move toward path points every frame
        :return: None
        """
        now_x, now_y = self.path[self.path_index]                             # now point(x, y)
        next_x, next_y = self.path[self.path_index + 1]                       # next point(x, y)
        distance = math.sqrt((now_x - next_x)**2 + (now_y - next_y)**2)     # two point distance calculate
        max_count = int(distance / self.stride)                             # two point need how many step

        if self.move_count < max_count:
            unit_vector_x = (next_x - now_x) / distance
            unit_vector_y = (next_y - now_y) / distance
            delta_x = unit_vector_x * self.stride
            delta_y = unit_vector_y * self.stride

            # update the coordinate and the counter

            self.x += delta_x
            self.y += delta_y
            self.move_count += 1

        else:
            self.path_index += 1      # update point index
            self.move_count = 0     # reset


class EnemyGroup:
    def __init__(self):
        self.gen_count = 0              # count now frame after pre-enemy output
        self.gen_max_count = 120           # (unit: frame)
        self.reserved_members = []      # store enemies to the list when you push key n
        self.expedition = [Enemy()]     # don't change this line until you do the EX.3
        self.path_button = 0            # chose path's button

    def campaign(self):
        """
        Send an enemy to go on an expedition once 120 frame
        :return: None
        """
        # show enemies from list reserved_member and interval 120 frame for each enemies
        if self.gen_count >= self.gen_max_count and not self.is_empty():
            self.expedition.append(self.reserved_members.pop())
            self.gen_count = 0         # reset

        else:
            self.gen_count += 1

    def generate(self, num):
        """
        Generate the enemies in this wave
        :param num: enemy number
        :return: None
        """
        # chose which path by path_button
        if self.path_button == 0:
            path = PATH
            self.path_button = 1
        else:
            path = PATH2
            self.path_button = 0

        # generate(store) enemies into backend
        for i in range(num):
            self.reserved_members.append(Enemy(path))

    def get(self):
        """
        Get the enemy list
        """
        return self.expedition

    def is_empty(self):
        """
        Return whether the enemy is empty (so that we can move on to next wave)
        """
        return False if self.reserved_members else True

    def retreat(self, enemy):
        """
        Remove the enemy from the expedition
        :param enemy: class Enemy()
        :return: None
        """
        self.expedition.remove(enemy)

    # def set_path(self, button):
    #   """
    #    Use to set path
    #    """
    #    self.path_button = button






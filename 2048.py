import logging
import math
import random
from enum import Enum

import pygame

logging.basicConfig(
    level=logging.DEBUG,
    format="[%(levelname)s]: %(message)s",
)


class Direction(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


class Game_2048:
    class Graphics:
        def __init__(self, rows, cols, state):
            self.rows = rows
            self.cols = cols
            self.outline_thickness = 10
            self.rect_width = 200
            self.rect_height = 200
            self.width = (
                self.rect_width + self.outline_thickness
            ) * cols - 3 * self.outline_thickness
            self.height = (
                self.rect_height + self.outline_thickness
            ) * rows - 3 * self.outline_thickness
            self.outline_color = (187, 173, 160)
            self.background_color = (205, 192, 180)
            self.font_color = (119, 110, 101)
            self.fps = 60
            pygame.init()
            self.window = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("2048 Game")
            self.font = pygame.font.SysFont("comicsans", 60, bold=True)
            self.move_vel = 20

            self.window.fill(self.background_color)
            for row in range(1, self.rows):
                y = row * self.rect_height + self.outline_thickness // 2 - 1
                pygame.draw.line(
                    self.window,
                    self.outline_color,
                    (0, y),
                    (self.width, y),
                    self.outline_thickness,
                )
            for col in range(1, self.cols):
                x = col * self.rect_width + self.outline_thickness // 2 - 1
                pygame.draw.line(
                    self.window,
                    self.outline_color,
                    (x, 0),
                    (x, self.width),
                    self.outline_thickness,
                )
            pygame.draw.rect(
                self.window,
                self.outline_color,
                (0, 0, self.width, self.height),
                self.outline_thickness,
            )
            self.update_tiles(state)
            pygame.display.update()

        def update_tiles(self, state):
            tiles = []
            for row in range(self.rows):
                for col in range(self.cols):
                    value = state[row][col]
                    if value != 0:
                        tiles.append(
                            self.Tile(
                                value,
                                row,
                                col,
                                self.rect_width,
                                self.rect_height,
                                self.font,
                                self.font_color,
                                self.outline_thickness,
                            )
                        )
            for tile in tiles:
                tile.draw(self.window)
            pygame.display.update()

        class Tile:
            COLOR = [
                (237, 229, 218),  # 2
                (238, 225, 201),  # 4
                (243, 178, 122),  # 8
                (246, 150, 101),  # 16
                (247, 124, 95),  # 32
                (247, 95, 59),  # 64
                (237, 208, 115),  # 128
                (237, 204, 99),  # 256
                (236, 202, 80),  # 512
                (239, 197, 63),  # 1024
                (239, 193, 47),  # 2048
                (255, 187, 34),  # 4096
                (255, 170, 0),  # 8192
                (255, 145, 0),  # 16384
                (255, 120, 0),  # 32768
                (204, 102, 255),  # 65536
                (170, 51, 255),  # 131072
                (140, 20, 255),  # 262144
                (115, 0, 230),  # 524288
                (90, 0, 200),  # 1048576
            ]

            def __init__(
                self,
                value,
                row,
                col,
                rect_width,
                rect_height,
                font,
                font_color,
                outline_thickness,
            ):
                self.value = value
                self.row = row
                self.col = col
                self.rect_width = rect_width
                self.rect_height = rect_height
                self.x = col * rect_width
                self.y = row * rect_height
                self.font = font
                self.font_color = font_color
                self.border = outline_thickness

            def get_color(self):
                color_index = int(math.log2(self.value)) - 1
                color = self.COLOR[color_index]
                return color

            def draw(self, window):
                color = self.get_color()
                pygame.draw.rect(
                    window,
                    color,
                    (
                        self.x + self.border,
                        self.y + self.border,
                        self.rect_width - self.border,
                        self.rect_height - self.border,
                    ),
                )
                text = self.font.render(str(self.value), 1, self.font_color)
                window.blit(
                    text,
                    (
                        self.x + (self.rect_width / 2 - text.get_width() / 2),
                        self.y + (self.rect_height / 2 - text.get_height() / 2),
                    ),
                )

    def __init__(self, graphics=True):
        logging.info("Game starting...")
        self.rows = 4
        self.cols = 4
        self.state = tuple(tuple(0 for _ in range(self.cols)) for _ in range(self.rows))
        self.state = self.generate_tile()
        # self.state = (
        #     (2, 4, 8, 16),
        #     (32, 64, 128, 256),
        #     (512, 1024, 2048, 4096),
        #     (8192, 16384, 32768, 65536),
        # )
        logging.debug(f"Initial game state: {self.state}")

        if graphics:
            self.graphics = self.Graphics(self.rows, self.cols, self.state)

    def generate_tile(self):
        state = [list(row) for row in self.state]
        empty_positions = [
            (r, c) for r in range(self.rows) for c in range(self.cols) if state[r][c] == 0
        ]
        if len(empty_positions) == 0:
            return tuple(tuple(row) for row in state)
        logging.debug(f"Empty positions: {empty_positions}")
        r, c = random.choice(empty_positions)
        state[r][c] = 2 if random.random() < 0.9 else 4
        return tuple(tuple(row) for row in state)

    def next_state(self, direction):
        logging.debug(f"Moving tiles {direction}")
        if direction == Direction.UP:
            pass



        next_state = self.generate_tile()
        if next_state == self.state:
            logging.info("game over")
            return False
        else:
            self.state = next_state
            return True


if __name__ == "__main__":
    run = True
    game = Game_2048()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    run = game.next_state(Direction.UP)
                elif event.key == pygame.K_DOWN:
                    run = game.next_state(Direction.DOWN)
                elif event.key == pygame.K_RIGHT:
                    run = game.next_state(Direction.RIGHT)
                elif event.key == pygame.K_LEFT:
                    run = game.next_state(Direction.LEFT)
                game.graphics.update_tiles(game.state)
    pygame.quit()

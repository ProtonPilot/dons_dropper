import random
import sys

import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

PLAYER_SPEED = 8
DROP_SPEED_START = 4
DROP_ACCELERATION = 0.05
SPAWN_EVERY_FRAMES = 24
MAX_MISSES = 5

BG_COLOR = (25, 27, 34)
TEXT_COLOR = (240, 240, 240)

GOOD_DROPS = ["🍩", "🍕", "🍔", "🌮"]
BAD_DROPS = ["🧨", "💣", "🧱"]


class Drop:
    def __init__(self, x: int, y: int, char: str, bad: bool) -> None:
        self.x = x
        self.y = y
        self.char = char
        self.bad = bad

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x - 18, self.y - 18, 36, 36)


def draw_text(surface: pygame.Surface, text: str, font: pygame.font.Font, x: int, y: int) -> None:
    image = font.render(text, True, TEXT_COLOR)
    surface.blit(image, (x, y))


def make_drop(emoji_font: pygame.font.Font) -> Drop:
    char = random.choice(GOOD_DROPS + BAD_DROPS)
    bad = char in BAD_DROPS
    x = random.randint(30, SCREEN_WIDTH - 30)
    y = -20

    # Try to ensure the emoji is renderable by falling back if needed.
    if emoji_font.render(char, True, (255, 255, 255)).get_width() <= 2:
        char = "X" if bad else "O"

    return Drop(x, y, char, bad)


def reset_game() -> tuple[list[Drop], int, int, float, int, str]:
    return [], 0, 0, DROP_SPEED_START, 0, ""


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Don's Dropper (No Binary Assets)")
    clock = pygame.time.Clock()

    ui_font = pygame.font.SysFont("arial", 28)
    emoji_font = pygame.font.SysFont("segoe ui emoji, apple color emoji, noto color emoji", 34)
    player_font = pygame.font.SysFont("arial", 54, bold=True)

    drops, score, misses, drop_speed, frame_count, message = reset_game()
    player_x = SCREEN_WIDTH // 2
    running = True
    game_over = False

    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r and game_over:
                    drops, score, misses, drop_speed, frame_count, message = reset_game()
                    game_over = False

        if not game_over:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x += PLAYER_SPEED

            player_x = max(35, min(SCREEN_WIDTH - 35, player_x))

            frame_count += 1
            if frame_count % SPAWN_EVERY_FRAMES == 0:
                drops.append(make_drop(emoji_font))

            caught: list[Drop] = []
            missed: list[Drop] = []

            player_rect = pygame.Rect(player_x - 30, SCREEN_HEIGHT - 70, 60, 60)

            for drop in drops:
                drop.y += drop_speed

                if drop.rect.colliderect(player_rect):
                    caught.append(drop)
                    if drop.bad:
                        score = max(0, score - 3)
                        message = "Ouch! Don caught a bad drop."
                    else:
                        score += 1
                        message = "Nice catch!"
                elif drop.y > SCREEN_HEIGHT + 20:
                    missed.append(drop)
                    if not drop.bad:
                        misses += 1
                        message = "Missed a good one!"

            if caught or missed:
                drops = [d for d in drops if d not in caught and d not in missed]

            drop_speed += DROP_ACCELERATION / FPS

            if misses >= MAX_MISSES:
                game_over = True
                message = "Game Over! Press R to restart."

        screen.fill(BG_COLOR)

        for drop in drops:
            draw_text(screen, drop.char, emoji_font, drop.x - 16, drop.y - 16)

        pygame.draw.ellipse(screen, (225, 205, 170), (player_x - 30, SCREEN_HEIGHT - 70, 60, 60))
        draw_text(screen, "😮", player_font, player_x - 24, SCREEN_HEIGHT - 68)

        draw_text(screen, f"Score: {score}", ui_font, 20, 12)
        draw_text(screen, f"Misses: {misses}/{MAX_MISSES}", ui_font, 20, 44)
        draw_text(screen, "Move: ←/→ or A/D | ESC: Quit", ui_font, 20, 76)

        if message:
            draw_text(screen, message, ui_font, 20, 110)

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 120))
            screen.blit(overlay, (0, 0))
            draw_text(screen, "DON'S DROPPER", player_font, SCREEN_WIDTH // 2 - 180, SCREEN_HEIGHT // 2 - 80)
            draw_text(screen, f"Final Score: {score}", ui_font, SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT // 2 - 20)
            draw_text(screen, "Press R to play again", ui_font, SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 20)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

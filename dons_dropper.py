import random
import sys
from pathlib import Path

import pygame


SCREEN_WIDTH = 900
SCREEN_HEIGHT = 640
FPS = 60

PLAYER_SPEED = 9
DROP_SPEED_START = 4.0
DROP_ACCELERATION = 0.04
SPAWN_EVERY_FRAMES = 24
MAX_MISSES = 5

BG_COLOR = (24, 26, 34)
TEXT_COLOR = (242, 242, 242)
BUTTON_COLOR = (51, 102, 209)
BUTTON_HOVER = (71, 128, 232)

ASSETS_DIR = Path(__file__).resolve().parent / "assets"

DROPPER_IMAGE = "dropper.jpg"
HEAD_OPEN_IMAGE = "head_open.jpg"
HEAD_CLOSED_IMAGE = "head_closed.jpg"
PANTS_IMAGE = "pants.jpg"


class Drop:
    def __init__(self, x: int, y: int, item_key: str, image: pygame.Surface) -> None:
        self.x = x
        self.y = y
        self.item_key = item_key
        self.image = image

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.x, self.y, self.image.get_width(), self.image.get_height())


class Button:
    def __init__(self, text: str, rect: pygame.Rect) -> None:
        self.text = text
        self.rect = rect

    def draw(self, surface: pygame.Surface, font: pygame.font.Font, mouse_pos: tuple[int, int]) -> None:
        color = BUTTON_HOVER if self.rect.collidepoint(mouse_pos) else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        pygame.draw.rect(surface, (235, 235, 235), self.rect, width=2, border_radius=10)
        label = font.render(self.text, True, (255, 255, 255))
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)


def draw_text(
    surface: pygame.Surface,
    text: str,
    font: pygame.font.Font,
    x: int,
    y: int,
    color: tuple[int, int, int] = TEXT_COLOR,
) -> None:
    image = font.render(text, True, color)
    surface.blit(image, (x, y))


def make_labeled_surface(size: tuple[int, int], label: str, fill: tuple[int, int, int]) -> pygame.Surface:
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))
    pygame.draw.rect(surface, fill, (0, 0, size[0], size[1]), border_radius=12)
    pygame.draw.rect(surface, (20, 20, 20), (0, 0, size[0], size[1]), width=3, border_radius=12)
    font = pygame.font.SysFont("arial", max(16, size[1] // 4), bold=True)
    label_img = font.render(label, True, (255, 255, 255))
    label_rect = label_img.get_rect(center=(size[0] // 2, size[1] // 2))
    surface.blit(label_img, label_rect)
    return surface


def make_emoji_surface(emoji: str, size: tuple[int, int] = (64, 64)) -> pygame.Surface:
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    fonts = [
        pygame.font.SysFont("apple color emoji", 52),
        pygame.font.SysFont("segoe ui emoji", 52),
        pygame.font.SysFont("noto color emoji", 52),
    ]

    glyph = None
    for font in fonts:
        candidate = font.render(emoji, True, (255, 255, 255))
        if candidate.get_width() > 8:
            glyph = candidate
            break

    if glyph is None:
        glyph = pygame.font.SysFont("arial", 26, bold=True).render("ITEM", True, (255, 255, 255))

    glyph_rect = glyph.get_rect(center=(size[0] // 2, size[1] // 2))
    surface.blit(glyph, glyph_rect)
    return surface


def load_image_if_exists(name: str, size: tuple[int, int]) -> pygame.Surface | None:
    image_path = ASSETS_DIR / name
    if not image_path.exists():
        return None
    image = pygame.image.load(image_path).convert_alpha()
    return pygame.transform.smoothscale(image, size)


def load_first_available_image(names: list[str], size: tuple[int, int]) -> pygame.Surface | None:
    for name in names:
        image = load_image_if_exists(name, size)
        if image is not None:
            return image
    return None


def make_drop_image(item_key: str, emoji: str, size: tuple[int, int] = (64, 64)) -> pygame.Surface:
    image = load_first_available_image([f"{item_key}.png", f"{item_key}.jpg", f"{item_key}.jpeg"], size)
    if image is not None:
        return image
    return make_emoji_surface(emoji, size)


def reset_game() -> tuple[list[Drop], int, int, float, int]:
    return [], 0, 0, DROP_SPEED_START, 0


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Don's Dropper")
    clock = pygame.time.Clock()

    don_img = load_image_if_exists(DROPPER_IMAGE, (170, 170)) or make_labeled_surface((170, 170), "DON", (196, 79, 84))
    bob_open_img = load_image_if_exists(HEAD_OPEN_IMAGE, (170, 95)) or make_labeled_surface((170, 95), "BOB :O", (85, 146, 98))
    bob_closed_img = load_image_if_exists(HEAD_CLOSED_IMAGE, (170, 95)) or make_labeled_surface((170, 95), "BOB :)", (68, 126, 82))

    pants_img = load_image_if_exists(PANTS_IMAGE, (64, 64)) or make_labeled_surface((64, 64), "PANTS", (246, 215, 66))

    drop_images = {
        "watermelon": make_drop_image("watermelon", "🍉"),
        "beer_mug": make_drop_image("beer_mug", "🍺"),
        "eggplant": make_drop_image("eggplant", "🍆"),
        "yellow_pants": pants_img,
    }

    ui_font = pygame.font.SysFont("arial", 28)
    big_font = pygame.font.SysFont("arial", 48, bold=True)
    button_font = pygame.font.SysFont("arial", 30, bold=True)

    start_button = Button("Start Game", pygame.Rect(SCREEN_WIDTH // 2 - 110, SCREEN_HEIGHT // 2 + 50, 220, 62))
    restart_button = Button("Start New Game", pygame.Rect(SCREEN_WIDTH // 2 - 135, SCREEN_HEIGHT // 2 + 35, 270, 62))

    item_keys = ["watermelon", "beer_mug", "eggplant", "yellow_pants"]
    next_wave: list[str] = []

    drops, score, misses, drop_speed, frame_count = reset_game()
    player_x = SCREEN_WIDTH // 2
    bob_catch_timer = 0

    game_state = "loading"
    running = True

    while running:
        dt_ms = clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif game_state in {"loading", "game_over"} and event.key in {pygame.K_RETURN, pygame.K_SPACE}:
                    drops, score, misses, drop_speed, frame_count = reset_game()
                    bob_catch_timer = 0
                    random.shuffle(item_keys)
                    next_wave = item_keys.copy()
                    game_state = "playing"
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if game_state == "loading" and start_button.rect.collidepoint(event.pos):
                    drops, score, misses, drop_speed, frame_count = reset_game()
                    bob_catch_timer = 0
                    random.shuffle(item_keys)
                    next_wave = item_keys.copy()
                    game_state = "playing"
                elif game_state == "game_over" and restart_button.rect.collidepoint(event.pos):
                    drops, score, misses, drop_speed, frame_count = reset_game()
                    bob_catch_timer = 0
                    random.shuffle(item_keys)
                    next_wave = item_keys.copy()
                    game_state = "playing"

        if game_state == "playing":
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                player_x -= PLAYER_SPEED
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                player_x += PLAYER_SPEED

            bob_width = bob_open_img.get_width()
            player_x = max(0, min(SCREEN_WIDTH - bob_width, player_x))

            frame_count += 1
            if frame_count % SPAWN_EVERY_FRAMES == 0:
                if not next_wave:
                    next_wave = item_keys.copy()
                    random.shuffle(next_wave)
                item_key = next_wave.pop()
                x = random.randint(35, SCREEN_WIDTH - 99)
                drops.append(Drop(x, -70, item_key, drop_images[item_key]))

            bob_rect = pygame.Rect(player_x + 24, SCREEN_HEIGHT - 120, bob_open_img.get_width() - 48, 64)

            active_drops: list[Drop] = []
            for drop in drops:
                drop.y += drop_speed
                if drop.rect.colliderect(bob_rect):
                    score += 1
                    bob_catch_timer = 140
                    continue

                if drop.y > SCREEN_HEIGHT:
                    misses += 1
                    if misses >= MAX_MISSES:
                        game_state = "game_over"
                    continue

                active_drops.append(drop)

            drops = active_drops
            drop_speed += DROP_ACCELERATION / FPS
            bob_catch_timer = max(0, bob_catch_timer - dt_ms)

        screen.fill(BG_COLOR)

        don_x = SCREEN_WIDTH // 2 - don_img.get_width() // 2
        screen.blit(don_img, (don_x, 14))

        for drop in drops:
            screen.blit(drop.image, (drop.x, drop.y))

        bob_image = bob_closed_img if bob_catch_timer > 0 else bob_open_img
        screen.blit(bob_image, (player_x, SCREEN_HEIGHT - 120))

        draw_text(screen, f"Score: {score}", ui_font, 20, 16)
        draw_text(screen, f"Misses: {misses}/{MAX_MISSES}", ui_font, 20, 50)

        if game_state == "playing":
            draw_text(screen, "Move: ←/→ or A/D", ui_font, 20, 84)
        elif game_state == "loading":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 155))
            screen.blit(overlay, (0, 0))

            title = "Don is losing all his stuff."
            subtitle = "Bob must catch it all to save the world!"
            draw_text(screen, title, big_font, SCREEN_WIDTH // 2 - 280, SCREEN_HEIGHT // 2 - 110)
            draw_text(screen, subtitle, ui_font, SCREEN_WIDTH // 2 - 250, SCREEN_HEIGHT // 2 - 55)
            start_button.draw(screen, button_font, mouse_pos)

        elif game_state == "game_over":
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 165))
            screen.blit(overlay, (0, 0))

            draw_text(screen, "GAME OVER", big_font, SCREEN_WIDTH // 2 - 155, SCREEN_HEIGHT // 2 - 90)
            draw_text(screen, f"Final Score: {score}", ui_font, SCREEN_WIDTH // 2 - 88, SCREEN_HEIGHT // 2 - 38)
            restart_button.draw(screen, button_font, mouse_pos)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

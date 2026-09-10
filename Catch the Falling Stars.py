import pygame
import random
import sys

# Initialize pygame
pygame.init()

# ---------------- SCREEN ----------------
WIDTH = 800
HEIGHT = 600

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catch the Falling Stars")

clock = pygame.time.Clock()

# ---------------- COLORS ----------------
BLACK = (15, 15, 25)
WHITE = (255, 255, 255)
YELLOW = (255, 220, 0)
BLUE = (50, 150, 255)
RED = (255, 70, 70)
GREEN = (50, 220, 100)

# ---------------- FONTS ----------------
font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 75)

# ---------------- BASKET ----------------
basket_width = 120
basket_height = 25
basket_speed = 8

# ---------------- STAR ----------------
star_size = 25
star_speed = 5


# Create a new game
def new_game():
    basket_x = WIDTH // 2 - basket_width // 2

    star_x = random.randint(
        20,
        WIDTH - star_size - 20
    )

    star_y = -star_size

    score = 0
    missed = 0

    return basket_x, star_x, star_y, score, missed


# ---------------- START SCREEN ----------------

start_screen = True

while start_screen:

    screen.fill(BLACK)

    title = big_font.render(
        "CATCH THE FALLING STARS",
        True,
        YELLOW
    )

    instruction1 = font.render(
        "Use LEFT and RIGHT arrows to move",
        True,
        WHITE
    )

    instruction2 = font.render(
        "Catch the stars and increase your score!",
        True,
        WHITE
    )

    instruction3 = font.render(
        "Press SPACE to Start",
        True,
        GREEN
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            170
        )
    )

    screen.blit(
        instruction1,
        (
            WIDTH // 2 - instruction1.get_width() // 2,
            280
        )
    )

    screen.blit(
        instruction2,
        (
            WIDTH // 2 - instruction2.get_width() // 2,
            325
        )
    )

    screen.blit(
        instruction3,
        (
            WIDTH // 2 - instruction3.get_width() // 2,
            390
        )
    )

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                start_screen = False

    clock.tick(60)


# ---------------- NEW GAME ----------------

basket_x, star_x, star_y, score, missed = new_game()

game_over = False


# ---------------- MAIN GAME LOOP ----------------

running = True

while running:

    # Events
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # Restart
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r and game_over:
                basket_x, star_x, star_y, score, missed = new_game()
                game_over = False

    # ---------------- GAME ----------------

    if not game_over:

        # Keyboard
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            basket_x -= basket_speed

        if keys[pygame.K_RIGHT]:
            basket_x += basket_speed

        # Keep basket inside screen
        if basket_x < 0:
            basket_x = 0

        if basket_x > WIDTH - basket_width:
            basket_x = WIDTH - basket_width

        # Make star faster as score increases
        current_speed = star_speed + score * 0.15

        # Move star
        star_y += current_speed

        # ---------------- COLLISION ----------------

        basket_y = HEIGHT - 70

        if star_y + star_size >= basket_y:

            if (
                star_x + star_size >= basket_x
                and star_x <= basket_x + basket_width
            ):
                # Caught
                score += 1

            else:
                # Missed
                missed += 1

            # Create new star
            star_x = random.randint(
                20,
                WIDTH - star_size - 20
            )

            star_y = -star_size

        # ---------------- GAME OVER ----------------

        if missed >= 5:
            game_over = True

    # ---------------- DRAW ----------------

    screen.fill(BLACK)

    if not game_over:

        # Draw star
        pygame.draw.circle(
            screen,
            YELLOW,
            (
                star_x + star_size // 2,
                star_y + star_size // 2
            ),
            star_size // 2
        )

        # Draw basket
        pygame.draw.rect(
            screen,
            BLUE,
            (
                basket_x,
                HEIGHT - 70,
                basket_width,
                basket_height
            )
        )

        # Score
        score_text = font.render(
            "Score: " + str(score),
            True,
            WHITE
        )

        # Missed
        missed_text = font.render(
            "Missed: " + str(missed) + "/5",
            True,
            WHITE
        )

        screen.blit(score_text, (20, 20))
        screen.blit(missed_text, (20, 60))

    else:

        # Game Over
        game_over_text = big_font.render(
            "GAME OVER",
            True,
            RED
        )

        final_score_text = font.render(
            "Final Score: " + str(score),
            True,
            WHITE
        )

        restart_text = font.render(
            "Press R to Restart",
            True,
            GREEN
        )

        screen.blit(
            game_over_text,
            (
                WIDTH // 2 - game_over_text.get_width() // 2,
                200
            )
        )

        screen.blit(
            final_score_text,
            (
                WIDTH // 2 - final_score_text.get_width() // 2,
                300
            )
        )

        screen.blit(
            restart_text,
            (
                WIDTH // 2 - restart_text.get_width() // 2,
                360
            )
        )

    pygame.display.update()

    # 60 FPS
    clock.tick(60)


# Quit
pygame.quit()
sys.exit()
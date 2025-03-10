import pygame
import random

# Constants
WIDTH, HEIGHT = 600, 400
BG_COLOR = (245, 222, 179)  # Index card color
STICK_COLOR = (0, 0, 0)
AIM_COLOR = (255, 0, 0)
NUB_COLOR = (255, 255, 0)  # Yellow Banana Nub
TIMER = 30  # Seconds
MAX_TRIES = 7

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Find the Solo Stick Person")
font = pygame.font.Font(None, 30)
clock = pygame.time.Clock()

# Game Variables
level = 1
num_sticks = 2
max_sticks = 300
high_score = 0
player_name = "Player"
stick_positions = []
aiming_lines = []
new_level = True
tries_left = MAX_TRIES

def draw_stick_figure(surface, x, y):
    pygame.draw.circle(surface, STICK_COLOR, (x, y), 5)  # Head
    pygame.draw.line(surface, STICK_COLOR, (x, y + 5), (x, y + 20), 2)  # Body
    pygame.draw.line(surface, STICK_COLOR, (x - 5, y + 10), (x + 5, y + 10), 2)  # Arms
    pygame.draw.line(surface, STICK_COLOR, (x, y + 20), (x - 5, y + 30), 2)  # Left leg
    pygame.draw.line(surface, STICK_COLOR, (x, y + 20), (x + 5, y + 30), 2)  # Right leg
    pygame.draw.arc(surface, NUB_COLOR, (x - 5, y + 8, 10, 10), 3.14, 0, 3)  # Banana-shaped yellow nub


def draw_dashed_line(surface, color, start, end, dash_length=3):
    x1, y1 = start
    x2, y2 = end
    dx, dy = x2 - x1, y2 - y1
    distance = (dx ** 2 + dy ** 2) ** 0.5
    dashes = int(distance // (2 * dash_length))
    for i in range(dashes):
        start_dash = (x1 + (dx / distance) * dash_length * i * 2, y1 + (dy / distance) * dash_length * i * 2)
        end_dash = (x1 + (dx / distance) * dash_length * (i * 2 + 1), y1 + (dy / distance) * dash_length * (i * 2 + 1))
        if (end_dash[0] - start[0]) ** 2 + (end_dash[1] - start[1]) ** 2 > distance ** 2:
            break
        pygame.draw.line(surface, color, start_dash, end_dash, 1)


def generate_sticks():
    global stick_positions, aiming_lines, solo_stick
    stick_positions = [(random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)) for _ in range(num_sticks)]
    aiming_lines = []
    targeted = set()

    for i, (sx, sy) in enumerate(stick_positions):
        if len(targeted) < num_sticks - 1:
            target = random.choice([j for j in range(num_sticks) if j != i and j not in targeted])
            tx, ty = stick_positions[target]
            aiming_lines.append(((sx, sy + 15), (tx, ty)))
            targeted.add(target)

    solo_stick = next(i for i in range(num_sticks) if i not in targeted)


def draw():
    screen.fill(BG_COLOR)

    for (sx, sy), (tx, ty) in aiming_lines:
        draw_dashed_line(screen, AIM_COLOR, (sx, sy), (tx, ty))

    for x, y in stick_positions:
        draw_stick_figure(screen, x, y)

    pygame.draw.rect(screen, (200, 0, 0), (WIDTH - 100, 10, 80, 30))
    stop_text = font.render("STOP", True, (255, 255, 255))
    screen.blit(stop_text, (WIDTH - 80, 15))

    score_text = font.render(f"Score: {level}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    tries_text = font.render(f"Tries Left: {tries_left}", True, (0, 0, 0))
    screen.blit(tries_text, (10, HEIGHT - 30))

    timer_text = font.render(f"Time Left: {int(time_left)}", True, (0, 0, 0))
    screen.blit(timer_text, (WIDTH // 4 - timer_text.get_width() // 2, 10))

    level_text = font.render(f"Level: {level}", True, (0, 0, 0))
    screen.blit(level_text, (WIDTH - level_text.get_width() - 10, HEIGHT - 30))

    pygame.display.flip()


def display_score():
    sx, sy = stick_positions[solo_stick]
    zoom_surface = pygame.Surface((100, 100))
    zoom_surface.blit(screen, (0, 0), (sx - 50, sy - 50, 100, 100))
    zoom_surface = pygame.transform.scale(zoom_surface, (WIDTH, HEIGHT))

    for _ in range(150):
        screen.blit(zoom_surface, (0, 0))
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (WIDTH // 3, HEIGHT // 3))
        pygame.display.flip()
        pygame.time.wait(33)
    pygame.time.wait(5000)


def main_menu():
    global player_name
    running = True
    name_input = ""
    while running:
        screen.fill(BG_COLOR)
        menu_text = font.render("Enter Your Name: " + name_input, True, (0, 0, 0))
        screen.blit(menu_text, (WIDTH // 4, HEIGHT // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name_input:
                    player_name = name_input
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    name_input = name_input[:-1]
                else:
                    name_input += event.unicode


main_menu()

time_left = TIMER
running = True
while running:
    if new_level:
        generate_sticks()
        new_level = False

    dt = clock.tick(30) / 1000
    time_left -= dt

    if time_left <= 0 or tries_left <= 0:
        print("Game over!")
        display_score()
        running = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if WIDTH - 100 <= x <= WIDTH - 20 and 10 <= y <= 40:
                main_menu()
            sx, sy = stick_positions[solo_stick]
            if abs(x - sx) < 10 and abs(y - sy) < 10:
                print("You found the solo stick person! Moving to next level!")
                level += 1
                num_sticks = min(num_sticks + 5, max_sticks)
                time_left = TIMER
                tries_left = MAX_TRIES
                high_score = max(high_score, level)
                new_level = True
            else:
                tries_left -= 1

    draw()

pygame.quit()

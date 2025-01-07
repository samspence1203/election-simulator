import pygame
import random  # For placeholder region colours

# Initialise Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("General Election Simulator - Interactive Map")

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
HIGHLIGHT = (180, 220, 255)

# Fonts
font = pygame.font.SysFont(None, 36)

# Placeholder regions (x, y, width, height, name)
regions = [
    (60, 120, 180, 150, "Scotland"),
    (260, 120, 180, 150, "North East"),
    (60, 300, 180, 150, "Wales"),
    (260, 300, 180, 150, "South West"),
]

# Helper function to draw regions
def draw_regions(hovered_region):
    for x, y, width, height, name in regions:
        color = HIGHLIGHT if name == hovered_region else GRAY
        pygame.draw.rect(screen, color, (x, y, width, height))
        pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)
        label_surface = font.render(name, True, BLACK)
        screen.blit(label_surface, (x + 10, y + 10))

# Main loop
running = True
hovered_region = None
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and hovered_region:
            print(f"Region clicked: {hovered_region}")

    # Detect mouse hover
    mouse_x, mouse_y = pygame.mouse.get_pos()
    hovered_region = None
    for x, y, width, height, name in regions:
        if x <= mouse_x <= x + width and y <= mouse_y <= y + height:
            hovered_region = name
            break

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw GUI sections
    pygame.draw.rect(screen, BLACK, (50, 100, 400, 600), 2)  # Map placeholder
    pygame.draw.rect(screen, BLACK, (500, 20, 400, 50), 2)   # Calendar placeholder
    pygame.draw.rect(screen, BLACK, (950, 100, 200, 600), 2) # Stats placeholder
    pygame.draw.rect(screen, BLACK, (500, 100, 400, 600), 2) # Events placeholder

    # Draw regions
    draw_regions(hovered_region)

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

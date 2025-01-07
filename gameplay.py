import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("General Election Simulator - Gameplay")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

# Fonts
font = pygame.font.SysFont(None, 36)

# Helper function to draw labeled sections
def draw_section(x, y, width, height, label):
    pygame.draw.rect(screen, BLACK, (x, y, width, height), 2)  # Draw the section border
    label_surface = font.render(label, True, BLACK)
    screen.blit(label_surface, (x + 10, y + 10))  # Add the label inside the section

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Draw GUI sections
    draw_section(50, 100, 400, 600, "Constituency Map")  # Left: Map
    draw_section(500, 20, 400, 50, "Calendar")          # Top Center: Calendar
    draw_section(950, 100, 200, 600, "Stats Bars")      # Right: Stats Bars
    draw_section(500, 100, 400, 600, "Events Box")      # Center: Events

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()

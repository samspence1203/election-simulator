# gameplay.py (with Pygame)

import pygame
from gameplay_classes import Campaign, Constituency, Region, Statistics

# Initialise Pygame
pygame.init()

# Game Window Settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Election Simulation")

# Game variables
campaign = Campaign(2019)
statistics = Statistics()

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with white
    screen.fill((255, 255, 255))

    # Draw basic campaign stats
    font = pygame.font.SysFont('Arial', 24)
    text = font.render(f"Campaign Year: {campaign.election_year}", True, (0, 0, 0))
    screen.blit(text, (10, 10))

    text = font.render(f"Funds: ${statistics.funds}", True, (0, 0, 0))
    screen.blit(text, (10, 40))

    text = font.render(f"Public Opinion: {statistics.public_opinion}%", True, (0, 0, 0))
    screen.blit(text, (10, 70))

    # Update the screen
    pygame.display.flip()

    # Pause for a brief moment (for testing)
    pygame.time.wait(500)

# Quit Pygame
pygame.quit()

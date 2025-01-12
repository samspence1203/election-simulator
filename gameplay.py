import pygame
from gameplay_classes import Campaign, Constituency, Region, Statistics

# Initialise Pygame
pygame.init()

# Game Window Settings
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Election Simulation")

# Game variables
campaign = Campaign(2024)  # Start the campaign for the 2024 election
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

    # Display current day and stage
    current_day_text = font.render(f"Day: {campaign.current_day + 1}", True, (0, 0, 0))
    current_stage_text = font.render(f"Stage: {campaign.campaign_calendar[campaign.current_day]}", True, (0, 0, 0))
    screen.blit(current_day_text, (10, 10))
    screen.blit(current_stage_text, (10, 40))

    # Display other campaign stats
    funds_text = font.render(f"Funds: ${statistics.funds}", True, (0, 0, 0))
    opinion_text = font.render(f"Public Opinion: {statistics.public_opinion}%", True, (0, 0, 0))
    screen.blit(funds_text, (10, 70))
    screen.blit(opinion_text, (10, 100))

    # Update the screen
    pygame.display.flip()

    # Wait for a brief moment (for testing)
    pygame.time.wait(500)

    # Advance the campaign day
    campaign.advance_day()

# Quit Pygame
pygame.quit()

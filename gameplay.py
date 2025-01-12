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

# Font for displaying text
font = pygame.font.SysFont('Arial', 24)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill screen with white
    screen.fill((255, 255, 255))

    # Update statistics from the campaign class
    statistics.update_from_campaign(campaign)

    # Draw basic campaign stats
    current_day_text = font.render(f"Day: {campaign.current_day + 1}", True, (0, 0, 0))
    current_stage_text = font.render(f"Stage: {campaign.campaign_calendar[campaign.current_day]}", True, (0, 0, 0))
    screen.blit(current_day_text, (10, 10))
    screen.blit(current_stage_text, (10, 40))

    # Display current event (if any)
    if campaign.current_day < len(campaign.campaign_calendar):
        current_stage = campaign.campaign_calendar[campaign.current_day]
        if current_stage == "Event":
            event_text = font.render("Current Event: Random Event Triggered!", True, (0, 0, 0))
            screen.blit(event_text, (10, 70))

    # Display other campaign stats directly from the statistics object
    funds_text = font.render(f"Funds: ${statistics.funds}", True, (0, 0, 0))
    opinion_text = font.render(f"Public Opinion: {statistics.public_opinion}%", True, (0, 0, 0))
    screen.blit(funds_text, (10, 100))
    screen.blit(opinion_text, (10, 130))

    # Update the screen
    pygame.display.flip()

    # Advance the day
    pygame.time.wait(500)
    campaign.advance_day()

# Quit Pygame
pygame.quit()

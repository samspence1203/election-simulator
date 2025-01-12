import pygame
import pymysql
from gameplay_classes import Campaign, Constituency, Statistics

# Initialise Pygame
pygame.init()

# Game Window Settings: Revert back to the original size (800x600)
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Election Simulation")

# Database connection
db_connection = pymysql.connect(
    host="localhost",
    user="root",
    password="SamSpence",
    database="election_simulator"
)

# Game variables
campaign = Campaign(2024)  # Start the campaign for 2024
statistics = Statistics()

# Fetch constituencies from the database
def fetch_constituencies(db_connection):
    query = """
    SELECT c.Constituency, p.Party, cr.WinningCandidate
    FROM constituency c
    JOIN constituencyresult cr ON c.ID = cr.ConstituencyID
    JOIN party p ON cr.FirstPartyID = p.ID
    WHERE cr.ElectionID = (SELECT ID FROM election WHERE Year = 2019)
    """
    with db_connection.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        return result  # List of tuples: (Constituency, Party, WinningCandidate)

# Get constituencies
constituencies_data = fetch_constituencies(db_connection)

# Create Constituency objects
constituencies = []
grid_width = 20  # Number of constituencies per row (adjust as needed)
box_width = 20  # Adjusted width for each constituency box
box_height = 10  # Adjusted height for each constituency box
padding = 5  # Padding between boxes

for i, data in enumerate(constituencies_data):
    name, party, winning_candidate = data
    constituency = Constituency(name, party, winning_candidate, 0, 0)  # Dummy values for now
    # Calculate position based on grid layout
    x_pos = (i % grid_width) * (box_width + padding) + padding
    y_pos = (i // grid_width) * (box_height + padding) + padding  # Padding from the top
    constituency.rect = pygame.Rect(x_pos, y_pos, box_width, box_height)
    constituency.party_controlled = party
    constituencies.append(constituency)

# Font for displaying text
font = pygame.font.SysFont('Arial', 24)

# Game loop variables
running = True
paused = True  # Game starts paused
calendar_text = font.render("PAUSED", True, (255, 0, 0))

# Party colors
party_colors = {
    'Conservatives': (0, 0, 255),  # Blue
    'Labour': (255, 0, 0),         # Red
    'Reform': (173, 216, 230),     # Light Blue
    'Greens': (0, 255, 0),         # Green
    'Liberal Democrats': (255, 165, 0),  # Orange
    'Other': (169, 169, 169)       # Grey
}

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Check if a constituency is clicked
            for constituency in constituencies:
                if constituency.rect.collidepoint(mouse_pos):
                    print(f"Clicked on {constituency.name}")
                    print(f"Party: {constituency.party_controlled}")
                    print(f"Winning Candidate: {constituency.winning_candidate}")

        # Space bar toggles the paused state
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused = not paused
                if paused:
                    print("Game Paused")
                else:
                    print("Game Unpaused")

    # Fill screen with white
    screen.fill((255, 255, 255))

    # Update statistics from the campaign (sync funds and public opinion)
    statistics.update_from_campaign(campaign)

    # Draw constituencies as colored boxes
    for constituency in constituencies:
        color = party_colors.get(constituency.party_controlled, (0, 0, 0))  # Default to black if no color is found
        pygame.draw.rect(screen, color, constituency.rect)

    # Show "PAUSED" message if the game is paused
    if paused:
        screen.blit(calendar_text, (screen.get_width() // 2 - calendar_text.get_width() // 2, 10))

    # Draw basic campaign stats
    current_day_text = font.render(f"Day: {campaign.current_day + 1}", True, (0, 0, 0))
    current_stage_text = font.render(f"Stage: {campaign.campaign_calendar[campaign.current_day]}", True, (0, 0, 0))
    screen.blit(current_day_text, (10, 10))
    screen.blit(current_stage_text, (10, 40))

    # Display updated funds and public opinion from the statistics object
    funds_text = font.render(f"Funds: ${statistics.funds}", True, (0, 0, 0))
    opinion_text = font.render(f"Public Opinion: {statistics.public_opinion}%", True, (0, 0, 0))
    screen.blit(funds_text, (10, 70))
    screen.blit(opinion_text, (10, 100))

    # Update the screen
    pygame.display.flip()

    # Only advance the day if not paused
    if not paused:
        campaign.advance_day()
        pygame.time.wait(500)  # Adjust time delay to suit the pace of the game

# Quit Pygame
pygame.quit()

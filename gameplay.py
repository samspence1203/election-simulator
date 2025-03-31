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
grid_width = 10  # Number of constituencies per row (adjust as needed)
box_width = 15  # Adjusted width for each constituency box
box_height = 6  # Adjusted height for each constituency box
padding = 3  # Padding between boxes

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

# Define the variables for constituency data display
clicked_constituency_data = ""

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
                    clicked_constituency_data = (
                        f"Constituency: {constituency.name}\n"
                        f"Party: {constituency.party_controlled}\n"
                        f"Winning Candidate: {constituency.winning_candidate}"
                    )

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
        screen.blit(calendar_text, (screen.get_width() // 2 - calendar_text.get_width() // 2, 70))

    # Draw basic campaign stats
    current_day_text = font.render(f"Day: {campaign.current_day + 1}", True, (0, 0, 0))
    current_stage_text = font.render(f"Stage: {campaign.campaign_calendar[campaign.current_day]}", True, (0, 0, 0))
    current_day_x = (screen_width - current_day_text.get_width()) // 2
    current_stage_x = (screen_width - current_stage_text.get_width()) // 2
    screen.blit(current_day_text, (current_day_x, 10))
    screen.blit(current_stage_text, (current_stage_x, 40))

    # Display updated funds and public opinion from the statistics object
    funds_text = font.render(f"Funds: ${statistics.funds}", True, (0, 0, 0))
    opinion_text = font.render(f"Public Opinion: {statistics.public_opinion}%", True, (0, 0, 0))
    stats_x = screen_width - 200
    screen.blit(funds_text, (stats_x, 70))
    screen.blit(opinion_text, (stats_x, 100))

    # Define the width and height of the decision box
    decision_box_width = 300
    decision_box_height = 400
    button_width = 180
    button_height = 40

    # Define the decision text and button labels
    decision_text = "Do you want to fund a rally?"
    button_labels = ["Decision 1", "Decision 2", "Decision 3"]

    # Calculate the position of the decision box (center of the screen)
    decision_box_x = (screen_width - decision_box_width) // 2
    decision_box_y = (screen_height - decision_box_height) // 2

    # Create a simple background for the decision box (gray rectangle)
    pygame.draw.rect(screen, (169, 169, 169), pygame.Rect(decision_box_x, decision_box_y, decision_box_width, decision_box_height))

    # Render the decision text (centered in the decision box)
    text = font.render(decision_text, True, (0, 0, 0))  # Black text
    text_rect = text.get_rect(center=(decision_box_x + decision_box_width // 2, decision_box_y + 40))  # 40px offset for spacing
    screen.blit(text, text_rect)

    # Draw the buttons above each other (vertically aligned)
    button_start_y = decision_box_y + 80  # Starting Y position for the first button

    # Draw the buttons below the text
    for i, label in enumerate(button_labels):
        button_x = decision_box_x + (decision_box_width - button_width) // 2  # Center the button horizontally
        button_y = button_start_y + (button_height + 10) * i  # Stack buttons vertically with 10px spacing
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Draw the button (light gray)
        pygame.draw.rect(screen, (211, 211, 211), button_rect)

        # Render the label on the button
        button_label = font.render(label, True, (0, 0, 0))  # Black text
        button_label_rect = button_label.get_rect(center=button_rect.center)
        screen.blit(button_label, button_label_rect)

    # Handle button clicks (for now, just print to the console)
    for i, label in enumerate(button_labels):
        if pygame.mouse.get_pressed()[0]:  # Check if left mouse button is clicked
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if pygame.Rect(button_x, button_y, button_width, button_height).collidepoint(mouse_x, mouse_y):
                print(f"{label} selected")

    # Render the constituency data if a constituency is clicked
    if clicked_constituency_data:
        # Define the font and position for the constituency data
        constituency_font = pygame.font.SysFont("Arial", 20)
        lines = clicked_constituency_data.split("\n")  # Split the data into multiple lines

        # Render each line of the constituency data
        y_offset = decision_box_y + 250  # Starting Y position for the text
        for line in lines:
            text = constituency_font.render(line, True, (0, 0, 0))  # Black text
            text_rect = text.get_rect(center=(decision_box_x + decision_box_width // 2, y_offset))
            screen.blit(text, text_rect)
            y_offset += 30  # Adjust the Y offset for each new line

    # Update the screen
    pygame.display.flip()

    # Only advance the day if not paused
    if not paused:
        campaign.advance_day()
        pygame.time.wait(1000)  # Adjust time delay to suit the pace of the game

# Quit Pygame
pygame.quit()

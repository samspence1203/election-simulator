class Campaign:
    def __init__(self, election_year):
        self.election_year = election_year
        self.constituencies = []
        self.regions = []
        self.campaign_calendar = []
        self.funds = 0
        self.public_opinion = 50  # Starting at 50% approval

    def start_campaign(self):
        # Initialize campaign with basic data
        print(f"Campaign for {self.election_year} started.")
        # Additional logic for starting the campaign (e.g., setting up the calendar)

    def advance_day(self):
        # Logic to move the campaign forward by one day
        pass


class Constituency:
    def __init__(self, name, party_controlled, winning_candidate):
        self.name = name
        self.party_controlled = party_controlled  # Store the party ID
        self.winning_candidate = winning_candidate  # Candidate's name
        self.majority = 0
        self.majority_percentage = 0.0

    def update_majority(self, majority, majority_percentage):
        self.majority = majority
        self.majority_percentage = majority_percentage


class Region:
    def __init__(self, name):
        self.name = name
        self.constituencies = []  # List of constituencies in the region
        self.vote_percentage = 0.0

    def update_vote_percentage(self, percentage):
        self.vote_percentage = percentage


class Statistics:
    def __init__(self):
        self.funds = 0
        self.party_members = 0
        self.public_opinion = 50

    def update_funds(self, amount):
        self.funds += amount

    def update_public_opinion(self, percentage_change):
        self.public_opinion += percentage_change

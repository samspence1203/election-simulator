class Campaign:
    def __init__(self, election_year):
        self.election_year = election_year
        self.constituencies = []
        self.regions = []
        self.campaign_calendar = []  # List of days (e.g., "Day 1", "Planning", "Day 2", "Event")
        self.funds = 100000  # Starting campaign funds
        self.public_opinion = 50  # Starting at 50% approval
        self.current_day = 0  # Track current day
        self.stages = ["Planning", "Event", "Last-Minute"]

        # Initialising the campaign calendar (e.g. 30 days in total for simplicity)
        self.initialise_calendar()

    def initialise_calendar(self):
        """
        Initialise the campaing calendar with phases.
        This is just a basic starter-for-ten to work from.
        """
        self.campaign_calendar = []

        # Add "Planning" phase for the first 10 days
        for _ in range(10):
            self.campaign_calendar.append("Planning")

        # Add "Event" phase for the next 15 days
        for _ in range(15):
            self.campaign_calendar.append("Event")

        # Add "Last-Minute" phase for the final 5 days
        for _ in range(5):
            self.campaign_calendar.append("Last-Minute")

        # Total days = 30

    def start_campaign(self):
        # Initialize campaign with basic data
        print(f"Campaign for {self.election_year} started.")
        # Additional logic for starting the campaign (e.g., setting up the calendar)

    def advance_day(self):
        """
        Advance the campaign by one day and trigger the relevant stage or event.
        """
        if self.current_day < len(self.campaign_calendar):
            current_stage = self.campaign_calendar[self.current_day]
            print(f"Day {self.current_day + 1}: {current_stage}")
            self.trigger_event(current_stage)
            self.current_day += 1
        else:
            print("Election day has arrived!")

    def trigger_event(self, stage):
        """
        Trigger events based on the current stage of the campaign.
        """
        if stage == "Planning":
            # Example: Setup initial campaign events
            self.public_opinion += 1  # Increase public opinion slightly during planning
            print("Planning events: Campaign strategy development.")
        elif stage == "Event":
            # Example: Major event, such as a rally
            self.public_opinion += 5  # Events increase public opinion
            self.funds -= 2000  # Events can cost money
            print("Event: Major rally held!")
        elif stage == "Last-Minute":
            # Example: Last-minute campaigning
            self.public_opinion += 10  # Big push towards election
            print("Last-Minute Campaigning: Final push to sway voters.")


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

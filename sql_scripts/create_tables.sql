#Drop child tables first to avoid foreign key constraint errors
DROP TABLE IF EXISTS regionresult;
DROP TABLE IF EXISTS donation;
DROP TABLE IF EXISTS constituencyresult;
DROP TABLE IF EXISTS resultbyparty;

#Drop parent tables last - not sure if election is parent or child so put it first
DROP TABLE IF EXISTS election;
DROP TABLE IF EXISTS region;
DROP TABLE IF EXISTS constituency;
DROP TABLE IF EXISTS party;

#Create DB
CREATE TABLE IF NOT EXISTS Constituency (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Constituency VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Party (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Party VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS Region (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Election (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Year INT NOT NULL,
    LargestPartyID INT NOT NULL,
    Turnout DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (LargestPartyID) REFERENCES Party(ID)
);

CREATE TABLE IF NOT EXISTS ConstituencyResult (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ElectionID INT NOT NULL,
    ConstituencyID INT NOT NULL,
    FirstPartyID INT NOT NULL,
    SecondPartyID INT NOT NULL,
    Majority INT NOT NULL,
    MajorityPercentage DECIMAL(5,2) NOT NULL,
    WinningCandidate VARCHAR(100) NOT NULL,
    NewMP BOOLEAN NOT NULL,
    FOREIGN KEY (ElectionID) REFERENCES Election(ID),
    FOREIGN KEY (ConstituencyID) REFERENCES Constituency(ID),
    FOREIGN KEY (FirstPartyID) REFERENCES Party(ID),
    FOREIGN KEY (SecondPartyID) REFERENCES Party(ID)
);

CREATE TABLE IF NOT EXISTS Donation (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ElectionID INT NOT NULL,
    PartyID INT NOT NULL,
    Individual DECIMAL(10,2) NOT NULL,
    Company DECIMAL(10,2),
    TradeUnion DECIMAL(10,2),
    Other DECIMAL(10,2),
    TotalValue DECIMAL(10,2) NOT NULL,
    TotalNum INT NOT NULL,
    SharePercentage DECIMAL(5,2) NOT NULL,
    FOREIGN KEY (ElectionID) REFERENCES Election(ID),
    FOREIGN KEY (PartyID) REFERENCES Party(ID)
);

CREATE TABLE IF NOT EXISTS ResultByParty (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ElectionID INT NOT NULL,
    PartyID INT NOT NULL,
    TotalVote INT NOT NULL,
    TotalVotePercentage DECIMAL(5,2) NOT NULL,
    Seats INT NOT NULL,
    FOREIGN KEY (ElectionID) REFERENCES Election(ID),
    FOREIGN KEY (PartyID) REFERENCES Party(ID)
);

CREATE TABLE IF NOT EXISTS RegionResult (
    ID INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    ElectionID INT NOT NULL,
    PartyID INT NOT NULL,
    RegionID INT NOT NULL,
    RegionVote INT NOT NULL,
    RegionVotePercentage DECIMAL(5,2),
    FOREIGN KEY (ElectionID) REFERENCES Election(ID),
    FOREIGN KEY (PartyID) REFERENCES Party(ID),
    FOREIGN KEY (RegionID) REFERENCES Region(ID)
);
-- Group 23: Juanette Van Wyk, Cara Walter
-- DDL sql file for for CS340 Portifolio Project
-- Tracking tickets by event for Gill Coliseum
-- Modified from MySQL data dump for creation and sample data addition for tables Teams, Events, EventOutcomes, EventOutcomesTeams, TicketHolders, TicketTypes, and Tickets

-- Disable foreign key checks and autocommits to reduce errors
-- source URL: https://canvas.oregonstate.edu/courses/1922991/assignments/9287071?module_item_id=23329619
SET FOREIGN_KEY_CHECKS=0;
SET autocommit=0;

--
-- Table structure for table `Teams`
--

-- Create Teams table
DROP TABLE IF EXISTS Teams;

CREATE TABLE Teams (
    teamID int NOT NULL AUTO_INCREMENT,
    teamName varchar(50) NOT NULL,
    PRIMARY KEY (teamID)
);

-- Add Teams data
INSERT INTO `Teams` (teamName)
VALUES ('OSU'),('WSU'),('UC Berkeley'),('UC Davis'),('PSU');

--
-- Table structure for table `Events`
--

DROP TABLE IF EXISTS Events;

CREATE TABLE Events (
  eventID int NOT NULL AUTO_INCREMENT,
  eventDate Date NOT NULL,
  startTime Time NOT NULL, 
  endTime Time NOT NULL,
  visitingTeamID int NOT NULL,
  PRIMARY KEY (eventID),
  FOREIGN KEY (visitingTeamID) REFERENCES Teams(teamID)
  ON UPDATE CASCADE
  ON DELETE CASCADE
);

--
-- Dumping data for table `Events`
--

INSERT INTO Events (eventDate,startTime,endTime,visitingTeamID)
VALUES ('2023-09-01','13:00:00','15:00:00',2),
('2023-09-02','19:00:00','21:00:00',2),
('2023-09-05','19:00:00','21:00:00',3),
('2023-09-14','13:00:00','15:00:00',4),
('2023-09-21','09:00:00','11:00:00',5);

--
-- Table structure for table `EventOutcomes`
--

DROP TABLE IF EXISTS EventOutcomes;

CREATE TABLE EventOutcomes (
  eventOutcomeID int NOT NULL AUTO_INCREMENT,
  eventID int NOT NULL, 
  winningScore int NOT NULL,
  losingScore int NOT NULL,
  PRIMARY KEY (eventOutcomeID),
  FOREIGN KEY (eventID) REFERENCES Events(eventID)
  ON DELETE CASCADE
  ON UPDATE CASCADE
);

--
-- Dumping data for table EventOutcomes
--

INSERT INTO EventOutcomes (eventID,winningScore,losingScore)
VALUES (1,15,10),
(2,2,1),
(3,8,3);


--
-- Table structure for table `EventOutcomes_has_Teams`
--

DROP TABLE IF EXISTS EventOutcomesTeams;

CREATE TABLE EventOutcomesTeams (
    eventOutcomesTeamID int NOT NULL AUTO_INCREMENT,
    eventOutcomeID int NOT NULL,
    teamID int NOT NULL,
    winner int NOT NULL,
    PRIMARY KEY (eventOutcomesTeamID),
    FOREIGN KEY (eventOutcomeID) REFERENCES EventOutcomes(eventOutcomeID)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (teamID) REFERENCES Teams(teamID)
	ON DELETE CASCADE
    ON UPDATE CASCADE
);

--
-- Dumping data for table EventOutcomesTeams
--

INSERT INTO EventOutcomesTeams (eventOutcomeID,teamID,winner)
VALUES (1,1,1),
(1,2,0),
(2,1,0),
(2,2,1),
(3,1,1),
(3,3,0);


--
-- Table structure for table `TicketTypes`
--

DROP TABLE IF EXISTS TicketTypes;

CREATE TABLE TicketTypes (
  ticketTypeID int NOT NULL AUTO_INCREMENT,
  ticketType varchar(10) NOT NULL,
  price decimal(4,2) NOT NULL,
  PRIMARY KEY (ticketTypeID)
);

--
-- Dumping data for table `TicketTypes`
--

INSERT INTO TicketTypes (ticketType,price)
VALUES ('single',10),
('season',8),
('student',0);


--
-- Table structure for table `TicketHolders`
--

DROP TABLE IF EXISTS TicketHolders;

CREATE TABLE TicketHolders (
  ticketHolderID int NOT NULL AUTO_INCREMENT,
  firstName varchar(40) NOT NULL,
  lastName varchar(40) NOT NULL,
  phone varchar(15) DEFAULT NULL,
  email varchar(50) NOT NULL,
  PRIMARY KEY (ticketHolderID)
);

--
-- Dumping data for table `TicketHolders`
--

INSERT INTO TicketHolders (firstName,lastName,phone,email)
VALUES ('Jane','Smith','541-862-1250','jane.smith@yahoo.com'),
('Rigby','Fields',NULL,'rfields@gmail.com'),
('Joseph','Jameson','503-652-1456','jj4ever@aol.com'),
('Veronica','Ruth','541-584-1010','veronicar@hotmail.com'),
('Isaac','Woods','415-698-1540','isawoo@gmail.com');


--
-- Table structure for table `Tickets`
-- includes contraint for the combination of eventID and seatID to be unique

DROP TABLE IF EXISTS Tickets;

CREATE TABLE Tickets (
  ticketID int NOT NULL AUTO_INCREMENT,
  seatID int NOT NULL,
  eventID int NOT NULL,
  ticketHolderID int,
  ticketTypeID int NOT NULL,
  INDEX eventSeat (eventID, seatID),
  CHECK (seatID < 9302 AND seatID > 0),
  PRIMARY KEY (ticketID),
  FOREIGN KEY (eventID) REFERENCES Events(eventID)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (ticketHolderID) REFERENCES TicketHolders(ticketHolderID)
  ON DELETE CASCADE
  ON UPDATE CASCADE,
  FOREIGN KEY (ticketTypeID) REFERENCES TicketTypes(ticketTypeID)
);

--
-- Dumping data for table `Tickets`
--

INSERT INTO Tickets(eventID,seatID,ticketHolderID,ticketTypeID)
VALUES (1,1,1,1),
(2,1,2,2),
(2,2,2,2),
(2,3,NULL,3),
(5,1,4,1);


-- turn back on foreign key checks and autocommit
-- -- source URL: https://canvas.oregonstate.edu/courses/1922991/assignments/9287071?module_item_id=23329619
SET FOREIGN_KEY_CHECKS=1;
COMMIT;
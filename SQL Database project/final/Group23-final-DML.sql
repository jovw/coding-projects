-- Group 23: Juanette Van Wyk, Cara Walter
-- DML sql file for for CS340 Portifolio Project
-- Tracking tickets by event for Gill Coliseum
-- Data Manipulation Queries for website
-- : symbol indicates variable that will be populated with a value from Flask

-- Events table
-- Insert new event
INSERT INTO Events (eventDate, startTime, endTime, visitingTeamID)
VALUES (:dateEntry, :startTimeEntry, :endTimeEntry, :teamIDEntry);

-- Display all events
SELECT Events.eventID, Events.eventDate, Events.startTime, Events.endTime, Events.visitingTeamID, Teams.teamName 
FROM Events
INNER JOIN Teams ON Events.visitingTeamID = Teams.teamID
ORDER BY eventDate;

-- Get single event by ID for update
SELECT Events.eventID, Events.eventDate, Events.startTime, Events.endTime, Teams.teamID, Teams.teamName
FROM Events
INNER JOIN Teams ON Events.visitingTeamID = Teams.teamID
WHERE Events.eventID = :eventID_from_edit_button;

-- drop down for event showing date and start time
SELECT eventID, CONCAT(eventDate, " ", startTime) as startDateTime FROM Events;

-- drop down for event showing date, time, and visiting team
SELECT eventID, CONCAT(eventDate, ' ', startTime) as startDateTime, 
(SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam 
FROM Events 
ORDER BY startDateTime;

-- Update event
UPDATE Events
SET eventDate = :dateEntry, startTime = :startTimeEntry, endTime = :endTimeEntry, visitingTeamID = :teamIDEntry
WHERE eventID = :eventID_from_edit_button;

-- event date and visiting team for delete confirmation
SELECT Events.eventDate, Teams.teamName
FROM Events
INNER JOIN Teams ON Teams.teamID = Events.visitingTeamID
WHERE eventID = :eventID_from_delete_button;

-- Delete single event by ID
DELETE FROM Events 
WHERE eventID = :eventID_from_delete_button;

------------------------------------------------------------------------
-- EventOutcomes table
-- Insert new EventOutcomes
INSERT INTO EventOutcomes (eventID,winningScore,losingScore)
VALUES (:eventID_from_dropdown, :winEntry, :loseEntry);

-- Display all EventOutcomes and EventOutcomes has Teams
SELECT EventOutcomes.eventOutcomeID, Events.eventID, CONCAT(eventDate,' ', startTime) as startDateTime, 
Teams.teamName AS WinningTeam, 
EventOutcomes.winningScore, 
EventOutcomes.losingScore 
FROM EventOutcomes 
INNER JOIN Events ON Events.eventID = EventOutcomes.eventID 
INNER JOIN EventOutcomesTeams ON EventOutcomesTeams.eventOutcomeID = EventOutcomes.eventOutcomeID 
INNER JOIN Teams ON Teams.teamID = EventOutcomesTeams.teamID AND EventOutcomesTeams.winner = 1 
ORDER BY Events.eventDate ASC;

-- Events without outcomes
-- select events without outcomes
SELECT Events.eventID
FROM Events
WHERE eventID NOT IN (SELECT EventOutcomes.eventID FROM EventOutcomes);

-- EventOutcomes display for Update
SELECT EventOutcomes.eventOutcomeID, Events.eventID, CONCAT(eventDate,' ', startTime) as startDateTime, EventOutcomes.winningScore, EventOutcomes.losingScore,
(SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam
FROM EventOutcomes 
INNER JOIN Events ON Events.eventID = EventOutcomes.eventID 
INNER JOIN EventOutcomesTeams ON EventOutcomesTeams.eventOutcomeID = EventOutcomes.eventOutcomeID
WHERE eventOutcomeID = :eventOutcomeID_from_edit_button
ORDER BY Events.eventDate ASC;

-- drop down for EventOutcomeTeams
SELECT EventOutcomes.eventID, CONCAT(Events.eventDate, ' ', Events.startTime) as startDateTime, EventOutcomes.eventOutcomeID
FROM EventOutcomes
INNER JOIN Events ON Events.eventID = EventOutcomes.eventID 
ORDER BY startDateTime;

-- Update for EventOutcomes
UPDATE EventOutcomes
SET eventID = :eventIDEntry, winningScore = :winEntry, losingScore = :loseEntry
WHERE eventOutcomeID = :eventOutcomeID_from_edit_button;

-- EventOutcomes display for delete
SELECT EventOutcomes.eventOutcomeID, Events.eventID, CONCAT(eventDate,' ', startTime) as startDateTime, EventOutcomes.winningScore, EventOutcomes.losingScore, 
(SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam
FROM EventOutcomes 
INNER JOIN Events ON Events.eventID = EventOutcomes.eventID 
INNER JOIN EventOutcomesTeams ON EventOutcomesTeams.eventOutcomeID = EventOutcomes.eventOutcomeID
WHERE eventID = :eventID_from_delete_button;

-- Delete for EventOutcomes
DELETE FROM EventOutcomes
WHERE eventOutcomeID = :eventOutcomeID_from_delete_button;

-------------------------------------------------------------------
-- EventOutcomesTeams table

-- add new EventOutcomesTeams
-- winning team entry
INSERT INTO EventOutcomesTeams (eventOutcomeID,teamID,winner)
VALUES (:eventOutcomeIDentry, :winningTeamIDentry, 1);
-- losing team entry
INSERT INTO EventOutcomesTeams (eventOutcomeID,teamID,winner)
VALUES (:eventOutcomeIDentry, :losingTeamIDentry, 0);

-- select for table display
SELECT EventOutcomesTeams.eventOutcomesTeamID, EventOutcomesTeams.eventOutcomeID, CONCAT(Events.eventDate, ' ', Events.startTime) as startDateTime, EventOutcomesTeams.teamID, Teams.teamName, EventOutcomesTeams.winner
FROM EventOutcomesTeams
INNER JOIN EventOutcomes ON EventOutcomes.eventOutcomeID = EventOutcomesTeams.eventOutcomeID
INNER JOIN Events ON Events.eventID = EventOutcomes.eventID \
INNER JOIN Teams on Teams.teamID = EventOutcomesTeams.teamID;

-- update for eventOutcomeTeams - winner
UPDATE EventOutcomesTeams
SET teamID = :winningTeamID
WHERE eventOutcomeID = :eventOutcomeID_from_edit_button and winner = 1;

-- update for eventOutcomeTeams - loser
UPDATE EventOutcomesTeams
SET teamID = :losingTeamID
WHERE eventOutcomeID = :eventOutcomeID_from_edit_button and winner = 0;

-- Delete for EventOutcomesTeams
DELETE FROM EventOutcomesTeams
WHERE eventOutcomeID = :eventOutcomeID_from_form;

--------------------------------------------------------------------
-- Tickets table

-- add new tickets - increment seatID to be the next one for the selected event inside Node.js
INSERT INTO Tickets (seatID, eventID, ticketHolderID, ticketTypeID)
VALUES (:nextSeatID,:eventIDentry, :ticketHolderIDentry, :ticketTypeIDentry);

-- figure out last used seatID for an event
SELECT MAX(seatID) FROM Tickets WHERE eventID = :eventIDentry;

-- Display all tickets
SELECT Tickets.ticketID, Tickets.seatID, Tickets.eventID, CONCAT(eventDate, " ", startTime) as startDateTime, 
Tickets.ticketHolderID, CONCAT(TicketHolders.firstName, " ", TicketHolders.lastName) AS fullname,
Tickets.ticketTypeID, TicketTypes.ticketType
FROM Tickets
INNER JOIN Events ON Events.eventID = Tickets.eventID
INNER JOIN TicketHolders ON TicketHolders.ticketHolderID = Tickets.ticketHolderID
INNER JOIN TicketTypes ON TicketTypes.ticketTypeID = Tickets.ticketTypeID
ORDER BY Events.eventDate ASC, TicketHolders.lastName ASC; 

-- Update for tickets
UPDATE Tickets
SET eventID = :eventIDentry, ticketHolderID = :ticketHolderIDentry, ticketTypeID = :ticketTypeIDentry
WHERE ticketID = :ticketIDentry;

-- Display for ticket delete
SELECT Tickets.ticketID,CONCAT(TicketHolders.firstName, " ", TicketHolders.lastName) AS fullname, 
(SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam,
Tickets.eventID,CONCAT(Events.eventDate, " ", Events.startTime) as startDateTime
FROM Tickets
INNER JOIN TicketHolders ON TicketHolders.ticketHolderID = Tickets.ticketHolderID
INNER JOIN Events ON Events.eventID = Tickets.eventID
WHERE ticketID = :ticketID_from_delete_button;

-- Delete for tickets
DELETE FROM Tickets
WHERE ticketID = :ticketID_from_delete_button;

------------------------------------------------------------------
-- Teams queries
-- Add Team
INSERT INTO Teams (teamName)
VALUES (:teamNameEntry);

-- For Drop down and display of all teams
SELECT teamID, teamName FROM Teams;

-- Winning team select for Event Outcome and Event Outcomes Teams Update
SELECT teamID, teamName FROM Teams
WHERE teamID = (SELECT teamID FROM EventOutcomesTeams WHERE eventOutcomeID = :eventOutcomeID_from_edit_button AND winner = 1);

-- Losing team select for Event Outcome and Event Outcomes Teams Update
SELECT teamID, teamName FROM Teams 
WHERE teamID = (SELECT teamID FROM EventOutcomesTeams WHERE eventOutcomeID = :eventOutcomeID_from_edit_button AND winner = 0);

-- Update for Teams
UPDATE Teams
SET teamName = :teamNameEntry
WHERE teamID = :teamID_from_edit_button;

-- Delete for Teams
DELETE FROM Teams
WHERE teamID = :teamID_from_delete_button;

----------------------------------------------------------------------
-- TicketTypes queries

-- drop down and display for all ticket types
SELECT ticketTypeID, ticketType, price FROM TicketTypes;

-- new ticket type
INSERT INTO TicketTypes (ticketType, price)
VALUES (:ticketTypeEntry, :priceEntry);

-- select one ticket type for update
SELECT ticketTypeID, ticketType, price 
FROM TicketTypes
WHERE ticketTypeID = :ticketTypeID_from_edit_button;

-- update ticket type
UPDATE TicketTypes
SET ticketType = :ticketTypeEntry, price = :priceEntry
WHERE ticketTypeID = :ticketTypeID_from_edit_button;

-- select one ticket type for delete
SELECT ticketTypeID, ticketType
FROM TicketTypes
WHERE ticketTypeID = :ticketTypeID_from_delete_button;

-- Delete one ticket type
DELETE FROM TicketTypes
WHERE ticketTypeID = :ticketTypeID_from_delete_button;

----------------------------------------------------------------------
-- Ticket Holder Queries

-- Display all ticket holders
SELECT ticketHolderID as 'ID', firstName as 'First Name', lastName as 'Last Name', phone as 'Phone', email as 'Email' FROM TicketHolders;

-- Add new ticket holder - complete
INSERT INTO TicketHolders (firstName, lastName, phone, email)
VALUES (:firstNameEntry, :lastNameEntry, :phoneEntry, :emailEntry);

-- Add new ticket holder - no phone
INSERT INTO TicketHolders (firstName, lastName, email)
VALUES (:firstNameEntry, :lastNameEntry, :emailEntry);

-- drop down for ticket holder with full name
SELECT ticketHolderID, CONCAT(firstName, " ", lastName) AS fullname FROM TicketHolders;

-- find ticket holder display
SELECT ticketHolderID, firstName, lastName
FROM TicketHolders
WHERE firstName = :firstNameEntry AND lastName = :lastNameEntry;

-- ticket holder display for update
SELECT ticketHolderID, firstName, lastName, phone, email
FROM TicketHolders
WHERE ticketHolderID = :ticketHolderID_from_edit_button;

UPDATE TicketHolders
SET firstName = :firstNameEntry, lastName = :lastNameEntry, phone = :phoneEntry, email = :emailEntry
WHERE ticketHolderID = :ticketHolderID_from_edit_button;

-- ticket holder display for delete
SELECT ticketHolderID, CONCAT(firstName, " ", lastName) AS fullname
FROM TicketHolders
WHERE ticketHolderID = :ticketHolderID_from_delete_button;

-- Delete individual ticket holder
DELETE FROM TicketHolders
WHERE ticketHolderID = :ticketHolderID_from_delete_button;
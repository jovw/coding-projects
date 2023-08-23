# Citation
# Date: 6/28/23
# Structure Based on
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app
# Changes: modified to use my username and password; different port number; new form attributes, new queries

from flask import Flask, render_template, json, redirect, request, jsonify
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_'  #fill in onid after _
app.config['MYSQL_PASSWORD'] = '' #last 4 of onid
app.config['MYSQL_DB'] = 'cs340_' #fill in onid after _
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)

# Routes
@app.route('/')
def root():
    return render_template("main.j2")

### event outcome has teams ###							   
@app.route("/eventoutcomesteams", methods=["POST", "GET"])
def eventoutcomesteams():
    if request.method == "GET":
        eventoutcomesteams_select = "SELECT EventOutcomesTeams.eventOutcomesTeamID, EventOutcomesTeams.eventOutcomeID, \
        CONCAT(Events.eventDate, ' ', Events.startTime) as 'Start Date Time', \
        EventOutcomesTeams.teamID as 'Team ID', Teams.teamName as 'Team Name', EventOutcomesTeams.winner as 'Winner'\
        FROM EventOutcomesTeams\
        INNER JOIN EventOutcomes ON EventOutcomes.eventOutcomeID = EventOutcomesTeams.eventOutcomeID \
        INNER JOIN Events ON Events.eventID = EventOutcomes.eventID \
        INNER JOIN Teams on Teams.teamID = EventOutcomesTeams.teamID;"
        cur = mysql.connection.cursor()
        cur.execute(eventoutcomesteams_select)
        eventoutcomesteamsData = cur.fetchall()

        # only include events in dropdown with eventOutcomeID
        event_data_dropdown = "SELECT EventOutcomes.eventID, \
        CONCAT(Events.eventDate, ' ', Events.startTime) as startDateTime, \
        EventOutcomes.eventOutcomeID\
        FROM EventOutcomes \
        INNER JOIN Events ON Events.eventID = EventOutcomes.eventID \
        ORDER BY startDateTime;"
        cur.execute(event_data_dropdown)
        eventsData = cur.fetchall()

        team_name_dropdown = "SELECT teamID, teamName FROM Teams"
        cur.execute(team_name_dropdown)
        teamsData = cur.fetchall()

        return render_template("eventoutcomesteams.j2", eventoutcomesteamsData=eventoutcomesteamsData, teamsData=teamsData, eventsData=eventsData)

    if request.method == "POST":
        if request.form.get("addEventOutcomesTeams"):
            # get inputs
            eventOutcomeID = request.form["eventDateDropdown"]
            winningTeamID = request.form["winningTeamDropdown"]
            losingTeamID = request.form["losingTeamDropdown"]

            # Insert winner into EventOutcomesTeams table
            query_event_outcomes_teams = "INSERT INTO \
            EventOutcomesTeams (eventOutcomeID, teamID, winner) \
            VALUES (%s, %s, %s)"
            params_event_outcomes_teams = (eventOutcomeID, winningTeamID, 1)
            cur = mysql.connection.cursor()
            cur.execute(query_event_outcomes_teams, params_event_outcomes_teams)
            mysql.connection.commit()

            # Insert loser into EventOutcomesTeams table
            query_event_outcomes_teams = "INSERT INTO \
            EventOutcomesTeams (eventOutcomeID, teamID, winner) \
            VALUES (%s, %s, %s)"
            params_event_outcomes_teams = (eventOutcomeID, losingTeamID, 0)
            cur.execute(query_event_outcomes_teams, params_event_outcomes_teams)
            mysql.connection.commit()

            return redirect("/eventoutcomesteams")

### events ###
@app.route("/events", methods=["POST", "GET"])
def events():
    if request.method == "GET":
        select_all = "SELECT Events.eventID as 'Event ID', Events.eventDate as 'Event Date', \
        Events.startTime as 'Start Time', Events.endTime as 'End Time', Events.visitingTeamID as 'Visiting Team ID', Teams.teamName as 'Team Name'\
        FROM Events \
        INNER JOIN Teams ON Events.visitingTeamID = Teams.teamID \
        ORDER BY eventDate;"
        cur = mysql.connection.cursor()
        cur.execute(select_all)
        eventsData = cur.fetchall()

        team_name_dropdown = "SELECT teamID, teamName FROM Teams;"
        cur.execute(team_name_dropdown)
        teamsData = cur.fetchall()

        return render_template("events.j2", eventsData=eventsData, teamsData=teamsData)

    if request.method == "POST":
        if request.form.get("addEvent"):
            eventDate = request.form["eventDate"]
            startTime = request.form["startTime"]
            endTime = request.form["endTime"]
            visitingTeamID = request.form["visitingTeamDropdown"]

            query_insert_event = "INSERT INTO Events (eventDate, startTime, endTime, visitingTeamID) \
                            VALUES (%s, %s, %s, %s);"
            params_insert_event = (eventDate, startTime, endTime, visitingTeamID)
            cur = mysql.connection.cursor()
            cur.execute(query_insert_event, params_insert_event)
            mysql.connection.commit()

            return redirect("/events")

### event outcomes ###
@app.route("/eventOutcomes", methods=["POST", "GET"])
def eventOutcomes():
    # if POST method 
    if request.method == "POST":
        if request.form.get("addEventOutcome"):
            # get inputs
            eventID = request.form["eventDateDropdown"]
            winningScore = request.form["winningScore"]
            losingScore = request.form["losingScore"]
            winningTeamID = request.form["winningTeamDropdown"]
            losingTeamID = request.form["losingTeamDropdown"]

            # all values cannot be null
            #insert into eventOutcomes table
            query_event_outcomes = "INSERT INTO \
            EventOutcomes (eventID, winningScore, losingScore) \
            VALUES (%s, %s, %s)"
            params_event_outcomes = (eventID, winningScore, losingScore)
            cur = mysql.connection.cursor()
            cur.execute(query_event_outcomes, params_event_outcomes)
            mysql.connection.commit()

            # Get the newly inserted eventOutcomeID
            eventOutcomeID = cur.lastrowid

            # Insert winner into EventOutcomesTeams table
            query_event_outcomes_teams = "INSERT INTO \
            EventOutcomesTeams (eventOutcomeID, teamID, winner) \
            VALUES (%s, %s, %s)"
            params_event_outcomes_teams = (eventOutcomeID, winningTeamID, 1)
            cur = mysql.connection.cursor()
            cur.execute(query_event_outcomes_teams, params_event_outcomes_teams)
            mysql.connection.commit()

            # Insert loser into EventOutcomesTeams table
            query_event_outcomes_teams = "INSERT INTO \
            EventOutcomesTeams (eventOutcomeID, teamID, winner) \
            VALUES (%s, %s, %s)"
            params_event_outcomes_teams = (eventOutcomeID, losingTeamID, 0)
            cur.execute(query_event_outcomes_teams, params_event_outcomes_teams)
            mysql.connection.commit()

            return redirect("/eventOutcomes")

    # if GET method
    if request.method == "GET":
        # grab all entries 
        select_all = "SELECT EventOutcomes.eventOutcomeID, Events.eventID, CONCAT(eventDate,' ', startTime) as 'Start Date Time', \
            Teams.teamName AS 'Winning Team', \
            EventOutcomes.winningScore as 'Winning Score', \
            EventOutcomes.losingScore as 'Losing Score' \
            FROM EventOutcomes \
            INNER JOIN Events ON Events.eventID = EventOutcomes.eventID \
            INNER JOIN EventOutcomesTeams ON EventOutcomesTeams.eventOutcomeID = EventOutcomes.eventOutcomeID \
            INNER JOIN Teams ON Teams.teamID = EventOutcomesTeams.teamID AND EventOutcomesTeams.winner = 1 \
            ORDER BY Events.eventDate ASC;"
        cur = mysql.connection.cursor()
        cur.execute(select_all)
        eventOutcomesData = cur.fetchall()

        # select events without outcomes
        select_available = "SELECT Events.eventID\
        FROM Events \
        WHERE eventID NOT IN (SELECT EventOutcomes.eventID FROM EventOutcomes);"
        cur.execute(select_available)
        availableEventsData = cur.fetchall()

        event_data_dropdown = "SELECT eventID, CONCAT(eventDate, ' ', startTime) as startDateTime, \
        (SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam \
        FROM Events ORDER BY startDateTime;"
        cur.execute(event_data_dropdown)
        eventsData = cur.fetchall()

        team_name_dropdown = "SELECT teamID, teamName FROM Teams"
        cur.execute(team_name_dropdown)
        teamsData = cur.fetchall()

        # render info on eventOutcome page
        return render_template("eventOutcomes.j2", eventOutcomesData=eventOutcomesData, eventsData=eventsData, teamsData=teamsData, availableEventsData=availableEventsData)

### update event outcomes ###
@app.route("/updateEventOutcome/<int:eventOutcomeID>", methods=["POST", "GET"])
def updateEventOutcome(eventOutcomeID):
    if request.method == "GET":
        # Grab relevant entry
        select_one = "SELECT EventOutcomes.eventOutcomeID, Events.eventID, CONCAT(eventDate,' ', startTime) as startDateTime, \
        EventOutcomes.winningScore, \
        EventOutcomes.losingScore, \
        (SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam\
        FROM EventOutcomes \
        INNER JOIN Events ON Events.eventID = EventOutcomes.eventID \
        INNER JOIN EventOutcomesTeams ON EventOutcomesTeams.eventOutcomeID = EventOutcomes.eventOutcomeID \
        WHERE EventOutcomes.eventOutcomeID = %s \
        ORDER BY Events.eventDate ASC;"
        cur = mysql.connection.cursor()
        cur.execute(select_one, (eventOutcomeID,))
        eventOutcomesData = cur.fetchall()

        winning_team_select = "SELECT teamID, teamName FROM Teams \
        WHERE teamID = (SELECT teamID FROM EventOutcomesTeams WHERE eventOutcomeID = %s AND winner = 1);"
        cur.execute(winning_team_select, (eventOutcomeID,))
        winningTeam = cur.fetchall()
        
        losing_team_select = "SELECT teamID, teamName FROM Teams \
        WHERE teamID = (SELECT teamID FROM EventOutcomesTeams WHERE eventOutcomeID = %s AND winner = 0);"
        cur.execute(losing_team_select, (eventOutcomeID,))
        losingTeam = cur.fetchall()

        event_data_dropdown = "SELECT eventID, CONCAT(eventDate, ' ', startTime) as startDateTime,\
        (SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam\
        FROM Events"
        cur.execute(event_data_dropdown)
        eventsData = cur.fetchall()

        select_available = "SELECT Events.eventID\
        FROM Events \
        WHERE eventID NOT IN (SELECT EventOutcomes.eventID FROM EventOutcomes);"
        cur.execute(select_available)
        availableEventsData = cur.fetchall()

        team_name_dropdown = "SELECT teamID, teamName FROM Teams"
        cur.execute(team_name_dropdown)
        teamsData = cur.fetchall()        

        # Render pass data based on ID
        return render_template("updateEventOutcome.j2", eventOutcomesData=eventOutcomesData, eventsData=eventsData, teamsData=teamsData, winningTeam=winningTeam,losingTeam=losingTeam, availableEventsData=availableEventsData)

    # If POST
    if request.method == "POST":
        # Fire off if user clicks the 'Update Event Outcome' button
        if request.form.get("updateEventOutcome"):

            # get inputs
            eventOutcomeID = request.form["eventOutcomeID"]
            eventID = request.form["eventDateDropdown"]
            winningScore = request.form["winningScore"]
            losingScore = request.form["losingScore"]

            # update eventOutcomes table
            query_event_outcomes_update = "UPDATE EventOutcomes SET eventID = %s, winningScore = %s, losingScore = %s WHERE eventOutcomeID = %s;"
            params_event_outcomes = (eventID, winningScore, losingScore, eventOutcomeID)
            cur = mysql.connection.cursor()
            cur.execute(query_event_outcomes_update, params_event_outcomes)
            mysql.connection.commit()

            # Update eventoutcomes has teams
            winningTeamID = request.form["winningTeamDropdown"]
            query_winner_event_outcomes_teams_update = "UPDATE EventOutcomesTeams SET teamID = %s \
                                            WHERE eventOutcomeID = %s AND winner = 1;"
            params_winner_event_outcomes_teams = (winningTeamID, eventOutcomeID)
            cur.execute(query_winner_event_outcomes_teams_update, params_winner_event_outcomes_teams)
            mysql.connection.commit()

            losingTeamID = request.form["losingTeamDropdown"]
            query_loser_event_outcomes_teams_update = "UPDATE EventOutcomesTeams SET teamID = %s\
                                            WHERE eventOutcomeID = %s AND winner = 0;"
            params_loser_event_outcomes_teams = (losingTeamID, eventOutcomeID)
            cur.execute(query_loser_event_outcomes_teams_update, params_loser_event_outcomes_teams)
            mysql.connection.commit()

            return redirect("/eventOutcomes")

### delete event outcomes ###
@app.route("/deleteEventOutcome", methods=["GET", "POST"])
def delete_eventoutcome():
    if request.method == "POST":
        eventOutcomeID = int(request.form.get("eventOutcomeID"))
        # mySQL query to delete the event outcome with the passed id
        query = "DELETE FROM EventOutcomes WHERE eventOutcomeID = %s;"
        cur = mysql.connection.cursor()
        cur.execute(query, (eventOutcomeID,))
        mysql.connection.commit()

        # delete entry from intersection table
        query_intersection = "DELETE FROM EventOutcomesTeams WHERE eventOutcomeID = %s;"
        cur.execute(query, (eventOutcomeID,))
        mysql.connection.commit()

        # Redirect back to the eventOutcomes page after deletion
        return redirect("/eventOutcomes")

    if request.method == "GET":
    # If it's a GET request, fetch the necessary data and render the template
        eventOutcomeID = int(request.args.get("eventOutcomeID"))
        eventID = int(request.args.get("eventID"))

        # Grab relevant entry
        select_one = "SELECT EventOutcomes.eventOutcomeID, Events.eventID, CONCAT(eventDate,' ', startTime) as startDateTime, \
                EventOutcomes.winningScore, \
                EventOutcomes.losingScore, \
                (SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam\
                FROM EventOutcomes \
                INNER JOIN Events ON Events.eventID = EventOutcomes.eventID \
                INNER JOIN EventOutcomesTeams ON EventOutcomesTeams.eventOutcomeID = EventOutcomes.eventOutcomeID \
                WHERE EventOutcomes.eventOutcomeID = %s;"
        cur = mysql.connection.cursor()
        cur.execute(select_one, (eventOutcomeID,))
        eventOutcomesData = cur.fetchall()

        winning_team_select = "SELECT teamID, teamName FROM Teams \
        WHERE teamID = (SELECT teamID FROM EventOutcomesTeams WHERE eventOutcomeID = %s AND winner = 1);"
        cur.execute(winning_team_select, (eventOutcomeID,))
        winningTeam = cur.fetchall()
        
        losing_team_select = "SELECT teamID, teamName FROM Teams \
        WHERE teamID = (SELECT teamID FROM EventOutcomesTeams WHERE eventOutcomeID = %s AND winner = 0);"
        cur.execute(losing_team_select, (eventOutcomeID,))
        losingTeam = cur.fetchall()
        
        event_information_query = "SELECT eventID, CONCAT(eventDate, ' ', startTime) as startDateTime FROM Events WHERE eventID = %s"
        cur.execute(event_information_query, (eventID,))
        eventsData = cur.fetchall()

        return render_template("deleteEventOutcome.j2", eventOutcomeID=eventOutcomeID, eventOutcomesData=eventOutcomesData, winningTeam=winningTeam, losingTeam=losingTeam)

### ticket types ###
@app.route("/ticketTypes", methods=["POST", "GET"])
def ticketTypes():
    if request.method == "GET":
        ticketTypes_select = "SELECT ticketTypeID as 'Ticket Type ID', ticketType as 'Ticket Type', price as 'Price' FROM TicketTypes;"
        cur = mysql.connection.cursor()
        cur.execute(ticketTypes_select)
        ticketTypesData = cur.fetchall()

        return render_template("ticketTypes.j2", ticketTypesData=ticketTypesData)

    if request.method == "POST":
        if request.form.get("addTicketType"):
            # get inputs
            ticketType = request.form["ticketType"]
            price = request.form["price"]

            # Insert into Ticket Types table
            ticketTypes_insert = "INSERT INTO \
            TicketTypes (ticketType, price) \
            VALUES (%s, %s)"
            params_ticket_types = (ticketType, price)
            cur = mysql.connection.cursor()
            cur.execute(ticketTypes_insert, params_ticket_types)
            mysql.connection.commit()

            return redirect("/ticketTypes")

### teams ###
@app.route("/teams", methods=["POST", "GET"])
def teams():
    if request.method == "GET":
        team_select = "SELECT teamID as 'Team ID', teamName as 'Team Name' FROM Teams"
        cur = mysql.connection.cursor()
        cur.execute(team_select)
        teamsData = cur.fetchall()

        return render_template("teams.j2", teamsData=teamsData)

    if request.method == "POST":
        if request.form.get("addTeam"):
            # get inputs
            teamName = request.form["teamName"]

            # Insert into Teams table - see different structure for only one attribute
            teams_insert = "INSERT INTO \
            Teams (teamName) \
            VALUES (%s);"
            cur = mysql.connection.cursor()
            cur.execute(teams_insert, (teamName,))
            mysql.connection.commit()

            return redirect("/teams")

### get teams for events ###
@app.route("/get_teams_for_event/<int:eventID>")
def get_teams_for_event(eventID):
    query = "SELECT Teams.teamID, Teams.teamName FROM Teams " \
            "INNER JOIN Events ON Teams.teamID = Events.visitingTeamID " \
            "WHERE Events.eventID = %s"
    cur = mysql.connection.cursor()
    cur.execute(query, (eventID,))
    teamsData = cur.fetchall()
    return jsonify(teamsData)

### ticket holders ###
@app.route("/ticketHolders", methods = ["POST", "GET"])
def ticketHolders():
    if request.method == "GET":
        ticketholders_select = "SELECT ticketHolderID as 'ID', firstName as 'First Name', lastName as 'Last Name', phone as 'Phone', email as 'Email' FROM TicketHolders"
        cur = mysql.connection.cursor()
        cur.execute(ticketholders_select)
        ticketHolderData = cur.fetchall()
    
        return render_template("ticketHolders.j2", ticketHolderData=ticketHolderData)

    if request.method == "POST":
        if request.form.get("addTicketHolder"):
            firstName = request.form["firstName"]
            lastName = request.form["lastName"]
            phone = request.form["phone"]
            email = request.form["email"]

            if phone == "":
                ticketHolder_insert = "INSERT INTO TicketHolders (firstName,lastName,email) VALUES (%s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(ticketHolder_insert, (firstName, lastName, email,))
                mysql.connection.commit()

            else: 
                ticketHolder_insert = "INSERT INTO TicketHolders (firstName, lastName, phone, email) VALUES (%s, %s, %s, %s)"
                cur = mysql.connection.cursor()
                cur.execute(ticketHolder_insert, (firstName, lastName, phone, email,))
                mysql.connection.commit()

            return redirect("/ticketHolders")

### tickets ###
@app.route("/tickets", methods = ["POST", "GET"])
def tickets():
    if request.method == "GET": 
        tickets_select = "SELECT \
                            Tickets.ticketID, \
                            Tickets.seatID AS 'Seat ID', \
                            Tickets.eventID AS 'Event ID', \
                            CONCAT(eventDate, ' ', startTime) as 'Start Date Time', \
                            Tickets.ticketHolderID AS 'Ticket Holder ID', \
                            CONCAT(TicketHolders.firstName, ' ', TicketHolders.lastName) AS 'Full Name', \
                            Tickets.ticketTypeID AS 'Ticket Type ID', \
                            TicketTypes.ticketType AS 'Ticket Type' \
                        FROM Tickets \
                        INNER JOIN Events ON Events.eventID = Tickets.eventID \
                        LEFT JOIN TicketHolders ON TicketHolders.ticketHolderID = Tickets.ticketHolderID \
                        INNER JOIN TicketTypes ON TicketTypes.ticketTypeID = Tickets.ticketTypeID \
                        ORDER BY Events.eventDate ASC, TicketHolders.lastName ASC; "
        cur = mysql.connection.cursor()
        cur.execute(tickets_select)
        ticketData = cur.fetchall()
    
        return render_template("tickets.j2", ticketData=ticketData)

@app.route("/insertTicket", methods = ["POST", "GET"])
def insertTicket():
    if request.method == "GET": 
        cur = mysql.connection.cursor()

        event_data_dropdown = "SELECT eventID, CONCAT(eventDate, ' ', startTime) as startDateTime, \
        (SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam \
        FROM Events ORDER BY startDateTime;"
        cur.execute(event_data_dropdown)
        eventsData = cur.fetchall()

        tickettype_data_dropdown = "SELECT ticketTypeID, ticketType, price FROM TicketTypes;"
        cur.execute(tickettype_data_dropdown)
        ticketTypeData = cur.fetchall()
    
        return render_template("insertTicket.j2", eventsData=eventsData, ticketTypeData=ticketTypeData)

    if request.method == "POST":
        if request.form.get("searchTicketHolder"):
            tickets_select = "SELECT \
                            Tickets.ticketID, \
                            Tickets.seatID AS 'Seat ID', \
                            Tickets.eventID AS 'Event ID', \
                            CONCAT(eventDate, ' ', startTime) as 'Start Date Time', \
                            Tickets.ticketHolderID AS 'Ticket Holder ID', \
                            CONCAT(TicketHolders.firstName, ' ', TicketHolders.lastName) AS 'Full Name', \
                            Tickets.ticketTypeID AS 'Ticket Type ID', \
                            TicketTypes.ticketType AS 'Ticket Type' \
                        FROM Tickets \
                        INNER JOIN Events ON Events.eventID = Tickets.eventID \
                        LEFT JOIN TicketHolders ON TicketHolders.ticketHolderID = Tickets.ticketHolderID \
                        INNER JOIN TicketTypes ON TicketTypes.ticketTypeID = Tickets.ticketTypeID \
                        ORDER BY Events.eventDate ASC, TicketHolders.lastName ASC; "
            cur = mysql.connection.cursor()
            cur.execute(tickets_select)
            ticketData = cur.fetchall()

            # Get the first name and last name from the submitted form
            firstNameEntry = request.form.get("firstName")
            lastNameEntry = request.form.get("lastName")
            
            # Update your SQL query to use placeholders and parameters
            search_ticketholder = "SELECT ticketHolderID, firstName, lastName \
                                FROM TicketHolders \
                                WHERE firstName = %s AND lastName = %s;"
            
            cur = mysql.connection.cursor()
            cur.execute(search_ticketholder, (firstNameEntry, lastNameEntry,))
            searchData = cur.fetchall()

            event_data_dropdown = "SELECT eventID, CONCAT(eventDate, ' ', startTime) as startDateTime, \
                        (SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam \
                        FROM Events ORDER BY startDateTime;"
            cur.execute(event_data_dropdown)
            eventsData = cur.fetchall()

            tickettype_data_dropdown = "SELECT ticketTypeID, ticketType, price FROM TicketTypes;"
            cur.execute(tickettype_data_dropdown)
            ticketTypeData = cur.fetchall()
            cur.close()

            # Return the search results to your template
            if not searchData:
                return render_template("insertTicket.j2", noResults=True, eventsData=eventsData, ticketTypeData=ticketTypeData, ticketData=ticketData)
            else:
                return render_template("insertTicket.j2", searchData=searchData, eventsData=eventsData, ticketTypeData=ticketTypeData, ticketData=ticketData)

        if request.form.get("addTicket"):
            eventID = request.form["eventID"]
            ticketHolderID = request.form["ticketHolderID"]  # You'll need to get this value from the form
            ticketTypeID = request.form["ticketTypeDropdown"]

            cur = mysql.connection.cursor()

            next_seat = "SELECT MAX(seatID) + 1 as 'seatID' FROM Tickets WHERE eventID = %s"
            cur.execute(next_seat, (eventID,))
            nextSeatRes = cur.fetchone()
            next_seat_id = nextSeatRes['seatID']

            if next_seat_id is None:
                next_seat_id = 1

            if ticketHolderID == "":
                ticket_insert = "INSERT INTO Tickets (seatID, eventID, ticketTypeID) \
                            VALUES (%s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(ticket_insert, (next_seat_id, eventID, ticketTypeID,))
                mysql.connection.commit()
                cur.close()
            else:
                ticket_insert = "INSERT INTO Tickets (seatID, eventID, ticketHolderID, ticketTypeID) \
                            VALUES (%s, %s, %s, %s);"
                cur = mysql.connection.cursor()
                cur.execute(ticket_insert, (next_seat_id, eventID, ticketHolderID, ticketTypeID,))
                mysql.connection.commit()
                cur.close()

            return redirect("/tickets")

@app.route("/updateTicket/<int:ticketID>", methods = ["POST", "GET"])
def updateTicket(ticketID):
    if request.method == "POST":
        if request.form.get("searchTicketHolder"):
            ticket_select = "SELECT \
                            Tickets.ticketID, \
                            Tickets.seatID AS 'Seat ID', \
                            Tickets.eventID AS 'Event ID', \
                            CONCAT(eventDate, ' ', startTime) as 'Start Date Time', \
                            Tickets.ticketHolderID AS 'Ticket Holder ID', \
                            CONCAT(TicketHolders.firstName, ' ', TicketHolders.lastName) AS 'Full Name', \
                            Tickets.ticketTypeID AS 'Ticket Type ID', \
                            TicketTypes.ticketType AS 'Ticket Type' \
                        FROM Tickets \
                        INNER JOIN Events ON Events.eventID = Tickets.eventID \
                        LEFT JOIN TicketHolders ON TicketHolders.ticketHolderID = Tickets.ticketHolderID \
                        INNER JOIN TicketTypes ON TicketTypes.ticketTypeID = Tickets.ticketTypeID \
                        WHERE Tickets.ticketID = %s \
                        ORDER BY Events.eventDate ASC, TicketHolders.lastName ASC; "
            cur = mysql.connection.cursor()
            cur.execute(ticket_select, (ticketID,))
            ticketData = cur.fetchall()

            # Get the first name and last name from the submitted form
            firstNameEntry = request.form.get("firstName")
            lastNameEntry = request.form.get("lastName")
            
            # Update your SQL query to use placeholders and parameters
            search_ticketholder = "SELECT ticketHolderID, firstName, lastName \
                                FROM TicketHolders \
                                WHERE firstName = %s AND lastName = %s;"
            
            cur = mysql.connection.cursor()
            cur.execute(search_ticketholder, (firstNameEntry, lastNameEntry,))
            searchData = cur.fetchall()


            event_data_dropdown = "SELECT eventID, CONCAT(eventDate, ' ', startTime) as startDateTime, \
                        (SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam \
                        FROM Events ORDER BY startDateTime;"
            cur.execute(event_data_dropdown)
            eventsData = cur.fetchall()

            tickettype_data_dropdown = "SELECT ticketTypeID, ticketType, price FROM TicketTypes;"
            cur.execute(tickettype_data_dropdown)
            ticketTypeData = cur.fetchall()
            cur.close()

            # Return the search results to your template
            if not searchData:
                return render_template("updateTicket.j2", noResults=True, eventsData=eventsData, ticketTypeData=ticketTypeData, ticketData=ticketData)
            else:
                return render_template("updateTicket.j2", searchData=searchData, eventsData=eventsData, ticketTypeData=ticketTypeData, ticketData=ticketData)

        if request.form.get("updateTicket"):
            # Get the form data from the submitted form
            eventID = request.form["eventID"]
            ticketHolderID = request.form["ticketHolderID"]
            ticketTypeID = request.form["ticketTypeDropdown"]
            ticketID = request.form["ticketID"]
            seatID = request.form["seatID"]

            # Fetch the old eventID from the database
            cur = mysql.connection.cursor()
            cur.execute("SELECT eventID FROM Tickets WHERE ticketID = %s", (ticketID,))
            oldEvent = cur.fetchone()
            oldEventID = oldEvent['eventID']

            if int(eventID) != int(oldEventID):
                next_seat_2 = "SELECT MAX(seatID) + 1 as 'seatID' FROM Tickets WHERE eventID = %s"
                cur.execute(next_seat_2, (eventID,))
                nextSeatRes_2 = cur.fetchone()
                seatID = nextSeatRes_2['seatID']
            
            if not ticketHolderID: 
                update_query = "UPDATE Tickets \
                        SET eventID = %s, ticketTypeID = %s, seatID = %s, ticketHolderID = NULL \
                        WHERE ticketID = %s"
                cur = mysql.connection.cursor()
                cur.execute(update_query, (eventID, ticketTypeID, seatID, ticketID,))
                mysql.connection.commit()
            else:
                update_query = "UPDATE Tickets \
                        SET eventID = %s, ticketHolderID = %s, ticketTypeID = %s, seatID = %s \
                        WHERE ticketID = %s"
                cur = mysql.connection.cursor()
                cur.execute(update_query, (eventID, ticketHolderID, ticketTypeID, seatID, ticketID,))
                mysql.connection.commit()

            return redirect('/tickets')
    
    if request.method == "GET": 
        ticket_select = "SELECT \
                            Tickets.ticketID, \
                            Tickets.seatID AS 'Seat ID', \
                            Tickets.eventID AS 'Event ID', \
                            CONCAT(eventDate, ' ', startTime) as 'Start Date Time', \
                            Tickets.ticketHolderID AS 'Ticket Holder ID', \
                            CONCAT(TicketHolders.firstName, ' ', TicketHolders.lastName) AS 'Full Name', \
                            Tickets.ticketTypeID AS 'Ticket Type ID', \
                            TicketTypes.ticketType AS 'Ticket Type' \
                        FROM Tickets \
                        INNER JOIN Events ON Events.eventID = Tickets.eventID \
                        LEFT JOIN TicketHolders ON TicketHolders.ticketHolderID = Tickets.ticketHolderID \
                        INNER JOIN TicketTypes ON TicketTypes.ticketTypeID = Tickets.ticketTypeID \
                        WHERE Tickets.ticketID = %s \
                        ORDER BY Events.eventDate ASC, TicketHolders.lastName ASC; "
        cur = mysql.connection.cursor()
        cur.execute(ticket_select, (ticketID,))
        ticketData = cur.fetchall()

        event_data_dropdown = "SELECT eventID, CONCAT(eventDate, ' ', startTime) as startDateTime, \
        (SELECT Teams.teamName FROM Teams WHERE Teams.teamID = Events.visitingTeamID) AS visitingTeam \
        FROM Events ORDER BY startDateTime;"
        cur.execute(event_data_dropdown)
        eventsData = cur.fetchall()

        tickettype_data_dropdown = "SELECT ticketTypeID, ticketType, price FROM TicketTypes;"
        cur.execute(tickettype_data_dropdown)
        ticketTypeData = cur.fetchall()
    
        return render_template("updateTicket.j2", ticketData=ticketData, eventsData=eventsData, ticketTypeData=ticketTypeData)
        
# Listener
if __name__ == "__main__":
    # 1024 < PORT < 65535 is acceptable, debug=True means reload on changes
    app.run(port=7569, debug=True)
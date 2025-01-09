# Tracking tickets by event for Gill Coliseum
by Juanette van Wyk & Cara Walter

## Project Purpose
Create a web-based interface to a database with entities. The project is written in Flask using Python and a MySQL database. 

## Overview 
Gill Coliseum hosts events for 5 sports (women and men’s basketball, wrestling, women’s gymnastics, and volleyball) at Oregon State University in Corvallis, OR. With a capacity of 9,301, and each sport hosting multiple events (at least 5) per season, the managers of Gill Coliseum would benefit from a web based database for tracking tickets and ticket holders by event as well as teams and outcomes for each event. This database will focus on events with up to two teams for volleyball only. Ticket holder information is optional as it will not be collected for tickets purchased at the event. With this database, managers could evaluate the draw of different visiting teams, event day and time, season ticket vs event ticket sales, and look at trends over a season relative to team performance.

## Citation
The code for the read tables for each entity template was copied with minor modification 7/25/23 from the CS340 Flask Starter app, specifically people.j2 at https://github.com/osu-cs340-ecampus/flask-starter-app/blob/89e5a326cb1e5cfe6b87168be1ffad4fb3e33673/bsg_people_app/templates/people.j2. The structure of the app.py code was based on while the imports, database connection commands, listener were copied from the CS340 Flask Starter app on 7/25/23, specifically the bsg_people_app/app.py at https://github.com/osu-cs340-ecampus/flask-starter-app/blob/89e5a326cb1e5cfe6b87168be1ffad4fb3e33673/bsg_people_app/app.py. 
The structure of the forms for each entity template were based on the CS340 Flask Starter app on 7/25/23, specifically people.j2 at https://github.com/osu-cs340-ecampus/flask-starter-app/blob/89e5a326cb1e5cfe6b87168be1ffad4fb3e33673/bsg_people_app/templates/people.j2 and edit_people.j2 at https://github.com/osu-cs340-ecampus/flask-starter-app/blob/89e5a326cb1e5cfe6b87168be1ffad4fb3e33673/bsg_people_app/templates/edit_people.j2
The styling, navigation, queries, and form content are original.

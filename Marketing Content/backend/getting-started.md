# Node.js Backend Startup

Instructions on getting the backend server running on your machine

## Prerequisites

Before you begin, ensure you have Node.js and npm installed on your system.

# Installation

## Clone the repository to your local machine

git clone https://github.com/jcjc2019/marketing_content_generator.git <br />
cd into marketing_content_generator/backend

## Install the required npm packages

npm install

## Create a .env file

Create a .env in /backend with the below variables. You can use .env.example as a template. Replace the respective values with their secret. Do not use quotation marks around the values. <br />
<br />
CLIENT_ID = Your Google app client ID <br />
CLIENT_SECRET = Your Google app client secret <br />
REDIRECT_URI = The URI where Google will send the response after authentication <br />
EXPRESS_SESSION_SECRET = Express session secret <br />

## Where to find secrets

Secrets can be viewed by authorized viewers by logging into GCP(https://cloud.google.com/?hl=en) with your credentials and searching 'Secret Manager' in GCP Console for the relevent project.

# Run authentication server

`nodemon server.js` or `npm start`

# POSTMAN tests

## Step 1: log into Google Cloud Console using email address.

## Step 2: copy and paste the URL below in the browser. Replace `YOUR_REDIRECT_URI` and `YOUR_CLIENT_ID` with your own values

https://accounts.google.com/o/oauth2/v2/auth?scope=email%20profile&access_type=offline&include_granted_scopes=true&response_type=code&state=state_parameter_passthrough_value&redirect_uri=YOUR_REDIRECT_URI&client_id=YOUR_CLIENT_ID

## Step 3: check all tokens in terminal, copy and paste token values into testing environment

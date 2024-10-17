# Slack-Based Vulnerability Alert System

## Description

This application monitors the National Vulnerability Database (NVD) for new security vulnerabilities and automatically alerts system administrators via Slack. Administrators can forward these alerts to team members for swift remediation

## Table of Contents

- [Installation](#installation)
- [Usage Instructions](#usage-Instructions)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Project Structure](#Project-Structure)

## Installation

### Prerequisites

- Python 3.2
- Django

### Steps

1. Clone the repository:

   ```sh
   git clone https://github.com/SlackBot/slack-vulnerability-app.git
   cd slack-vulnerability-app
   ```

2. Create and activate a virtual environment:

   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Run the Django server:
   ```sh
   python manage.py runserver
   ```

## Usage Instructions

1. Ensure the Django server is running.
2. Set up your Slack app to send interactive message payloads to your server’s designated endpoint.
3. Under Slack's OAuth & Permissions settings, ensure these scopes are enabled:
   chat:write
   chat:write.public
   incoming-webhook
   users:read
   users:read.email
4. Add the end point in allowed hosts in settings.py file of the project.
5. The application will fetch new vulnerabilities at the configured interval (you can adjust  this in scheduler.py file) and notify the admin on Slack.


## Configuration

- **SLACK_TOKEN:** Your Slack API token.
- **ADMIN_ID:** The Slack user ID of the administrator.

## API Endpoints

- **api/slack/interactive:** Endpoint for handling interactive responses from Slack. Sample -> https://5bb8-103-97-242-221.ngrok-free.app/api/slack/interactive/

## File Structure and Description

Here is an overview of the project's structure and a brief description of each file and directory:

1. get_new_vulnerabilities.py -> This file is reponsible for fetching the new vulnerabilties added to the NVD database, using the API end point provided by them, in the last 24 hours. You can change the time duration to suit your needs.

2. main.py file -> Run this file to start the application's scheduler, which automatically checks for new vulnerabilities

3. message_payloads.py -> used for creating message payloads to be sent to the slack API to send messages to admin or user.

4. scheduler.py -> starts the scheduler which fetches data from NVD at regular intervals and send message to admin

5. send_to_slack.py -> Sends vulnerability alerts directly to the admin on Slack

6. api folder -> Contains the Django application files, which can be expanded for more features and endpoints.

7. api/views.py -> Defines the API logic for processing Slack's interactive messages..

8. api/urls.py -> Maps additional API endpoints for future scalability, handled in views.py

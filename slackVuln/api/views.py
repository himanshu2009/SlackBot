from rest_framework.decorators import api_view
from rest_framework.response import Response
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from message_payloads import create_to_reply, create_to_send_to_team

# this handles the post request sent by slack after button click

@api_view(['POST'])
def button_clicked(request):

    payload = json.loads(request.data.get('payload', ''))
    # if not payload_data:
    #     return Response({"error": "Empty payload received"}, status=400)
   

    
    # parsing of payload to extract the information required
    reply_by_member = ''
    information = payload['state']['values']
    
    for i in information:
        for j in information[i]:
            if 'selected_options' in information[i][j]:
                selected_users = information[i][j]['selected_options']
            else:
                reply_by_member = information[i][j]['value']

    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config.json'))

    try:
        with open(config_path) as config_file:
            config = json.load(config_file)
            slack_token = config['slack_token']
            admin_id = config['admin_id']
    except FileNotFoundError:
        print("Error: config.json file not found.")
        exit(1)
    except KeyError as e:
        print(f"Error: Missing key {e} in config.json.")
        exit(1) 

    client = WebClient(token=slack_token)


    description = payload['message']['text']
    sent_by = payload['user']['username']
    
    # if a team member replies
    if reply_by_member:

        message = create_to_reply(description, sent_by, reply_by_member)

        try:
            response = client.chat_postMessage(
                channel= admin_id,
                blocks = message["blocks"]
            )
            
            # Check response and handle errors if needed
            if response["ok"]:
                print(f"Confirmation message sent successfully to {admin_id}")
            else:
                print(f"Failed to send confirmation message to {admin_id}: {response}")
        
        except SlackApiError as e:
            print(f"Error sending confirmation message to {admin_id}: {e.response['error']}")

    # if a confirm/foward button is clicked
    else:

        # need not do anything if confirm button is clicked and hence early return
        if payload['actions'][0]['type'] == 'multi_static_select':
            return Response({"Succesful": "!!!"})

        user_ids = []
        for i in range(len(selected_users)):
            user_ids.append(selected_users[i]['value'])
        
        message = create_to_send_to_team(description)
        for user_id in user_ids:

            try:
                response = client.chat_postMessage(
                    channel=user_id,
                    blocks=message["blocks"]
                    )
                assert response["ok"]
                print("Message sent successfully to admin.")
            except SlackApiError as e:
                print(f"Error sending message: {e.response['error']}")

        
    return Response({"Succesful": "!!!"})



# @api_view(['POST'])
# def button_clicked(request):
#     payload_data = request.data.get('payload', '')  # Fetch the payload

#     if not payload_data:
#         return Response({"error": "Empty payload received"}, status=400)
    
#     try:
#         payload = json.loads(payload_data)  # Safely parse the JSON payload
#     except json.JSONDecodeError:
#         return Response({"error": "Invalid JSON payload"}, status=400)
   
#     # Parsing of payload to extract the information required
#     reply_by_member = ''
#     information = payload.get('state', {}).get('values', {})
    
#     selected_users = []
#     for i in information:
#         for j in information[i]:
#             if 'selected_options' in information[i][j]:
#                 selected_users = information[i][j]['selected_options']
#             else:
#                 reply_by_member = information[i][j]['value']
    
#     # Config loading logic
#     config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../config.json'))
#     try:
#         with open(config_path) as config_file:
#             config = json.load(config_file)
#             slack_token = config.get('slack_token')
#             admin_id = config.get('admin_id')
#     except FileNotFoundError:
#         return Response({"error": "Config file not found"}, status=500)
#     except KeyError as e:
#         return Response({"error": f"Missing key {e} in config.json"}, status=500)
    
#     # Initialize Slack client
#     client = WebClient(token=slack_token)
    
#     description = payload.get('message', {}).get('text', '')
#     sent_by = payload.get('user', {}).get('username', '')

#     # If a team member replies
#     if reply_by_member:
#         message = create_to_reply(description, sent_by, reply_by_member)
#         try:
#             response = client.chat_postMessage(
#                 channel=admin_id,
#                 blocks=message["blocks"]
#             )
#             if response["ok"]:
#                 print(f"Confirmation message sent successfully to {admin_id}")
#             else:
#                 print(f"Failed to send confirmation message: {response}")
#         except SlackApiError as e:
#             print(f"Error sending confirmation message: {e.response['error']}")
#             return Response({"error": f"Failed to send confirmation: {e.response['error']}"}, status=500)

#     # If a confirm/forward button is clicked
#     else:
#         if payload.get('actions', [{}])[0].get('type') == 'multi_static_select':
#             return Response({"Successful": "Action confirmed"}, status=200)
        
#         user_ids = [user['value'] for user in selected_users]

#         message = create_to_send_to_team(description)
#         for user_id in user_ids:
#             try:
#                 response = client.chat_postMessage(
#                     channel=user_id,
#                     blocks=message["blocks"]
#                 )
#                 if response["ok"]:
#                     print(f"Message sent successfully to {user_id}")
#                 else:
#                     print(f"Failed to send message to {user_id}: {response}")
#             except SlackApiError as e:
#                 print(f"Error sending message to {user_id}: {e.response['error']}")
#                 return Response({"error": f"Failed to send message to {user_id}: {e.response['error']}"}, status=500)
        
#     return Response({"Successful": "Message sent"}, status=200)



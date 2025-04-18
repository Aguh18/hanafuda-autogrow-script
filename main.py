import requests
import schedule
import time
import os
from datetime import datetime
import configparser


ASCII_ART = """
  ___        _            _                    
 / _ \\      | |          | |                   
/ /_\\ \\_   _| |_ ___   __| |_ __ ___  _ __ ____
|  _  | | | | __/ _ \\ / _` | '__/ _ \\| '_ \\_  /
| | | | |_| | || (_) | (_| | | | (_) | |_) / / 
\\_| |_/\\__,_|\\__\\___/ \\__,_|_|  \\___/| .__/___|
                                     | |       
                                     |_|       
"""
CREDIT = """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🧑‍💻 Created by        : Aguhh
🌐 GitHub            : https://github.com/Aguh18
💬 Join Telegram     : https://t.me/+V_JQTTMVZVU3YTM9
🔗 LinkedIn          : https://www.linkedin.com/in/asep-teguh-hidayat/
🎮 Join Discord      : https://discord.gg/wjxASXVD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""


def load_config_from_file(file_path="config.txt"):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config['DEFAULT'] if 'DEFAULT' in config else {}


def get_config():
    config_file = load_config_from_file()
    
    
    return {
        'refresh_token': os.getenv('FIREBASE_REFRESH_TOKEN', config_file.get('REFRESH_TOKEN', '')),
        'telegram_bot_token': os.getenv('TELEGRAM_BOT_TOKEN', config_file.get('TELEGRAM_BOT_TOKEN', '')),
        'telegram_chat_id': os.getenv('TELEGRAM_CHAT_ID', config_file.get('TELEGRAM_CHAT_ID', '')),
        'minute': int(os.getenv('MINUTE', config_file.get('MINUTE', '35')))
    }


config = get_config()
refresh_token = config['refresh_token']
telegram_bot_token = config['telegram_bot_token']
telegram_chat_id = config['telegram_chat_id']
minute = config['minute']

if not refresh_token:
    print("Error: Refresh token not found. Set FIREBASE_REFRESH_TOKEN in environment variables or config.txt.")
    exit()
if not telegram_bot_token or not telegram_chat_id:
    print("Error: Telegram Bot Token or Chat ID not found. Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment variables or config.txt.")
    exit()


def send_telegram_message(message):
    telegram_url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": telegram_chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(telegram_url, json=payload)
        if response.status_code == 200:
            print("Telegram notification sent to private chat:", message)
        else:
            print("Failed to send Telegram notification:", response.json())
    except Exception as e:
        print("Error sending Telegram notification:", str(e))


def run_hanafuda_task():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n[{timestamp}] Running Hanafuda task...")


    refresh_url = "https://securetoken.googleapis.com/v1/token?key=AIzaSyDipzN0VRfTPnMGhQ5PSzO27Cxm3DohJGY"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }


    try:
        response = requests.post(refresh_url, json=payload)
        if response.status_code == 200:
            id_token = response.json().get("id_token")
            user_id = response.json().get("user_id")
            success_message = (
                f"✅ *[{timestamp}] Login Successful*\n"
                f"ID Token: `{id_token[:20]}...`\n"
                f"User ID: `{user_id}`"
            )
            print(success_message)
            send_telegram_message(success_message)
        else:
            error = response.json().get("error", {})
            if error.get("message") == "INVALID_REFRESH_TOKEN":
                error_message = f"❌ *[{timestamp}] Error*: Invalid refresh token. Please log in again at https://hanafuda.hana.network/login."
            else:
                error_message = f"❌ *[{timestamp}] Login Failed*: {response.json()}"
            print(error_message)
            send_telegram_message(error_message)
            return
    except Exception as e:
        error_message = f"❌ *[{timestamp}] Login Error*: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)
        return

 
    headers = {
        "Authorization": f"Bearer {id_token}",
        "Content-Type": "application/json"
    }

    graphql_url = "https://hanafuda-backend-app-520478841386.us-central1.run.app/graphql"

    grow_payload = {
        "query": """
            mutation ExecuteGrowAction($withAll: Boolean) {
                executeGrowAction(withAll: $withAll) {
                    baseValue
                    leveragedValue
                    totalValue
                    multiplyRate
                }
            }
        """,
        "variables": {"withAll": True},
        "operationName": "ExecuteGrowAction"
    }

  
    try:
        response = requests.post(graphql_url, headers=headers, json=grow_payload)
        if response.status_code == 200:
            data = response.json()
            if "errors" in data:
                error_message = "❌ Failed to perform Grow All: "
                print(error_message)
                send_telegram_message(error_message)
            else:
                grow_data = data["data"]["executeGrowAction"]
                success_message = (
                    f"✅ *[{timestamp}] Grow All Successful*\n"
                    f"Base Value: `{grow_data['baseValue']}`\n"
                    f"Leveraged Value: `{grow_data['leveragedValue']}`\n"
                    f"Total Value: `{grow_data['totalValue']}`\n"
                    f"Multiply Rate: `{grow_data['multiplyRate']}`"
                )
                print(success_message)
                send_telegram_message(success_message)
        else:
            error_message = f"❌ *[{timestamp}] Failed to Access Grow API*: Status {response.status_code}\n{response.text}"
            print(error_message)
            send_telegram_message(error_message)
    except Exception as e:
        error_message = f"❌ *[{timestamp}] Grow All Error*: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)


print(ASCII_ART)
print(CREDIT)
schedule.every().hour.at(f":{minute:02d}").do(run_hanafuda_task)



start_message = f"🚀 *[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Hanafuda Script Started*\nWill run every hour at minute {minute:02d}"
print(start_message)
send_telegram_message(start_message)


while True:
    schedule.run_pending()
    time.sleep(60) 
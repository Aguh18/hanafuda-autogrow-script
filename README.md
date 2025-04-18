🌸 Hanafuda Auto Login & Grow Script
This Python script automates logging into Hanafuda, retrieves an id_token using a refresh_token, and performs the Grow All action periodically every hour at a specified minute. Result notifications are sent to a private Telegram chat via a bot.
✨ Features

Automatic Login: Uses Firebase refresh_token for seamless authentication.
Grow All Execution: Performs the GraphQL mutation Grow All action.
Telegram Notifications: Sends success or failure notifications to a private Telegram chat.
Customizable Schedule: Configurable to run every hour at a specified minute (default: 35th minute).

📦 Requirements

Python 3.7 or higher
Required Python packages:pip install requests schedule



🛠 Setup

Clone the Repository:
git clone https://github.com/your-username/hanafuda-auto-script.git
cd hanafuda-auto-script


Install Dependencies:
pip install requests schedule


Configure the Script:The script retrieves configuration from environment variables or a config.txt file. You need to provide:

FIREBASE_REFRESH_TOKEN: Obtain from Hanafuda login.
TELEGRAM_BOT_TOKEN: Your Telegram bot token (e.g., 7872772160:AAGB8WAJAYsfdqGs8Fooo2re5j1gb8WImIw).
TELEGRAM_CHAT_ID: Your Telegram chat ID (contact your provider for this).
MINUTE: The minute of each hour to run the script (e.g., 35 for the 35th minute).

Option 1: Environment Variables (Recommended):
export FIREBASE_REFRESH_TOKEN="your_refresh_token"
export TELEGRAM_BOT_TOKEN="7872772160:AAGB8WAJAYsfdqGs8Fooo2re5j1gb8WImIw"
export TELEGRAM_CHAT_ID="your_chat_id"
export MINUTE=35

Option 2: Config File:Create a config.txt file in the same directory as the script with the following format:
[DEFAULT]
REFRESH_TOKEN=your_refresh_token
TELEGRAM_BOT_TOKEN=7872772160:AAGB8WAJAYsfdqGs8Fooo2re5j1gb8WImIw
TELEGRAM_CHAT_ID=your_chat_id
MINUTE=35



🚀 Usage

Run the Script:
python hanafuda_script.py

The script will:

Display an ASCII art banner.
Send an initial Telegram notification indicating the script has started.
Run the Grow All task every hour at the specified minute (e.g., :35).
Send Telegram notifications for login success/failure and Grow All results.


Keep the Script Running:To ensure the script runs continuously, use a tool like nohup, screen, or tmux:
nohup python hanafuda_script.py &


Monitor Output:

Check the console for debug logs and error messages.
Verify Telegram notifications for task results.



🐛 Troubleshooting

Config Error: Ensure config.txt has a [DEFAULT] section or environment variables are set correctly.
Scheduler Not Triggering: Verify the MINUTE value is between 0-59 and the system clock is correct.
API Errors: Check the validity of the refresh_token by logging in again at Hanafuda.
Telegram Issues: Confirm the TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID are correct.

For detailed logs, enable debug prints in the script (already included in the provided version).
📝 Notes

The script requires a stable internet connection to communicate with Firebase and Hanafuda APIs.
Keep your refresh_token secure and do not share it publicly.
Contact your Telegram chat ID provider (e.g., "Teguh") if you encounter issues with notifications.

🤝 Contributing
Feel free to submit issues or pull requests to improve the script. Ensure any changes are well-documented and tested.
📜 License
This project is licensed under the MIT License. See the LICENSE file for details.

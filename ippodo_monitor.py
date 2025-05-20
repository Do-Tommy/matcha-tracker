import requests
from bs4 import BeautifulSoup
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Discord webhook URL - you'll need to set this in your .env file
DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')
DISCORD_USER_MENTION = os.getenv('DISCORD_USER_MENTION', '')  # e.g. <@123456789012345678>

# Product URL
PRODUCT_URL = "https://ippodotea.com/collections/all/products/ikuyo-100"

def check_stock():
    try:
        # Send request with headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(PRODUCT_URL, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for "Sold out" text
        sold_out_element = soup.find(string="Sold out")
        
        return sold_out_element is None
        
    except Exception as e:
        print(f"Error checking stock: {e}")
        return False

def send_discord_notification():
    try:
        data = {
            "content": f"{DISCORD_USER_MENTION} 🎉 Ikuyo Matcha is back in stock! 🍵\n{PRODUCT_URL}"
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Discord notification: {e}")

def send_discord_start_message():
    try:
        data = {
            "content": f"{DISCORD_USER_MENTION} 👋 Ippodo Tea stock monitor has started! Monitoring: {PRODUCT_URL}"
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Discord start message: {e}")

def main():
    print("Starting Ippodo Tea stock monitor...")
    print(f"Monitoring: {PRODUCT_URL}")
    send_discord_start_message()
    
    while True:
        if check_stock():
            print("Product is in stock! Sending notification...")
            send_discord_notification()
            break
        else:
            print("Product is still out of stock. Checking again in 5 minutes...")
            time.sleep(300)  # Wait 5 minutes before checking again

if __name__ == "__main__":
    main() 
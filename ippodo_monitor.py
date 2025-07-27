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

# List of products to monitor
PRODUCTS = [
    {
        "name": "Ikuyo Matcha",
        "url": "https://ippodotea.com/collections/all/products/ikuyo-100"
    },
    # Add more products here as needed
]

def check_stock(product_url):
    try:
        # Send request with headers to mimic a browser
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(product_url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Look for "Sold out" text
        sold_out_element = soup.find(string="Sold out")
        
        return sold_out_element is None
        
    except Exception as e:
        print(f"Error checking stock: {e}")
        return False

def send_discord_notification(product_name, product_url):
    try:
        data = {
            "content": f"{DISCORD_USER_MENTION} 🎉 {product_name} is back in stock! 🍵\n{product_url}"
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Discord notification: {e}")

def send_discord_start_message():
    try:
        # Create a list of product names
        product_names = [product["name"] for product in PRODUCTS]
        products_list = "\n".join([f"- {name}" for name in product_names])
        
        data = {
            "content": f"{DISCORD_USER_MENTION} 👋 Ippodo Tea stock monitor has started! Monitoring:\n{products_list}"
        }
        response = requests.post(DISCORD_WEBHOOK_URL, json=data)
        response.raise_for_status()
    except Exception as e:
        print(f"Error sending Discord start message: {e}")

def test_mode():
    """Test mode that simulates stock changes"""
    print("Starting test mode...")
    print("This will check all products every 30 seconds")
    print("Press Ctrl+C to stop")
    
    for product in PRODUCTS:
        print(f"\nChecking {product['name']}...")
        if check_stock(product['url']):
            print(f"✅ {product['name']} is in stock")
        else:
            print(f"❌ {product['name']} is out of stock")
    
    print("\nWaiting 30 seconds...")
    time.sleep(30)
    
    print("\nSecond check:")
    for product in PRODUCTS:
        print(f"\nChecking {product['name']}...")
        if check_stock(product['url']):
            print(f"✅ {product['name']} is in stock")
        else:
            print(f"❌ {product['name']} is out of stock")
    
    print("\nTest completed successfully!")

def main():
    print("Starting Ippodo Tea stock monitor...")
    print("Monitoring the following products:")
    for product in PRODUCTS:
        print(f"- {product['name']}: {product['url']}")
    
    send_discord_start_message()
    
    # Keep track of which products are in stock
    in_stock_products = set()
    
    while True:
        for product in PRODUCTS:
            if product['name'] not in in_stock_products:  # Only check products not yet in stock
                print(f"\nChecking {product['name']}...")
                if check_stock(product['url']):
                    print(f"✅ {product['name']} is in stock! Sending notification...")
                    send_discord_notification(product['name'], product['url'])
                    in_stock_products.add(product['name'])
                else:
                    print(f"❌ {product['name']} is still out of stock")
        
        if len(in_stock_products) == len(PRODUCTS):
            print("\nAll products are in stock! Stopping monitor...")
            break
        else:
            print("\nWaiting 5 minutes before next check...")
            time.sleep(300)  # Wait 5 minutes before checking again

if __name__ == "__main__":
    # Uncomment the line below to run in test mode
    # test_mode()
    main() 
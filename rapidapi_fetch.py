import requests
from google_sheets import get_instagram_usernames  # Отримуємо імена з Google Sheets
from config import RAPIDAPI_URL, RAPIDAPI_KEY

def fetch_instagram_info(username):
    url = f"https://{RAPIDAPI_URL}/userinfo/instagram"
    
    querystring = {"username_or_id_or_url": username}
    
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,  # Заміни на свій ключ
        "x-rapidapi-host": RAPIDAPI_URL
    }
     
    try:
        response = requests.get(url, headers=headers, params=querystring)
        response.raise_for_status()  # Перевіряє, чи є помилка в запиті
        data = response.json()
        
        # Перевірити, чи є потрібні дані в відповіді
        if 'public_phone_number' in data and 'public_email' in data:
            return {
                'phone': data.get('full_name', 'Номер не знайдено'),
                'email': data.get('public_email', 'Email не знайдено')
            }
        else:
            print(f"Data for {username} does not contain 'phone' or 'email'.")
            return {
                'phone': 'Номер не знайдено',
                'email': 'Email не знайдено'
            }
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {username}: {http_err}")
        return {
            'phone': 'Номер не знайдено',
            'email': 'Email не знайдено'
        }
    except Exception as err:
        print(f"Other error occurred for {username}: {err}")
        return {
            'phhone': 'Номер не знайдено',
            'email': 'Email не знайдено'
        }

def fetch_info_for_all_users():
    usernames = get_instagram_usernames()  # Це функція, яка отримує імена користувачів із Google Sheets
    results = []

    for username in usernames:
        instagram_info = fetch_instagram_info(username)
        if instagram_info:
            results.append(instagram_info)
    
    return results
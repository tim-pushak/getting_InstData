from google_sheets import update_google_sheet, get_instagram_usernames  # Функції для роботи з Google Sheets
from rapidapi_fetch import fetch_info_for_all_users  # Функція для отримання даних з RapidAPI

def main():
    # Отримати інформацію з RapidAPI для всіх користувачів
    instagram_data = fetch_info_for_all_users()
    
    # Оновити Google Sheets отриманими даними
    if instagram_data:
        update_google_sheet(instagram_data)
        print("Дані успішно оновлені в Google Sheets")
    else:
        print("Не вдалося отримати дані з RapidAPI")

if __name__ == "__main__":
    main()
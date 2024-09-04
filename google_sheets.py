from google.oauth2 import service_account
from googleapiclient.discovery import build

# Налаштування доступу до Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = './serviceAccountFile.json'
SPREADSHEET_ID = '1DCKQmLhy25XnOygjmzD-9zx_zBcg-dXZW6fjsim6INA'
RANGE_USERNAMES = 'Sheet1!A:A'  # Діапазон для нікнеймів
RANGE_CONTACTS = 'Sheet1!B:D'  # Діапазон для контактів (пошта і телефон)

def get_instagram_usernames():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_USERNAMES).execute()
    values = result.get('values', [])

    # Перетворення даних у список імен користувачів
    usernames = [row[0] for row in values if row]
    return usernames

def update_google_sheet(data):
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    # Підготуємо значення для оновлення у стовпцях B і C
    values = []
    for item in data:
        phone = item.get('phone') if item.get('phone') else "Номер не знайдено"  # Записуємо номер телефону
        email = item.get('email') if item.get('email') else "Email не знайдено"  # Записуємо email
        values.append([phone, email])  # Додаємо ці значення у список

    # Оновлюємо діапазон, який починається зі стовпця B (номер телефону) і C (email)
    RANGE_NAME = 'Sheet1!B1'  # Зміни діапазон на той, де починаються стовпці B і C

    body = {
        'values': values
    }

    # Оновлюємо таблицю
    result = sheet.values().update(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME, valueInputOption='RAW', body=body).execute()
    return result
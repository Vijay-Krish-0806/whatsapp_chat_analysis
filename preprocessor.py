import re
import pandas as pd

def preprocess(data):
    # Matches Android-style exports, with or without AM/PM, with or without seconds
    pattern = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}(?::\d{2})?\s?(?:[APap][Mm])?\s-\s"

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    if not dates:
        raise ValueError(
            "No messages matched the expected WhatsApp format. "
            "Please check that you exported the chat as .txt without media, "
            "and that the date format matches DD/MM/YY, HH:MM - "
        )

    df = pd.DataFrame({'user_message': messages, "message_date": dates})
    df['message_date'] = df['message_date'].str.strip()

    # Try 24-hour format first, fall back to 12-hour with AM/PM
    try:
        df['date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %H:%M -")
    except ValueError:
        try:
            df['date'] = pd.to_datetime(df['message_date'], format="%d/%m/%y, %I:%M %p -")
        except ValueError:
            # Last resort: let pandas infer it
            df['date'] = pd.to_datetime(df['message_date'], errors='coerce')

    df.drop(columns=['message_date'], inplace=True)

    users = []
    messages_list = []
    for message in df['user_message']:
        entry = re.split(r'([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages_list.append(entry[2])
        else:
            users.append('group_notification')
            messages_list.append(entry[0])

    df['user'] = users
    df['message'] = messages_list
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['day_name'] = df['date'].dt.day_name()
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df

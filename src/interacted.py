import json
import os

INTERACTED_FILE = 'interacted.json'


def load():
    try:
        with open(INTERACTED_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []


def save(users):
    with open(INTERACTED_FILE, 'w') as f:
        json.dump(users, f, indent=4)


def interacted(user):
    if not os.path.exists(INTERACTED_FILE):
        save([])

    users_interacted = load()

    if not any(existing_user['user_id'] == user.id for existing_user in users_interacted):
        user_data = {
            'user_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'language_code': user.language_code,
        }

        users_interacted.append(user_data)
        save(users_interacted)

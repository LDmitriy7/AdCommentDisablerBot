def username_to_url(username: str):
    return f'https://t.me/{username.removeprefix("@")}'

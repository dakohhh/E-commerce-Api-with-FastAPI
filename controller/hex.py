import secrets


def generate_hex(lenght:int):
    return secrets.token_hex(lenght)


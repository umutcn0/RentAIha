def password_policy(password, password_confirm):
    if len(password) < 8:
        return False
    if password != password_confirm:
        return False
    return True
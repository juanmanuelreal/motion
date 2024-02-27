def valid_form(orm_user, username: str, password: str):
    if not username or not password or len(password)<5:
        return False, "The username and password must be filled in, password may conntain at leats 5 characters"
    
    user_exist = orm_user.get_user_by_username(username=username)
    if user_exist:
        return False, "The username already exists."
    
    return True, "Correct data"
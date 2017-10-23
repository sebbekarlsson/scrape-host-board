from scrapehost.password import get_hashed_password, check_password


def test_correct_password():
    password = 'mypasswordisprettybad'
    hashed_pass = get_hashed_password(password)

    assert check_password(hashed_pass, password) == True

def test_wrong_password():
    password = 'mypasswordisprettybad'
    hashed_pass = get_hashed_password(password)

    assert check_password(hashed_pass, 'thispasswordiswrong') == False 

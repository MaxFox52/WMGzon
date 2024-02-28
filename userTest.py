import pytest
from flaskStuff import User, UserList, user_populate

# test User class initialisation
def test_user_initialization():
    user = User(1, "test@example.com", "password123", "admin", "John", "Doe", 5)
    assert user.id == 1
    assert user.email == "test@example.com"
    assert user.password == "password123"
    assert user.permission == "admin"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.basket_count == 5

# test UserList addUser function
def test_add_user():
    user_list = UserList()
    user = User(1, "test@example.com", "password123", "admin", "John", "Doe", 5)
    user_list.addUser(user)
    assert len(user_list.UserArray) == 1
    assert user_list.UserArray[0] == user

# mock JSON data
mock_json_data = {
    "user1": {
        "id": 1,
        "email": "test@example.com",
        "password": "password123",
        "permission": "admin",
        "first_name": "John",
        "last_name": "Doe",
        "basket_count": 5
    }
}

# test user_populate function
def test_user_populate():
    values = user_populate(mock_json_data["user1"])
    expected_values = [1, "test@example.com", "password123", "admin", "John", "Doe", 5]
    assert values == expected_values

if __name__ == "__main__":
    import sys
    sys.exit(pytest.main([__file__]))






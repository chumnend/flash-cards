import uuid
from datetime import datetime
from unittest.mock import Mock, patch

from flashly.models.user import UserModel


class TestUserModel:
    """Test cases for UserModel."""

    def test_user_model_creation(self, sample_user):
        """Test creating a UserModel instance."""
        assert isinstance(sample_user.id, uuid.UUID)
        assert sample_user.first_name == "John"
        assert sample_user.last_name == "Doe"
        assert sample_user.username == "johndoe"
        assert sample_user.email == "john@example.com"
        assert sample_user.password_hash == "hashed_password"
        assert isinstance(sample_user.created_at, datetime)
        assert isinstance(sample_user.updated_at, datetime)

    def test_set_password(self, sample_user):
        """Test password hashing functionality."""
        password = "test_password"
        sample_user.set_password(password)

        # Password hash should be set and different from plain text
        assert sample_user.password_hash != password
        assert sample_user.password_hash is not None
        assert len(sample_user.password_hash) > 0

    def test_check_password_correct(self, sample_user):
        """Test checking correct password."""
        password = "test_password"
        sample_user.set_password(password)

        assert sample_user.check_password(password) is True

    def test_check_password_incorrect(self, sample_user):
        """Test checking incorrect password."""
        password = "test_password"
        wrong_password = "wrong_password"
        sample_user.set_password(password)

        assert sample_user.check_password(wrong_password) is False

    def test_check_password_no_hash(self, sample_user):
        """Test checking password when no hash is set."""
        sample_user.password_hash = None

        assert sample_user.check_password("any_password") is False

    def test_save_user(self, sample_user, mock_db_conn):
        """Test saving a user to database."""
        mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value

        sample_user.save(mock_db_conn)

        # Verify that execute was called with correct SQL
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "INSERT INTO users" in args[0]
        assert sample_user.id in args[1]
        assert sample_user.first_name in args[1]
        assert sample_user.last_name in args[1]
        assert sample_user.username in args[1]
        assert sample_user.email in args[1]
        assert sample_user.password_hash in args[1]

    @patch("flashly.models.user.UserModel.find_by_email")
    def test_find_by_email(self, mock_find):
        """Test finding user by email."""
        mock_db_conn = Mock()
        email = "test@example.com"
        mock_find.return_value = ("user_data",)

        result = UserModel.find_by_email(mock_db_conn, email)

        mock_find.assert_called_once_with(mock_db_conn, email)
        assert result == ("user_data",)

    @patch("flashly.models.user.UserModel.find_by_username")
    def test_find_by_username(self, mock_find):
        """Test finding user by username."""
        mock_db_conn = Mock()
        username = "testuser"
        mock_find.return_value = ("user_data",)

        result = UserModel.find_by_username(mock_db_conn, username)

        mock_find.assert_called_once_with(mock_db_conn, username)
        assert result == ("user_data",)

    def test_tablename_attribute(self):
        """Test that __tablename__ is set correctly."""
        assert UserModel.__tablename__ == "users"

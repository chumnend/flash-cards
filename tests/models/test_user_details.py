import uuid
from datetime import datetime

from flashly.models.user_details import UserDetailsModel


class TestUserDetailsModel:
    """Test cases for UserDetailsModel."""

    def test_user_details_model_creation(self, sample_user_details):
        """Test creating a UserDetailsModel instance."""
        assert isinstance(sample_user_details.id, uuid.UUID)
        assert isinstance(sample_user_details.user_id, uuid.UUID)
        assert sample_user_details.about_me == "I love learning!"
        assert isinstance(sample_user_details.created_at, datetime)
        assert isinstance(sample_user_details.updated_at, datetime)

    def test_save_user_details(self, sample_user_details, mock_db_conn):
        """Test saving user details to database."""
        mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value

        sample_user_details.save(mock_db_conn)

        # Verify that execute was called with correct SQL
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "INSERT INTO user_details" in args[0]
        assert sample_user_details.id in args[1]
        assert sample_user_details.user_id in args[1]
        assert sample_user_details.about_me in args[1]

        # Verify commit was called
        mock_db_conn.commit.assert_called_once()

    def test_empty_about_me(self):
        """Test user details with empty about_me."""
        user_details = UserDetailsModel(
            id=uuid.uuid4(), user_id=uuid.uuid4(), about_me="", created_at=datetime.now(), updated_at=datetime.now()
        )
        assert user_details.about_me == ""

    def test_long_about_me(self):
        """Test user details with long about_me text."""
        long_text = "A" * 1000  # 1000 character string
        user_details = UserDetailsModel(
            id=uuid.uuid4(),
            user_id=uuid.uuid4(),
            about_me=long_text,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )
        assert user_details.about_me == long_text

    def test_tablename_attribute(self):
        """Test that __tablename__ is set correctly."""
        assert UserDetailsModel.__tablename__ == "user_details"

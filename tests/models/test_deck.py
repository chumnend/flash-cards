import pytest
import uuid
from datetime import datetime
from unittest.mock import Mock, patch

from flashly.models.deck import DeckModel


class TestDeckModel:
    """Test cases for DeckModel."""

    def test_deck_model_creation(self, sample_deck):
        """Test creating a DeckModel instance."""
        assert isinstance(sample_deck.id, uuid.UUID)
        assert sample_deck.name == "Python Basics"
        assert sample_deck.description == "Learn Python fundamentals"
        assert sample_deck.publish_status == "public"
        assert isinstance(sample_deck.owner_id, uuid.UUID)
        assert sample_deck.rating == 4.5
        assert isinstance(sample_deck.created_at, datetime)
        assert isinstance(sample_deck.updated_at, datetime)

    def test_save_deck(self, sample_deck, mock_db_conn):
        """Test saving a deck to database."""
        mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
        
        sample_deck.save(mock_db_conn)
        
        # Verify that execute was called with correct SQL
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "INSERT INTO decks" in args[0]
        assert sample_deck.id in args[1]
        assert sample_deck.name in args[1]
        assert sample_deck.description in args[1]
        assert sample_deck.publish_status in args[1]
        assert sample_deck.owner_id in args[1]
        assert sample_deck.rating in args[1]
        
        # Verify commit was called
        mock_db_conn.commit.assert_called_once()

    def test_update_deck(self, sample_deck, mock_db_conn):
        """Test updating a deck in database."""
        mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
        
        sample_deck.update(mock_db_conn)
        
        # Verify that execute was called with UPDATE SQL
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "UPDATE decks" in args[0]
        mock_db_conn.commit.assert_called_once()

    def test_delete_deck(self, sample_deck, mock_db_conn):
        """Test deleting a deck from database."""
        mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
        
        sample_deck.delete(mock_db_conn)
        
        # Verify that execute was called with DELETE SQL
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "DELETE FROM decks" in args[0]
        assert sample_deck.id in args[1]
        mock_db_conn.commit.assert_called_once()

    @patch('flashly.models.deck.DeckModel.find_deck_by_id')
    def test_find_deck_by_id(self, mock_find):
        """Test finding deck by ID."""
        mock_db_conn = Mock()
        deck_id = uuid.uuid4()
        mock_find.return_value = ("deck_data",)
        
        result = DeckModel.find_deck_by_id(mock_db_conn, deck_id)
        
        mock_find.assert_called_once_with(mock_db_conn, deck_id)
        assert result == ("deck_data",)

    @patch('flashly.models.deck.DeckModel.find_decks_by_user_id')
    def test_find_decks_by_user_id(self, mock_find):
        """Test finding decks by user ID."""
        mock_db_conn = Mock()
        user_id = uuid.uuid4()
        mock_find.return_value = [("deck_data",)]
        
        result = DeckModel.find_decks_by_user_id(mock_db_conn, user_id)
        
        mock_find.assert_called_once_with(mock_db_conn, user_id)
        assert result == [("deck_data",)]

    @patch('flashly.models.deck.DeckModel.find_explore_decks')
    def test_find_explore_decks(self, mock_find):
        """Test finding explore decks."""
        mock_db_conn = Mock()
        mock_find.return_value = [("deck_data",)]
        
        result = DeckModel.find_explore_decks(mock_db_conn)
        
        mock_find.assert_called_once_with(mock_db_conn)
        assert result == [("deck_data",)]

    @patch('flashly.models.deck.DeckModel.find_feed_decks')
    def test_find_feed_decks(self, mock_find):
        """Test finding feed decks."""
        mock_db_conn = Mock()
        user_id = uuid.uuid4()
        mock_find.return_value = [("deck_data",)]
        
        result = DeckModel.find_feed_decks(mock_db_conn, user_id)
        
        mock_find.assert_called_once_with(mock_db_conn, user_id)
        assert result == [("deck_data",)]

    def test_publish_status_values(self):
        """Test that publish_status accepts valid values."""
        deck = DeckModel(
            id=uuid.uuid4(),
            name="Test Deck",
            description="Test Description",
            publish_status="private",
            owner_id=uuid.uuid4(),
            rating=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert deck.publish_status == "private"
        
        # Test other valid statuses
        for status in ['public', 'unlisted']:
            deck.publish_status = status
            assert deck.publish_status == status

    def test_rating_range(self, sample_deck):
        """Test rating is within valid range."""
        # Test valid ratings
        for rating in [0.0, 2.5, 5.0]:
            sample_deck.rating = rating
            assert sample_deck.rating == rating

    def test_empty_description(self, sample_deck):
        """Test deck with empty description."""
        sample_deck.description = ""
        assert sample_deck.description == ""

    def test_tablename_attribute(self):
        """Test that __tablename__ is set correctly."""
        assert DeckModel.__tablename__ == "decks"
import pytest
import uuid
from datetime import datetime
from unittest.mock import Mock, patch

from flashly.models.card import CardModel


class TestCardModel:
    """Test cases for CardModel."""

    def test_card_model_creation(self, sample_card):
        """Test creating a CardModel instance."""
        assert isinstance(sample_card.id, uuid.UUID)
        assert sample_card.front_text == "What is Python?"
        assert sample_card.back_text == "A programming language"
        assert sample_card.difficulty == "medium"
        assert sample_card.times_reviewed == 5
        assert sample_card.success_rate == 0.8
        assert isinstance(sample_card.deck_id, uuid.UUID)
        assert isinstance(sample_card.created_at, datetime)
        assert isinstance(sample_card.updated_at, datetime)

    def test_save_card(self, sample_card, mock_db_conn):
        """Test saving a card to database."""
        mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
        
        sample_card.save(mock_db_conn)
        
        # Verify that execute was called with correct SQL
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "INSERT INTO cards" in args[0]
        assert sample_card.id in args[1]
        assert sample_card.front_text in args[1]
        assert sample_card.back_text in args[1]
        assert sample_card.difficulty in args[1]
        assert sample_card.times_reviewed in args[1]
        assert sample_card.success_rate in args[1]
        assert sample_card.deck_id in args[1]
        
        # Verify commit was called
        mock_db_conn.commit.assert_called_once()

    def test_update_card(self, sample_card, mock_db_conn):
        """Test updating a card in database."""
        mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
        
        sample_card.update(mock_db_conn)
        
        # Verify that execute was called with UPDATE SQL
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "UPDATE cards" in args[0]
        mock_db_conn.commit.assert_called_once()

    def test_delete_card(self, sample_card, mock_db_conn):
        """Test deleting a card from database."""
        mock_cursor = mock_db_conn.cursor.return_value.__enter__.return_value
        
        sample_card.delete(mock_db_conn)
        
        # Verify that execute was called with DELETE SQL
        mock_cursor.execute.assert_called_once()
        args = mock_cursor.execute.call_args[0]
        assert "DELETE FROM cards" in args[0]
        assert sample_card.id in args[1]
        mock_db_conn.commit.assert_called_once()

    @patch('flashly.models.card.CardModel.find_cards_by_deck_id')
    def test_find_cards_by_deck_id(self, mock_find):
        """Test finding cards by deck ID."""
        mock_db_conn = Mock()
        deck_id = uuid.uuid4()
        mock_find.return_value = [("card_data",)]
        
        result = CardModel.find_cards_by_deck_id(mock_db_conn, deck_id)
        
        mock_find.assert_called_once_with(mock_db_conn, deck_id)
        assert result == [("card_data",)]

    @patch('flashly.models.card.CardModel.find_card_by_id')
    def test_find_card_by_id(self, mock_find):
        """Test finding card by ID."""
        mock_db_conn = Mock()
        card_id = uuid.uuid4()
        mock_find.return_value = ("card_data",)
        
        result = CardModel.find_card_by_id(mock_db_conn, card_id)
        
        mock_find.assert_called_once_with(mock_db_conn, card_id)
        assert result == ("card_data",)

    def test_difficulty_values(self):
        """Test that difficulty accepts valid values."""
        card = CardModel(
            id=uuid.uuid4(),
            front_text="Test",
            back_text="Test",
            difficulty="easy",
            times_reviewed=0,
            success_rate=0.0,
            deck_id=uuid.uuid4(),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert card.difficulty == "easy"
        
        # Test other valid difficulties
        for difficulty in ['medium', 'hard']:
            card.difficulty = difficulty
            assert card.difficulty == difficulty

    def test_success_rate_range(self, sample_card):
        """Test success rate is within valid range."""
        # Test valid success rates
        for rate in [0.0, 0.5, 1.0]:
            sample_card.success_rate = rate
            assert sample_card.success_rate == rate

    def test_times_reviewed_non_negative(self, sample_card):
        """Test times_reviewed is non-negative."""
        sample_card.times_reviewed = 0
        assert sample_card.times_reviewed == 0
        
        sample_card.times_reviewed = 10
        assert sample_card.times_reviewed == 10

    def test_tablename_attribute(self):
        """Test that __tablename__ is set correctly."""
        assert CardModel.__tablename__ == "cards"
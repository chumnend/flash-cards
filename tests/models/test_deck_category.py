import uuid

from flashly.models.deck_category import DeckCategoryModel


class TestDeckCategoryModel:
    """Test cases for DeckCategoryModel."""

    def test_deck_category_model_creation(self, sample_deck_category):
        """Test creating a DeckCategoryModel instance."""
        assert isinstance(sample_deck_category.deck_id, uuid.UUID)
        assert isinstance(sample_deck_category.category_id, uuid.UUID)

    def test_different_deck_category_ids(self):
        """Test deck category with different IDs."""
        deck_id = uuid.uuid4()
        category_id = uuid.uuid4()

        # Ensure they are different
        assert deck_id != category_id

        deck_category = DeckCategoryModel(deck_id=deck_id, category_id=category_id)

        assert deck_category.deck_id == deck_id
        assert deck_category.category_id == category_id

    def test_multiple_categories_per_deck(self):
        """Test that a deck can have multiple categories."""
        deck_id = uuid.uuid4()
        categories = [uuid.uuid4() for _ in range(3)]

        deck_categories = []
        for category_id in categories:
            deck_category = DeckCategoryModel(deck_id=deck_id, category_id=category_id)
            deck_categories.append(deck_category)

        # All should have the same deck_id but different category_ids
        for dc in deck_categories:
            assert dc.deck_id == deck_id

        category_ids = [dc.category_id for dc in deck_categories]
        assert len(set(category_ids)) == len(category_ids)  # All unique

    def test_multiple_decks_per_category(self):
        """Test that a category can be associated with multiple decks."""
        category_id = uuid.uuid4()
        decks = [uuid.uuid4() for _ in range(3)]

        deck_categories = []
        for deck_id in decks:
            deck_category = DeckCategoryModel(deck_id=deck_id, category_id=category_id)
            deck_categories.append(deck_category)

        # All should have the same category_id but different deck_ids
        for dc in deck_categories:
            assert dc.category_id == category_id

        deck_ids = [dc.deck_id for dc in deck_categories]
        assert len(set(deck_ids)) == len(deck_ids)  # All unique

    def test_tablename_attribute(self):
        """Test that __tablename__ is set correctly."""
        assert DeckCategoryModel.__tablename__ == "deck_categories"

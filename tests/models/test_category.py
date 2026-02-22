import pytest
import uuid
from datetime import datetime
from unittest.mock import Mock

from flashly.models.category import CategoryModel


class TestCategoryModel:
    """Test cases for CategoryModel."""

    def test_category_model_creation(self, sample_category):
        """Test creating a CategoryModel instance."""
        assert isinstance(sample_category.id, uuid.UUID)
        assert sample_category.name == "Programming"
        assert isinstance(sample_category.created_at, datetime)
        assert isinstance(sample_category.updated_at, datetime)

    def test_category_with_different_names(self):
        """Test category with different names."""
        names = ["Programming", "Science", "Math", "History", "Art"]
        for name in names:
            category = CategoryModel(
                id=uuid.uuid4(),
                name=name,
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
            assert category.name == name

    def test_category_name_case_sensitivity(self):
        """Test category name case sensitivity."""
        category = CategoryModel(
            id=uuid.uuid4(),
            name="Programming",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert category.name == "Programming"
        
        category.name = "programming"
        assert category.name == "programming"

    def test_empty_category_name(self):
        """Test category with empty name."""
        category = CategoryModel(
            id=uuid.uuid4(),
            name="",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        assert category.name == ""

    def test_tablename_attribute(self):
        """Test that __tablename__ is set correctly."""
        assert CategoryModel.__tablename__ == "categories"

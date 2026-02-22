import pytest
import uuid
from datetime import datetime
from unittest.mock import Mock, MagicMock
from pyramid.config import Configurator
from pyramid.request import Request
from pyramid.testing import DummyRequest

from flashly.models.user import UserModel
from flashly.models.card import CardModel
from flashly.models.deck import DeckModel
from flashly.models.user_details import UserDetailsModel
from flashly.models.follower import FollowerModel
from flashly.models.deck_category import DeckCategoryModel


@pytest.fixture
def mock_db_conn():
    """Mock database connection for testing."""
    mock_conn = Mock()
    mock_cursor = Mock()
    
    # Set up the context manager properly
    mock_context = Mock()
    mock_context.__enter__ = Mock(return_value=mock_cursor)
    mock_context.__exit__ = Mock(return_value=False)
    mock_conn.cursor.return_value = mock_context
    mock_conn.commit = Mock()
    return mock_conn


@pytest.fixture
def sample_user():
    """Create a sample user for testing."""
    return UserModel(
        id=uuid.uuid4(),
        first_name="John",
        last_name="Doe", 
        username="johndoe",
        email="john@example.com",
        password_hash="hashed_password",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_user_details():
    """Create sample user details for testing."""
    user_id = uuid.uuid4()
    return UserDetailsModel(
        id=uuid.uuid4(),
        user_id=user_id,
        about_me="I love learning!",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_card():
    """Create a sample card for testing."""
    return CardModel(
        id=uuid.uuid4(),
        front_text="What is Python?",
        back_text="A programming language",
        difficulty="medium",
        times_reviewed=5,
        success_rate=0.8,
        deck_id=uuid.uuid4(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_deck():
    """Create a sample deck for testing."""
    return DeckModel(
        id=uuid.uuid4(),
        name="Python Basics",
        description="Learn Python fundamentals",
        publish_status="public",
        owner_id=uuid.uuid4(),
        rating=4.5,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.fixture
def sample_category():
    """Create a sample category for testing."""
    # Note: category.py appears to have a naming issue - commenting out for now
    # return CategoryModel(
    #     id=uuid.uuid4(),
    #     name="Programming",
    #     created_at=datetime.now(),
    #     updated_at=datetime.now()
    # )
    return None


@pytest.fixture
def sample_follower():
    """Create a sample follower relationship for testing."""
    return FollowerModel(
        id=uuid.uuid4(),
        follower_id=uuid.uuid4(),
        following_id=uuid.uuid4(),
        created_at=datetime.now()
    )


@pytest.fixture
def sample_deck_category():
    """Create a sample deck category relationship for testing."""
    return DeckCategoryModel(
        deck_id=uuid.uuid4(),
        category_id=uuid.uuid4()
    )


@pytest.fixture
def mock_request():
    """Create a mock Pyramid request for testing views."""
    request = DummyRequest()
    request.db_conn = Mock()
    request.json_body = {}
    request.params = {}
    request.matchdict = {}
    
    # Set up response mock with status attributes
    mock_response = Mock()
    mock_response.status = 200
    mock_response.status_code = 200
    request.response = mock_response
    
    return request


@pytest.fixture
def pyramid_config():
    """Create a Pyramid configuration for testing."""
    config = Configurator()
    config.include('pyramid_chameleon')
    return config
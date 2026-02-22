import uuid
from datetime import datetime

from flashly.models.follower import FollowerModel


class TestFollowerModel:
    """Test cases for FollowerModel."""

    def test_follower_model_creation(self, sample_follower):
        """Test creating a FollowerModel instance."""
        assert isinstance(sample_follower.id, uuid.UUID)
        assert isinstance(sample_follower.follower_id, uuid.UUID)
        assert isinstance(sample_follower.following_id, uuid.UUID)
        assert isinstance(sample_follower.created_at, datetime)

    def test_different_follower_following_ids(self):
        """Test follower with different IDs."""
        follower_id = uuid.uuid4()
        following_id = uuid.uuid4()

        # Ensure they are different
        assert follower_id != following_id

        follower = FollowerModel(
            id=uuid.uuid4(), follower_id=follower_id, following_id=following_id, created_at=datetime.now()
        )

        assert follower.follower_id == follower_id
        assert follower.following_id == following_id

    def test_follower_relationship_symmetry(self):
        """Test that follower relationships can be bidirectional."""
        user_a_id = uuid.uuid4()
        user_b_id = uuid.uuid4()

        # User A follows User B
        follow_1 = FollowerModel(
            id=uuid.uuid4(), follower_id=user_a_id, following_id=user_b_id, created_at=datetime.now()
        )

        # User B follows User A
        follow_2 = FollowerModel(
            id=uuid.uuid4(), follower_id=user_b_id, following_id=user_a_id, created_at=datetime.now()
        )

        assert follow_1.follower_id == user_a_id
        assert follow_1.following_id == user_b_id
        assert follow_2.follower_id == user_b_id
        assert follow_2.following_id == user_a_id

    def test_unique_follower_ids(self):
        """Test that follower IDs are unique."""
        followers = []
        for _ in range(5):
            follower = FollowerModel(
                id=uuid.uuid4(), follower_id=uuid.uuid4(), following_id=uuid.uuid4(), created_at=datetime.now()
            )
            followers.append(follower)

        # Check that all IDs are unique
        ids = [f.id for f in followers]
        assert len(set(ids)) == len(ids)

    def test_tablename_attribute(self):
        """Test that __tablename__ is set correctly."""
        assert FollowerModel.__tablename__ == "followers"

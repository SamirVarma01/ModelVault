"""Tests for metadata management."""

import pytest
import json
from pathlib import Path
from nexus.metadata import MetadataManager


class TestMetadataManager:
    """Test metadata file management."""

    @pytest.fixture
    def tmp_project(self, tmp_path):
        """Create a temporary project directory."""
        return tmp_path

    @pytest.fixture
    def metadata_manager(self, tmp_project):
        """Create metadata manager."""
        return MetadataManager(tmp_project)

    def test_add_model(self, metadata_manager, tmp_project):
        """Test adding a model to metadata."""
        metadata_manager.add_model(
            commit_hash="abc123",
            model_name="test_model",
            storage_uri="test_model/abc123.pt",
            file_size=1024,
            file_extension="pt"
        )
        metadata_manager.save()

        # Verify metadata was added
        metadata_file = tmp_project / ".nexus_meta.json"
        assert metadata_file.exists()

        data = json.loads(metadata_file.read_text())
        assert "test_model" in data["models"]
        assert "abc123" in data["models"]["test_model"]
        assert data["models"]["test_model"]["abc123"]["commit_hash"] == "abc123"
        assert data["latest"]["test_model"] == "abc123"

    def test_add_multiple_models(self, metadata_manager):
        """Test adding multiple versions of same model."""
        # Add first version
        metadata_manager.add_model(
            commit_hash="abc123",
            model_name="test_model",
            storage_uri="test_model/abc123.pt",
            file_size=1024,
            file_extension="pt"
        )
        metadata_manager.save()

        # Add second version
        metadata_manager.add_model(
            commit_hash="def456",
            model_name="test_model",
            storage_uri="test_model/def456.pt",
            file_size=2048,
            file_extension="pt"
        )

        models = metadata_manager.list_models()
        assert len(models) == 2

        # Latest should be the second one
        latest = [m for m in models if m["is_latest"]][0]
        assert latest["commit_hash"] == "def456"

    def test_get_storage_uri(self, metadata_manager):
        """Test retrieving storage URI by commit hash."""
        metadata_manager.add_model(
            commit_hash="abc123",
            model_name="test_model",
            storage_uri="test_model/abc123.pt",
            file_size=1024,
            file_extension="pt"
        )
        metadata_manager.save()

        uri = metadata_manager.get_storage_uri("abc123")
        assert uri == "test_model/abc123.pt"

    def test_get_latest_model(self, metadata_manager):
        """Test retrieving latest model."""
        # Add multiple versions
        metadata_manager.add_model(
            commit_hash="abc123",
            model_name="test_model",
            storage_uri="test_model/abc123.pt",
            file_size=1024,
            file_extension="pt"
        )
        metadata_manager.save()

        metadata_manager.add_model(
            commit_hash="def456",
            model_name="test_model",
            storage_uri="test_model/def456.pt",
            file_size=2048,
            file_extension="pt"
        )

        # Get latest
        uri = metadata_manager.get_storage_uri("latest", "test_model")
        assert uri == "test_model/def456.pt"

    def test_rollback(self, metadata_manager):
        """Test rolling back to previous version."""
        # Add two versions
        metadata_manager.add_model(
            commit_hash="abc123",
            model_name="test_model",
            storage_uri="test_model/abc123.pt",
            file_size=1024,
            file_extension="pt"
        )
        metadata_manager.save()

        metadata_manager.add_model(
            commit_hash="def456",
            model_name="test_model",
            storage_uri="test_model/def456.pt",
            file_size=2048,
            file_extension="pt"
        )
        metadata_manager.save()

        # Rollback to first version
        metadata_manager.set_latest("abc123", "test_model")

        # Verify
        uri = metadata_manager.get_storage_uri("latest", "test_model")
        assert uri == "test_model/abc123.pt"

    def test_list_models(self, metadata_manager):
        """Test listing all models."""
        # Add models
        metadata_manager.add_model(
            commit_hash="abc123",
            model_name="model_a",
            storage_uri="model_a/abc123.pt",
            file_size=1024,
            file_extension="pt"
        )
        metadata_manager.save()

        metadata_manager.add_model(
            commit_hash="def456",
            model_name="model_b",
            storage_uri="model_b/def456.pt",
            file_size=2048,
            file_extension="pt"
        )

        models = metadata_manager.list_models()
        assert len(models) == 2

        names = [m["model_name"] for m in models]
        assert "model_a" in names
        assert "model_b" in names

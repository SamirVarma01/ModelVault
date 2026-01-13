"""Tests for configuration management."""

import pytest
from pathlib import Path
from nexus.config import Config, CloudProvider


class TestConfig:
    """Test configuration loading and validation."""

    @pytest.fixture
    def tmp_project(self, tmp_path):
        """Create temporary project directory."""
        return tmp_path

    def test_load_s3_config(self, tmp_project):
        """Test loading S3 configuration."""
        config_file = tmp_project / ".nexusrc"
        config_file.write_text("provider: s3\nbucket: my-s3-bucket\n")

        config = Config(tmp_project)
        assert config.provider == CloudProvider.S3
        assert config.bucket_name == "my-s3-bucket"

    def test_load_gcs_config(self, tmp_project):
        """Test loading GCS configuration."""
        config_file = tmp_project / ".nexusrc"
        config_file.write_text("provider: gcs\nbucket: my-gcs-bucket\n")

        config = Config(tmp_project)
        assert config.provider == CloudProvider.GCS
        assert config.bucket_name == "my-gcs-bucket"

    def test_missing_bucket(self, tmp_project):
        """Test error when bucket is not configured."""
        config_file = tmp_project / ".nexusrc"
        config_file.write_text("provider: s3\n")

        config = Config(tmp_project)
        with pytest.raises(ValueError, match="Bucket name not configured"):
            _ = config.bucket_name

    def test_invalid_provider(self, tmp_project):
        """Test error with invalid provider."""
        config_file = tmp_project / ".nexusrc"
        config_file.write_text("provider: invalid\nbucket: test\n")

        config = Config(tmp_project)
        with pytest.raises(ValueError, match="Invalid provider"):
            _ = config.provider

    def test_default_provider(self, tmp_project):
        """Test default provider is S3."""
        config_file = tmp_project / ".nexusrc"
        config_file.write_text("bucket: test-bucket\n")

        config = Config(tmp_project)
        assert config.provider == CloudProvider.S3

    def test_no_config_file(self, tmp_project):
        """Test behavior when config file doesn't exist."""
        config = Config(tmp_project)

        # Should default to S3
        assert config.provider == CloudProvider.S3

        # But should fail when accessing bucket
        with pytest.raises(ValueError, match="Bucket name not configured"):
            _ = config.bucket_name

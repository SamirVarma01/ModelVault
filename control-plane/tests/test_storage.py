"""Tests for cloud storage backends."""

import pytest
import os
from pathlib import Path
import tempfile
from nexus.storage import S3StorageBackend, GCSStorageBackend, get_storage_backend
from nexus.config import Config


class TestS3Storage:
    """Test S3 storage backend."""

    @pytest.fixture
    def s3_storage(self):
        """Create S3 storage instance."""
        # Skip if no AWS credentials
        if not os.getenv('AWS_ACCESS_KEY_ID'):
            pytest.skip("AWS credentials not configured")

        bucket = os.getenv('TEST_BUCKET', 'test-nexus-bucket')
        return S3StorageBackend(bucket)

    def test_upload_download(self, s3_storage, tmp_path):
        """Test uploading and downloading a file."""
        # Create a test file
        test_file = tmp_path / "test_model.txt"
        test_content = b"test model content"
        test_file.write_bytes(test_content)

        # Upload to S3
        storage_uri = "test/test_model.txt"
        s3_storage.upload(test_file, storage_uri)

        # Download from S3
        download_path = tmp_path / "downloaded_model.txt"
        s3_storage.download(storage_uri, download_path)

        # Verify content
        assert download_path.read_bytes() == test_content

        # Cleanup - delete from S3
        s3_storage.client.delete_object(
            Bucket=s3_storage.bucket_name,
            Key=storage_uri
        )


class TestGCSStorage:
    """Test Google Cloud Storage backend."""

    @pytest.fixture
    def gcs_storage(self):
        """Create GCS storage instance."""
        # Skip if no GCP credentials
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            pytest.skip("GCP credentials not configured")

        bucket = os.getenv('TEST_BUCKET', 'test-nexus-bucket')
        return GCSStorageBackend(bucket)

    def test_upload_download(self, gcs_storage, tmp_path):
        """Test uploading and downloading a file."""
        # Create a test file
        test_file = tmp_path / "test_model.txt"
        test_content = b"test model content"
        test_file.write_bytes(test_content)

        # Upload to GCS
        storage_uri = "test/test_model.txt"
        gcs_storage.upload(test_file, storage_uri)

        # Download from GCS
        download_path = tmp_path / "downloaded_model.txt"
        gcs_storage.download(storage_uri, download_path)

        # Verify content
        assert download_path.read_bytes() == test_content

        # Cleanup
        blob = gcs_storage.bucket.blob(storage_uri)
        blob.delete()


class TestStorageFactory:
    """Test storage backend factory."""

    def test_get_s3_backend(self, tmp_path):
        """Test getting S3 backend from config."""
        # Create a config file
        config_file = tmp_path / ".nexusrc"
        config_file.write_text("provider: s3\nbucket: test-bucket\n")

        config = Config(tmp_path)
        storage = get_storage_backend(config)

        assert isinstance(storage, S3StorageBackend)
        assert storage.bucket_name == "test-bucket"

    def test_get_gcs_backend(self, tmp_path):
        """Test getting GCS backend from config."""
        # Skip if no GCP credentials
        if not os.getenv('GOOGLE_APPLICATION_CREDENTIALS'):
            pytest.skip("GCP credentials not configured")

        # Create a config file
        config_file = tmp_path / ".nexusrc"
        config_file.write_text("provider: gcs\nbucket: test-bucket\n")

        config = Config(tmp_path)
        storage = get_storage_backend(config)

        assert isinstance(storage, GCSStorageBackend)
        assert storage.bucket_name == "test-bucket"

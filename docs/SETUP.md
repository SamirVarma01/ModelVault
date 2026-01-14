# NexusML Control Plane Setup Guide

## Installation

1. Navigate to the control-plane directory and install in development mode:
   ```bash
   cd control-plane
   pip install -e .
   ```

2. Configure cloud credentials:

   **For AWS S3:**
   - Set up AWS credentials using one of these methods:
     - AWS CLI: `aws configure`
     - Environment variables: `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
     - IAM role (if running on EC2)

   **For Google Cloud Storage:**
   - Install and configure gcloud CLI
   - Set up application default credentials:
     ```bash
     gcloud auth application-default login
     ```
   - Or set `GOOGLE_APPLICATION_CREDENTIALS` environment variable to point to a service account key file

3. Create a `.nexusrc` configuration file in your project root:
   ```yaml
   provider: s3  # or "gcs"
   bucket: your-bucket-name
   ```

## Usage Examples

1. **Store a model:**
   ```bash
   nexus store ./models/my_model.pkl my_model
   ```
   This will:
   - Check that the Git repository is clean
   - Get the current commit hash
   - Upload the model to cloud storage
   - Create/update `.nexus_meta.json`
   - Prompt you to commit and push the metadata file

2. **Load a model:**
   ```bash
   # Load by commit hash
   nexus load abc123def456 ./models/restored_model.pkl

   # Load latest model
   nexus load latest ./models/latest_model.pkl --model-name my_model
   ```

3. **List all stored models:**
   ```bash
   nexus list
   ```

4. **Rollback to a previous version:**
   ```bash
   nexus rollback abc123def456 my_model
   ```

## Project Structure

```
NexusML/
├── control-plane/
│   ├── nexus/
│   │   ├── __init__.py
│   │   ├── cli.py           # CLI commands
│   │   ├── config.py        # Configuration management
│   │   ├── storage.py       # Cloud storage abstraction (S3/GCS)
│   │   ├── git_utils.py     # Git integration
│   │   └── metadata.py      # Metadata management
│   ├── tests/               # Test suite
│   ├── scripts/             # Utility scripts
│   └── pyproject.toml       # Package configuration
├── data-plane/              # Inference serving (future)
├── docs/                    # Documentation
└── .nexusrc                 # Config file

```

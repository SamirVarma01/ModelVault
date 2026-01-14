# NexusML Demo Guide

## Quick Demo (No Cloud Required)

Run the demo script to see metadata and Git integration:

```bash
cd control-plane/scripts
python3 demo.py
```

This shows:
- How metadata is stored and managed
- Git integration features
- CLI command overview

## Full Demo (Requires Cloud Setup)

### Step 1: Set Up Configuration

Create a `.nexusrc` file in the project root:

```yaml
provider: s3  # or "gcs"
bucket: your-bucket-name
```

### Step 2: Configure Cloud Credentials

**For AWS S3:**
```bash
aws configure
# Or set environment variables:
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export TEST_BUCKET=your-bucket-name
```

**For Google Cloud Storage:**
```bash
gcloud auth application-default login
# Or set service account:
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

### Step 3: Create a Sample Model File

```bash
# Create a pickle model file for testing
python3 << 'EOF'
import pickle
model_data = {'weights': [1.0, 2.0, 3.0], 'accuracy': 0.95}
with open('test_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)
EOF
```

### Step 4: Test the Commands

```bash
# Make sure you're in a Git repository and it's clean
git status

# Store a model
nexus store test_model.pkl my_test_model

# List stored models
nexus list

# Load a model (replace COMMIT_HASH with actual hash from list)
nexus load COMMIT_HASH ./restored_model.pkl

# Load latest version
nexus load latest ./latest_model.pkl --model-name my_test_model
```

## Expected Output

### `nexus store`
```
Current commit hash: abc123def456
Uploading model to cloud storage...
✓ Model artifact stored successfully!
Storage URI: my_test_model/abc123def456.pkl

Action required: Please git commit and git push the updated .nexus_meta.json file.
```

### `nexus list`
```
┌─────────────┬──────────────┬──────────────────────────────────┬─────────┬─────────────────────┬────────┐
│ Model Name  │ Commit Hash  │ Storage URI                      │ Size    │ Timestamp           │ Latest │
├─────────────┼──────────────┼──────────────────────────────────┼─────────┼─────────────────────┼────────┤
│ my_test_model│ abc123def456 │ my_test_model/abc123def456.pkl  │ 10.00 MB│ 2024-01-15 10:30:00 │   ✓    │
└─────────────┴──────────────┴──────────────────────────────────┴─────────┴─────────────────────┴────────┘
```

### `nexus load`
```
Downloading model from cloud storage...
✓ Model artifact from commit abc123def456 successfully loaded to ./restored_model.pkl
```

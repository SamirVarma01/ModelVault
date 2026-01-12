# ModelVault

A Model Artifact Management CLI - Git-integrated versioned storage for model files.

ModelVault handles the off-site storage of large model binaries while maintaining a lightweight, version-controlled link to the code that created it. This tool ensures reproducibility by linking model artifacts to specific Git commits.

## Installation

```bash
pip install -e .
```

## Quick Start

1. Configure your cloud storage settings:
   ```bash
   # Create .modelvaultrc file in your project root
   ```

2. Store a model:
   ```bash
   modelvault store ./models/my_model.pkl my_model
   ```

3. Load a model:
   ```bash
   modelvault load <commit_hash> ./models/restored_model.pkl
   ```

## Commands

- `modelvault store <model_path> <model_name>` - Store a model artifact
- `modelvault load <commit_hash> <output_path>` - Load a model artifact
- `modelvault list` - List all stored models
- `modelvault rollback <commit_hash>` - Rollback to a previous model version

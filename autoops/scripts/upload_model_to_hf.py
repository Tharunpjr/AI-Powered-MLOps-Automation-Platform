#!/usr/bin/env python3
"""
Upload trained models to Hugging Face Model Hub (Free Storage)
"""

import argparse
import os
from pathlib import Path

try:
    from huggingface_hub import HfApi, create_repo
    from huggingface_hub.utils import RepositoryNotFoundError
except ImportError:
    print("Installing huggingface_hub...")
    os.system("pip install huggingface_hub")
    from huggingface_hub import HfApi, create_repo
    from huggingface_hub.utils import RepositoryNotFoundError


def upload_models(repo_id: str, models_dir: str = "models", token: str = None):
    """
    Upload all models from models directory to Hugging Face Hub.
    
    Args:
        repo_id: Repository ID (username/repo-name)
        models_dir: Directory containing models
        token: HF token (or set HF_TOKEN env var)
    """
    api = HfApi(token=token)
    
    # Create repository if it doesn't exist
    try:
        api.repo_info(repo_id=repo_id, repo_type="model")
        print(f"Repository {repo_id} already exists")
    except RepositoryNotFoundError:
        print(f"Creating repository {repo_id}...")
        create_repo(repo_id=repo_id, repo_type="model", token=token)
    
    # Upload all model files
    models_path = Path(models_dir)
    
    if not models_path.exists():
        print(f"Error: Models directory {models_dir} not found")
        return
    
    model_files = list(models_path.glob("*.pkl")) + list(models_path.glob("*.pt"))
    
    if not model_files:
        print(f"No model files found in {models_dir}")
        return
    
    print(f"\nUploading {len(model_files)} model files to {repo_id}...")
    
    for model_file in model_files:
        print(f"  Uploading {model_file.name}...")
        api.upload_file(
            path_or_fileobj=str(model_file),
            path_in_repo=model_file.name,
            repo_id=repo_id,
            repo_type="model",
            token=token
        )
        print(f"  ✅ {model_file.name} uploaded successfully")
    
    # Upload metadata files
    metadata_files = list(models_path.glob("*.json"))
    for metadata_file in metadata_files:
        print(f"  Uploading {metadata_file.name}...")
        api.upload_file(
            path_or_fileobj=str(metadata_file),
            path_in_repo=metadata_file.name,
            repo_id=repo_id,
            repo_type="model",
            token=token
        )
    
    print(f"\n✅ All models uploaded successfully!")
    print(f"📦 View your models at: https://huggingface.co/{repo_id}")
    print(f"\n💡 To download in your app:")
    print(f"   from huggingface_hub import hf_hub_download")
    print(f"   model_path = hf_hub_download(repo_id='{repo_id}', filename='model.pkl')")


def main():
    parser = argparse.ArgumentParser(description="Upload models to Hugging Face Hub")
    parser.add_argument("--repo-id", required=True, help="Repository ID (username/repo-name)")
    parser.add_argument("--models-dir", default="models", help="Models directory")
    parser.add_argument("--token", help="HF token (or set HF_TOKEN env var)")
    
    args = parser.parse_args()
    
    token = args.token or os.getenv("HF_TOKEN")
    
    if not token:
        print("Error: Hugging Face token required")
        print("Get your token from: https://huggingface.co/settings/tokens")
        print("Then either:")
        print("  1. Pass --token YOUR_TOKEN")
        print("  2. Set HF_TOKEN environment variable")
        return
    
    upload_models(args.repo_id, args.models_dir, token)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Download models from Hugging Face Model Hub
"""

import argparse
import os
from pathlib import Path

try:
    from huggingface_hub import hf_hub_download
except ImportError:
    print("Installing huggingface_hub...")
    os.system("pip install huggingface_hub")
    from huggingface_hub import hf_hub_download


def download_models(repo_id: str, output_dir: str = "models", token: str = None):
    """
    Download all models from Hugging Face Hub.
    
    Args:
        repo_id: Repository ID (username/repo-name)
        output_dir: Output directory for models
        token: HF token (optional for public repos)
    """
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # List of common model files
    model_files = [
        "model.pkl",
        "pytorch_model.pt",
        "model_metadata.json",
        "pytorch_model_metadata.json"
    ]
    
    print(f"Downloading models from {repo_id}...")
    
    for filename in model_files:
        try:
            print(f"  Downloading {filename}...")
            downloaded_path = hf_hub_download(
                repo_id=repo_id,
                filename=filename,
                token=token,
                cache_dir=None,
                local_dir=output_dir,
                local_dir_use_symlinks=False
            )
            print(f"  ✅ {filename} downloaded to {downloaded_path}")
        except Exception as e:
            print(f"  ⚠️  {filename} not found or error: {e}")
    
    print(f"\n✅ Models downloaded to {output_dir}")


def main():
    parser = argparse.ArgumentParser(description="Download models from Hugging Face Hub")
    parser.add_argument("--repo-id", required=True, help="Repository ID (username/repo-name)")
    parser.add_argument("--output-dir", default="models", help="Output directory")
    parser.add_argument("--token", help="HF token (optional for public repos)")
    
    args = parser.parse_args()
    
    token = args.token or os.getenv("HF_TOKEN")
    
    download_models(args.repo_id, args.output_dir, token)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
AutoOps CLI - Command Line Interface
Main CLI for AutoOps MLOps automation toolkit.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import Dict, Any, Optional

# Add the project root to the path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from cli.commands.start import start_service
from cli.commands.status import check_status


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser."""
    parser = argparse.ArgumentParser(
        prog="autoops",
        description="AutoOps MLOps automation toolkit CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  autoops start                    # Start the model service
  autoops status                   # Check service status
  autoops train --data data.csv    # Train a model
  autoops deploy --env production  # Deploy to environment
        """
    )
    
    # Global options
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default="configs/default_config.yaml",
        help="Path to configuration file"
    )
    
    # Subcommands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands"
    )
    
    # Start command
    start_parser = subparsers.add_parser(
        "start",
        help="Start AutoOps services"
    )
    start_parser.add_argument(
        "--service",
        choices=["model", "all"],
        default="all",
        help="Service to start"
    )
    start_parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port for model service"
    )
    start_parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host for model service"
    )
    
    # Status command
    status_parser = subparsers.add_parser(
        "status",
        help="Check service status"
    )
    status_parser.add_argument(
        "--service",
        choices=["model", "all"],
        default="all",
        help="Service to check"
    )
    status_parser.add_argument(
        "--url",
        type=str,
        default="http://localhost:8000",
        help="Service URL"
    )
    
    # Train command
    train_parser = subparsers.add_parser(
        "train",
        help="Train a model"
    )
    train_parser.add_argument(
        "--data",
        type=str,
        required=True,
        help="Path to training data"
    )
    train_parser.add_argument(
        "--output",
        type=str,
        default="models/",
        help="Output directory for model"
    )
    train_parser.add_argument(
        "--model-type",
        choices=["random_forest", "dummy"],
        default="random_forest",
        help="Type of model to train"
    )
    
    # Deploy command
    deploy_parser = subparsers.add_parser(
        "deploy",
        help="Deploy to environment"
    )
    deploy_parser.add_argument(
        "--env",
        choices=["dev", "staging", "production"],
        default="dev",
        help="Target environment"
    )
    deploy_parser.add_argument(
        "--namespace",
        type=str,
        default="autoops",
        help="Kubernetes namespace"
    )
    deploy_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be deployed"
    )
    
    # Test command
    test_parser = subparsers.add_parser(
        "test",
        help="Run tests"
    )
    test_parser.add_argument(
        "--type",
        choices=["unit", "integration", "all"],
        default="all",
        help="Type of tests to run"
    )
    test_parser.add_argument(
        "--coverage",
        action="store_true",
        help="Run with coverage"
    )
    
    return parser


def handle_start_command(args: argparse.Namespace) -> int:
    """Handle the start command."""
    try:
        result = start_service(
            service=args.service,
            port=args.port,
            host=args.host,
            verbose=args.verbose
        )
        
        if result["success"]:
            print("✅ Service started successfully")
            return 0
        else:
            print(f"❌ Failed to start service: {result['error']}")
            return 1
            
    except Exception as e:
        print(f"❌ Error starting service: {e}")
        return 1


def handle_status_command(args: argparse.Namespace) -> int:
    """Handle the status command."""
    try:
        result = check_status(
            service=args.service,
            url=args.url,
            verbose=args.verbose
        )
        
        if result["success"]:
            print("✅ Service is healthy")
            return 0
        else:
            print(f"❌ Service is not healthy: {result['error']}")
            return 1
            
    except Exception as e:
        print(f"❌ Error checking status: {e}")
        return 1


def handle_train_command(args: argparse.Namespace) -> int:
    """Handle the train command."""
    try:
        import subprocess
        
        # Build training command
        cmd = [
            "python", "pipelines/training/train.py",
            "--data", args.data,
            "--out", args.output,
            "--model-type", args.model_type
        ]
        
        print(f"🔄 Training model with data: {args.data}")
        print(f"📁 Output directory: {args.output}")
        print(f"🤖 Model type: {args.model_type}")
        
        # Run training
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Model training completed successfully")
            print(result.stdout)
            return 0
        else:
            print(f"❌ Model training failed: {result.stderr}")
            return 1
            
    except Exception as e:
        print(f"❌ Error training model: {e}")
        return 1


def handle_deploy_command(args: argparse.Namespace) -> int:
    """Handle the deploy command."""
    try:
        import subprocess
        
        # Build deployment command
        cmd = ["bash", "scripts/deploy_k8s.sh"]
        
        if args.namespace:
            cmd.extend(["--namespace", args.namespace])
        
        if args.dry_run:
            cmd.append("--dry-run")
        
        print(f"🚀 Deploying to environment: {args.env}")
        print(f"📦 Namespace: {args.namespace}")
        
        if args.dry_run:
            print("🔍 Dry run mode - showing what would be deployed")
        
        # Run deployment
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Deployment completed successfully")
            print(result.stdout)
            return 0
        else:
            print(f"❌ Deployment failed: {result.stderr}")
            return 1
            
    except Exception as e:
        print(f"❌ Error deploying: {e}")
        return 1


def handle_test_command(args: argparse.Namespace) -> int:
    """Handle the test command."""
    try:
        import subprocess
        
        # Build test command
        cmd = ["python", "-m", "pytest"]
        
        if args.type == "unit":
            cmd.append("services/model_service/tests/")
        elif args.type == "integration":
            cmd.append("tests/integration/")
        else:  # all
            cmd.append("tests/")
            cmd.append("services/model_service/tests/")
        
        if args.coverage:
            cmd.extend(["--cov", "--cov-report=html"])
        
        print(f"🧪 Running {args.type} tests...")
        
        if args.coverage:
            print("📊 Coverage report will be generated")
        
        # Run tests
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ All tests passed")
            print(result.stdout)
            return 0
        else:
            print(f"❌ Some tests failed: {result.stderr}")
            return 1
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return 1


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Handle no command
    if not args.command:
        parser.print_help()
        return 1
    
    # Route to appropriate handler
    handlers = {
        "start": handle_start_command,
        "status": handle_status_command,
        "train": handle_train_command,
        "deploy": handle_deploy_command,
        "test": handle_test_command
    }
    
    handler = handlers.get(args.command)
    if handler:
        return handler(args)
    else:
        print(f"❌ Unknown command: {args.command}")
        return 1


if __name__ == "__main__":
    sys.exit(main())

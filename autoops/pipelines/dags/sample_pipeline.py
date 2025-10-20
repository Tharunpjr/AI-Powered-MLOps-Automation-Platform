"""
AutoOps Sample Pipeline DAG
Example DAG for MLOps pipeline orchestration.
This can be used with Apache Airflow or Dagster.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List
import os
import sys
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent.parent.parent
sys.path.append(str(project_root))

# For Airflow DAG
try:
    from airflow import DAG
    from airflow.operators.python import PythonOperator
    from airflow.operators.bash import BashOperator
    from airflow.sensors.filesystem import FileSensor
    AIRFLOW_AVAILABLE = True
except ImportError:
    AIRFLOW_AVAILABLE = False
    print("Airflow not available - using mock DAG structure")

# For Dagster
try:
    from dagster import job, op, sensor, RunRequest, SkipReason
    DAGSTER_AVAILABLE = True
except ImportError:
    DAGSTER_AVAILABLE = False
    print("Dagster not available - using mock DAG structure")


def data_ingestion_task(**context) -> Dict[str, Any]:
    """
    Data ingestion task.
    
    Returns:
        Dictionary with ingestion results
    """
    print("🔄 Starting data ingestion...")
    
    # Simulate data ingestion
    data_path = "examples/sample_data/small_dataset.csv"
    
    if not os.path.exists(data_path):
        print(f"Creating sample data at {data_path}")
        # Create sample data if it doesn't exist
        import pandas as pd
        import numpy as np
        
        np.random.seed(42)
        n_samples = 1000
        n_features = 4
        
        # Generate synthetic data
        X = np.random.randn(n_samples, n_features)
        y = np.sum(X, axis=1) + 0.1 * np.random.randn(n_samples)
        
        # Create DataFrame
        feature_names = [f"feature_{i}" for i in range(n_features)]
        df = pd.DataFrame(X, columns=feature_names)
        df['target'] = y
        
        # Save data
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        df.to_csv(data_path, index=False)
        print(f"Created sample data with {n_samples} samples and {n_features} features")
    
    result = {
        "data_path": data_path,
        "samples": 1000,
        "features": 4,
        "status": "success"
    }
    
    print("✅ Data ingestion completed")
    return result


def data_preprocessing_task(**context) -> Dict[str, Any]:
    """
    Data preprocessing task.
    
    Returns:
        Dictionary with preprocessing results
    """
    print("🔄 Starting data preprocessing...")
    
    # Get data from previous task
    data_path = context['task_instance'].xcom_pull(task_ids='data_ingestion')['data_path']
    
    # Simulate preprocessing
    import pandas as pd
    
    df = pd.read_csv(data_path)
    print(f"Loaded data with shape: {df.shape}")
    
    # Basic preprocessing
    df_processed = df.copy()
    
    # Handle missing values
    if df_processed.isnull().any().any():
        df_processed = df_processed.fillna(df_processed.mean())
        print("Handled missing values")
    
    # Save processed data
    processed_path = "data/processed_data.csv"
    os.makedirs(os.path.dirname(processed_path), exist_ok=True)
    df_processed.to_csv(processed_path, index=False)
    
    result = {
        "processed_data_path": processed_path,
        "original_shape": df.shape,
        "processed_shape": df_processed.shape,
        "status": "success"
    }
    
    print("✅ Data preprocessing completed")
    return result


def model_training_task(**context) -> Dict[str, Any]:
    """
    Model training task.
    
    Returns:
        Dictionary with training results
    """
    print("🔄 Starting model training...")
    
    # Get processed data from previous task
    processed_data_path = context['task_instance'].xcom_pull(task_ids='data_preprocessing')['processed_data_path']
    
    # Run training script
    training_cmd = f"python pipelines/training/train.py --data {processed_data_path} --out models/ --model-type random_forest"
    
    import subprocess
    result = subprocess.run(training_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Training failed: {result.stderr}")
    
    training_result = {
        "model_path": "models/model.pkl",
        "training_status": "success",
        "output": result.stdout
    }
    
    print("✅ Model training completed")
    return training_result


def model_evaluation_task(**context) -> Dict[str, Any]:
    """
    Model evaluation task.
    
    Returns:
        Dictionary with evaluation results
    """
    print("🔄 Starting model evaluation...")
    
    # Get model from previous task
    model_path = context['task_instance'].xcom_pull(task_ids='model_training')['model_path']
    processed_data_path = context['task_instance'].xcom_pull(task_ids='data_preprocessing')['processed_data_path']
    
    # Run evaluation
    evaluation_cmd = f"python pipelines/training/evaluate.py --model {model_path} --data {processed_data_path} --out evaluation_results.json"
    
    import subprocess
    result = subprocess.run(evaluation_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Evaluation failed: {result.stderr}")
    
    # Load evaluation results
    import json
    with open("evaluation_results.json", 'r') as f:
        eval_results = json.load(f)
    
    evaluation_result = {
        "evaluation_results": eval_results,
        "evaluation_status": "success",
        "passes_quality_gates": eval_results.get("passes_quality_gates", False)
    }
    
    print("✅ Model evaluation completed")
    return evaluation_result


def model_deployment_task(**context) -> Dict[str, Any]:
    """
    Model deployment task.
    
    Returns:
        Dictionary with deployment results
    """
    print("🔄 Starting model deployment...")
    
    # Get evaluation results
    eval_results = context['task_instance'].xcom_pull(task_ids='model_evaluation')['evaluation_results']
    
    # Check if model passes quality gates
    if not eval_results.get("passes_quality_gates", False):
        print("❌ Model failed quality gates - skipping deployment")
        return {
            "deployment_status": "skipped",
            "reason": "Quality gates failed"
        }
    
    # Simulate deployment
    print("Deploying model to staging environment...")
    
    # Build and push Docker image
    build_cmd = "cd services/model_service && docker build -t autoops/model-service:latest ."
    
    import subprocess
    result = subprocess.run(build_cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode != 0:
        raise Exception(f"Build failed: {result.stderr}")
    
    deployment_result = {
        "deployment_status": "success",
        "image_tag": "autoops/model-service:latest",
        "environment": "staging"
    }
    
    print("✅ Model deployment completed")
    return deployment_result


def model_validation_task(**context) -> Dict[str, Any]:
    """
    Model validation task.
    
    Returns:
        Dictionary with validation results
    """
    print("🔄 Starting model validation...")
    
    # Simulate model validation
    validation_result = {
        "validation_status": "success",
        "health_check": "passed",
        "performance_test": "passed",
        "load_test": "passed"
    }
    
    print("✅ Model validation completed")
    return validation_result


# Airflow DAG Definition
if AIRFLOW_AVAILABLE:
    default_args = {
        'owner': 'autoops',
        'depends_on_past': False,
        'start_date': datetime(2024, 1, 1),
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=5),
    }
    
    dag = DAG(
        'autoops_ml_pipeline',
        default_args=default_args,
        description='AutoOps MLOps Pipeline',
        schedule_interval=timedelta(days=1),
        catchup=False,
        tags=['mlops', 'autoops']
    )
    
    # Define tasks
    data_ingestion = PythonOperator(
        task_id='data_ingestion',
        python_callable=data_ingestion_task,
        dag=dag
    )
    
    data_preprocessing = PythonOperator(
        task_id='data_preprocessing',
        python_callable=data_preprocessing_task,
        dag=dag
    )
    
    model_training = PythonOperator(
        task_id='model_training',
        python_callable=model_training_task,
        dag=dag
    )
    
    model_evaluation = PythonOperator(
        task_id='model_evaluation',
        python_callable=model_evaluation_task,
        dag=dag
    )
    
    model_deployment = PythonOperator(
        task_id='model_deployment',
        python_callable=model_deployment_task,
        dag=dag
    )
    
    model_validation = PythonOperator(
        task_id='model_validation',
        python_callable=model_validation_task,
        dag=dag
    )
    
    # Define task dependencies
    data_ingestion >> data_preprocessing >> model_training >> model_evaluation >> model_deployment >> model_validation


# Dagster Job Definition
if DAGSTER_AVAILABLE:
    @op
    def data_ingestion_op():
        """Data ingestion operation."""
        return data_ingestion_task()
    
    @op
    def data_preprocessing_op(data_ingestion_result):
        """Data preprocessing operation."""
        return data_preprocessing_task()
    
    @op
    def model_training_op(data_preprocessing_result):
        """Model training operation."""
        return model_training_task()
    
    @op
    def model_evaluation_op(model_training_result):
        """Model evaluation operation."""
        return model_evaluation_task()
    
    @op
    def model_deployment_op(model_evaluation_result):
        """Model deployment operation."""
        return model_deployment_task()
    
    @op
    def model_validation_op(model_deployment_result):
        """Model validation operation."""
        return model_validation_task()
    
    @job
    def autoops_ml_pipeline():
        """AutoOps MLOps Pipeline Job."""
        data_result = data_ingestion_op()
        preprocessed_data = data_preprocessing_op(data_result)
        trained_model = model_training_op(preprocessed_data)
        evaluation_results = model_evaluation_op(trained_model)
        deployment_results = model_deployment_op(evaluation_results)
        validation_results = model_validation_op(deployment_results)
        return validation_results


# Standalone pipeline runner
def run_pipeline():
    """Run the pipeline standalone."""
    print("🚀 Starting AutoOps MLOps Pipeline")
    
    try:
        # Run tasks in sequence
        ingestion_result = data_ingestion_task()
        preprocessing_result = data_preprocessing_task()
        training_result = model_training_task()
        evaluation_result = model_evaluation_task()
        deployment_result = model_deployment_task()
        validation_result = model_validation_task()
        
        print("✅ Pipeline completed successfully!")
        
        return {
            "status": "success",
            "results": {
                "ingestion": ingestion_result,
                "preprocessing": preprocessing_result,
                "training": training_result,
                "evaluation": evaluation_result,
                "deployment": deployment_result,
                "validation": validation_result
            }
        }
        
    except Exception as e:
        print(f"❌ Pipeline failed: {e}")
        return {"status": "failed", "error": str(e)}


if __name__ == "__main__":
    # Run standalone pipeline
    result = run_pipeline()
    print(f"Pipeline result: {result}")

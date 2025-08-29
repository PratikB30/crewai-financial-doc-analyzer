import eventlet
eventlet.monkey_patch()

from celery import Celery
from crewai import Crew, Process
from sqlalchemy.orm import Session
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import financial_analysis, verification, investment_analysis, risk_assessment
from database import SessionLocal
import models
import os

# Configure Celery
# Replace 'redis://localhost:6379/0' with your Redis server URL if different
celery = Celery('tasks', broker='redis://localhost:6379/0')

@celery.task
def run_crew_task(task_id: str, query: str, file_path: str):
    """
    A Celery task to run the CrewAI process in the background.
    """
    db: Session = SessionLocal()
    try:
        # Define the crew
        financial_crew = Crew(
            agents=[financial_analyst, risk_assessor, investment_advisor, verifier],
            tasks=[financial_analysis, risk_assessment, investment_analysis, verification],
            process=Process.sequential,
        )

        # Kick off the crew with the provided inputs
        result = financial_crew.kickoff({
            'query': query,
            'file_path': file_path
        })

        # Update the database with the successful result
        db_task = db.query(models.TaskResult).filter(models.TaskResult.task_id == task_id).first()
        if db_task:
            db_task.status = "SUCCESS"
            db_task.result = str(result)
            db.commit()
            print(f"Database updated successfully for task_id: {task_id}")
        else:
            print(f"Warning: No database task found for task_id: {task_id}")
            
        return str(result)  # Return the result for Celery

    except Exception as e:
        print(f"Error in CrewAI task: {str(e)}")
        # If an error occurs, update the database with the failure status and error message
        db_task = db.query(models.TaskResult).filter(models.TaskResult.task_id == task_id).first()
        if db_task:
            db_task.status = "FAILURE"
            db_task.result = f"Failed analyzing the document: {str(e)}"
            db.commit()
            print(f"Database updated with failure for task_id: {task_id}")
        else:
            print(f"Warning: No database task found for task_id: {task_id}")
            
        return f"Error: {str(e)}"  # Return error for Celery
    finally:
        # Clean up the temporary file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Cleaned up file: {file_path}")
            except Exception as e:
                print(f"Error cleaning up file: {str(e)}")
        db.close()
        print("Database connection closed")
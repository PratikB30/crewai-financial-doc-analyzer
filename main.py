import eventlet
eventlet.monkey_patch()


from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
import os
import uuid
from sqlalchemy.orm import Session
import asyncio
from crewai import Crew, Process
from agents import financial_analyst, risk_assessor, investment_advisor, verifier
from task import (
    financial_analysis, 
    risk_assessment, 
    investment_analysis, 
    verification
)

#Import Celery task and db components
from celery_tasks import run_crew_task
import models
from database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Financial Document Analyzer")

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def run_crew(query: str, file_path: str="data/TSLA-Q2-2025-Update.pdf"):
    """To run the whole crew"""
    financial_crew = Crew(
        agents=[
            financial_analyst, 
            risk_assessor, 
            investment_advisor, 
            verifier
        ],
        tasks=[
            financial_analysis, 
            risk_assessment, 
            investment_analysis, 
            verification
        ],
        process=Process.sequential,
    )
    
    result = financial_crew.kickoff({
        'query': query,
        'file_path': file_path
    })
    return result

@app.get("/")
async def root():
    return {"message": "Financial Document Analyzer API is running"}


@app.post("/analyze", status_code=202)
async def analyze_financial_doc(
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights"),
    db: Session = Depends(get_db)
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    try:
        file_id = str(uuid.uuid4())
        file_path = f"data/financial_document_{file_id}.pdf"
        
        print(f"Generated file path: {file_path}")
    
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
            print(f"File saved successfully. Size: {len(content)} bytes")
            
        # 2. Create a task entry in the database
        task_id = str(uuid.uuid4())
        db_task = models.TaskResult(
            task_id=task_id,
            status="PENDING",
            file_path=file_path
        )
        db.add(db_task)
        db.commit()
        db.refresh(db_task)
        print(f"Database task created with ID: {task_id}")
        
        # 3. Send the task to the Celery worker
        print("Sending task to Celery worker...")
        run_crew_task.delay(task_id, query.strip(), file_path)
        print("Task sent to Celery worker successfully")

        return {"message": "Analysis has been queued.", "task_id": task_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing financial document: {str(e)}")


@app.get("/results/{task_id}")
async def get_analysis_result(task_id: str, db: Session = Depends(get_db)):
    """
    Fetches the result of an analysis task.
    """
    db_task = db.query(models.TaskResult).filter(models.TaskResult.task_id == task_id).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    if db_task.status == "PENDING":
        return {"status": "PENDING", "message": "Analysis is still in progress. Please check back later."}

    if db_task.status == "FAILURE":
        return JSONResponse(
            status_code=500,
            content={"status": "FAILURE", "result": db_task.result}
        )
        
        # If the task was successful, save the result to a file before returning
    if db_task.status == "SUCCESS":
        try:
            # Ensure the outputs directory exists
            output_dir = "outputs"
            os.makedirs(output_dir, exist_ok=True)
            
            # Define the output file path
            output_file_path = os.path.join(output_dir, f"{task_id}.txt")
            
            # Write the analysis result to the text file
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(db_task.result)
        except Exception as e:
            
            # Optional: Log an error if saving fails, but don't block the response
            print(f"Warning: Could not save result to file for task {task_id}. Error: {e}")

    return {"status": "SUCCESS", "result": db_task.result}


# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
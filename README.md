# crewai-financial-doc-analyzer

## Bugs Fixed
### 1. LLM model not defined for the Agents
- Defined a Google Cloud Console project to create a vertex-ai project using google's free credits.

### 2. Incomplete Investment Tool, Risk Tool classes in tools.py
- Implemented functions within the classes to run both async and sync. Additionally added a tool for Verification as well.

### 3. Wrong Task description in task.py
- Replaced task descriptions for all task to produce accurate analysis.

#### Upgrades
- Implemented async execution
- Added context to verification Task such that all the analysis generated is verified before passing.

### 4. Wrong Agent description in agents.py
- Replaced agent descriptions for all agents to ensure reliable analysis.

### 5. requirements.txt
- Found out modules and updated requirements.txt with packagew versions to stably run this project on crewai==0.130.0

### 6. Missing pdf module for FinancialDocumentTool Class
- Import pypdf to extract text from uploaded documents.


## Features added 
### 1. Implemented Celery and Redis based queue system (Clery
- Defined celery in celery_tasks.py which works with redis docker image.
- Once a user uploads and hits the route, a id is generated through which he can check his result on another route /results/{task_id} to know the status of the analysis.
  
### 2. SQLachemy datbase integration for small scale production
- Data is stored in a datbase "analysis_results.db".
- User can access their analysis data anytime using the task_id generated during generation.

### 3. Enhanced Analysis Quality
- Specialized Focus: Each agent focuses on their specific expertise
- Comprehensive Coverage: Multiple perspectives on the same data
- Cross-Verification: All findings are verified against original source


##	Setup and usage instructions

### 📂 Project Structure
- Here's a breakdown of the key files in this project:

```  
├── main.py                 # FastAPI application entry point, defines API endpoints.
├── celery_tasks.py         # Defines the Celery application and the background task for running the crew.
├── agents.py               # Defines the specialist AI agents (Financial Analyst, Risk Assessor, etc.).
├── tasks.py                # Defines the individual `Task` objects for each agent.
├── tools.py                # Contains custom `BaseTool` classes for agents (e.g., PDF reader).
├── database.py             # SQLAlchemy database setup (engine, SessionLocal).
├── models.py               # SQLAlchemy ORM models for database tables (e.g., TaskResult).
├── .env.template           # structure for .env file.
└── requirements.txt        # Python project dependencies.
```

### Running the System

1. Install package from requirements.txt

```
pip install -r requirements.txt
```

2. Start the redis docker container in the background

```
docker run -d -p 6379:6379 redis
```

3. Start Celery Queue using the following command in the repository terminal

```
celery -A celery_tasks.celery worker --loglevel=info -P eventlet
```

4. Run your FastAPI app

```
uvicorn main:app --reload
```

## API documentation

### 1. After completing system run, hit
```bash
http://localhost:8000/
```
If you see a message "Financial Document Analyzer API is running" that means your app is running.

### 2. Upload a PDF:
You can either open
```bash
http://localhost:8000/docs
```
and use /analyze route for analysis .

OR

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "file=@your_financial_document.pdf" \
  -F "query=Analyze this document for investment insights"
```

You will recieve a task_id after successful upload which can be used to check the status of the result.


### 3. Check Results:
You can either open
```bash
http://localhost:8000/docs
```

and use /result/{task_id} route for checking result.



OR

```bash
curl "http://localhost:8000/results/{task_id}"
```

Additionally, you can also check the entire result in outputs folder in your repository with your task_id as file name.
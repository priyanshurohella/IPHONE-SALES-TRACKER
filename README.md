### Run with Docker
1. Install Docker + Docker Compose
2. set up virtual environment [if running locally without docker]
   python3 -m venv venv
   source venv/bin/activate
   run pip install -r requirements.txt
3. Run: `docker-compose up --build`
4. API available at: http://0.0.0.0:8000
5. Swagger docs: http://0.0.0.0:8000/docs

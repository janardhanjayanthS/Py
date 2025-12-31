import logging
import os
import sys
from pathlib import Path

import uvicorn
from dotenv import load_dotenv

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
sys.path.insert(0, project_root)

# Load environment variables from .env.backend
# env_path = Path(project_root) / ".env.backend"
# load_dotenv(dotenv_path=env_path)

from lambda_handler import app

logger = logging.getLogger(__name__)

# Run the FastAPI app directly
if __name__ == "__main__":
    logger.info("Starting backend orchestrator server on http://0.0.0.0:5050")
    logger.info("API documentation available at http://localhost:5050/docs")
    # app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=5050)
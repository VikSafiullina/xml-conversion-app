from fastapi import FastAPI, HTTPException, Depends, Path
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import httpx
from base64 import b64encode
from app.utils import convert_to_custom_xml
from app.config import USERNAME, PASSWORD
from app.services import fetch_annotation_data, post_converted_data
import logging


app = FastAPI()
security = HTTPBasic()

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class AnnotationResponse(BaseModel):
    success: bool

def authenticate(credentials: HTTPBasicCredentials = Depends(security)):
    logger.debug(f"Received credentials: {credentials.username}, {credentials.password}")
    logger.debug(f"Expected credentials: {USERNAME}, {PASSWORD}")
    correct_username = credentials.username == USERNAME
    correct_password = credentials.password == PASSWORD
    if not (correct_username and correct_password):
        logger.warning("Authentication failed for user: %s", credentials.username)
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return credentials



@app.post("/export/{annotation_id}/{queue_id}", response_model=AnnotationResponse)
async def export_data(
    annotation_id: int = Path(..., title="Annotation ID", description="The ID of the annotation", ge=1),
    queue_id: int = Path(..., title="Queue ID", description="The ID of the queue", ge=1),
    credentials: HTTPBasicCredentials = Depends(authenticate)
):
    try:
        data = await fetch_annotation_data(annotation_id, queue_id)

        converted_xml = convert_to_custom_xml(data)
        logger.debug(converted_xml)

        encoded_xml = b64encode(converted_xml.encode()).decode()

        post_data = {
            "annotationId": annotation_id,
            "content": encoded_xml
        }

        success = await post_converted_data(post_data)

        return {"success": success}
    except httpx.HTTPStatusError as e:
        logger.error("HTTP error occurred: %s", e)
        raise HTTPException(status_code=e.response.status_code, detail="Failed to fetch annotation data")
    except Exception as e:
        logger.error("An error occurred: %s", e)
        raise HTTPException(status_code=500, detail="Internal server error")

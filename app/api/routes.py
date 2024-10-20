# app/api/routes.py
import logging
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from app.services.file_handler import handle_file
from app.services.data_validator import validate_data
from app.services.data_transformer import transform_data
from app.services.saas_api_client import saas_api_client
from app.utils.security import get_current_user
from app.dependencies import settings
from slowapi import Limiter
from slowapi.util import get_remote_address
import aiohttp

logger = logging.getLogger(__name__)

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/onboard")
@limiter.limit("5/minute")
async def onboard_customer(
    request: Request, 
    file: UploadFile = File(...), 
    current_user: dict = Depends(get_current_user)
):
    try:
        data = await handle_file(file)
        logger.info(f"File handled successfully: {file.filename}")

        validated_data = validate_data(data)
        logger.info("Data validated successfully")

        transformed_data = transform_data(validated_data)
        logger.info("Data transformed successfully")

        results = []
        for customer in transformed_data:
            result = await saas_api_client.onboard_customer(customer)
            results.append(result)
        logger.info(f"SaaS API integration successful: {results}")

        async with aiohttp.ClientSession() as session:
            url = f"{settings.SAAS_API_URL}{settings.MOCK_UPLOAD_SUCCESS}"
            async with session.get(url) as response:
                success_data = await response.json()
        logger.info(f"Mock upload successful: {success_data}")

        return {"message": success_data.get("message", "Upload successful"), "results": results}

    except Exception as e:
        logger.error(f"Error in onboard_customer: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"An error occurred during onboarding: {str(e)}")
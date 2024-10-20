# app/services/file_handler.py
import os
import aiohttp
from fastapi import UploadFile, HTTPException
from app.dependencies import settings

async def handle_file(file: UploadFile):
    # Check file size
    file_size = await file.read()
    await file.seek(0)
    if len(file_size) > settings.MAX_FILE_SIZE:
        async with aiohttp.ClientSession() as session:
            url = f"{settings.SAAS_API_URL}{settings.MOCK_FILE_SIZE_LIMIT}"
            async with session.get(url) as response:
                error_data = await response.json()
                raise HTTPException(status_code=400, detail=error_data["detail"])

    # Check file extension
    file_extension = os.path.splitext(file.filename)[1][1:].lower()
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        async with aiohttp.ClientSession() as session:
            url = f"{settings.SAAS_API_URL}{settings.MOCK_INVALID_FILE_TYPE}"
            async with session.get(url) as response:
                error_data = await response.json()
                raise HTTPException(status_code=400, detail=error_data["detail"])

    # Read the file content
    content = await file.read()
    return content.decode()
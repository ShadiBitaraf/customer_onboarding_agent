# app/services/data_validator.py
from pydantic import BaseModel, EmailStr
from typing import List, Dict, Any
import json


class CustomerData(BaseModel):
    name: str
    email: EmailStr
    company: str
    role: str


def validate_data(data: str) -> List[CustomerData]:
    try:
        # Parse the string data into a list of dictionaries
        parsed_data = json.loads(data)
        if not isinstance(parsed_data, list):
            parsed_data = [parsed_data]
    except json.JSONDecodeError:
        # If JSON parsing fails, assume it's a CSV-like string and parse it manually
        lines = data.strip().split("\n")
        headers = lines[0].split(",")
        parsed_data = [dict(zip(headers, line.split(","))) for line in lines[1:]]

    validated_data = []
    errors = []

    for idx, item in enumerate(parsed_data):
        try:
            validated_item = CustomerData(**item)
            validated_data.append(validated_item)
        except Exception as e:
            errors.append(f"Error in record {idx}: {str(e)}")

    if errors:
        raise ValueError("\n".join(errors))

    return validated_data

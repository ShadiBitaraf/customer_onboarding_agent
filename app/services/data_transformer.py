# app/services/data_transformer.py
from typing import List
from app.services.data_validator import CustomerData
from app.dependencies import settings  # Updated import

def transform_data(data: List[CustomerData]) -> List[dict]:
    transformed_data = []
    for item in data:
        transformed_item = {
            "customer_name": item.name,
            "customer_email": item.email,
            "customer_company": item.company,
            "customer_role": item.role
        }
        transformed_data.append(transformed_item)
    return transformed_data
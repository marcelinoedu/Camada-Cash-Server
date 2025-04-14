from models.category import Category
from repositories.category_repository import fetch_categories_by_type, fetch_categories
from typing import List

def fetch_categories_by_type_service(category_type: str) -> List[Category]:
    return fetch_categories_by_type(category_type)

def fetch_categories_service() -> List[Category]:
    return fetch_categories()

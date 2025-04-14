from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from services.category_service import fetch_categories_by_type_service, fetch_categories_service

router = APIRouter()

@router.get("")
def fetch_categories(category_type: str = Query(..., description="Tipo da categoria: income ou outcome")):
    try:
        categories = fetch_categories_by_type_service(category_type)
        return JSONResponse(
            status_code=200,
            content={"categories": jsonable_encoder(categories)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/all")
def fetch_all_categories():
    try:
        categories = fetch_categories_service()
        return JSONResponse(
            status_code=200,
            content={"categories": jsonable_encoder(categories)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

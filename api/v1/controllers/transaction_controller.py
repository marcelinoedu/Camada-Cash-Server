from fastapi import APIRouter, Request, HTTPException, Depends, Query
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import List
from models.transaction import Transaction
from services.transaction_service import (
    create_transaction_service,
    get_transaction_by_id_service,
    get_all_transactions_service,
    update_transaction_service,
    delete_transaction_service
)

from repositories.transaction_repository import (
    link_transaction_to_category)

from schemas.transaction import TransactionCategoryLinkRequest

router = APIRouter()

@router.post("")
def create_transaction(transaction: Transaction):
    try:
        new_transaction = create_transaction_service(transaction)
        return JSONResponse(status_code=201, content=jsonable_encoder(new_transaction))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{transaction_id}")
def get_transaction(transaction_id: str):
    try:
        transaction = get_transaction_by_id_service(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada")
        return JSONResponse(status_code=200, content=jsonable_encoder(transaction))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("")
def get_all_transactions(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    type: str = Query(None, regex="^(income|outcome)$"),
    categories: str = Query(None),
):
    try:
        category_ids = []
        if categories:
            category_ids = [str(cid) for cid in categories.split(",")]

        transactions, total = get_all_transactions_service(
            page=page,
            limit=limit,
            transaction_type=type,
            category_ids=category_ids,
        )

        return JSONResponse(
            status_code=200,
            content={
                "total": total,
                "page": page,
                "limit": limit,
                "transactions": jsonable_encoder(transactions),
            },
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.put("/{transaction_id}")
def update_transaction(transaction_id: str, updated_transaction: Transaction):
    try:
        transaction = update_transaction_service(transaction_id, updated_transaction)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada para atualizar")
        return JSONResponse(status_code=200, content=jsonable_encoder(transaction))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{transaction_id}")
def delete_transaction(transaction_id: str):
    try:
        transaction = delete_transaction_service(transaction_id)
        if not transaction:
            raise HTTPException(status_code=404, detail="Transação não encontrada para deletar")
        return JSONResponse(status_code=200, content={"message": "Transação deletada com sucesso"})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{transaction_id}/categories")
def link_category_to_transaction(transaction_id: str, body: TransactionCategoryLinkRequest, request: Request):
    try:
        result = link_transaction_to_category(transaction_id=transaction_id, category_id=body.category_id)
        return JSONResponse(status_code=201, content={"message": "Categoria vinculada com sucesso", "relation": result})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao vincular categoria: {str(e)}")

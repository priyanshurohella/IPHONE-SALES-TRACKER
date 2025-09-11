from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from . import database
from .crud import create_sale,get_sales,get_sale_by_id,update_sale,delete_sale
from .schemas import IPhoneSaleCreate, IPhoneSaleResponse, IPhoneSaleUpdate

router = APIRouter(prefix="/sales", tags=["Sales"])



def error_response(message: str, status_code: int = 400):
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
            "data": [],
        },
    )


@router.post("/")
def create_sales(sale: IPhoneSaleCreate, db: Session = Depends(database.get_db)):
    try:
        new_sale = create_sale(db, sale)
        return {
            "success": True,
            "message": "Sale created successfully",
            "data": IPhoneSaleResponse.model_validate(new_sale).model_dump(),
        }
    except Exception as e:
        return error_response(str(e), status_code=400)

@router.get("/")
def get_all_sales(phone_model: str = None, db: Session = Depends(database.get_db)):
    try:
        sales = get_sales(db, phone_model)
        return {
            "success": True,
            "message": "Sales fetched successfully",
            "data": [IPhoneSaleResponse.model_validate(sale).model_dump() for sale in sales],
        }
    except Exception as e:
        return error_response(str(e), status_code=400)

@router.get("/{sale_id}")
def get_sale(sale_id: int, db: Session = Depends(database.get_db)):
    try:
        sale = get_sale_by_id(db, sale_id)
        if not sale:
            return error_response("Sale not found",status_code=404)
        return {
            "success": True,
            "message": "Sale fetched successfully",
            "data": IPhoneSaleResponse.model_validate(sale).model_dump(),
        }
    except Exception as e:
        return error_response(str(e), status_code=400)

@router.put("/{sale_id}")
def update_sales(sale_id: int, sale: IPhoneSaleUpdate, db: Session = Depends(database.get_db)):
    try:
        updated = update_sale(db, sale_id, sale)
        if not updated:
            return error_response("Sale not found",status_code=404)
        return {
            "success": True,
            "message": "Sale updated successfully",
            "data": IPhoneSaleResponse.model_validate(updated).model_dump(),
        }
    except Exception as e:
        return error_response(str(e), status_code=400)

@router.delete("/{sale_id}")
def delete_sales(sale_id: int, db: Session = Depends(database.get_db)):
    try:
        deleted = delete_sale(db, sale_id)
        if not deleted:
            return error_response("Sale not found",status_code=404)
        return {
            "success": True,
            "message": "Sale deleted successfully",
            "data": {"id": sale_id},
        }
    except Exception as e:
        return error_response(str(e), status_code=400)
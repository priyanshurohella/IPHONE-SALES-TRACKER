from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models,crud, database
from .schemas import IPhoneSaleCreate,IPhoneSaleResponse,IPhoneSaleUpdate

app = FastAPI(title="iPhone Sales Tracker")

@app.on_event("startup")
def on_startup():
    models.Base.metadata.create_all(bind=database.engine)

@app.post("/sales")
def create_sale(sale: IPhoneSaleCreate, db: Session = Depends(database.get_db)):
    try:
        new_sale = crud.create_sale(db, sale)
        return {
            "success": True,
            "message": "Sale created successfully",
            "data": IPhoneSaleResponse.model_validate(new_sale).model_dump(),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/sales")
def get_sales(phone_model: str = None, db: Session = Depends(database.get_db)):
    sales = crud.get_sales(db, phone_model)
    return {
        "success": True,
        "message": "Sales fetched successfully",
        "data": [IPhoneSaleResponse.model_validate(sale).model_dump() for sale in sales],
    }

@app.get("/sales/{sale_id}")
def get_sale(sale_id: int, db: Session = Depends(database.get_db)):
    sale = crud.get_sale_by_id(db, sale_id)
    if not sale:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {
        "success": True,
        "message": "Sale fetched successfully",
        "data": IPhoneSaleResponse.model_validate(sale).model_dump(),
    }

@app.put("/sales/{sale_id}")
def update_sale(sale_id: int, sale: IPhoneSaleUpdate, db: Session = Depends(database.get_db)):
    updated = crud.update_sale(db, sale_id, sale)
    if not updated:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {
        "success": True,
        "message": "Sale updated successfully",
        "data": IPhoneSaleResponse.model_validate(updated).model_dump(),
    }


@app.delete("/sales/{sale_id}")
def delete_sale(sale_id: int, db: Session = Depends(database.get_db)):
    deleted = crud.delete_sale(db, sale_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Sale not found")
    return {
        "success": True,
        "message": "Sale deleted successfully",
        "data": {"id": sale_id},
    }
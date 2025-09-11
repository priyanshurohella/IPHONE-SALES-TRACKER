from sqlalchemy.orm import Session
from .models import IPhoneSale
from .schemas import IPhoneSaleCreate,IPhoneSaleUpdate

def create_sale(db: Session, sale: IPhoneSaleCreate):
    new_sale = IPhoneSale(**sale.dict())
    db.add(new_sale)
    db.commit()
    db.refresh(new_sale)
    return new_sale

def get_sales(db: Session, phone_model: str = None):
    if phone_model:
        return db.query(IPhoneSale).filter(IPhoneSale.phone_model == phone_model).all()
    return db.query(IPhoneSale).all()

def get_sale_by_id(db: Session, sale_id: int):
    return db.query(IPhoneSale).filter(IPhoneSale.id == sale_id).first()

def update_sale(db: Session, sale_id: int, sale: IPhoneSaleUpdate):
    db_sale = get_sale_by_id(db, sale_id)
    if not db_sale:
        return None
    for key, value in sale.dict().items():
        setattr(db_sale, key, value)
    db.commit()
    db.refresh(db_sale)
    return db_sale

def delete_sale(db: Session, sale_id: int):
    db_sale = get_sale_by_id(db, sale_id)
    if not db_sale:
        return None
    db.delete(db_sale)
    db.commit()
    return db_sale

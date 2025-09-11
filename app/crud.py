from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from .models import IPhoneSale
from .schemas import IPhoneSaleCreate, IPhoneSaleUpdate


def create_sale(db: Session, sale: IPhoneSaleCreate):
    try:
        new_sale = IPhoneSale(**sale.dict())
        db.add(new_sale)
        db.commit()
        db.refresh(new_sale)
        return new_sale
    except SQLAlchemyError as e:
        db.rollback() 
        raise RuntimeError(f"Database error while creating sale: {str(e)}")


def get_sales(db: Session, phone_model: str = None):
    try:
        if phone_model:
            return db.query(IPhoneSale).filter(IPhoneSale.phone_model == phone_model).all()
        return db.query(IPhoneSale).all()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error while fetching sales: {str(e)}")


def get_sale_by_id(db: Session, sale_id: int):
    try:
        return db.query(IPhoneSale).filter(IPhoneSale.id == sale_id).first()
    except SQLAlchemyError as e:
        raise RuntimeError(f"Database error while fetching sale by ID {sale_id}: {str(e)}")


def update_sale(db: Session, sale_id: int, sale: IPhoneSaleUpdate):
    try:
        db_sale = get_sale_by_id(db, sale_id)
        if not db_sale:
            return None
        for key, value in sale.dict(exclude_unset=True).items():
            setattr(db_sale, key, value)
        db.commit()
        db.refresh(db_sale)
        return db_sale
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error while updating sale {sale_id}: {str(e)}")


def delete_sale(db: Session, sale_id: int):
    try:
        db_sale = get_sale_by_id(db, sale_id)
        if not db_sale:
            return None
        db.delete(db_sale)
        db.commit()
        return db_sale
    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Database error while deleting sale {sale_id}: {str(e)}")

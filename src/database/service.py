from fastapi import HTTPException


def check_exist_in_db(db, model, model_filter, schema_filter):
    db_model = db.query(model).filter(model_filter == schema_filter).first()
    if db_model:
        raise HTTPException(status_code=302, detail="No changes")


def check_name_exist_in_db(db, schema, model):
    db_model = db.query(model).filter(model.name == schema.name).first()
    if db_model:
        raise HTTPException(status_code=400, detail=f"{schema.name} already exist")


def add_to_db(db, model, new_model):
    if isinstance(new_model, model):
        db.add(new_model)
        db.commit()
        db.refresh(new_model)

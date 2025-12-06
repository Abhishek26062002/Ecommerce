from fastapi import APIRouter, Request, Depends, HTTPException, Form, File, UploadFile
from app.models.machines import Machine
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.services.cloudinary import upload_file_to_cloudinary
import uuid


router = APIRouter(prefix="/machines", tags=["machines"])


@router.get("/get_all_machines")
async def get_machines(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Machine))
    machines = result.scalars().all()
    return machines

@router.get("/get_machine/{machine_id}")
async def get_machine(machine_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Machine).where(Machine.machine_id == machine_id))
    machine = result.scalars().first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    return machine

@router.post("/add_machine")
async def add_machine(
    name: str = Form(...),
    price: float = Form(...),
    description: str = Form(None),
    brand: str = Form(None),
    machine_type: str = Form(None),
    images : List[UploadFile] = File(...),
    discount_price: float = Form(None),
    color: str = Form(None),
    size: str = Form(None),
    stock_count: int = Form(None),
    db: AsyncSession = Depends(get_db)
):

    # Check duplicate machine_id
    machine_id = f'machine_{str(uuid.uuid4())}'
    existing = await db.execute(select(Machine).where(Machine.machine_id == machine_id))
    if existing.scalars().first():
        raise HTTPException(status_code=400, detail="Machine ID already exists")
    # Upload images to Cloudinary
    images_urls = []
    for image in images:
        upload_result = await upload_file_to_cloudinary(image)
        if upload_result:
            images_urls.append(upload_result["secure_url"])
    new_machine = Machine(
        machine_id=machine_id,
        name=name,
        description=description,
        brand=brand,
        machine_type=machine_type,
        images_urls=images_urls,
        price=price,
        discount_price=discount_price,
        color=color,
        size=size,
        stock_count=stock_count,
    )

    db.add(new_machine)
    await db.commit()
    await db.refresh(new_machine)

    return {"message": "Machine added successfully", "machine": new_machine}




@router.post("/update_machine")
async def update_machine(
    machine_id: str,
    name: str = Form(None),
    price: float = Form(None),
    description: str = Form(None),
    brand: str = Form(None),
    machine_type: str = Form(None),
    images : List[UploadFile] = File(None),
    image_urls : List[str] = Form(None),
    discount_price: float = Form(None),
    color: str = Form(None),
    size: str = Form(None),
    stock_count: int = Form(None),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Machine).where(Machine.machine_id == machine_id))
    machine = result.scalars().first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    if name is not None:
        machine.name = name
    if price is not None:
        machine.price = price
    if description is not None:
        machine.description = description
    if brand is not None:
        machine.brand = brand
    if machine_type is not None:
        machine.machine_type = machine_type
    if images is not None:
        images_urls = image_urls if image_urls is not None else []
        for image in images:
            print("Uploading image to Cloudinary")
            upload_result = await upload_file_to_cloudinary(image)
            print(f"Upload result: {upload_result}")
            if upload_result:
                print(f"Uploaded image URL: {upload_result['secure_url']}")
                images_urls.append(upload_result["secure_url"])
        machine.images_urls = images_urls
    if discount_price is not None:
        machine.discount_price = discount_price
    if color is not None:
        machine.color = color
    if size is not None:
        machine.size = size
    if stock_count is not None:
        machine.stock_count = stock_count

    await db.commit()
    await db.refresh(machine)

    return {"message": "Machine updated successfully", "machine": machine}



@router.delete("/delete_machine/{machine_id}")
async def delete_machine(machine_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Machine).where(Machine.machine_id == machine_id))
    machine = result.scalars().first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")

    await db.delete(machine)
    await db.commit()

    return {"message": "Machine deleted successfully"}
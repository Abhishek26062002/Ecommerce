from app.models.Embroidery_machines import EmbroideryMachine
from fastapi import APIRouter, Depends, HTTPException, File, Form, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.orders import Order
from app.models.orderitems import OrderItem
from sqlalchemy.future import select
from typing import List
from datetime import datetime
import uuid
from app.services.cloudinary import upload_file_to_cloudinary


router = APIRouter(prefix='/embriodery_machines', tags = ['Embriodery Machines'])


@router.post('/add_machine')
async def add_machine(name : str = Form(None),
                      description : str = Form(None),
                      brand : str = Form(None),
                      machine_type : str = Form(None),
                      images : List[UploadFile] = File(...),
                      model : str = Form(None),
                      needle_count : int = Form(None),
                      head_count : int = Form(None),
                      max_embroidery_area : str = Form(None),
                      max_spm : int = Form(None),
                      file_formats : List[str] = Form(None),
                      auto_thread_trimmer : bool = Form(False),
                      auto_color_change : bool = Form(False),
                      thread_break_detection : bool = Form(False),
                      usb : bool = Form(False),
                      wifi : bool = Form(False),
                      price : float = Form(...),
                      discount_price : float = Form(None),
                      stock_count : int = Form(None),
                      db: AsyncSession = Depends(get_db)):
    try:
        machine_id = f'Embrioding_machine_{str(uuid.uuid4())}'
        images_urls = []
        for image in images:
            upload_result = await upload_file_to_cloudinary(image)
            images_urls.append(upload_result['secure_url'])
        new_machine = EmbroideryMachine(
            machine_id=machine_id,
            name=name,
            description=description,
            brand=brand,
            model=model,
            machine_type=machine_type,
            images_urls=images_urls,
            needle_count=needle_count,
            head_count=head_count,
            max_embroidery_area=max_embroidery_area,
            max_spm=max_spm,
            file_formats=file_formats,
            auto_thread_trimmer=auto_thread_trimmer,
            auto_color_change=auto_color_change,
            thread_break_detection=thread_break_detection,
            usb=usb,
            wifi=wifi,
            price=price,
            discount_price=discount_price,
            stock_count=stock_count,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.add(new_machine) 
        await db.commit()
        await db.refresh(new_machine)
        return {"message": "Embroidery machine added successfully", "machine_id": new_machine.machine_id}
    except Exception as e:
        print(f"Error adding embroidery machine: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    
    
@router.get('/get_machines')
async def get_machines(db: AsyncSession = Depends(get_db)):
    machines = await db.execute(select(EmbroideryMachine))
    machines = machines.scalars().all()
    return machines


@router.get('/get_machine/{machine_id}')
async def get_machine(machine_id: str, db: AsyncSession = Depends(get_db)):
    machine = await db.execute(select(EmbroideryMachine).where(EmbroideryMachine.machine_id == machine_id))
    machine = machine.scalars().first()
    if not machine:
        raise HTTPException(status_code=404, detail="Embroidery machine not found")
    return machine



@router.delete('/delete_machine/{machine_id}')
async def delete_machine(machine_id: str, db: AsyncSession = Depends(get_db)):
    machine = await db.execute(select(EmbroideryMachine).where(EmbroideryMachine.machine_id == machine_id))
    machine = machine.scalars().first()
    if not machine:
        raise HTTPException(status_code=404, detail="Embroidery machine not found")
    await db.delete(machine)
    await db.commit()
    return {"message": "Embroidery machine deleted successfully"}


@router.put('/update_machine/{machine_id}')
async def update_machine(machine_id: str,
                            name : str = Form(None),
                            description : str = Form(None),
                            brand : str = Form(None),
                            model : str = Form(None),
                            machine_type : str = Form(None),
                            images : List[UploadFile] = File(None),
                            needle_count : int = Form(None),
                            head_count : int = Form(None),
                            max_embroidery_area : str = Form(None),
                            max_spm : int = Form(None),
                            file_formats : List[str] = Form(None),
                            auto_thread_trimmer : bool = Form(None),
                            auto_color_change : bool = Form(None),
                            thread_break_detection : bool = Form(None),
                            usb : bool = Form(None),
                            wifi : bool = Form(None),
                            price : float = Form(None),
                            discount_price : float = Form(None),
                            stock_count : int = Form(None),
                            db: AsyncSession = Depends(get_db)):
        try:
            machine_query = await db.execute(select(EmbroideryMachine).where(EmbroideryMachine.machine_id == machine_id))
            machine = machine_query.scalars().first()
            if not machine:
                raise HTTPException(status_code=404, detail="Embroidery machine not found")
            
            if name:
                machine.name = name
            if description:
                machine.description = description
            if brand:
                machine.brand = brand
            if model:
                machine.model = model
            if machine_type:
                machine.machine_type = machine_type
            if images:
                images_urls = []
                for image in images:
                    upload_result = await upload_file_to_cloudinary(image)
                    images_urls.append(upload_result['secure_url'])
                machine.images_urls = images_urls
            if needle_count is not None:
                machine.needle_count = needle_count
            if head_count is not None:
                machine.head_count = head_count
            if max_embroidery_area:
                machine.max_embroidery_area = max_embroidery_area
            if max_spm is not None:
                machine.max_spm = max_spm
            if file_formats:
                machine.file_formats = file_formats
            if auto_thread_trimmer is not None:
                machine.auto_thread_trimmer = auto_thread_trimmer
            if auto_color_change is not None:
                machine.auto_color_change = auto_color_change
            if thread_break_detection is not None:
                machine.thread_break_detection = thread_break_detection
            if usb is not None:
                machine.usb = usb
            if wifi is not None:
                machine.wifi = wifi
            if price is not None:
                machine.price = price  
            if discount_price is not None:
                machine.discount_price = discount_price
            if stock_count is not None:
                machine.stock_count = stock_count
            machine.updated_at = datetime.now()
            await db.commit()
            await db.refresh(machine)   
            return {"message": "Embroidery machine updated successfully", "machine_id": machine.machine_id}
        except Exception as e:
            print(f"Error updating embroidery machine: {e}")
            raise HTTPException(status_code=500, detail=str(e))
from fastapi import APIRouter, Request, Depends, HTTPException
from app.models.machines import Machine
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.schemas.machines import MachineSchema



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
async def add_machine(machine: Machine, db: AsyncSession = Depends(get_db)):
    db.add(machine)
    await db.commit()
    await db.refresh(machine)
    return machine
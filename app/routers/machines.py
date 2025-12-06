from fastapi import APIRouter, Request, Depends, HTTPException
from app.models.machines import Machine
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
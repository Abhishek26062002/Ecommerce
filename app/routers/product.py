from fastapi import APIRouter, Depends, HTTPException, status, Form, UploadFile, File, Query
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.models.product import Product
from sqlalchemy.future import select
from typing import List, Optional, Union
from app.services.cloudinary import upload_file_to_cloudinary
from app.services.r2_client import upload_to_r2, generate_r2_download_url, delete_from_r2
from app.models.orderitems import OrderItem
from app.models.orders import Order

router = APIRouter(prefix="/products", tags=["products"])


def valid_upload(f):
    return hasattr(f, "filename") and bool(f.filename)



@router.get("/get_all_products_infinite_scroll")
async def get_products(
    db: AsyncSession = Depends(get_db),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    # Fetch paginated products
    result = await db.execute(
        select(Product).offset(offset).limit(limit)
    )
    products = result.scalars().all()

    # Get total count for frontend decision making
    total_query = await db.execute(select(func.count(Product.id)))
    total = total_query.scalar()

    return {
        "products": products,
        "total": total,
        "limit": limit,
        "offset": offset,
        "hasMore": offset + limit < total
    }

@router.get("/get_all_products")
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products


@router.get("/{product_id}")
async def get_product(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    return product  




@router.get("/category/{category_name}")
async def get_products_by_category(category_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.category == category_name))
    products = result.scalars().all()
    return products


@router.get("/get_sub_category_names/{category_name}")
async def get_sub_category_names(category_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product.sub_category).where(Product.category == category_name).distinct())
    sub_categories = [row[0] for row in result.all() if row[0] is not None]
    return sub_categories

@router.get("/category_wise/{category}/{sub_category_name}")
async def get_products_by_sub_category(category: str, sub_category_name: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.category == category).where(Product.sub_category == sub_category_name))
    products = result.scalars().all()
    return products


@router.post("/add_product")
async def add_product(name : str = Form(...),
                      description : str = Form(None),
                      price : float = Form(...),
                      discount_price : float = Form(None),
                      in_stock : bool = Form(True),
                      sub_category : str = Form(None),
                      category : str = Form(None),
                      brand : str = Form(None),
                      machine_type : str = Form(None),
                      color : str = Form(None),
                      size : str = Form(None),
                      stock_count : int = Form(None),
                      images : List[UploadFile] = File(...),
                      dst: Optional[Union[UploadFile, str]] = File(None),
                      jef: Optional[Union[UploadFile, str]] = File(None),
                      db: AsyncSession = Depends(get_db)):
    
        # Upload images first
    images_urls = []
    for image in images:
        upload_result = await upload_file_to_cloudinary(image)
        if upload_result:
            images_urls.append(upload_result["secure_url"])
    print("DST TYPE:", type(dst))
    print("UploadFile TYPE:", UploadFile)
    print("isinstance(dst, UploadFile):", isinstance(dst, UploadFile))


    # Now R2 uploads are safe
    if valid_upload(dst):
        print("Uploading DST file to R2")
        dst_filename = await upload_to_r2(dst)
        
    else:
        print("No valid DST file provided")
        dst_filename = None

    if valid_upload(jef):
        print("Uploading JEF file to R2")
        jef_filename = await upload_to_r2(jef)
    else:
        print("No valid JEF file provided")
        jef_filename = None

    

    
        
    
    new_product = Product(
        name=name,
        description=description,
        price=price,
        discount_price=discount_price,
        in_stock=in_stock,
        sub_category=sub_category,
        images_urls=images_urls,
        category=category,
        brand=brand,
        machine_type=machine_type,
        color=color,
        size=size,
        dst=dst_filename if dst else None,
        jef=jef_filename if jef else None,
        stock_count=stock_count
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product



@router.delete("/{product_id}")
async def delete_product(product_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    # Delete associated files from R2
    if product.dst:
        await delete_from_r2(product.dst)
    if product.jef:
        await delete_from_r2(product.jef)
    
    await db.delete(product)
    await db.commit()
    return {"detail": "Product deleted successfully"}




@router.get("/generate-r2-url/{product_id}")
async def generate_r2_url(product_id: str, expiry: int = 3600, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    urls = {}
    if product.dst:
        dst_url = await generate_r2_download_url(product.dst, expiry)
        urls['dst_url'] = dst_url
    if product.jef:
        jef_url = await generate_r2_download_url(product.jef, expiry)
        urls['jef_url'] = jef_url
    
    return urls







@router.put("/edit_product/{product_id}")
async def update_product(product_id: str,
                         name : Optional[str] = Form(None),
                         description : Optional[str] = Form(None),
                         price : Optional[float] = Form(None),
                         discount_price : Optional[float] = Form(None),
                         in_stock : Optional[bool] = Form(None),
                         sub_category : Optional[str] = Form(None),
                         category : Optional[str] = Form(None),
                         brand : Optional[str] = Form(None),
                         machine_type : Optional[str] = Form(None),
                         color : Optional[str] = Form(None),
                         size : Optional[str] = Form(None),
                         stock_count : Optional[int] = Form(None),
                         images : List[UploadFile] = File(None),
                         image_urls : List[str] = Form(None),
                         dst: Optional[Union[UploadFile, str]] = File(None),
                         jef: Optional[Union[UploadFile, str]] = File(None),
                         db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    print("Fetched product:", product)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    print("Updating product fields")
    print("Current product data:", product.__dict__)
    print("Received update data:", {
        "name": name,
        "description": description,
        "price": price,
        "discount_price": discount_price,
        "in_stock": in_stock,
        "sub_category": sub_category,
        "category": category,
        "brand": brand,
        "machine_type": machine_type,
        "color": color,
        "size": size,
        "stock_count": stock_count,
        "images": images,
        "dst": dst,
        "jef": jef
    })
    if name is not None:
        product.name = name
    if description is not None:
        product.description = description
    if price is not None:
        product.price = price
    if discount_price is not None:
        product.discount_price = discount_price
    if in_stock is not None:
        product.in_stock = in_stock
    if sub_category is not None:
        product.sub_category = sub_category
    if category is not None:
        product.category = category
    if brand is not None:
        product.brand = brand
    if machine_type is not None:
        product.machine_type = machine_type
    if color is not None:
        product.color = color
    if size is not None:
        product.size = size
    if stock_count is not None:
        product.stock_count = stock_count

    # Handle image uploads
    if images is not None:
        images_urls = image_urls if image_urls is not None else []
        for image in images:
            print("Uploading image to Cloudinary")
            upload_result = await upload_file_to_cloudinary(image)
            print(f"Upload result: {upload_result}")
            if upload_result:
                print(f"Uploaded image URL: {upload_result['secure_url']}")
                images_urls.append(upload_result["secure_url"])
        product.images_urls = images_urls

    # Handle DST upload
    if valid_upload(dst):

        print("Uploading DST file to R2")
        dst_filename = await upload_to_r2(dst)
        if product.dst:
            await delete_from_r2(product.dst)
        print(f"Uploaded DST file: {dst_filename}")

        product.dst = dst_filename
    if valid_upload(jef):
        print("Uploading JEF file to R2")
        jef_filename = await upload_to_r2(jef)
        if product.jef:
            await delete_from_r2(product.jef)
        print(f"Uploaded JEF file: {jef_filename}")
        product.jef = jef_filename
    await db.commit()
    await db.refresh(product)
    return product

@router.get("/product_download_urls/{payment_id}/{file_type}")
async def get_product_download_urls(payment_id: str, file_type: str, expiry: int = 3600, db: AsyncSession = Depends(get_db)):
    order_status = await db.execute(select(Order).where(Order.payment_id == payment_id))
    order_status = order_status.scalars().first()
    print(order_status.status if order_status else "No order found")
    if not order_status or order_status.status != "paid":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Payment not completed for this order",
        )
    item_id = await db.execute(select(OrderItem).where(OrderItem.order_id == order_status.id))
    item_id = item_id.scalars().first()
    product_id = item_id.product_id
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalars().first()
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found",
        )
    
    if file_type == "dst" and product.dst:
        dst_url = await generate_r2_download_url(product.dst, expiry)
        return {"dst_url": dst_url}
    elif file_type == "jef" and product.jef:
        jef_url = await generate_r2_download_url(product.jef, expiry)
        return {"jef_url": jef_url}
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{file_type.upper()} file not found for this product",
        )
        
        
        
@router.get('/latest_products')
async def get_latest_products(db: AsyncSession = Depends(get_db), limit: int = 10):
    result = await db.execute(select(Product).order_by(Product.created_at.desc()).limit(limit))
    products = result.scalars().all()
    return products
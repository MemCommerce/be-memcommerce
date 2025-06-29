from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

from schemas.storefront_schemas import StorefrontData, StorefrontProduct, StorefrontVariant
from storage.gcp_storage import generate_signed_url


class StorefrontManager:
    @staticmethod
    async def select_hole_storefront_data(db: AsyncSession) -> StorefrontData:
        query = text("""
            SELECT
                p.id,
                p.name,
                p.brand,
                p.description,
                c.name as category_name,
                (SELECT json_agg(
                    json_build_object(
                        'id', pv.id,
                        'color_id', pv.color_id,
                        'color', (SELECT name FROM colors WHERE id = pv.color_id),
                        'color_hex', (SELECT hex FROM colors WHERE id = pv.color_id),
                        'size_id', pv.size_id,
                        'size', (SELECT label FROM sizes WHERE id = pv.size_id),
                        'price', pv.price,
                        'image_name', pv.image_name
                    )
                ) FROM product_variants pv WHERE pv.product_id = p.id) as variants
            FROM products p
            JOIN categories c ON c.id = p.category_id
        """)
        
        result = await db.execute(query)
        rows = result.mappings().fetchall()  # This returns dict-like objects
        
        products = [
            StorefrontProduct(
                id=str(row["id"]),
                name=row["name"],
                brand=row["brand"],
                description=row["description"],
                category_name=row["category_name"],
                variants=[StorefrontVariant(
                    id=variant["id"],
                    size=variant["size"],
                    size_id=variant["size_id"],
                    color=variant["color"],
                    color_hex=variant["color_hex"],
                    color_id=variant["color_id"],
                    price=variant["price"],
                    image_url=generate_signed_url(variant["image_name"]) if variant["image_name"] else ""
                ) for variant in (row["variants"] or [])]
            ) for row in rows if row["variants"]
        ]

        return StorefrontData(products=products)
    
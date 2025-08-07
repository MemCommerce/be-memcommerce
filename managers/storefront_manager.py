from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from sqlalchemy.exc import NoResultFound

from schemas.storefront_schemas import (
    StorefrontData,
    StorefrontProduct,
    StorefrontVariant,
    SFReview,
    SFProductWithReviews,
)
from schemas.pagination_schemas import PaginationResponse
from storage.gcp_storage import generate_signed_url


class StorefrontManager:
    @staticmethod
    async def select_storefront_product_by_id(
        product_id: str, db: AsyncSession
    ) -> StorefrontProduct:
        query = text(
            """
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
                ) FROM product_variants pv WHERE pv.product_id = p.id) AS variants,
                (
                    SELECT json_agg(
                        json_build_object(
                            'id', r.id,
                            'title', r.title,
                            'rating', r.rating,
                            'content', r.content,
                            'product_variant_id', r.product_variant_id,
                            'name', u.first_name
                        )
					) 
                    FROM reviews r 
				    JOIN users u ON u.id = r.user_id
				    WHERE r.product_variant_id IN (SELECT id FROM product_variants prv WHERE prv.product_id = p.id)
                ) AS reviews
            FROM products p
            JOIN categories c ON c.id = p.category_id
            WHERE p.id = :product_id
        """
        )
        result = await db.execute(query, {"product_id": product_id})
        row = result.mappings().fetchone()
        if row is None:
            raise NoResultFound(f"Product with id {product_id} is not found!")

        product = SFProductWithReviews(
            id=str(row["id"]),
            name=row["name"],
            brand=row["brand"],
            description=row["description"],
            category_name=row["category_name"],
            variants=[
                StorefrontVariant(
                    id=variant["id"],
                    size=variant["size"],
                    size_id=variant["size_id"],
                    color=variant["color"],
                    color_hex=variant["color_hex"],
                    color_id=variant["color_id"],
                    price=variant["price"],
                    image_url=(
                        generate_signed_url(variant["image_name"])
                        if variant["image_name"]
                        else ""
                    ),
                )
                for variant in (row["variants"] or [])
            ],
            reviews=[
                SFReview(
                    id=review["id"],
                    rating=review["rating"],
                    title=review["title"],
                    content=review["content"],
                    product_variant_id=review["product_variant_id"],
                    reviewer_name=review["name"]
                )
                for review in (row["reviews"] or [])
            ]
        )
        return product

    @staticmethod
    async def select_hole_storefront_data(db: AsyncSession) -> StorefrontData:
        query = text(
            """
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
        """
        )

        result = await db.execute(query)
        rows = result.mappings().fetchall()

        products = [
            StorefrontProduct(
                id=str(row["id"]),
                name=row["name"],
                brand=row["brand"],
                description=row["description"],
                category_name=row["category_name"],
                variants=[
                    StorefrontVariant(
                        id=variant["id"],
                        size=variant["size"],
                        size_id=variant["size_id"],
                        color=variant["color"],
                        color_hex=variant["color_hex"],
                        color_id=variant["color_id"],
                        price=variant["price"],
                        image_url=(
                            generate_signed_url(variant["image_name"])
                            if variant["image_name"]
                            else ""
                        ),
                    )
                    for variant in (row["variants"] or [])
                ],
            )
            for row in rows
            if row["variants"]
        ]

        return StorefrontData(products=products)

    @staticmethod
    async def select_paginated_storefront_data(
        limit: int, offset: int, db: AsyncSession
    ) -> PaginationResponse[StorefrontProduct]:
        query = text(
            """
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
			WHERE EXISTS (SELECT 1 FROM product_variants pv WHERE pv.product_id = p.id)
            LIMIT :limit
			OFFSET :offset
        """
        )

        result = await db.execute(query, {"limit": limit, "offset": offset})
        rows = result.mappings().fetchall()

        products = [
            StorefrontProduct(
                id=str(row["id"]),
                name=row["name"],
                brand=row["brand"],
                description=row["description"],
                category_name=row["category_name"],
                variants=[
                    StorefrontVariant(
                        id=variant["id"],
                        size=variant["size"],
                        size_id=variant["size_id"],
                        color=variant["color"],
                        color_hex=variant["color_hex"],
                        color_id=variant["color_id"],
                        price=variant["price"],
                        image_url=(
                            generate_signed_url(variant["image_name"])
                            if variant["image_name"]
                            else ""
                        ),
                    )
                    for variant in (row["variants"] or [])
                ],
            )
            for row in rows
            if row["variants"]
        ]

        total_query = text(
            """
        SELECT
            COUNT(p.*) 
        FROM products p
        JOIN categories c ON c.id = p.category_id
        WHERE EXISTS (SELECT 1 FROM product_variants pv WHERE pv.product_id = p.id);
        """
        )
        count_result = await db.execute(total_query)
        count = count_result.fetchone()
        if count is None:
            raise NoResultFound("Error!")
        pagination_data = PaginationResponse(items=products, total=int(count[0]))

        return pagination_data

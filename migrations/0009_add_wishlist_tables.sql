-- Create the wishlist_items table
CREATE TABLE wishlist_items (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    product_variant_id UUID NOT NULL,
    price NUMERIC(10, 2) NOT NULL,
    image_name VARCHAR(255),
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

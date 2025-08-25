ALTER TABLE wishlist_items
  DROP COLUMN IF EXISTS product_variant_id,
  ADD COLUMN product_id UUID NOT NULL,
  ADD CONSTRAINT uniq_wishlist_user_product UNIQUE (user_id, product_id);
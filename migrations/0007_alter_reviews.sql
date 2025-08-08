ALTER TABLE reviews
  ADD COLUMN sentiment VARCHAR(20),    
  ADD COLUMN tags TEXT[],                  
  ADD COLUMN aspect_sentiment JSONB;    

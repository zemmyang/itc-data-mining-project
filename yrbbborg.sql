USE bbborg;


CREATE TABLE IF NOT EXISTS yelp_business_id (
  yelp_id VARCHAR(25) NOT NULL,
  business_name VARCHAR(100),
  address VARCHAR(300),
  coord_lat DECIMAL(5,2),
  coord_long DECIMAL(5,2),
  display_phone VARCHAR(12),
  city VARCHAR(20),
  country VARCHAR(2),
  zipcode INT(10),
  yelp_url VARCHAR(50),
  yelp_rating DECIMAL(5,1),
  PRIMARY KEY (yelp_id) );


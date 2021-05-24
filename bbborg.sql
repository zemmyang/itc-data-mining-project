DROP SCHEMA IF EXISTS bbborg;
CREATE SCHEMA bbborg;

USE bbborg;

CREATE TABLE IF NOT EXISTS business_profile (
  business_id VARCHAR(28) NOT NULL,
  business_name VARCHAR(100),
  alerts VARCHAR(100),
  location VARCHAR(400),
  website VARCHAR(50),
  phone_number VARCHAR(20),
  bbb_file_opened VARCHAR(15),
  type_of_entity VARCHAR(45),
  bbb_rating VARCHAR(5),
  PRIMARY KEY (business_id) );

CREATE TABLE IF NOT EXISTS categories (
  category_id INT(8) ZEROFILL AUTO_INCREMENT NOT NULL,
  category_name VARCHAR(100) NOT NULL,
  PRIMARY KEY (category_id));

CREATE TABLE IF NOT EXISTS complaints (
  idcomplaints INT(8) ZEROFILL AUTO_INCREMENT NOT NULL,
  adverting_sales INT NULL,
  billing_collections INT NULL,
  delivery_issues INT NULL,
  guarantee_warranty INT NULL,
  problem_product_service INT NULL,
  business_profile_business_id VARCHAR(28) NOT NULL,
  PRIMARY KEY (idcomplaints),
  FOREIGN KEY (business_profile_business_id) REFERENCES business_profile (business_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reviews (
  idreviews INT AUTO_INCREMENT NOT NULL,
  name VARCHAR(45) NULL,
  review_text MULTILINESTRING NULL,
  date DATE NULL,
  star_rating INT NULL,
  PRIMARY KEY (idreviews));

CREATE TABLE IF NOT EXISTS business_profile_has_categories (
  business_profile_business_id VARCHAR(28) NOT NULL,
  categories_category_id INT(8) ZEROFILL AUTO_INCREMENT NOT NULL,
  PRIMARY KEY (business_profile_business_id, categories_category_id),
  FOREIGN KEY (business_profile_business_id) REFERENCES business_profile (business_id) ON DELETE CASCADE,
  FOREIGN KEY (categories_category_id) REFERENCES categories (category_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS reviews_has_business_profile (
  reviews_idreviews INT AUTO_INCREMENT NOT NULL,
  business_profile_business_id VARCHAR(28) NOT NULL,
  PRIMARY KEY (reviews_idreviews, business_profile_business_id),
  FOREIGN KEY (reviews_idreviews) REFERENCES reviews (idreviews) ON DELETE CASCADE,
  FOREIGN KEY (business_profile_business_id) REFERENCES business_profile (business_id) ON DELETE CASCADE
);

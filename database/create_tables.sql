-- TABLES

-- Category
CREATE TABLE Category (
                id INT AUTO_INCREMENT NOT NULL,
                level INT NOT NULL,
                name VARCHAR(100) NOT NULL,
                url_link VARCHAR(100),
                PRIMARY KEY (id)
);
-- index
CREATE UNIQUE INDEX category_idx
 ON Category
 ( level ASC, name ASC );

-- Product
CREATE TABLE Product (
                id INT AUTO_INCREMENT NOT NULL,
                name VARCHAR(100) NOT NULL,
                brands VARCHAR(100) NOT NULL,
                nutrition_grade VARCHAR(1) NOT NULL,
                url_link VARCHAR(100) NOT NULL,
                description VARCHAR(1000) NOT NULL,
                stores VARCHAR(100),
                PRIMARY KEY (id)
);
-- index 1
CREATE UNIQUE INDEX product_idx
 ON Product
 ( name ASC, brands ASC );
-- index 2
CREATE INDEX product_nutrition_grade_idx
 ON Product
 ( nutrition_grade ASC );

-- Favorite
CREATE TABLE Favorite (
                product_id INT NOT NULL,
                substitute_id INT NOT NULL,
                PRIMARY KEY (product_id, substitute_id)
);

-- CategoryProduct
CREATE TABLE CategoryProduct (
                category_id INT NOT NULL,
                product_id INT NOT NULL,
                PRIMARY KEY (category_id, product_id)
);


-- FOREIGN KEYS

-- constraint 1
ALTER TABLE CategoryProduct ADD CONSTRAINT category_category_product_fk
FOREIGN KEY (category_id)
REFERENCES Category (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
-- constraint 2
ALTER TABLE CategoryProduct ADD CONSTRAINT product_category_product_fk
FOREIGN KEY (product_id)
REFERENCES Product (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
-- constraint 3
ALTER TABLE Favorite ADD CONSTRAINT product_favorite_fk
FOREIGN KEY (product_id)
REFERENCES Product (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
-- constraint 4
ALTER TABLE Favorite ADD CONSTRAINT subsitute_favorite_fk
FOREIGN KEY (substitute_id)
REFERENCES Product (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

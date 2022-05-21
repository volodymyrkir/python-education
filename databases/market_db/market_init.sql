CREATE TABLE Users(
    user_id int UNIQUE,
    email varchar(255),
    password varchar(255),
    first_name varchar(255),
    last_name varchar(255),
    middle_name varchar(255),
    is_staff smallint,
    country varchar(255),
    city varchar(255),
    address text
);

CREATE TABLE Carts(
    cart_id int UNIQUE,
    users_user_id int REFERENCES Users(user_id),
    subtotal decimal,
    total decimal,
    timestamp timestamp(2)
);

CREATE TABLE Order_status(
    order_status_id int UNIQUE,
    status_name varchar(255)
);

CREATE TABLE Orders(
    order_id int UNIQUE,
    carts_cart_id int REFERENCES Carts(cart_id),
    order_status_order_status_id int REFERENCES Order_status(order_status_id),
    shipping_total decimal,
    total decimal,
    created_at timestamp(2),
    uploaded_at timestamp(2)
);

CREATE TABLE Categories(
    category_id int UNIQUE,
    category_title varchar(255),
    category_description text
);

CREATE TABLE Products(
    product_id int UNIQUE,
    product_title varchar(255),
    product_description text,
    in_stock int,
    price float,
    slug varchar(45),
    category_id int REFERENCES Categories(category_id)
);

CREATE TABLE Cart_product(
    carts_cart_id int REFERENCES Carts(cart_id),
    products_product_id int REFERENCES  Products(product_id)
);




COPY Users(user_id, email, password, first_name, last_name, middle_name, is_staff, country, city, address)
FROM '/usr/src/users.csv' DELIMITER ',';

COPY Carts(cart_id, users_user_id, subtotal, total, timestamp)
FROM '/usr/src/carts.csv' DELIMITER ',';

COPY Order_status(order_status_id, status_name)
FROM '/usr/src/order_statuses.csv' DELIMITER ',';

COPY Orders(order_id, carts_cart_id, order_status_order_status_id, shipping_total, total, created_at, uploaded_at)
FROM '/usr/src/orders.csv' DELIMITER ',';

COPY Categories(category_id, category_title, category_description)
FROM '/usr/src/categories.csv' DELIMITER ',';

COPY Products(product_id, product_title, product_description, in_stock, price, slug, category_id)
FROM '/usr/src/products.csv' DELIMITER ',';

COPY Cart_product(carts_cart_id, products_product_id)
FROM '/usr/src/cart_products.csv' DELIMITER ',';



ALTER TABLE Users ADD COLUMN phone_number int;

ALTER TABLE Users ALTER COLUMN phone_number TYPE varchar(30);

UPDATE products SET price = price*2;
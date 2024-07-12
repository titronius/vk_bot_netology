-- Создание базы данных
CREATE DATABASE vkinder_db;

-- Создание таблицы user
CREATE TABLE "user" (
    id SERIAL PRIMARY KEY,
    vk_id INTEGER NOT NULL UNIQUE,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    profile_url TEXT,
    city VARCHAR(50),
    age INTEGER,
    gender CHAR(1),
    bdate DATE,
    relation VARCHAR(50),
    smoking VARCHAR(50),
    alcohol VARCHAR(50),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Создание таблицы photo
CREATE TABLE photo (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    photo_url TEXT,
    photo_vk_id INT,
    likes INTEGER,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE
);

-- Создание таблицы relationship_status
CREATE TABLE relationship_status (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE
);

-- Создание таблицы relationship
CREATE TABLE relationship (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    related_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES "user" (id) ON DELETE CASCADE,
    FOREIGN KEY (related_id) REFERENCES "user" (id) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES relationship_status (id) ON DELETE CASCADE
);

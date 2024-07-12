-- Создание базы данных
CREATE DATABASE vkinder_db;


-- Создание таблицы users
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
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
    alcohol VARCHAR(50)
);

-- Создание таблицы photos
CREATE TABLE photos (
    photo_id SERIAL PRIMARY KEY,
    vk_id INTEGER NOT NULL,
    photo_url TEXT,
    likes INTEGER,
    FOREIGN KEY (vk_id) REFERENCES users (vk_id) ON DELETE CASCADE
);

-- Создание таблицы relationships
CREATE TABLE relationships (
    id SERIAL PRIMARY KEY,
    user_vk_id INTEGER NOT NULL,
    related_vk_id INTEGER NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('favorite', 'blacklisted')),
    date_added TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_vk_id) REFERENCES users (vk_id) ON DELETE CASCADE,
    FOREIGN KEY (related_vk_id) REFERENCES users (vk_id) ON DELETE CASCADE
);

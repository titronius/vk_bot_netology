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
    gender CHAR(1)
);

-- Создание таблицы photos
CREATE TABLE photos (
    photo_id SERIAL PRIMARY KEY,
    vk_id INTEGER NOT NULL,
    photo_url TEXT,
    likes INTEGER,
    FOREIGN KEY (vk_id) REFERENCES users (vk_id) ON DELETE CASCADE
);

-- Создание таблицы favorites
CREATE TABLE favorites (
    id SERIAL PRIMARY KEY,
    user_vk_id INTEGER NOT NULL,
    favorite_vk_id INTEGER NOT NULL,
    FOREIGN KEY (user_vk_id) REFERENCES users (vk_id) ON DELETE CASCADE,
    FOREIGN KEY (favorite_vk_id) REFERENCES users (vk_id) ON DELETE CASCADE
);

-- Создание таблицы blacklist
CREATE TABLE blacklist (
    id SERIAL PRIMARY KEY,
    user_vk_id INTEGER NOT NULL,
    blocked_vk_id INTEGER NOT NULL,
    FOREIGN KEY (user_vk_id) REFERENCES users (vk_id) ON DELETE CASCADE,
    FOREIGN KEY (blocked_vk_id) REFERENCES users (vk_id) ON DELETE CASCADE
);

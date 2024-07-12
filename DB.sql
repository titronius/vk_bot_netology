CREATE TABLE Users (
    id INT PRIMARY KEY UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    bdate DATE NOT NULL,
    sex SMALLINT,
    city VARCHAR(100),
    relation SMALLINT,
    smoking SMALLINT,
    alcohol SMALLINT
);

CREATE TABLE Photos (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    photo_url VARCHAR(512) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);

CREATE TABLE Favorites (
    id SERIAL PRIMARY KEY,
    user_id INT UNIQUE NOT NULL,
    favorited_user_id INT NOT NULL,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (favorited_user_id) REFERENCES Users(id),
    UNIQUE (user_id, favorited_user_id)
);

CREATE TABLE Blacklist (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    blacklisted_user_id INT NOT NULL,
    date_added TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES Users(id),
    FOREIGN KEY (blacklisted_user_id) REFERENCES Users(id),
    UNIQUE (user_id, blacklisted_user_id)
);

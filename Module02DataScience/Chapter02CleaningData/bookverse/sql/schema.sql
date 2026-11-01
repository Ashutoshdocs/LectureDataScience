-- ============================================================================
-- BookVerse schema (MySQL 8).  For reference only – data_pipeline.py creates
-- these tables automatically through SQLAlchemy.
-- ============================================================================
CREATE TABLE users (
  user_id       INT PRIMARY KEY,
  username      VARCHAR(50) NOT NULL UNIQUE,
  full_name     VARCHAR(100),
  city          VARCHAR(60),
  email         VARCHAR(120),
  password_hash VARCHAR(255)          -- only the 2 demo users can log in
);

CREATE TABLE books (
  book_id INT PRIMARY KEY,
  title   VARCHAR(200) NOT NULL,
  author  VARCHAR(120),
  genre   VARCHAR(40),
  year    INT,
  pages   INT,
  INDEX ix_books_genre (genre)
);

CREATE TABLE ratings (
  rating_id INT AUTO_INCREMENT PRIMARY KEY,
  user_id   INT NOT NULL,
  book_id   INT NOT NULL,
  rating    FLOAT NOT NULL,
  rated_at  DATETIME,
  UNIQUE KEY uq_user_book (user_id, book_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (book_id) REFERENCES books(book_id)
);

CREATE TABLE friendships (            -- stored once with user_a < user_b
  user_a INT NOT NULL,
  user_b INT NOT NULL,
  PRIMARY KEY (user_a, user_b),
  FOREIGN KEY (user_a) REFERENCES users(user_id),
  FOREIGN KEY (user_b) REFERENCES users(user_id)
);

CREATE TABLE user_activity (          -- what each demo user is looking at right now
  user_id    INT PRIMARY KEY,
  view       VARCHAR(60),
  title      VARCHAR(200),
  payload    LONGTEXT,                -- JSON snapshot of the screen
  updated_at DATETIME,
  last_seen  DATETIME,
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE activity_log (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  user_id    INT,
  action     VARCHAR(255),
  created_at DATETIME,
  INDEX ix_log_user (user_id),
  FOREIGN KEY (user_id) REFERENCES users(user_id)
);

-- ============================================================================
-- Handy queries to show in a demo:   sudo mysql bookverse
-- ============================================================================
-- Most popular genres
-- SELECT b.genre, COUNT(*) AS ratings, ROUND(AVG(r.rating),2) AS avg_rating
-- FROM ratings r JOIN books b USING (book_id) GROUP BY b.genre ORDER BY ratings DESC;

-- Alice's friends
-- SELECT u.full_name FROM friendships f
-- JOIN users u ON u.user_id = IF(f.user_a = 1, f.user_b, f.user_a)
-- WHERE 1 IN (f.user_a, f.user_b);

-- What is Bob looking at right now?
-- SELECT u.username, a.view, a.title, a.updated_at
-- FROM user_activity a JOIN users u USING (user_id);

-- Live feed
-- SELECT u.username, l.action, l.created_at FROM activity_log l
-- JOIN users u USING (user_id) ORDER BY l.id DESC LIMIT 10;

# db.py

import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

DB_NAME = "business_cards.db"

# Connect to database
def connect_db():
    conn = sqlite3.connect(DB_NAME)
    return conn

# Initialize database tables
def init_db():
    conn = connect_db()
    c = conn.cursor()
    
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # Profile Information table
    c.execute('''
        CREATE TABLE IF NOT EXISTS profile (
            user_id INTEGER PRIMARY KEY,
            profile_photo BLOB,
            first_name TEXT,
            last_name TEXT,
            role TEXT,
            company_name TEXT,
            company_logo BLOB,
            bio TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Contact Information table
    c.execute('''
        CREATE TABLE IF NOT EXISTS contact (
            user_id INTEGER PRIMARY KEY,
            email TEXT,
            cellphone TEXT,
            website TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # Social Links table
    c.execute('''
        CREATE TABLE IF NOT EXISTS social_links (
            user_id INTEGER PRIMARY KEY,
            linkedin TEXT,
            youtube TEXT,
            twitter TEXT,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()

# Register a new user
def register_user(username, password):
    hashed_password = generate_password_hash(password)
    conn = connect_db()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# Verify user login
def login_user(username, password):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    conn.close()
    if user and check_password_hash(user[1], password):
        return user[0]
    return None

# Save profile data
def save_profile(user_id, profile_data):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO profile 
        (user_id, profile_photo, first_name, last_name, role, company_name, company_logo, bio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, profile_data['profile_photo'], profile_data['first_name'], profile_data['last_name'],
          profile_data['role'], profile_data['company_name'], profile_data['company_logo'], profile_data['bio']))
    conn.commit()
    conn.close()

# Save contact information
def save_contact(user_id, contact_data):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO contact 
        (user_id, email, cellphone, website)
        VALUES (?, ?, ?, ?)
    ''', (user_id, contact_data['email'], contact_data['cellphone'], contact_data['website']))
    conn.commit()
    conn.close()

# Save social links
def save_social_links(user_id, social_data):
    conn = connect_db()
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO social_links 
        (user_id, linkedin, youtube, twitter)
        VALUES (?, ?, ?, ?)
    ''', (user_id, social_data['linkedin'], social_data['youtube'], social_data['twitter']))
    conn.commit()
    conn.close()

# Fetch profile data for a user
def get_profile(user_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT profile_photo, first_name, last_name, role, company_name, company_logo, bio FROM profile WHERE user_id = ?", (user_id,))
    profile = c.fetchone()
    conn.close()
    return profile

# Fetch contact information for a user
def get_contact(user_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT email, cellphone, website FROM contact WHERE user_id = ?", (user_id,))
    contact = c.fetchone()
    conn.close()
    return contact

# Fetch social links for a user
def get_social_links(user_id):
    conn = connect_db()
    c = conn.cursor()
    c.execute("SELECT linkedin, youtube, twitter FROM social_links WHERE user_id = ?", (user_id,))
    social_links = c.fetchone()
    conn.close()
    return social_links

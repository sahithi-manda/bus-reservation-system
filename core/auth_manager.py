import sqlite3
import hashlib
from database.db_setup import DB_PATH

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    # Using SHA-256 for a built-in zero-dependency hashing
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def register_user(username, email, phone_number, password):
    """
    Registers a new user in the database.
    Returns (True, "Success message") or (False, "Error message")
    """
    if not username or not email or not phone_number or not password:
        return False, "All fields are required!"
        
    hashed_pwd = hash_password(password)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("INSERT INTO users (username, email, phone_number, password_hash) VALUES (?, ?, ?, ?)",
                       (username, email, phone_number, hashed_pwd))
        conn.commit()
        return True, "Registration successful!"
        
    except sqlite3.IntegrityError as e:
        if 'username' in str(e).lower() or 'unique constraint failed: users.username' in str(e).lower():
            return False, "Username already exists!"
        elif 'email' in str(e).lower() or 'unique constraint failed: users.email' in str(e).lower():
            return False, "Email already registered!"
        else:
            return False, "Database integrity error."
    except Exception as e:
        return False, f"An error occurred: {e}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def authenticate_user(username, password):
    """
    Authenticates a user.
    Returns (True, "Login successful") or (False, "Error message")
    """
    if not username or not password:
        return False, "Username and password are required!"
        
    hashed_pwd = hash_password(password)
    
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result:
            stored_hash = result[0]
            if stored_hash == hashed_pwd:
                return True, "Login successful!"
            else:
                return False, "Invalid username or password!"
        else:
            return False, "Invalid username or password!"
            
    except Exception as e:
        return False, f"An error occurred: {e}"
    finally:
        if 'conn' in locals() and conn:
            conn.close()

def get_user_profile(username):
    """Fetches user details from DB."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT username, email, phone_number FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        
        if result:
            return True, {"username": result[0], "email": result[1], "phone": result[2]}
        return False, "User Not Found"
    except Exception as e:
        return False, str(e)
    finally:
        if 'conn' in locals() and conn:
            conn.close()

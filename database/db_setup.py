import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "bus_reservation.db")

def initialize_database():
    """Create the database and required tables if they don't exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone_number TEXT,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # Simple migration in case the database was already created
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN phone_number TEXT")
    except sqlite3.OperationalError:
        pass

    # Create buses table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS buses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            operator TEXT NOT NULL,
            bus_type TEXT NOT NULL,
            departure_time TEXT NOT NULL,
            arrival_time TEXT NOT NULL,
            price INTEGER NOT NULL,
            total_seats INTEGER NOT NULL,
            route_from TEXT NOT NULL,
            route_to TEXT NOT NULL
        )
    ''')
    
    # Create bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            bus_id INTEGER NOT NULL,
            seat_numbers TEXT NOT NULL,
            travel_date TEXT NOT NULL,
            total_amount INTEGER NOT NULL,
            FOREIGN KEY (bus_id) REFERENCES buses(id)
        )
    ''')

    # Automatically generate 200+ mock bus variations across popular routes if db is empty!
    cursor.execute("SELECT COUNT(*) FROM buses")
    if cursor.fetchone()[0] == 0:
        seed_mock_buses(cursor)
        
    conn.commit()
    conn.close()

def seed_mock_buses(cursor):
    """Generates a massive matrix of fake bus combinations between popular cities so searching instantly works!"""
    import random
    
    CITIES = ["Hyderabad", "Bangalore", "Chennai", "Goa", "Vijayawada", "Nellore"]
    OPERATORS = ["SRS Travels", "VRL Travels", "Orange Tours", "Kaveri Travels", "Morning Star", "IntrCity SmartBus"]
    TYPES = ["A/C Sleeper (2+1)", "Non A/C Seater (2+2)", "Volvo Multi-Axle A/C", "A/C Seater (2+2)"]
    
    mock_buses = []
    # Force permutation iterations for huge data set
    for origin in CITIES:
        for dest in CITIES:
            if origin == dest: continue
            
            num_buses = random.randint(3, 8)
            for _ in range(num_buses):
                operator = random.choice(OPERATORS)
                bus_type = random.choice(TYPES)
                
                dep_hour = random.randint(6, 23)
                dep_min = random.choice(["00", "15", "30", "45"])
                # Arrival is usually 6-12 hours later
                arr_hour = (dep_hour + random.randint(6, 12)) % 24
                arr_min = random.choice(["00", "15", "30", "45"])
                
                price = random.randint(500, 2500)
                price = int(round(price / 10.0)) * 10
                
                seats = 30 if "Sleeper" in bus_type else 40
                
                mock_buses.append((operator, bus_type, f"{dep_hour:02d}:{dep_min}", f"{arr_hour:02d}:{arr_min}", price, seats, origin, dest))
                
    cursor.executemany('''
        INSERT INTO buses (operator, bus_type, departure_time, arrival_time, price, total_seats, route_from, route_to)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', mock_buses)
    print(f"Generated {len(mock_buses)} mock buses effortlessly!")

if __name__ == "__main__":
    initialize_database()
    print("Database initialized successfully.")

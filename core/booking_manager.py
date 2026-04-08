import sqlite3
from database.db_setup import DB_PATH

_IN_MEMORY_BUSES = {}

def search_buses(route_from, route_to, date):
    """
    Dynamically generates in-memory buses based on user input, completely bypassing the DB search!
    Returns: (True, [list of dictionaries]) or (False, Error string)
    """
    import random
    global _IN_MEMORY_BUSES
    _IN_MEMORY_BUSES.clear()

    OPERATORS = ["SRS Travels", "VRL Travels", "Orange Tours", "Kaveri Travels", "Morning Star", "IntrCity SmartBus", "AbhiBus Select"]
    TYPES = ["A/C Sleeper (2+1)", "Non A/C Seater (2+2)", "Volvo Multi-Axle A/C", "A/C Seater (2+2)"]
    BOARDING = ["Ameerpet", "KPHB", "LB Nagar", "Miyapur", "Kukatpally", "Secunderabad", "Mehdipatnam"]
    DROPPING = ["Majestic", "Koyambedu", "RTC Bus Stand", "Silk Board", "Madiwala", "Electronic City", "Koramangala"]

    mock_buses = []
    num_buses = random.randint(5, 12)
    
    for _ in range(num_buses):
        operator = random.choice(OPERATORS)
        bus_type = random.choice(TYPES)
        
        dep_hour = random.randint(6, 23)
        dep_min = random.choice([0, 15, 30, 45])
        duration_hours = random.randint(6, 14)
        duration_mins = random.choice([0, 15, 30, 45])
        
        arr_total_mins = (dep_hour * 60 + dep_min) + (duration_hours * 60 + duration_mins)
        arr_hour = (arr_total_mins // 60) % 24
        arr_min = arr_total_mins % 60
        
        price = random.randint(30, 300) * 10  # 300 to 3000
        seats = 30 if "Sleeper" in bus_type else 40
        
        bus_id = random.randint(100000, 999999) # Safe Integer for SQLite ID
        
        bus_data = {
            "id": bus_id,
            "operator": operator,
            "bus_type": bus_type,
            "departure_time": f"{dep_hour:02d}:{dep_min:02d}",
            "departure_hour": dep_hour, # for backend filtering
            "arrival_time": f"{arr_hour:02d}:{arr_min:02d}",
            "duration": f"{duration_hours}h {duration_mins}m",
            "price": price,
            "total_seats": seats,
            "route_from": route_from,
            "route_to": route_to,
            "boarding_points": random.sample(BOARDING, random.randint(1, 4)),
            "dropping_points": random.sample(DROPPING, random.randint(1, 4))
        }
        mock_buses.append(bus_data)
        _IN_MEMORY_BUSES[bus_id] = bus_data
        
    return True, mock_buses

def ensure_bus_in_db(bus_id):
    """If an in-memory bus is checked out, we inject it into the DB so history works elegantly!"""
    if bus_id not in _IN_MEMORY_BUSES:
        return False
        
    b = _IN_MEMORY_BUSES[bus_id]
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if already injected
        cursor.execute("SELECT id FROM buses WHERE id = ?", (b['id'],))
        if cursor.fetchone():
            return True
            
        cursor.execute('''
            INSERT INTO buses (id, operator, bus_type, departure_time, arrival_time, price, total_seats, route_from, route_to)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (b['id'], b['operator'], b['bus_type'], b['departure_time'], b['arrival_time'], b['price'], b['total_seats'], b['route_from'], b['route_to']))
        conn.commit()
    except Exception as e:
        print(f"Error injecting virtual bus: {e}")
    finally:
        if 'conn' in locals() and conn:
            conn.close()
    return True

_GLOBAL_BOOKINGS = {}
_USER_TICKETS = {}
_LOCKED_SEATS = {} # key: "busId_date", value: set of seats

def get_booked_seats(bus_id, travel_date):
    """In-memory fetch of locked seats."""
    # Since bus_id regenerates, technically every search is a new bus natively.
    # We still isolate by ID correctly.
    key = f"{bus_id}_{travel_date}"
    return True, list(_LOCKED_SEATS.get(key, set()))

def create_booking(username, bus_dict, seat_numbers, travel_date, total_amount):
    """Saves ticket globally in memory and locks seats."""
    import uuid
    booking_id = "B" + str(uuid.uuid4().hex[:8]).upper()
    
    # Structure full ticket dictionary
    ticket = {
        "booking_id": booking_id,
        "username": username,
        "bus_id": bus_dict["id"],
        "seat_numbers": ",".join(seat_numbers),
        "travel_date": travel_date,
        "total_amount": total_amount,
        "operator": bus_dict["operator"],
        "route_from": bus_dict["route_from"],
        "route_to": bus_dict["route_to"],
        "departure_time": bus_dict["departure_time"],
        "arrival_time": bus_dict["arrival_time"],
        "duration": bus_dict["duration"]
    }
    
    _GLOBAL_BOOKINGS[booking_id] = ticket
    
    if username not in _USER_TICKETS:
        _USER_TICKETS[username] = []
    _USER_TICKETS[username].append(booking_id)
    
    key = f"{bus_dict['id']}_{travel_date}"
    if key not in _LOCKED_SEATS:
        _LOCKED_SEATS[key] = set()
    for s in seat_numbers:
        _LOCKED_SEATS[key].add(s)
        
    return True, booking_id

def get_user_bookings(username):
    """Retrieves all Tickets for a user reversed chronological."""
    if username not in _USER_TICKETS:
        return True, []
        
    tickets = []
    for bid in reversed(_USER_TICKETS[username]):
        tickets.append(_GLOBAL_BOOKINGS[bid])
    return True, tickets
    
def cancel_booking(username, booking_id):
    """Releases seats and deletes history dict."""
    if booking_id not in _GLOBAL_BOOKINGS:
        return False, "Not Found"
        
    ticket = _GLOBAL_BOOKINGS[booking_id]
    
    # 1. Remove from User Tickets
    if username in _USER_TICKETS and booking_id in _USER_TICKETS[username]:
        _USER_TICKETS[username].remove(booking_id)
        
    # 2. Free up the seats mathematically
    key = f"{ticket['bus_id']}_{ticket['travel_date']}"
    if key in _LOCKED_SEATS:
        seats = ticket['seat_numbers'].split(",")
        for s in seats:
            if s in _LOCKED_SEATS[key]:
                _LOCKED_SEATS[key].remove(s)
                
    # 3. Destroy record
    del _GLOBAL_BOOKINGS[booking_id]
    
    return True, "Cancelled Successfully"

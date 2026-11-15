# Bus Reservation System (Bus Yatra)

A desktop bus ticket booking app built with Python, CustomTkinter and SQLite. It follows the flow of popular booking sites like AbhiBus and RedBus: register, log in, search routes, filter and sort buses, pick seats on a visual bus layout, pay (mock), and manage your tickets.

This is a learning and portfolio project. Bus listings are generated randomly and payment is simulated, so nothing here talks to real operators or charges real money.

## Features

- **Accounts.** Register with username, email, phone number and password, then log in. Duplicate usernames and emails are caught with clear error messages.
- **Route search.** Choose a departure city, destination and travel date. A city dropdown shows popular cities (Hyderabad, Bangalore, Chennai, Goa, Vijayawada, Nellore), and a calendar popup plus Today/Tomorrow shortcuts handle dates.
- **Filters and sorting.** Narrow results by price range (₹300 to ₹3000) and departure window (before 10 AM, 10 AM to 5 PM, 5 PM to 11 PM, after 11 PM). Sort by price, low to high or high to low.
- **Bus details.** Each result shows the operator, bus type (A/C Sleeper, Non A/C Seater, Volvo Multi-Axle and so on), departure and arrival times, duration, fare, and boarding and dropping points.
- **Seat selection.** An interactive seat map marks seats as available, selected or booked, with a live fare summary.
- **Mock payment.** Pay with a UPI ID or card number (simulated), then get a booking confirmation with a booking ID.
- **My Bookings.** View your tickets, newest first, and cancel any of them. Cancelling frees the seats again.
- **Profile and logout.** View your account details and switch users without restarting the app.

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3 |
| GUI | CustomTkinter 5.2.2, tkcalendar 1.6.1 |
| Images | Pillow 10.2.0 |
| Database | SQLite (built into Python) |

## Project structure

```
bus-reservation-system/
├── main.py                  # Entry point: sets up the DB, opens the login window
├── requirements.txt
├── bus_reservation.db       # SQLite database (created automatically if missing)
├── assets/
│   └── logo.png             # App logo, background stripped at load time
├── database/
│   └── db_setup.py          # Table creation and sample bus seeding
├── core/
│   ├── auth_manager.py      # Registration, login, user profile
│   ├── booking_manager.py   # Bus search, seat locking, bookings, cancellation
│   └── utils.py             # Logo loading helper
└── gui/
    ├── auth_window.py       # Login and registration screens
    ├── dashboard.py         # Search, filters, results, booking history, profile
    └── booking_flows.py     # Seat selection, payment, confirmation screens
```

## Getting started

### Prerequisites

- Python 3.8 or newer, with Tkinter included (it ships with the standard Python installers for Windows and macOS; on Linux install `python3-tk`)

### Install and run

```bash
git clone https://github.com/sahithi-manda/bus-reservation-system.git
cd bus-reservation-system

python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

On first launch the app creates the database and tables. Click **Register Here**, create an account, log in, and start searching.

### Try it out

1. Register a new user and log in.
2. Pick a leaving city and a destination from the dropdown, choose a date, and click **Search**.
3. Use the filters on the left, then select a bus.
4. Choose your seats, continue to payment, and enter any UPI ID or card number. Payment is simulated.
5. Open **My Bookings** to see the ticket or cancel it.

## How it works

- **Database tables.** `users`, `buses` and `bookings` are created by `database/db_setup.py`. On a fresh database it also seeds sample buses for every pair of the six cities.
- **Search results.** `search_buses` currently generates 5 to 12 random buses for each search in memory, so results change every time you search. A bus is written to the database only when it is used in a booking.
- **Bookings and seat locks.** Tickets and locked seats are held in memory while the app runs, keyed by bus and travel date. Closing the app clears them.
- **Passwords.** Stored as SHA-256 hashes.

## Known limitations and ideas for improvement

- Persist bookings in the existing `bookings` table so tickets survive restarts (the table is created but not used yet)
- Use a real inventory: store fixed bus schedules in the `buses` table and search them instead of generating random results
- Replace unsalted SHA-256 with a salted password hash such as bcrypt or PBKDF2
- Validate email format and phone number on registration
- Add ticket download (PDF) and booking email or SMS confirmation
- Add unit tests for `auth_manager` and `booking_manager`
- Add an admin screen to manage buses and routes

## Author

Built by Manda Sahithi.

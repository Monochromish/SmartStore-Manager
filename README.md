# SmartStore Manager

SmartStore Manager is a Python-based store management application designed to simplify inventory and sales processes for small-sized retail stores. Utilizing Tkinter for the user interface and MySQL for backend data management, this application offers an easy-to-use, efficient, and dynamic approach to store management.

## Features

- **Real-Time Inventory Management**: Add, remove, and update inventory items on the fly.
- **Seamless Checkout System**: Easily manage sales transactions with an integrated checkout system.
- **Dynamic Data Updates**: Reflect inventory changes in real-time, ensuring data accuracy.
- **User-Friendly Interface**: Designed with Tkinter for simplicity and ease of use.

## Getting Started

### Prerequisites

- Python (3.x recommended)
- MySQL Server
- Tkinter
- MySQL Connector for Python

### Set up

1. **Clone/Download the repository:**
2. Install required Python modules:

   ```console
   pip install mysql-connector-python
   ```

   Tkinter is usually included in the standard Python package.

3. Install MySQL Server and set up a new database.

   Create the items table in your database:

   ```sql
   CREATE TABLE items (
       item_id INT AUTO_INCREMENT PRIMARY KEY,
       name VARCHAR(255) NOT NULL,
       price DECIMAL(10, 2) NOT NULL,
       quantity INT NOT NULL
   );
   ```

4. Configure code:

   Update the connect function in the Python script with your MySQL credentials.

5. Run the Script

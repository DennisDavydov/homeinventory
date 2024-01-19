
# Node.js Inventory Server

This is a Node.js inventory server designed to run on a Linux machine or Raspberry Pi. It uses Express.js for the web framework and MySQL as the database.

## Prerequisites

Before you get started, make sure you have the following prerequisites installed:

- Node.js: [Download and install Node.js](https://nodejs.org/).
- MySQL: [Download and install MySQL](https://dev.mysql.com/downloads/mysql/).

## Setup

1. Clone this repository to your Linux machine or Raspberry Pi:

   ```
   git clone https://github.com/DennisDavydov/homeinvetorypi.git
   cd homeinventorypi
   ```

2. Install the required Node.js packages by running:

   ```
   npm install
   ```

3. Create a MySQL database for the server. You can do this using the MySQL command-line tool or a GUI like phpMyAdmin. Make sure to note down the database name, username, and password.

4. Open the `server.js` file and update the MySQL connection configuration with your database details:

   ```javascript
   const connection = mysql.createConnection({
       host: 'hostname',
       user: 'user',
       password: 'yourpassword',
       database: 'databasename' 
   });
   ```

5. Run the server:

   ```
   node server.js
   ```

The server should now be running on http://localhost:8080.

## Usage

- Access the server in your web browser by navigating to http://localhost:8080.
- The server provides an interface to manage inventory data.
- You add, delete, and view inventory items.

## API Endpoints

- **GET /:** Access the home page with inventory data.
- **POST /deleteRow:** Delete a specific inventory item by providing its barcode in the request body.

## Contributing

If you would like to contribute to this project, feel free to fork the repository and submit pull requests with your changes.

## Acknowledgments

- This project was created with Node.js, Express.js, and MySQL.


# Node.js Inventory Server

This is a Node.js inventory server designed to run on a Linux machine or Raspberry Pi. It uses Express.js for the web framework and MySQL as the database.

This is written to work in pair with the [barcode reader](https://github.com/DennisDavydov/barcodeReaderPy), but can be used on its own through the webpage.

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

2. Open the `config.json` file and update the MySQL connection configuration with your database details:

   ```json
      "db": {
       "host": "localhost",
       "user": "user",
       "password": "yourpassword",
       "database": "databasename",
       "port": 3306
      },
      "app": {
        "port": 8080,
        "hostname": "localhost"
      }
   ```

3. Run the `run.sh` script

4. Install the required Node.js packages by running:

   ```
   npm install
   ```

5. Run the server:

   ```
   node app.js
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

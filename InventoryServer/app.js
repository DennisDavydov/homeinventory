const express = require('express');
const app = express();
const mysql = require('mysql');
const port = 3000;

// Set the view engine to EJS
app.set('view engine', 'ejs');

// Serve static files (like CSS or images)
app.use(express.static('public'));

// Create a MySQL connection
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'root',
    database: 'inventory_db'
});

// Connect to the database
connection.connect((err) => {
    if (err) {
        console.error('Error connecting to MySQL:', err);
        throw err;
    }
    console.log('Connected to MySQL database');
});

// Route for the home page
app.get('/', (req, res) => {
    // Fetch data from the products table
    const sql = 'SELECT * FROM products';
    connection.query(sql, (error, results) => {
        if (error) {
            console.error('Error fetching data:', error);
            return res.status(500).send('Error fetching data');
        }
        // Render the index.ejs template with the fetched data
        res.render('index', { products: results,  });
    });
});


function get_data(){
	
	
	}
// Start the server
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://localhost:${port}`);
});

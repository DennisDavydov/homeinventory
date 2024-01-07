const express = require('express');
const app = express();
const mysql = require('mysql');
const port = 8080;

// Set the view engine to EJS
app.set('view engine', 'ejs');

// Serve static files (like CSS or images)
app.use(express.static('public'));

// Create a MySQL connection
const connection = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: 'Actimel1234',
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
    const productsSQL = 'SELECT * FROM (SELECT p.*, t.total_amount, t.earliest_expiry_date, ROW_NUMBER() OVER(PARTITION BY p.barcode ORDER BY p.id) AS row_num FROM products p JOIN (SELECT barcode, SUM(amount) AS total_amount, MIN(expiry_date) AS earliest_expiry_date FROM products GROUP BY barcode) t ON p.barcode = t.barcode) subquery WHERE row_num = 1';

    // Fetch data from the second table
    const secondTableSQL = 'SELECT * FROM products';

    // Use Promise.all to execute both queries in parallel
    Promise.all([
        new Promise((resolve, reject) => {
            connection.query(productsSQL, (error, productsResults) => {
                if (error) {
                    console.error('Error fetching data from products table:', error);
                    reject(error);
                } else {
                    resolve(productsResults);
                }
            });
        }),
        new Promise((resolve, reject) => {
            connection.query(secondTableSQL, (error, secondTableResults) => {
                if (error) {
                    console.error('Error fetching data from second table:', error);
                    reject(error);
                } else {
                    resolve(secondTableResults);
                }
            });
        })
    ])
    .then(([products, secondTableData]) => {
        // Render the index.ejs template with both sets of fetched data
        res.render('index', { products: products, fullproducts: secondTableData });
    })
    .catch((error) => {
        console.error('Error fetching data:', error);
        res.status(500).send('Error fetching data');
    });
});


function get_data(){
	
	
	}
// Start the server
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://localhost:${port}`);
});

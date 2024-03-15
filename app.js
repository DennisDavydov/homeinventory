const express = require('express');
const app = express();
const mysql = require('mysql');
const user_config = require('./config.json')
const port = user_config["app"]["port"]
const hostname = user_config["app"]["hostname"]

// Set the view engine to EJS
app.set('view engine', 'ejs');

// Serve static files (like CSS or images)
app.use(express.static('public'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

console.log("Running with configuration: ")
console.log(user_config["db"])

// Create a MySQL connection
const connection = mysql.createConnection(user_config);

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


app.post('/deleteRow', (req, res) => {

    console.log('Received request body:', req.body);
    const { barcode } = req.body; // Assuming the 'id' is sent in the request body
    // Construct and execute the SQL query to delete the row
    const query = `DELETE FROM products WHERE barcode = ${connection.escape(barcode)} order by expiry_date limit 1`; // Replace 'your_table_name' with your actual table name

    connection.query(query, (error, results) => {
        if (error) {
            console.error('Error deleting row:', error);
            res.status(500).send('Error deleting row');
            return;
        }
        console.log('Row deleted successfully');
        res.status(200).send('Row deleted successfully');
    });
});



function get_data(){


	}
// Start the server
app.listen(port, '0.0.0.0', () => {
    console.log(`Server running on http://${hostname}:${port}`);
});

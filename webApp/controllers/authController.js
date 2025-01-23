const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const db = require('../models/db');

const JWT_SECRET = 'your_secret_key';

module.exports.register = async (req, res) => {
  try {
    const { firstname, lastname, email, password, companyname, } = req.body;

    if (!firstname ||!lastname ||!email ||!password ||!companyname ) {
      return res.status(400).send('All fields are required');
    }

    const hashedPassword = await bcrypt.hash(password, 10);

    const sql = 'INSERT INTO Users (firstname, lastname, email, password, companyname) VALUES (?, ?, ?, ?, ?)';
    const values = [firstname, lastname, email, hashedPassword, companyname ];

    // Insert the user into the database and get the insertId (user_id)
    const [result] = await db.query(sql, values);  // Use db.query for promise-based queries
    const user_id = result.insertId;

    const payload = {
      user_id: user_id,
      firstname: firstname,
      lastname: lastname,
      email: email,
    };

    const token = jwt.sign(payload, JWT_SECRET, { expiresIn: '1h' });

    // Respond with the token and user information
    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      token: token,
      user: {
        user_id: user_id,
        firstname: firstname,
        lastname: lastname,
        email: email,
      },
    });
  } catch (error) {
    console.error('Error during registration:', error.message);
    res.status(500).send('Internal Server Error');
  }
};

module.exports.login = async (req, res) => { 
  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ success: false, message: 'Email and password are required' });
    }

    const sql = 'SELECT * FROM Users WHERE email = ?';
    const [results] = await db.query(sql, [email]);  // Use promise-based query

    if (results.length > 0) {
      const match = await bcrypt.compare(password, results[0].password);  

      if (match) {
        // Create a payload for the JWT
        const payload = {
          user_id: results[0].user_id,
          username: results[0].username,
          email: results[0].email,
        };

        // Generate a JWT token
        const token = jwt.sign(payload, JWT_SECRET, { expiresIn: '1h' });

        // Respond with the token and user information
        res.status(200).json({
          success: true,
          message: 'Login successful',
          token: token,  // Send the token in the response
          user: {
            user_id: results[0].user_id,
            username: results[0].username,
            email: results[0].email,
          },
        });
      } else {
        res.status(401).json({ success: false, message: 'Invalid username or password' });
      }
    } else {
      res.status(401).json({ success: false, message: 'Invalid username or password' });
    }
  } catch (error) {
    console.error("Error during login:", error.message);
    res.status(500).json({ success: false, message: 'Internal Server Error' });
  }
};


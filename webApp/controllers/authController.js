const jwt = require('jsonwebtoken');
const bcrypt = require('bcrypt');
const db = require('../models/db');
const JWT_SECRET = 'drake';

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
      tenantId: user_id,
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
        tenantId: user_id,
        firstname: firstname,
        lastname: lastname,
        email: email,
      },
    });
  } 
  catch (error) {
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
        const payload = {
          tenantId: results[0].user_id,
          username: results[0].username,
          email: results[0].email,
        };
        // Ensure JWT_SECRET is available
        const token = jwt.sign(payload, process.env.JWT_SECRET, { expiresIn: '1h' });
        res.status(200).json({
          success: true,
          message: 'Login successful',
          token: token,
          user: {
            tenantId: results[0].user_id,
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

module.exports.saveCustomEntry = async (req, res) => {
  try {
    const tenantId = req.user.tenantId; // Access tenantId from the JWT payload
    const { entryData } = req.body;

    if (!entryData) {
      return res.status(400).json({ message: 'Entry Data is required' });
    }

    const [result] = await db.query(
      'INSERT INTO custom_entries (tenant_id, entry_data) VALUES (?, ?)',
      [tenantId, JSON.stringify(entryData)]
    );

    const entryId = result.insertId;
    return res.status(201).json({ message: 'Custom entry saved successfully', entryId });
  } catch (error) {
    console.error('Database query error:', error);
    res.status(500).json({ message: 'Error saving custom entry', error: error.message || error });
  }
};
// Fetch all custom entries for a tenant
module.exports.getCustomEntries = async (req, res) => {
  try {
      const { tenantId } = req.params;

      const [entries] = await db.query(
          'SELECT * FROM custom_entries WHERE tenant_id = ?',
          [tenantId]
      );

      return res.status(200).json({ entries });
  } catch (error) {
      console.error('Database query error:', error);
      res.status(500).json({ message: 'Error fetching custom entries', error: error.message || error });
  }
};

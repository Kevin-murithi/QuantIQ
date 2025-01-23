const express = require('express');
const cors = require('cors');
const path = require('path');
const hbs = require('express-handlebars');
const Handlebars = require('handlebars');
const dotenv = require('dotenv');
const db = require('./models/db');
const authRoutes = require("./routes/authRoutes");
const morgan = require('morgan');
const jwt = require('jsonwebtoken'); // Added JWT
// JWT Middleware
const verifyToken = (req, res, next) => {
  const authHeader = req.headers.authorization;

  if (!authHeader || !authHeader.startsWith('Bearer ')) {
    return res.status(401).json({ success: false, message: 'Access denied. No token provided.' });
  }

  const token = authHeader.split(' ')[1]; // Extract token from "Bearer <token>"
  try {
    const decoded = jwt.verify(token, process.env.JWT_SECRET || 'your_secret_key'); // Verify token
    req.user = decoded; // Attach user data to the request object
    next(); // Proceed to the next middleware or route handler
  } catch (error) {
    res.status(403).json({ success: false, message: 'Invalid or expired token.' });
  }
};

dotenv.config();
const app = express();

//Set view engine
const { allowInsecurePrototypeAccess } = require('@handlebars/allow-prototype-access');

// const handlebars = hbs.create({
//   helpers: {
//     // Equality check helper
//     eq: (a, b) => a === b,

//     // Date formatting helper
//     formatDate: (date) => {
//       const d = new Date(date);
//       return `${d.getMonth() + 1}/${d.getDate()}/${d.getFullYear()}`;
//     },

//     // Uppercase string helper
//     uppercase: (str) => str.toUpperCase(),

//     // Conditional check: if a value is greater than another
//     gt: (a, b) => a > b,

//     // Greater than or equal check
//     gte: (a, b) => a >= b,

//     // JSON stringifying helper
//     json: (context) => JSON.stringify(context),

//     // Check if user has claimed a food item
//     checkClaimed: async (userId, foodId) => {
//       const sql = 'SELECT * FROM claimed_items WHERE user_id = ? AND food_id = ?';
//       const [result] = await db.promise().query(sql, [userId, foodId]);

//       return result.length > 0;
//     }
//   },
//   extname: '.hbs',
//   handlebars: allowInsecurePrototypeAccess(Handlebars)
// });

// app.engine('.hbs', handlebars.engine);
// app.set('view engine', '.hbs');
// app.set('views', path.join(__dirname, 'views'));

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, 'public')));
app.use(authRoutes);
app.use(cors(
  {origin: 'http://localhost:5500'}
));
app.use(morgan("dev"));

// JWT Middleware to protect certain routes
// Protected Route Example
app.use('/protected', verifyToken, (req, res) => {
  res.json({
    success: true,
    message: 'Access to protected route granted.',
    user: req.user, // Include user data from the token
  });
});

// Default Route
app.get('/', (req, res) => {
  res.json({
    success: true,
    message: 'Welcome to the API!',
  });
});

const PORT = process.env.PORT || 8080;

app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
  console.log('Your app is finally complete!!!!');
});

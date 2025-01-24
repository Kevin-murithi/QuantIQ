// middleware/authMiddleware.js
const jwt = require('jsonwebtoken');
const JWT_SECRET = 'drake'; // Make sure this matches the secret you used for signing the token

module.exports.verifyToken = (req, res, next) => {
  const token = req.headers['authorization']?.split(' ')[1]; // Assuming the token is passed in the Authorization header as "Bearer token"

  if (!token) {
    return res.status(403).json({ message: 'Token is required' });
  }

  try {
    const decoded = jwt.verify(token, JWT_SECRET);
    req.user = decoded; // Attach the decoded user info (including tenantId) to the request object
    next(); // Pass control to the next middleware or route handler
  } catch (err) {
    console.error('Invalid or expired token:', err);
    res.status(403).json({ message: 'Invalid or expired token' });
  }
};

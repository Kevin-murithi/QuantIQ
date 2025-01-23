const jwt = require ('jsonwebtoken');
const User = require ("../models/db");

//check and verify token
const requireAuth = (req, res, next) => {
  const token = req.cookies.jwt;
  
  if (token) {
    jwt.verify (token, process.env.SECRET, (err, decodedToken) => {
      if (err) {
        console.log (err.message);
        res.redirect ('/sign_in');
      }
      else {
        console.log (decodedToken);
        next();
      }
    })
  }
  else {
    res.redirect ('/sign_in');
  }
}

//check user
const checkUser = (req, res, next) => {
  const token = req.cookies.jwt;
  
  if (token) {
    jwt.verify (token, process.env.SECRET, async (err, decodedToken) => {
      if (err) {
        console.log (err.message);
        res.locals.user = null;
        next();
      }
      else {
        console.log (decodedToken);
        const user = await User.findById(decodedToken.id);
        res.locals.user = user;
        next();
      }
    })
  }
  else {
    res.locals.user = null;
    next();
  }
}

module.exports = { requireAuth, checkUser };
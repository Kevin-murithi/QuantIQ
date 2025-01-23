const { Router } = require ('express');
const authController = require ('../controllers/authController');
const loadPages = require ('../controllers/loadPages');

const router = Router();

// create application/json parser
const bodyParser = require('body-parser');
var jsonParser = bodyParser.json();

// Page rendering routes
router.get ("/", loadPages.landingPage);
router.get ("/signup", loadPages.signupPage);
router.get ("/login", loadPages.loginPage);

// Other (CRUD/auth) routes
router.post('/register', authController.register);
router.post('/login', authController.login);

module.exports = router;
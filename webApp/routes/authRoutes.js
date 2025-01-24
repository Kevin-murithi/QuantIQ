const { Router } = require ('express');
const authController = require ('../controllers/authController');
const loadPages = require ('../controllers/loadPages');
const { verifyToken } = require('../middleware/authMiddleware');

const router = Router();

// create application/json parser
const bodyParser = require('body-parser');
var jsonParser = bodyParser.json();

// Page rendering routes
router.get ("/", loadPages.landingPage);
router.get ("/dashboard", loadPages.dashboard);
router.get ("/signup", loadPages.signupPage);
router.get ("/login", loadPages.loginPage);
router.get("/customfield", loadPages.customfieldspage);
router.get ("/signin", loadPages.loginPage);

// Other (CRUD/auth) routes

router.post('/register', jsonParser, authController.register);
router.post('/login', jsonParser, authController.login);

router.post('/customentries', verifyToken, authController.saveCustomEntry);       // Save a custom entry
router.get('/customentries/:tenantId', verifyToken, authController.getCustomEntries);

module.exports = router;
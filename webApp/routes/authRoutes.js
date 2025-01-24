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
<<<<<<< HEAD
router.get ("/login", loadPages.loginPage);
router.get("/customfield", loadPages.customfieldspage);
=======
router.get ("/signin", loadPages.loginPage);
>>>>>>> 85ab000ca1e50d3c9ae010d136895ff9f8a0fd44

// Other (CRUD/auth) routes

router.post('/register', jsonParser, authController.register);
router.post('/login', jsonParser, authController.login);

router.post('/customentries', authController.saveCustomEntry);       // Save a custom entry
router.get('/customentries/:tenantId', authController.getCustomEntries);

module.exports = router;
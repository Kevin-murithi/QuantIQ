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
router.get ("/signup", loadPages.signupPage);
router.get ("/login", loadPages.loginPage);
router.get ("/signin", loadPages.loginPage);
router.get("/customfield", loadPages.customfieldspage);
router.get ("/dashboard", loadPages.dashboard);
router.get ("/ai_insights", loadPages.ai_insights);
router.get ("/customer_insights", loadPages.customer_insights);
router.get ("/forecasting", loadPages.forecasting);
router.get ("/esg_metrics", loadPages.esg_metrics);
router.get ("/sentiment_analysis", loadPages.sentiment_analysis);
router.get ("/account_management", loadPages.account_management);
router.get ("/files", loadPages.files);
router.get ("/settings", loadPages.settings);
router.get ("/sales_analytics", loadPages.sales_analytics);

// Other (CRUD/auth) routes

router.post('/register', jsonParser, authController.register);
router.post('/login', jsonParser, authController.login);

router.post('/customentries', verifyToken, authController.saveCustomEntry);       // Save a custom entry
router.get('/customentries/:tenantId', verifyToken, authController.getCustomEntries);

module.exports = router;
module.exports.landingPage = (_req, res) => {
  res.render('landingpage', {pageTitle: "Langing Page"});
}

module.exports.signupPage = (_req, res) => {
  res.render('signup', {pageTitle: "Signup Form"});
}

module.exports.loginPage = (_req, res) => {
  res.render('login', {pageTitle: "Signin Form"});
}

module.exports.customfieldspage = (_req, res) => {
  res.render('customfields', {pageTitle: "Custom Fields"});
}

module.exports.dashboard = (_req, res) => {
  res.render('dashboard', {pageTitle: "Dashboard"});
}

module.exports.ai_insights = (_req, res) => {
  res.render('ai_insights', { pageTitle: "AI Insights" });
};

module.exports.customer_insights = (_req, res) => {
  res.render('customer_insights', { pageTitle: "Customer Insights" });
};

module.exports.forecasting = (_req, res) => {
  res.render('forecasting', { pageTitle: "Forecasting" });
};

module.exports.esg_metrics = (_req, res) => {
  res.render('esg_metrics', { pageTitle: "ESG Metrics" });
};

module.exports.sentiment_analysis = (_req, res) => {
  res.render('sentiment_analysis', { pageTitle: "Sentiment Analysis" });
};

module.exports.account_management = (_req, res) => {
  res.render('account_management', { pageTitle: "Account Management" });
};

module.exports.files = (_req, res) => {
  res.render('files', { pageTitle: "Files" });
};

module.exports.settings = (_req, res) => {
  res.render('settings', { pageTitle: "Settings" });
};

module.exports.sales_analytics = (_req, res) => {
  res.render('sales_analytics', { pageTitle: "Sales Analytics" });
};
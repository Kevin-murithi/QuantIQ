module.exports.landingPage = (_req, res) => {
  res.render('landingpage', {pageTitle: "Landing Page"});
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
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Anomalies(models.Model):
    anomaly_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    anomaly_type = models.CharField(max_length=19)
    detected_at = models.DateTimeField(blank=True, null=True)
    details = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Anomalies'


class CustomerClv(models.Model):
    clv_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    customer = models.ForeignKey('Customers', models.DO_NOTHING)
    lifetime_value = models.JSONField()
    last_purchase_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer_CLV'


class CustomerSegments(models.Model):
    segment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    segment_name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    customer_count = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customer_Segments'


class Customers(models.Model):
    customer_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    age = models.JSONField(blank=True, null=True)
    gender = models.CharField(max_length=6, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    loyalty_status = models.CharField(max_length=12, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Customers'


class EsgScores(models.Model):
    esg_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    environmental_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    social_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    governance_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    total_esg_score = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    recommendations = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ESG_Scores'


class HistoricalTrends(models.Model):
    trend_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    year = models.TextField()  # This field type is a guess.
    total_sales = models.JSONField()
    top_category = models.CharField(max_length=50, blank=True, null=True)
    campaign_performance = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Historical_Trends'


class Products(models.Model):
    product_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING) 
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)
    stock_quantity = models.JSONField(blank=True, null=True)
    reorder_level = models.JSONField(blank=True, null=True)
    supplier = models.ForeignKey('Suppliers', models.DO_NOTHING, blank=True, null=True)
    price = models.JSONField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Products'


class Returns(models.Model):
    return_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey('Transactions', models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    quantity = models.JSONField()
    refund_amount = models.JSONField()
    reason = models.TextField(blank=True, null=True)
    return_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Returns'


class Revenue(models.Model):
    revenue_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    date = models.DateField()
    gross_revenue = models.JSONField()
    net_revenue = models.JSONField()
    discounts_applied = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Revenue'


class SalesForecasts(models.Model):
    forecast_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    forecast_period = models.CharField(max_length=20)
    predicted_sales = models.JSONField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sales_Forecasts'


class SentimentAnalysis(models.Model):
    sentiment_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    total_reviews = models.JSONField()
    positive_reviews = models.JSONField()
    neutral_reviews = models.JSONField()
    negative_reviews = models.JSONField()
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Sentiment_Analysis'


class StockForecasts(models.Model):
    stock_forecast_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    forecasted_demand = models.JSONField()
    restock_recommendation = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Stock_Forecasts'


class Suppliers(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    supplier_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Suppliers'


class Transactions(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    customer = models.ForeignKey(Customers, models.DO_NOTHING, blank=True, null=True)
    product = models.ForeignKey(Products, models.DO_NOTHING)
    quantity = models.JSONField()
    unit_price = models.JSONField()
    total_amount = models.JSONField()
    transaction_date = models.DateTimeField(blank=True, null=True)
    payment_method = models.CharField(max_length=6)

    class Meta:
        managed = False
        db_table = 'Transactions'


class Users(models.Model):
    user_id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.CharField(
        unique=True, 
        max_length=100, 
        null=False,  # Disallow NULL
        blank=False,  # Disallow empty strings
        error_messages={
            'unique': "A user with that email already exists.",
        }
    )
    password = models.CharField(max_length=255)
    companyname = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Users'

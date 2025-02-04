from django.shortcuts import render
from django.http import JsonResponse
import json
import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from django.shortcuts import get_object_or_404
from quant_logic.models import SentimentAnalysis, SalesForecasts, Revenue,Transactions, Anomalies, CustomerClv, Users, Customers, CustomerSegments, EsgScores, HistoricalTrends, Products
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from datetime import datetime, timedelta
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA
from prophet import Prophet
from sklearn.model_selection import train_test_split
import random
from decimal import Decimal



def detect_user_anomalies(request, user_id):
    try:
        # Step 1: Get the user from the database
        user = get_object_or_404(Users, user_id=user_id)  # Use 'user_id' instead of 'id'

        # Step 2: Fetch transaction data for the specific user
        transactions = Transactions.objects.filter(user=user).values('transaction_id', 'total_amount', 'transaction_date')
        if not transactions:
            return JsonResponse({'status': 'error', 'message': 'No transactions found for this user.'})

        df = pd.DataFrame(transactions)

        # Step 3: Preprocess data (handling missing values, normalizing, etc.)
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        
        # Convert 'total_amount' to float if it is a Decimal
        df['total_amount'] = df['total_amount'].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
        
        # Apply further processing for total_amount in case it is a dictionary
        df['total_amount'] = df['total_amount'].apply(lambda x: x.get('amount', 0) if isinstance(x, dict) else x)
        
        df = df.dropna(subset=['total_amount'])
        df['transaction_date'] = df['transaction_date'].apply(lambda x: x.timestamp())  # Convert to timestamp for model

        # Step 4: Normalize the data
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df[['total_amount', 'transaction_date']])

        # Step 5: Train Isolation Forest model
        model = IsolationForest(contamination=0.05)  # Adjust contamination parameter
        anomalies = model.fit_predict(df_scaled)

        # Step 6: Identify and store anomalies
        anomaly_data = []
        for index, anomaly in enumerate(anomalies):
            if anomaly == -1:  # -1 indicates an anomaly
                anomaly_data.append({
                    'user': user,  # Link anomaly to the specific user
                    'anomaly_type': 'Transaction Anomaly',
                    'detected_at': datetime.now(),
                    'details': f"Anomaly detected in transaction ID {transactions[index]['transaction_id']}"
                })

        # Step 7: Save anomalies to the database
        for anomaly in anomaly_data:
            Anomalies.objects.create(**anomaly)

        # Step 8: Return success response with anomaly count
        return JsonResponse({'status': 'success', 'message': f'{len(anomaly_data)} anomalies detected and stored for user {user_id}.'})

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})



def calculate_user_clv(request, user_id):
    try:
        # Step 1: Get the user from the database
        user = get_object_or_404(Users, id=user_id)

        # Step 2: Fetch customer transaction data for the specific user
        transactions = Transactions.objects.filter(user=user).values('user', 'amount', 'transaction_date')
        if not transactions:
            return JsonResponse({'status': 'error', 'message': 'No transactions found for this user.'})

        df = pd.DataFrame(transactions)

        # Step 3: Perform RFM analysis
        df['transaction_date'] = pd.to_datetime(df['transaction_date'])
        current_date = datetime.now()

        # Recency: How recently did the customer purchase
        df['recency'] = (current_date - df['transaction_date']).dt.days

        # Frequency: Number of purchases per user
        frequency = df.groupby('user')['transaction_date'].count().reset_index(name='frequency')

        # Monetary: Total amount spent by each user
        monetary = df.groupby('user')['amount'].sum().reset_index(name='monetary')

        # Merging RFM values into one dataframe
        rfm = pd.merge(frequency, monetary, on='user')
        rfm = pd.merge(rfm, df[['user', 'recency']].drop_duplicates(), on='user')

        # Step 4: Train a predictive model (e.g., Linear Regression)
        X = rfm[['recency', 'frequency', 'monetary']]  # Features
        y = rfm['monetary']  # Target - here we're predicting monetary value as proxy for CLV

        model = LinearRegression()  # Or XGBoost
        model.fit(X, y)

        # Step 5: Predict lifetime value (CLV)
        predictions = model.predict(X)

        # Step 6: Save results in Customer_CLV table for this user
        clv_data = {
            'user': user,
            'customer': Customers.objects.get(user_id=user_id),  # Ensure customer exists
            'lifetime_value': {'predicted_clv': predictions[0]},  # For this user
            'last_purchase_date': df[df['user'] == user_id]['transaction_date'].max(),
            'created_at': current_date
        }

        # Insert data into the Customer_CLV table
        CustomerClv.objects.create(**clv_data)

        # Step 7: Return success response
        return JsonResponse({'status': 'success', 'message': f'CLV calculated and stored for user {user_id}.'})

    except Exception as e:
        # Handle errors
        return JsonResponse({'status': 'error', 'message': str(e)})


def calculate_user_segmentation(request, user_id):
    try:
        # Step 1: Get the user from the database
        user = get_object_or_404(Users, id=user_id)

        # Step 2: Fetch customer data for the specific user
        customers = Customers.objects.filter(user=user).values('user', 'age', 'gender', 'purchase_frequency', 'avg_spent', 'last_purchase_date')
        if not customers:
            return JsonResponse({'status': 'error', 'message': 'No customer data found for this user.'})

        df = pd.DataFrame(customers)

        # Step 3: Preprocessing - Handle missing data if necessary (e.g., using fillna)
        df = df.fillna(df.mean())

        # Step 4: Feature selection (e.g., age, gender, purchase behavior)
        features = df[['age', 'purchase_frequency', 'avg_spent']]  # You can add more features if available
        X = features.values

        # Step 5: Reduce dimensionality using PCA (Optional: You can try t-SNE for more complex data)
        pca = PCA(n_components=2)  # Reduce to 2 components for visualization
        X_pca = pca.fit_transform(X)

        # Step 6: Apply K-Means Clustering (You can use DBSCAN or Hierarchical Clustering instead)
        kmeans = KMeans(n_clusters=4)  # You can adjust the number of clusters based on your use case
        df['segment'] = kmeans.fit_predict(X_pca)

        # Step 7: Assign this user to a segment and store the results
        user_segment = df.iloc[0]['segment']  # Assuming the user belongs to one segment, based on their data
        segment_name = f'Segment {user_segment + 1}'
        segment_description = f'Description for Segment {user_segment + 1}'

        # Create or update the segment information for the user
        CustomerSegments.objects.create(
            user=user,
            segment_name=segment_name,
            description=segment_description,
            customer_count={'count': 1},  # Count is 1 since it's a single user
            created_at=datetime.now()
        )

        # Step 8: Return a success response
        return JsonResponse({
            'status': 'success',
            'message': f'Customer segmentation completed for user {user_id} and stored in the database.',
            'segment_name': segment_name,
            'segment_description': segment_description
        })

    except Exception as e:
        # Handle errors
        return JsonResponse({'status': 'error', 'message': str(e)})
    

# View to calculate ESG score for a specific user
def calculate_user_esg(request, user_id):
    try:
        # Step 1: Get the user from the database
        user = get_object_or_404(Users, id=user_id)

        # Step 2: Check if ESG score already exists for the user
        esg_record, created = EsgScores.objects.get_or_create(user=user, defaults={
            'environmental_score': None,
            'social_score': None,
            'governance_score': None,
            'total_esg_score': None,
            'recommendations': None,
            'created_at': datetime.now()
        })

        # Step 3: If ESG score exists, update it; otherwise, create a new record
        environmental_score = round(random.uniform(20, 100), 2)  # Simulate ESG score calculation
        social_score = round(random.uniform(20, 100), 2)
        governance_score = round(random.uniform(20, 100), 2)

        total_esg_score = round((environmental_score + social_score + governance_score) / 3, 2)
        recommendations = generate_recommendations(environmental_score, social_score, governance_score)

        # Step 4: Update the ESG record
        esg_record.environmental_score = environmental_score
        esg_record.social_score = social_score
        esg_record.governance_score = governance_score
        esg_record.total_esg_score = total_esg_score
        esg_record.recommendations = recommendations
        esg_record.created_at = datetime.now()
        esg_record.save()

        # Return ESG data for the user
        return JsonResponse({
            'status': 'success',
            'user_id': user_id,
            'environmental_score': environmental_score,
            'social_score': social_score,
            'governance_score': governance_score,
            'total_esg_score': total_esg_score,
            'recommendations': recommendations
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})


# Helper function to generate ESG recommendations
def generate_recommendations(environmental_score, social_score, governance_score):
    recommendations = []

    if environmental_score < 50:
        recommendations.append("Improve waste management and carbon footprint.")

    if social_score < 50:
        recommendations.append("Enhance employee welfare and social responsibility.")

    if governance_score < 50:
        recommendations.append("Strengthen corporate governance and compliance.")

    if not recommendations:
        return "Company meets ESG standards."

    return " | ".join(recommendations)

# View to analyze historical trends for a specific user
def analyze_user_trends(request, user_id):
    try:
        # Step 1: Get the user from the database
        user = get_object_or_404(Users, id=user_id)

        # Step 2: Check if trends exist for the user
        trend_record, created = HistoricalTrends.objects.get_or_create(user=user, defaults={
            'year': str(datetime.now().year),
            'total_sales': None,
            'top_category': None,
            'campaign_performance': None,
            'created_at': datetime.now()
        })

        # Step 3: Generate simulated sales data for each month (Replace with real data later)
        years = list(range(2018, datetime.now().year + 1))
        sales_data = {str(year): round(random.uniform(5000, 50000), 2) for year in years}
        
        # Convert to DataFrame for analysis
        df = pd.DataFrame(list(sales_data.items()), columns=['year', 'sales'])
        df['year'] = df['year'].astype(int)
        df.set_index('year', inplace=True)

        # Step 4: Calculate simple moving average trend (Basic approach)
        df['sales_trend'] = df['sales'].rolling(window=2, min_periods=1).mean()

        # Step 5: Determine top category (Simulated)
        categories = ['Electronics', 'Fashion', 'Groceries', 'Sports']
        top_category = random.choice(categories)

        # Step 6: Simulate campaign performance (Replace with real campaign data)
        campaign_performance = {
            'Black Friday': round(random.uniform(5000, 20000), 2),
            'Christmas': round(random.uniform(7000, 25000), 2),
            'Summer Sale': round(random.uniform(4000, 15000), 2),
        }

        # Step 7: Save/update historical trend record
        trend_record.total_sales = df.to_dict()  # Store sales trend as JSON
        trend_record.top_category = top_category
        trend_record.campaign_performance = campaign_performance
        trend_record.created_at = datetime.now()
        trend_record.save()

        # Step 8: Return JSON response
        return JsonResponse({
            'status': 'success',
            'user_id': user_id,
            'yearly_sales': df.to_dict(),
            'top_category': top_category,
            'campaign_performance': campaign_performance
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
# View to analyze revenue trends for a specific user
def analyze_user_revenue(request, user_id):
    try:
        # Step 1: Get the user from the database
        user = get_object_or_404(Users, id=user_id)

        # Step 2: Check if revenue data exists for the user
        revenue_record, created = Revenue.objects.get_or_create(user=user, defaults={
            'date': datetime.now().date(),
            'gross_revenue': None,
            'net_revenue': None,
            'discounts_applied': None,
            'created_at': datetime.now()
        })

        # Step 3: Simulate revenue data (Replace with real data)
        num_days = 30  # Simulating for the last 30 days
        dates = [(datetime.now().date() - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(num_days)]
        
        # Generate random revenue data
        gross_revenue_data = {date: round(random.uniform(500, 5000), 2) for date in dates}
        discount_data = {date: round(random.uniform(10, 500), 2) for date in dates}
        net_revenue_data = {date: gross_revenue_data[date] - discount_data[date] for date in dates}

        # Convert to DataFrame for aggregation
        df = pd.DataFrame({
            'date': dates,
            'gross_revenue': list(gross_revenue_data.values()),
            'net_revenue': list(net_revenue_data.values()),
            'discounts_applied': list(discount_data.values()),
        })

        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Step 4: Calculate total revenue metrics
        total_gross_revenue = df['gross_revenue'].sum()
        total_net_revenue = df['net_revenue'].sum()
        total_discounts = df['discounts_applied'].sum()

        # Step 5: Store/update revenue record
        revenue_record.gross_revenue = gross_revenue_data
        revenue_record.net_revenue = net_revenue_data
        revenue_record.discounts_applied = discount_data
        revenue_record.created_at = datetime.now()
        revenue_record.save()

        # Step 6: Return JSON response
        return JsonResponse({
            'status': 'success',
            'user_id': user_id,
            'total_gross_revenue': total_gross_revenue,
            'total_net_revenue': total_net_revenue,
            'total_discounts': total_discounts,
            'daily_revenue_data': df.to_dict()
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
# View to forecast sales for a specific user
def forecast_user_sales(request, user_id):
    try:
        # Step 1: Get the user
        user = get_object_or_404(Users, id=user_id)

        # Step 2: Fetch user's past sales data
        revenue_record = Revenue.objects.filter(user=user).first()
        if not revenue_record or not revenue_record.gross_revenue:
            return JsonResponse({'status': 'error', 'message': 'No revenue data available for forecasting.'})

        # Convert JSON revenue data into a pandas DataFrame
        sales_data = revenue_record.gross_revenue
        df = pd.DataFrame(list(sales_data.items()), columns=['date', 'sales'])
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)

        # Step 3: Apply ARIMA model for forecasting
        df = df.asfreq('D')  # Ensure daily frequency
        df['sales'].fillna(method='ffill', inplace=True)  # Handle missing values

        # Define ARIMA model parameters
        model = ARIMA(df['sales'], order=(5, 1, 0))  # ARIMA(p=5, d=1, q=0)
        model_fit = model.fit()

        # Forecast sales for the next 30 days
        forecast_period = 30
        forecast_dates = [df.index[-1] + timedelta(days=i) for i in range(1, forecast_period + 1)]
        forecast_values = model_fit.forecast(steps=forecast_period)

        # Convert forecast into a dictionary
        forecast_data = {str(date.date()): round(value, 2) for date, value in zip(forecast_dates, forecast_values)}

        # Step 4: Store/update forecast record
        forecast_record, created = SalesForecasts.objects.get_or_create(
            user=user,
            forecast_period="30 days",
            defaults={'predicted_sales': forecast_data, 'created_at': datetime.now()}
        )
        forecast_record.predicted_sales = forecast_data
        forecast_record.created_at = datetime.now()
        forecast_record.save()

        # Step 5: Return JSON response
        return JsonResponse({
            'status': 'success',
            'user_id': user_id,
            'forecast_period': '30 days',
            'predicted_sales': forecast_data
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
# Download NLTK resources (first-time setup)
nltk.download('vader_lexicon')

# Initialize Sentiment Intensity Analyzer
sia = SentimentIntensityAnalyzer()

def analyze_user_sentiment(request, user_id):
    try:
        # Step 1: Get the user
        user = get_object_or_404(Users, id=user_id)

        # Step 2: Retrieve user's reviews (Assuming reviews come from an external source)
        # Replace this with real review-fetching logic (e.g., from a database or API)
        user_reviews = [
            "This product is amazing! I love it.",
            "It's okay, nothing special.",
            "Worst experience ever. I regret buying this."
        ]

        if not user_reviews:
            return JsonResponse({'status': 'error', 'message': 'No reviews available for analysis.'})

        # Step 3: Perform sentiment analysis
        positive_reviews = []
        neutral_reviews = []
        negative_reviews = []

        for review in user_reviews:
            score = sia.polarity_scores(review)['compound']
            if score >= 0.05:
                positive_reviews.append(review)
            elif score <= -0.05:
                negative_reviews.append(review)
            else:
                neutral_reviews.append(review)

        # Prepare JSON-storable data
        sentiment_data = {
            'total_reviews': len(user_reviews),
            'positive_reviews': positive_reviews,
            'neutral_reviews': neutral_reviews,
            'negative_reviews': negative_reviews,
            'created_at': datetime.now().isoformat()
        }

        # Step 4: Store/update sentiment record
        sentiment_record, created = SentimentAnalysis.objects.get_or_create(
            user=user,
            defaults={
                'total_reviews': json.dumps(len(user_reviews)),
                'positive_reviews': json.dumps(positive_reviews),
                'neutral_reviews': json.dumps(neutral_reviews),
                'negative_reviews': json.dumps(negative_reviews),
                'created_at': datetime.now()
            }
        )
        sentiment_record.total_reviews = json.dumps(len(user_reviews))
        sentiment_record.positive_reviews = json.dumps(positive_reviews)
        sentiment_record.neutral_reviews = json.dumps(neutral_reviews)
        sentiment_record.negative_reviews = json.dumps(negative_reviews)
        sentiment_record.created_at = datetime.now()
        sentiment_record.save()

        # Step 5: Return JSON response
        return JsonResponse({
            'status': 'success',
            'user_id': user_id,
            'sentiment_analysis': sentiment_data
        })

    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
    
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from datetime import timedelta, datetime
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from .models import Products, StockForecasts

def forecast_stock(request):
    try:
        # Step 1: Fetch product data from the Products table
        products = Products.objects.all()  # You can filter based on conditions if necessary
        forecasts = []

        for product in products:
            # Example: Assume 'stock_quantity' field has time-series data
            stock_data = product.stock_quantity  # This should ideally be a time series (date and quantity)

            if stock_data:  # Only proceed if there is data
                # Convert stock quantity into a pandas DataFrame (if it's not already)
                stock_df = pd.DataFrame(stock_data)  # Assuming stock_data is a list of dictionaries or JSON objects
                stock_df['date'] = pd.to_datetime(stock_df['date'])
                stock_df = stock_df.rename(columns={'date': 'ds', 'quantity': 'y'})  # Prophet requires 'ds' for date and 'y' for values

                # Step 2: Use ARIMA to forecast the demand
                model = ARIMA(stock_df['y'], order=(5, 1, 0))  # ARIMA(p=5, d=1, q=0)
                model_fit = model.fit()

                # Forecast for the next 30 days
                forecast_period = 30
                forecast_values = model_fit.forecast(steps=forecast_period)
                forecast_dates = [stock_df['ds'].max() + timedelta(days=i) for i in range(1, forecast_period + 1)]

                # Step 3: Prepare forecast data
                forecast_data = {
                    'product_id': product.id,
                    'forecast_period': '30 days',
                    'forecast_dates': [date.date().isoformat() for date in forecast_dates],
                    'forecast_values': [round(value, 2) for value in forecast_values]
                }
                forecasts.append(forecast_data)

        # Step 4: Return JSON response
        return JsonResponse({'status': 'success', 'forecasts': forecasts})

    except Exception as e:
        # Handle exceptions and return error message
        return JsonResponse({'status': 'error', 'message': str(e)})

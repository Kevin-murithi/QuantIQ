from django.urls import path
from . import views

urlpatterns = [
    path('detect-anomalies/<int:user_id>/', views.detect_user_anomalies, name='detect_anomalies'),
    path('calculate-clv/<int:user_id>/', views.calculate_user_clv, name='calculate_clv'),
    path('customer-segmentation/<int:user_id>/', views.calculate_user_segmentation, name='customer_segmentation'),
    path('calculate-esg/<int:user_id>/', views.calculate_user_esg, name='calculate_user_esg'),
    path('analyze-trends/<int:user_id>/', views.analyze_user_trends, name='analyze_user_trends'),
    path('analyze-revenue/<int:user_id>/', views.analyze_user_revenue, name='analyze_user_revenue'),
     path('analyze-sentiment/<int:user_id>/', views.analyze_user_sentiment, name='analyze_user_sentiment'),
     path('forecast/', views.forecast_stock, name='forecast_stock'),
]

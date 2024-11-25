# Airbnb price prediction

## Problem description

> Can we predict prices of airbnb listings based on their features?

The short answer is YES. To prove it I trained a Machine Learning Model using data from five U.S. cities:
- Los Angeles, California
- San Diego, California
- Chicago, Illinois
- Austin, Texas
- Dallas, Texas 

Here's an example of a listing that the model is able to predict its price:
```
new_data = {
    'host_response_rate': 92.0,
    'host_acceptance_rate': 99.0,
    'latitude': 33.75747,
    'longitude': -118.1309,
    'accommodates': 4,
    'bathrooms': 1.0,
    'bedrooms': 1.0,
    'beds': 2.0,
    'minimum_nights': 1,
    'maximum_nights': 30,
    'availability_30': 6,
    'availability_60': 28,
    'availability_90': 58,
    'availability_365': 148,
    'number_of_reviews': 530,
    'number_of_reviews_ltm': 81,
    'number_of_reviews_l30d': 4,
    'review_scores_rating': 4.87,
    'review_scores_accuracy': 4.92,
    'review_scores_cleanliness': 4.9,
    'review_scores_checkin': 4.82,
    'review_scores_communication': 4.87,
    'review_scores_location': 4.93,
    'review_scores_value': 4.73,
    'calculated_host_listings_count': 1,
    'calculated_host_listings_count_entire_homes': 1,
    'calculated_host_listings_count_private_rooms': 0,
    'calculated_host_listings_count_shared_rooms': 0,
    'reviews_per_month': 7.63,
    'host_is_superhost_flag': 1,
    'host_has_profile_pic_flag': 1,
    'host_identity_verified_flag': 1,
    'has_availability_flag': 1,
    'instant_bookable_flag': 1,
    'host_email_verified_flag': 1,
    'host_phone_verified_flag': 1,
    'host_work_email_verified_flag': 0,
    'host_response_time': 'within an hour',
    'property_type': 'entire rental unit',
    'room_type': 'entire home/apt',
    'state': 'california',
    'city': 'los angeles'
}
```
I used datasets from the official airbnb data repository: https://insideairbnb.com/get-the-data/

These datasets have many features that can be used to train models but I only selected some of them for this version. The full dictionary of these datasets can be viewed in `data/raw/Inside Airbnb Data Dictionary.xlsx`

## Quickstart

1. Clone the repository in a desired directory
    ```
    mkdir airbnb-price-prediction
    cd airbnb-price-prediction
    git clone https://github.com/ayar-yps/airbnb-price-prediction.git .
    ```
1. Install dependencies
    ```
    pip install pipenv  #--(Only if not installed already)
    pipenv install
    ```
1. Test the prediction service locally
    ```
    bash build-and-local-deploy.sh
    python tests/test_predict.py --host localhost:9696
    ```

## Test the prediction service on AWS
1. Login to AWS using AWS CLI
1. Create an environment variable for you profile
    ```
    export AWS_EB_PROFILE=XXXXXXXXXXXXX
    ```
1. Deploy the service
    ```
    bash aws-deploy.sh
    ```
1. Test the prediction service on AWS. Replace `<domain>` with the output domain after deployment
    ```
    python tests/test_predict.py --host <domain>
    ```
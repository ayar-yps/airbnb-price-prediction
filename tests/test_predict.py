import requests
import logging
import sys
import argparse

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO,
    format='%(asctime)s -  %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name='test')

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, required=True)
args = parser.parse_args()

host = args.host
predict_url = f"http://{host}/predict"

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

logger.info(f"host: {host}")
logger.info(f"new_data:\n{new_data}\n")

prediction_resp = requests.post(predict_url, json=new_data).json()

logger.info(prediction_resp)
#-------------------
# 1. Import modules
#-------------------

import pandas as pd
import numpy as np

from sklearn.preprocessing import TargetEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction import DictVectorizer

from sklearn.ensemble import RandomForestRegressor

import pickle
import logging
import sys

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO,
    format='%(asctime)s -  %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name='train')


#---------------------
# 2. Define functions
#---------------------

def closed_range(start, stop, step=1):
    if step - round(step) == 0:
        aux_delta = 1 if step > 0 else -1
        return [*range(start, stop + aux_delta, step)]
    else:
        aux_delta = step/100
        step_decimal_places = len(str(step).split(".")[1])
        return np.round(np.arange(start, stop + aux_delta, step), step_decimal_places).tolist()


#-------------------------
# 3. Define main function
#-------------------------

def main():

    #------------------
    # 3.1 Prepare data
    #------------------
    
    train_data = pd.read_csv("../data/clean/train.csv")
    X_train, y_train = train_data.loc[:,[col for col in train_data.columns if col != 'price']], train_data['price']

    # Apply missing values imputation and target encoding
    nm_features = X_train.select_dtypes(include=['int64', 'float64']).columns.tolist()
    ct_features = X_train.select_dtypes(include=['object']).columns.tolist()
    features_to_target_encode = ['property_type']

    nm_missing_values_imputer = SimpleImputer(missing_values=np.nan, strategy='median')
    ct_missing_values_imputer = SimpleImputer(missing_values=np.nan, strategy='constant', fill_value='none')

    target_encoder = TargetEncoder(target_type='continuous')

    column_transformer_missing_imputation = ColumnTransformer(
        transformers=[
            ('nm_missing_values_imputer', nm_missing_values_imputer,
            nm_features),
            ('ct_missing_values_imputer', ct_missing_values_imputer,
            [feature for feature in ct_features if feature not in features_to_target_encode]),
        ],
        remainder='passthrough',
        verbose_feature_names_out=False)

    column_transformer_target_encoding = ColumnTransformer(
        transformers=[
            ('target_encoder',
            target_encoder,
            slice(-1, None)),
        ],
        remainder='passthrough',
        verbose_feature_names_out=False)

    transformer_pipeline = Pipeline(
        steps=[
            ('column_transformer_missing_imputation', column_transformer_missing_imputation),
            ('column_transformer_stage_2', column_transformer_target_encoding)
        ]
    )

    X_train_t = transformer_pipeline.fit_transform(X_train, y_train) 
    X_train_t = pd.DataFrame(X_train_t,columns=transformer_pipeline.get_feature_names_out())

    # Use dict vectorizer to apply one hot encoding
    dict_vectorizer = DictVectorizer(sparse=False)
    X_train_t = dict_vectorizer.fit_transform(X_train_t.to_dict(orient='records'))
    X_train_t = pd.DataFrame(X_train_t, columns=dict_vectorizer.get_feature_names_out())

    logger.info(">> main: Prepare data finished (1/2)")

    #-----------------
    # 3.2 Train model
    #-----------------

    rf_model = RandomForestRegressor(
        n_estimators=50,
        min_samples_split=10,
        min_samples_leaf=4,
        max_depth=30)

    rf_model.fit(X_train_t.values, np.log10(y_train))

    logger.info(">> main: Train model finished (2/2")

    return transformer_pipeline, dict_vectorizer, rf_model


#------------------
# 4. Main function
#------------------

if __name__ == "__main__":

    transformer_pipeline, dict_vectorizer, rf_model = main()

    with open('./artifacts/transformer_pipeline.pkl', 'wb') as tp_f:
        pickle.dump(transformer_pipeline, tp_f)
    logger.info(">> transformer_pipeline saved")

    with open('./artifacts/dict_vectorizer.pkl', 'wb') as dv_f:
        pickle.dump(transformer_pipeline, dv_f)
    logger.info(">> dict_vectorizer saved")

    with open('./artifacts/rf_model.pkl', 'wb') as rfm_f:
        pickle.dump(rf_model, rfm_f)
    logger.info(">> rf_model saved")

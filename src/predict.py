#-------------------
# 1. Import modules
#-------------------

import pandas as pd
import pickle
import logging
import sys
from flask import Flask, request, jsonify


#---------------------
# 2. Setup
#---------------------

logging.basicConfig(
    stream=sys.stdout, level=logging.INFO,
    format='%(asctime)s -  %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(name='predict')

app = Flask('predict')

with\
    open('./artifacts/transformer_pipeline.pkl', 'rb') as tp_f,\
    open('./artifacts/dict_vectorizer.pkl', 'rb') as dv_f,\
    open('./artifacts/rf_model.pkl', 'rb') as rfm_f:

    transformer_pipeline = pickle.load(tp_f)
    dict_vectorizer = pickle.load(dv_f)
    rf_model = pickle.load(rfm_f)


#---------------------
# 3. Define functions
#---------------------

def predict(new_data: pd.DataFrame) -> float:
    
    X_data = transformer_pipeline.transform(new_data)
    X_data = pd.DataFrame(X_data, columns=transformer_pipeline.get_feature_names_out())

    X_data = dict_vectorizer.transform(X_data.to_dict(orient='records'))
    X_data = pd.DataFrame(X_data, columns=dict_vectorizer.get_feature_names_out())

    y_pred = rf_model.predict(X_data.values)[0]

    y_pred_t = float(10 ** y_pred)

    return y_pred_t

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    
    new_data = request.get_json()
    new_data = pd.DataFrame([new_data])
    logger.info(f"new_data:\n{new_data.to_dict(orient='records')}\n")
    
    prediction = predict(new_data)
    logger.info(f"prediction: {prediction}")
    
    result = {
        'prediction': prediction
    }
    
    return jsonify(result)


#------------------------------
# 4. Run in development mode
#------------------------------

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=9696)
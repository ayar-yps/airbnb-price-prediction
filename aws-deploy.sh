echo "*************************"
echo "DEPLOY ON AWS FOR TESTING"
echo "*************************"
echo ">> After running successfully, execute: python tests/test_predict.py --host <domain>"
eb init -p docker -r us-east-1 airbnb-price-prediction
eb create airbnb-price-prediction-env --enable-spot
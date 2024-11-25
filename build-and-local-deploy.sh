echo "******************"
echo "BUILD CUSTOM IMAGE"
echo "******************"
docker build -t airbnb-price-prediction .

echo "************************"
echo "DEPLOY FOR LOCAL TESTING"
echo "************************"
echo ">> After running successfully, execute: python tests/test_predict.py --host localhost:9696"
docker run -it --rm -p 9696:9696 airbnb-price-prediction
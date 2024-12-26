git clone https://github.com/openai/shap-e.git .
mv modeling.py ./shap_e/examples/
python3 ./setup.py install
pip install -r requirements.txt
flask --app main run
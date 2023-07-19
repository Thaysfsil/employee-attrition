#Install Libraries
from flask import Flask, request, jsonify
import pandas as pd
import cloudpickle
import os, sys
import traceback

#external config
PATH_PROCESS = os.environ.get('PATH_PROCESS')
PATH_MODEL = os.environ.get('PATH_MODEL')


app = Flask(__name__)
@app.route("/prediction", methods=["POST"])
#define function
def predict():
    if model and preprocessing:
        try:
            json_ = request.json
            data = pd.DataFrame(json_, index=[0])
            processed = preprocessing.transform(data)
            predict = model.predict(processed)
            predict_proba = model.predict_proba(processed)
            return jsonify({"Prediction": str(predict),
            "probability": str(predict_proba) })
        except:
            return jsonify({"trace": traceback.format_exc()})
    else:
        return ("unable to load model")


if __name__ == "__main__":
    try:
        port = int(sys.argv[1])
    except:
        port = 12345 
    with open(PATH_PROCESS, "rb") as f:
        preprocessing = cloudpickle.load(f)
    print("loaded preprocessing")
    with open(PATH_MODEL, "rb") as f:
        model = cloudpickle.load(f) 
    print("loaded model")
    app.run(port=port, debug=True)
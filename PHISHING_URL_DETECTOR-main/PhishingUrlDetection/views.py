from flask import Blueprint, render_template,request
from flask_login import login_required, current_user
import joblib
from website.model import Url_features
import os
views = Blueprint('views',__name__)


model_path = os.path.join(os.path.dirname(__file__),'model','Random Forest_model.pkl')
mlmodel = joblib.load(model_path)


@views.route('/')
@login_required
def home():
    return render_template("home.html",user=current_user)

@views.route('/predict',methods=['GET','POST'])

def predicts():
    if request.method == 'GET':
        return render_template('predict.html')
    if request.method=='POST':
        url = request.form.get("url")
        features = Url_features.extract_features(url)
        prediction = mlmodel.predict([features])
        prediction_proba = mlmodel.predict_proba([features])[0][1]  # Probability of being phishing
        result = 'Phishing' if prediction[0] == 1 else 'Legitimate'
        confidence_percentage = round(prediction_proba * 100, 2)
        return render_template('result.html', result=result, confidence=confidence_percentage)



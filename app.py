from flask import Flask, request
import joblib
import pandas as pd
python
import google.generativeai as genai

# Configure your Gemini AI
genai.configure(api_key="AQ.Ab8RN6IEqoxkBhAmqFFwmzC0k7fhXCdI5AO1fDAtRx8pNHEqeQ")
model_ai = genai.GenerativeModel('gemini-1.5-flash')

app = Flask(__name__)

# Load the three models into the server's memory
model_capacity = joblib.load('xgb_capacity.pkl')
model_heat = joblib.load('xgb_heat.pkl')
model_selectivity = joblib.load('xgb_selectivity.pkl')

# A simple test page to make sure the server is awake
@app.route('/')
def home():
    return "Project P.H.O.E.N.I.X. API is live and running!"

# The actual endpoint MIT App Inventor will talk to
@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        # Catch the variables MIT App Inventor sends in the URL
        pld = float(request.args.get('pld'))
        sa = float(request.args.get('sa'))
        vf = float(request.args.get('vf'))

        # Format them for XGBoost
        input_data = pd.DataFrame({'PLD': [pld], 'SA': [sa], 'VF': [vf]}).values

        # Make predictions and round to 2 decimal places
        cap = round(float(model_capacity.predict(input_data)[0]), 2)
        heat = round(float(model_heat.predict(input_data)[0]), 2)
        sel = round(float(model_selectivity.predict(input_data)[0]), 2)

        # Return the pure comma-separated string back to the app
        return f"{cap},{heat},{sel}"

    except Exception as e:
        return f"Error: {str(e)}"

python
@app.route('/ask-gemini', methods=['POST'])
def ask_gemini():
    try:
        spoken_question = request.data.decode('utf-8')
        prompt = f"You are PHOENIX, an AI chemistry assistant. Answer this briefly: {spoken_question}"
        response = model_ai.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

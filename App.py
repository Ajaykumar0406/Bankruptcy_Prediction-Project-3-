# -*- coding: utf-8 -*-
"""Untitled75.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1eh2naKHPCRVwd4BxWKrOIp-XrT6ygKCX
"""

import streamlit as st
import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix, roc_auc_score
import joblib

# Load and preprocess the data
def load_data():
    file_path = r"C:\Users\akura\OneDrive\Desktop\bankruptcy-prevention (1).xlsx"
    data = pd.read_excel(file_path, sheet_name='bankruptcy-prevention', engine='openpyxl')

    # Check if the first column is of type string, if not convert it to string
    if data.iloc[:, 0].dtype != object:
        data.iloc[:, 0] = data.iloc[:, 0].astype(str)

    data_split = data.iloc[:, 0].str.split(';', expand=True)

    if data_split.shape[1] != 7:
        st.error(f"Expected 7 columns after split, but got {data_split.shape[1]}. Please check the data format.")
        st.stop()

    data_split.columns = ["industrial_risk", "management_risk", "financial_flexibility",
                          "credibility", "competitiveness", "operating_risk", "class"]

    # Convert data types
    data_split['industrial_risk'] = data_split['industrial_risk'].astype(float)
    data_split['management_risk'] = data_split['management_risk'].astype(float)
    data_split['financial_flexibility'] = data_split['financial_flexibility'].astype(float)
    data_split['credibility'] = data_split['credibility'].astype(float)
    data_split['competitiveness'] = data_split['competitiveness'].astype(float)
    data_split['operating_risk'] = data_split['operating_risk'].astype(float)
    data_split['class'] = data_split['class'].map({'non-bankruptcy': 0, 'bankruptcy': 1})

    return data_split

# Train and save the model
def train_and_save_model(data):
    X = data.drop('class', axis=1)
    y = data['class']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    xgb_model = xgb.XGBClassifier(random_state=42)
    xgb_model.fit(X_train, y_train)

    # Save the model
    joblib.dump(xgb_model, 'xgboost_model.pkl')

    y_pred_xgb = xgb_model.predict(X_test)
    y_pred_prob_xgb = xgb_model.predict_proba(X_test)[:, 1]

    return xgb_model, y_pred_xgb, y_pred_prob_xgb, y_test

# Load the model
def load_model():
    model = joblib.load('xgboost_model.pkl')
    return model

# Make predictions
def predict_bankruptcy(model, features):
    df = pd.DataFrame([features], columns=[
        'industrial_risk', 'management_risk', 'financial_flexibility',
        'credibility', 'competitiveness', 'operating_risk'
    ])
    prediction = model.predict(df)
    return prediction[0]

# Main Streamlit app
def main():
    st.title("Bankruptcy Prediction Model")

    # Load and preprocess data
    data = load_data()
    train_and_save_model(data)

    # Load the trained model
    model = load_model()

    # Create input fields for the features
    industrial_risk = st.selectbox("Industrial Risk", [0, 0.5, 1])
    management_risk = st.selectbox("Management Risk", [0, 0.5, 1])
    financial_flexibility = st.selectbox("Financial Flexibility", [0, 0.5, 1])
    credibility = st.selectbox("Credibility", [0, 0.5, 1])
    competitiveness = st.selectbox("Competitiveness", [0, 0.5, 1])
    operating_risk = st.selectbox("Operating Risk", [0, 0.5, 1])

    # Create a button to make predictions
    if st.button("Predict Bankruptcy"):
        features = [
            industrial_risk, management_risk, financial_flexibility,
            credibility, competitiveness, operating_risk
        ]
        prediction = predict_bankruptcy(model, features)
        st.write(f"The predicted class is: {'Bankruptcy' if prediction == 1 else 'Non-Bankruptcy'}")

if __name__ == "__main__":
    main()








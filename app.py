from flask import Flask, render_template, request, redirect, url_for
import os
import pandas as pd
import joblib  # Import joblib to load the trained model
from model import train_model  # Import train_model function to load the model

app = Flask(__name__)

# Load the dataset
data = pd.read_csv("C:/Users/bhavy/OneDrive/Desktop/TravelVista/data/Top Indian Places to Visit.csv")

# Load the trained model
model_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "model.pkl")
model = joblib.load(model_file_path)

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Get user input from the form
        query = request.form['search_query']
        # Implement search logic based on user query
        # Here, you can use the dataset directly to find the attraction
        # For simplicity, let's assume we directly use the sample data
        attraction = data[data['Name'].str.lower() == query.lower()].iloc[0].to_dict() if not data[data['Name'].str.lower() == query.lower()].empty else None
        if attraction:
            return redirect(url_for('attraction_info', attraction_name=attraction['Name']))
        else:
            return render_template('no_search_found.html')
    return render_template('index.html')

@app.route('/recommendations', methods=['GET', 'POST'])
def recommendations():
    if request.method == 'POST':
        # Get user preferences from the form
        # Note: You can add more fields as needed for preferences
        city = request.form['city']
        state = request.form['state']
        type=request.form['type']

        # Initialize filtered data with the full dataset
        filtered_data = data
        
        # Apply filtering based on user preferences
        if city:
            filtered_data = filtered_data[filtered_data['City'].str.lower() == city.lower()]
        if state:
            filtered_data = filtered_data[filtered_data['State'].str.lower() == state.lower()]
        if type:
            filtered_data = filtered_data[filtered_data['Type'].str.lower() == type.lower()]
        
        
        if not filtered_data.empty:
            # Use the trained model to make predictions
            predictions = model.predict(filtered_data)  # Assuming the model predicts the best time to visit
            # Add the predictions to the filtered data
            filtered_data['Predicted_Best_Time'] = predictions
            
            # Convert filtered data to dictionary format for rendering
            recommendations = filtered_data.to_dict(orient='records')
            return render_template('recommendations.html', recommendations=recommendations)
    
    return render_template('recommendations.html', recommendations=[])

@app.route('/attraction_info/<attraction_name>')
def attraction_info(attraction_name):
    # Retrieve attraction information based on the attraction name
    # Here, we'll use the sample data
    attraction = data[data['Name'].str.lower() == attraction_name.lower()].iloc[0].to_dict() if not data[data['Name'].str.lower() == attraction_name.lower()].empty else None
    if attraction:
        return render_template('attraction_info.html', attraction=attraction)
    else:
        return render_template('no_search_found.html')

if __name__ == '__main__':
    app.run(debug=True)

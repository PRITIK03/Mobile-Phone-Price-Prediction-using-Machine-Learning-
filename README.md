# Mobile Phone Price Prediction using Machine Learning

This project is a web application that predicts the price range of mobile phones based on various features using machine learning models.

## Features
- Predicts mobile phone price range from user input features
- Interactive web interface (Flask)
- Uses a trained machine learning model
- Data visualization and summary statistics
- CSV data file for training and testing

## Project Structure
```
├── app.py                # Main Flask application
├── main.py               # Model training and prediction logic
├── phones_data.csv       # Dataset used for training
├── models/               # Saved machine learning models
├── templates/
│   └── index.html        # Web interface template
```

## How to Run
1. **Clone the repository:**
   ```bash
   git clone https://github.com/PRITIK03/Mobile-Phone-Price-Prediction-using-Machine-Learning-.git
   cd Mobile-Phone-Price-Prediction-using-Machine-Learning-
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```bash
   python app.py
   ```
4. **Open your browser:**
   Go to `http://127.0.0.1:5000/`

## Requirements
- Python 3.7+
- Flask
- scikit-learn
- pandas
- (See `requirements.txt` for full list)

## Usage
- Enter the required features in the web form.
- Click 'Predict' to see the predicted price range.

## Possible Improvements
- Add user authentication
- Support for batch predictions (CSV upload)
- Model explainability (feature importance)
- REST API endpoint
- Enhanced UI/UX

## License
This project is licensed under the MIT License.

## Author
- [PRITIK03](https://github.com/PRITIK03)

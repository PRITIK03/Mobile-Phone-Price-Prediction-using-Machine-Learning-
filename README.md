
# Mobile Phone Price Prediction using Machine Learning

This project is a full-stack web application that predicts the price range of mobile phones using machine learning. It features a Flask backend (with authentication, REST API, and model serving) and a modern React frontend for user interaction.

---

## Features

- **Price Prediction:** Predicts mobile phone price range from user input features using a trained ML model.
- **User Authentication:** Register and login with secure JWT-based authentication.
- **Interactive UI:** Modern React frontend with Material UI, protected routes, and notifications.
- **Dashboard:** View model metrics and summary statistics (placeholder for future enhancements).
- **Prediction History:** (Frontend demo) See previous predictions (can be extended to real backend history).
- **REST API:** Flask backend exposes endpoints for prediction, registration, and login.
- **Data Visualization:** (Planned) Add charts and feature importance.

---

## Project Structure

```
├── app.py                # Flask backend: API, auth, model serving
├── main.py               # Model training and serialization
├── phones_data.csv       # Dataset for training
├── requirements.txt      # Python dependencies
├── models/               # Saved ML models (regressor.pkl, classifier.pkl, label_encoder.pkl)
├── templates/
│   └── index.html        # (Legacy) Flask template
├── predict_utils.py      # Prediction helpers: caching, mock predictions
├── frontend/             # (Legacy/minimal) React app
├── react/
│   └── frontend/         # Main React app (modern UI)
│       ├── src/
│       │   ├── components/   # Navbar, AuthForm, NotificationProvider, ProtectedRoute
│       │   ├── pages/        # Dashboard, LoginPage, RegisterPage, PredictionForm
│       │   └── App.js        # Main React app entry
│       ├── public/           # Static assets
│       └── package.json      # React dependencies
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/PRITIK03/Mobile-Phone-Price-Prediction-using-Machine-Learning-.git
cd Mobile-Phone-Price-Prediction-using-Machine-Learning-
```

### 2. Backend Setup (Flask API)

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Run the Flask server:

```bash
python app.py
```

The API will be available at `http://localhost:5000/`.

### 3. Frontend Setup (React App)

Navigate to the React frontend directory:

```bash
cd react/frontend
npm install
npm start
```

The React app will run at `http://localhost:3000/` and communicate with the Flask backend.

---

## Usage

1. **Register** a new user or **login** with existing credentials.
2. Go to the **Predict** page, enter mobile features (battery size, brand, memory, etc.), and submit.
3. View the predicted price range instantly.
4. Access the **Dashboard** (after login) for model info (future: metrics, charts).
5. (Optional) Extend the app to store and display real prediction history per user.

### Mock mode (useful when model files are missing)

If you don't have the trained model files in `models/`, the backend will run in a lightweight mock mode that produces deterministic, plausible predictions for testing. To force mock mode set the environment variable `MOCK_MODE=1`. To disable mock mode and require real models set `MOCK_MODE=0`.

Example (PowerShell):

```powershell
setx MOCK_MODE 1
python app.py
```

Batch prediction example (uses sample CSV at `examples/phones_sample.csv`):

```powershell
# start the server first
curl -F "file=@examples/phones_sample.csv" http://127.0.0.1:5000/api/predict/batch -o predictions.csv
```

## Code modularization

I refactored some helper logic into `predict_utils.py` to keep `app.py` focused on the Flask app and routing. Highlights:

- `predict_utils.py`: contains caching helpers (`get_cache_key`, `get_cached_prediction`, `cache_prediction`), a lightweight `mock_predict_single()` for development without model files, and the in-memory `prediction_cache`.
- `app.py`: remains the application entrypoint and defines DB models, routes, authentication, and uses helpers from `predict_utils.py`.

This separation makes it easier to test prediction logic independently and to replace the cache with Redis or another store later.

---

## API Endpoints (Flask)

- `POST /api/register` — Register a new user
- `POST /api/login` — Login and receive JWT token
- `POST /api/predict` — Predict price range (requires input features)

---

## Requirements

- Python 3.7+
- Flask, Flask-CORS, Flask-JWT-Extended, Flask-Bcrypt, Flask-SQLAlchemy
- scikit-learn, pandas, numpy
- Node.js & npm (for React frontend)
- See `requirements.txt` and `react/frontend/package.json` for full lists

---

## Possible Improvements

- Store and display real prediction history per user
- Add model explainability (feature importance, SHAP)
- Batch predictions (CSV upload)
- Enhanced dashboard with charts and metrics
- Dockerize for easy deployment
- Add unit and integration tests

---

## License

This project is licensed under the MIT License.

## Author

- [PRITIK03](https://github.com/PRITIK03)

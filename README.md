# Mobile Phone Price Prediction using Machine Learning

This project is a full-stack web application that predicts the price range of mobile phones using machine learning. The backend is now modularized into focused Flask modules, and the main user experience is a polished dashboard-style UI with single prediction and batch CSV upload support.

---

## Features

- **Price Prediction:** Predicts mobile phone price range from user input features using a trained ML model or mock mode when model files are missing.
- **User Authentication:** Register and login with secure JWT-based authentication.
- **Modern UI:** Responsive glassmorphism-style dashboard with clean cards, charts, and a better visual hierarchy.
- **Batch Upload:** Upload a CSV and download predictions with enriched output columns.
- **Prediction History:** Store prediction history in the database for authenticated users.
- **REST API:** Flask backend exposes endpoints for prediction, registration, login, history, comparison, and health checks.
- **Redis-Ready Cache:** Optional Redis-backed prediction cache with in-memory fallback.

---

## Project Structure

```text
├── app.py                # Thin Flask bootstrapper
├── app_factory.py        # App factory, model loading, extension wiring
├── extensions.py         # Shared Flask extension instances
├── models.py             # Database models
├── auth_routes.py        # Authentication endpoints
├── prediction_routes.py  # Prediction, compare, and batch endpoints
├── utility_routes.py     # Health, history, and stats endpoints
├── web_routes.py         # Homepage route
├── routes.py             # Compatibility shim for blueprint imports
├── predict_utils.py      # Prediction helpers, cache, Redis fallback, mock mode
├── main.py               # Model training and serialization
├── phones_data.csv       # Dataset for training
├── requirements.txt      # Python dependencies
├── models/               # Saved ML models (regressor.pkl, classifier.pkl, label_encoder.pkl)
├── templates/
│   └── index.html        # Modern dashboard UI
├── examples/
│   └── phones_sample.csv # Sample CSV for batch predictions
├── react/
│   └── frontend/         # Additional React frontend work-in-progress
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

### 3. Frontend Setup (optional React app)

The polished primary interface is the Flask dashboard. The React frontend remains available for experimentation in `react/frontend`.

```bash
cd react/frontend
npm install
npm start
```

---

## Usage

1. Register a new user or login with existing credentials.
2. Use the homepage form to enter battery size, brand, and memory.
3. Upload a CSV for batch predictions if you want multiple rows processed at once.
4. Review the result cards and charts rendered on the page.
5. Access the API endpoints directly if you want to integrate another client.

---

## Mock Mode

If the trained model files are missing from `models/`, the backend can run in mock mode so the UI remains usable for demos and development.

Set `MOCK_MODE=1` to force mock predictions or `MOCK_MODE=0` to require the real model files.

PowerShell example:

```powershell
setx MOCK_MODE 1
python app.py
```

Batch prediction example using the sample CSV:

```powershell
curl -F "file=@examples/phones_sample.csv" http://127.0.0.1:5000/api/predict/batch -o predictions.csv
```

---

## Code Modularization

The backend is split into focused modules:

- `app.py`: thin bootstrapper.
- `app_factory.py`: builds the Flask app, loads models, and registers blueprints.
- `extensions.py`: shared Flask extension instances.
- `models.py`: database models only.
- `auth_routes.py`: registration and login.
- `prediction_routes.py`: prediction, comparison, and batch upload.
- `utility_routes.py`: health check, history, stats, and delete endpoints.
- `web_routes.py`: homepage rendering.
- `routes.py`: compatibility shim that re-exports the blueprints.
- `predict_utils.py`: cache helpers, Redis fallback, and mock prediction logic.

This separation makes the code easier to maintain, test, and extend.

---

## API Endpoints

- `POST /api/register` - Register a new user
- `POST /api/login` - Login and receive JWT token
- `POST /api/predict` - Predict price range
- `POST /api/predict/batch` - Batch CSV predictions
- `POST /api/compare` - Compare multiple phones
- `GET /api/health` - Health check
- `GET /api/predictions/history` - User history
- `GET /api/predictions/stats` - Prediction statistics

---

## Requirements

- Python 3.7+
- Flask, Flask-CORS, Flask-JWT-Extended, Flask-Bcrypt, Flask-SQLAlchemy
- scikit-learn, pandas, numpy, redis
- Node.js & npm for the optional React frontend

---

## Possible Improvements

- Add more charts and trend summaries to the dashboard
- Add automated tests for API routes and UI rendering
- Dockerize the application for deployment
- Add feature importance or SHAP explanations

---

## License

This project is licensed under the MIT License.

## Author

- [PRITIK03](https://github.com/PRITIK03)

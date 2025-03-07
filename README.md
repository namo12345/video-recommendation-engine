# Video Recommendation Engine

Hey folks! This is my Video Recommendation Engine—a project I built to suggest personalized videos, drawing inspiration from the motivational vibes of the Empowerverse app ([Android](https://play.google.com/store/apps/details?id=com.empowerverse.app) | [iOS](https://apps.apple.com/us/app/empowerverse/id6449552284)). It’s powered by FastAPI and a neural network (mocked for now), pulling data from the Socialverse API.

## Project Overview

The objective of this project is to develop a recommendation system that:
- Provides video recommendations based on users' viewing history, likes, and ratings.
- Assists new users (cold-start users) by displaying all available posts and exploring innovative features like mood-based selections.
- Utilizes a deep neural network to analyze data (currently implemented with placeholder data).
- Integrates with the Socialverse API to access real-world engagement metrics.
- Ensures a seamless user experience by incorporating pagination.

While the system is still in development, it serves as a promising foundation for future enhancements.

## Technology Stack

- **Backend**: FastAPI (love how fast it is!)
- **Machine Learning**: TensorFlow (supplemented with NumPy and Pandas for data manipulation and analysis)
- **API Testing**: Postman
- **Migrations**: Alembic (setting up for a database later)

## Prerequisites

- Python: Version 3.9 or higher (compatible with 3.8, but 3.9 is preferred)
- Virtual Environment: To maintain an organized development environment and prevent dependency conflicts

## How to Fire It Up

Here’s my step-by-step:

1. **Clone the Repository**
   ```bash
   git clone <url>
   cd video-recommendation-engine

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv/Scripts/activate
   ```
3. **Install Dependencies**

   ```bash
   pip install fastapi uvicorn requests python-dotenv tensorflow numpy pandas alembic sqlalchemy
   ```
4. **Configure Environment Variables**
   Create a `.env` file in the root directory:

   ```env

   FLIC_TOKEN=flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f
   API_BASE_URL=https://api.socialverseapp.com
   ```
5. **Run Database Migrations**

   ```bash
   alembic upgrade head
   ```
6. **Start the Engine**

   ```bash
   uvicorn app.main:app --reload
   ```

## API Endpoints

### Main Endpoints

1. **Get Personalized Feed**

   ```
   GET /feed?username={username}
   ```

   Returns personalized video recommendations for a specific user.
2. **Get Category-based Feed**

   ```
   GET /feed?username={username}&category_id={category_id}
   ```

   Narrows it down to a specific category—say, motivational talks.
3. **All Videos**

   ```
   GET /posts/all
   ```

   Grabs everything from the Socialverse API’s summary endpoint.

### Data Collection Endpoints (Internal Use)

The system uses the following APIs for data collection:

### APIs

1. **Get All Viewed Posts** (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/view?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
   ```
2. **Get All Liked Posts** (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/like?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
   ```
3. **Get All Inspired posts** (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/inspire?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
   ```
4. **Get All Rated posts** (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/rating?page=1&page_size=1000&resonance_algorithm=resonance_algorithm_cjsvervb7dbhss8bdrj89s44jfjdbsjd0xnjkbvuire8zcjwerui3njfbvsujc5if
   ```
5. **Get All Posts** (Header required*) (METHOD: GET):

   ```
   https://api.socialverseapp.com/posts/summary/get?page=1&page_size=1000
   ```
6. **Get All Users** (Header required*) (METHOD: GET):

   ```
   https://api.socialverseapp.com/users/get_all?page=1&page_size=1000
   ```

### Authorization

Every API call needs this header:


```json
"Flic-Token": "flic_11d3da28e403d182c36a3530453e290add87d0b4a40ee50f17611f180d47956f"
```

**Note**: All external API calls require the Flic-Token header:

## Algorithm Implementation

The recommendation engine uses a Deep Neural Network (DNN) architecture with the following components:

1. **Data Preprocessing**

   - Feature engineering
   - Data normalization
   - Missing value handling
   - Categorical encoding
2. **Model Architecture**

   - Embedding layers for categorical features
   - Dense layers with ReLU activation
   - Dropout for regularization
   - Output layer with appropriate activation
3. **Cold Start Handling**

   - Mood-based initial recommendations
   - Content-based filtering fallback
   - Popularity-based recommendations

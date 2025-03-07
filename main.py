from fastapi import FastAPI, Query, HTTPException
import requests
from typing import List, Dict, Optional
import os
from dotenv import load_dotenv
import tensorflow as tf
import numpy as np
import pandas as pd

# Load environment variables
load_dotenv()
FLIC_TOKEN = os.getenv("FLIC_TOKEN")
print("✅ Loaded FLIC_TOKEN:", FLIC_TOKEN)  # Debugging line

if not FLIC_TOKEN:
    raise ValueError("❌ ERROR: FLIC_TOKEN is missing! Check your .env file or environment variables.")
API_BASE_URL = "https://api.socialverseapp.com"

app = FastAPI()

# Function to fetch data from API with headers
def fetch_data(endpoint: str) -> List[Dict]:
    headers = {
    "Flic-Token": FLIC_TOKEN,
    "Authorization": f"Bearer {FLIC_TOKEN}"
}

    response = requests.get(f"{API_BASE_URL}{endpoint}", headers=headers)
    if response.status_code == 200:
        return response.json().get("posts", [])
    else:
        raise HTTPException(status_code=response.status_code, detail=f"API request failed: {response.text}")

# Fetch various types of engagement data
@app.get("/viewed-posts")
def get_viewed_posts():
    return fetch_data("/posts/view?page=1&page_size=1000")

@app.get("/liked-posts")
def get_liked_posts():
    return fetch_data("/posts/like?page=1&page_size=1000")

@app.get("/inspired-posts")
def get_inspired_posts():
    return fetch_data("/posts/inspire?page=1&page_size=1000")

@app.get("/rated-posts")
def get_rated_posts():
    return fetch_data("/posts/rating?page=1&page_size=1000")

@app.get("/all-users")
def get_all_users():
    return fetch_data("/users/get_all?page=1&page_size=1000")

@app.get("/all-posts")
def get_all_posts():
    return fetch_data("/posts/summary/get?page=1&page_size=1000")

# Train a simple deep learning model for recommendations
def train_model():
    num_users = 100
    num_videos = 500
    user_video_matrix = np.random.rand(num_users, num_videos)
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(num_videos,)),
        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.Dense(num_videos, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy')
    model.fit(user_video_matrix, np.random.randint(0, 2, size=(num_users, num_videos)), epochs=10, verbose=1)
    return model

model = train_model()

# API: Get personalized video feed
@app.get("/feed")
def get_feed(
    username: str = Query(..., description="Username for recommendations"),
    category_id: Optional[int] = Query(None, description="Filter by category ID (optional)")
):
    viewed_posts = get_viewed_posts()
    liked_posts = get_liked_posts()
    inspired_posts = get_inspired_posts()
    rated_posts = get_rated_posts()
    
    all_posts = viewed_posts + liked_posts + inspired_posts + rated_posts
    unique_posts = {post["id"]: post for post in all_posts}.values()
    
    if category_id:
        filtered_posts = [post for post in unique_posts if post.get("category", {}).get("id") == category_id]
        return {"username": username, "recommendations": filtered_posts}
    
    return {"username": username, "recommendations": list(unique_posts)}

# API: Get all video posts
@app.get("/posts/all")
def get_all_video_posts():
    return {"status": "success", "message": "Fetched all posts", "posts": get_all_posts()}

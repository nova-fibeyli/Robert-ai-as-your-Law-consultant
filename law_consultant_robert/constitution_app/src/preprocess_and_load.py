import pandas as pd
from pymongo import MongoClient

# Load the training dataset
train_data = pd.read_csv("EmpatheticDialogues/train.csv")

# Extract relevant columns
dialogues = train_data[["prompt", "utterance"]].drop_duplicates().dropna()

# Convert to dictionary format for MongoDB
dialogue_records = dialogues.to_dict(orient="records")

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.support_bot
dialogue_collection = db.dialogues

# Insert dialogues into MongoDB
dialogue_collection.insert_many(dialogue_records)
print("Dataset loaded into MongoDB successfully!")

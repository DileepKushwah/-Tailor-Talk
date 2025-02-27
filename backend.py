import os
import pandas as pd
from fastapi import FastAPI, HTTPException

app = FastAPI()
csv_file = "titanic_final.csv"



if not os.path.exists(csv_file):
    raise FileNotFoundError(f"Dataset file '{csv_file}' not found!")


df = pd.read_csv(csv_file)

@app.get("/")
def home():
    return {"message": "Titanic API is running!"}

@app.get("/total_passengers")
def total_passengers():
    return {"total_passengers": len(df)}


@app.get("/percentage_male")
def percentage_male():
    
    # Calculate the percentage of male passengers
    
    
    male_percentage = (df['Sex'].value_counts(normalize=True).get('male', 0)) * 100
    return {"percentage_male": male_percentage}


@app.get("/average_fare")
def average_fare():
    # Calculate the average fare
    avg_fare = df['Fare'].mean()
    return {"average_fare": avg_fare}


@app.get("/survival_rate")
def survival_rate():
    # Calculate the survival rate (mean of the 'Survived' column times 100)
    survival_percent = (df['Survived'].mean()) * 100
    return {"survival_rate": survival_percent}


# The /query endpoint interprets the user's question and calls the appropriate endpoint.
@app.get("/query")
def query(question: str):
    question = question.lower()


    if "how many passengers" in question:
        return total_passengers()
    if "percentage of passengers were male" in question:
        return percentage_male()
    if "average ticket fare" in question:
        return average_fare()
    if "survival rate" in question:
        return survival_rate()
    
    
    return {"answer": "I don't understand that question."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)

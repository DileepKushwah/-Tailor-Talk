import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


#Use st.cache_data to efficiently load the dataset
@st.cache_data
def load_data():
    return pd.read_csv("titanic_final.csv")



data = load_data()

st.title("🚢 Titanic Dataset Chatbot with Visual Insights")



question = st.text_input("Ask me anything about the Titanic dataset:")

if st.button("Ask"):
    if question.strip():
        q = question.lower()


        if "how many passengers" in q or "total passengers" in q:
            total = len(data)
            st.write(f"**Total Passengers:** {total}")
            fig, ax = plt.subplots()
            ax.bar(["Total Passengers"], [total], color="skyblue")
            ax.set_ylabel("Count")
            ax.set_title("Total Passengers on the Titanic")
            st.pyplot(fig)


        #Survival Information Visualization
        elif "survived" in q:
            survival_counts = data["Survived"].value_counts().sort_index()
            survivors = survival_counts.get(1, 0)
            non_survivors = survival_counts.get(0, 0)
            st.write(f"**Survivors:** {survivors} \n**Did Not Survive:** {non_survivors}")
            fig, ax = plt.subplots()
            labels = ["Did Not Survive", "Survived"]
            sizes = [non_survivors, survivors]
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90,
                   colors=["lightcoral", "lightgreen"])
            ax.axis("equal")
            ax.set_title("Survival Distribution")
            st.pyplot(fig)
            

        #Gender Distribution Visualization
        elif "male" in q or "female" in q:
            gender_counts = data["Sex"].value_counts()
            males = gender_counts.get("male", 0)
            females = gender_counts.get("female", 0)
            st.write(f"**Males:** {males} \n**Females:** {females}")
            fig, ax = plt.subplots()
            labels = ["Male", "Female"]
            sizes = [males, females]
            ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90,
                   colors=["cornflowerblue", "lightpink"])
            ax.axis("equal")
            ax.set_title("Gender Distribution")
            st.pyplot(fig)
            

        #Average Ticket Fare Visualization
        elif "average ticket fare" in q or "average fare" in q:
            avg_fare = data["Fare"].mean()
            st.write(f"**Average Ticket Fare:** ${avg_fare:.2f}")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data["Fare"].dropna(), bins=30, kde=True, ax=ax, color="mediumpurple")
            ax.set_xlabel("Fare")
            ax.set_ylabel("Frequency")
            ax.set_title("Fare Distribution")
            st.pyplot(fig)
            

        #Embarkation Information Visualization
        elif "embarked" in q:
            embarked_counts = data["Embarked"].value_counts()
            st.write("**Embarkation Counts:**", embarked_counts.to_dict())
            fig, ax = plt.subplots(figsize=(8, 5))
            sns.barplot(x=embarked_counts.index, y=embarked_counts.values, ax=ax, palette="viridis")
            ax.set_xlabel("Port of Embarkation")
            ax.set_ylabel("Number of Passengers")
            ax.set_title("Passengers per Embarkation Port")
            st.pyplot(fig)
            

        #Age Distribution Visualization
        elif "histogram" in q and "age" in q:
            st.write("**Histogram of Passenger Ages:**")
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.histplot(data["Age"].dropna(), bins=30, kde=True, ax=ax, color="teal")
            ax.set_xlabel("Age")
            ax.set_ylabel("Number of Passengers")
            ax.set_title("Distribution of Passenger Ages")
            st.pyplot(fig)
            
        # If none of the above conditions match, attempt to get a text response from your backend.
        else:
            try:
                response = requests.get(f"http://127.0.0.1:8000/query?question={question}")
                st.write("**Text Result:**", response.json())
            except Exception as e:
                st.error(f"Error connecting to the backend: {e}")
    else:
        st.warning("Please enter a question before clicking Ask.")

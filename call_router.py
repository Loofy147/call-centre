import pandas as pd
import re
from difflib import SequenceMatcher

# Load the comprehensive dataset
try:
    # Assuming the dataset is in the main call-centre directory
    DATASET_PATH = 'algerian_call_center_dataset.csv'
    df = pd.read_csv(DATASET_PATH)
except FileNotFoundError:
    print(f"Error: Dataset not found at {DATAET_PATH}. Please ensure it is in the correct directory.")
    exit()

def get_best_match(query, column):
    """Finds the best matching query in a given column using simple string similarity."""
    best_score = 0
    best_match_index = -1
    
    # Simple preprocessing: convert to lowercase and remove punctuation/extra spaces
    processed_query = re.sub(r'[^\w\s]', '', query).lower().strip()

    for index, row in df.iterrows():
        # Handle potential NaN values in the column
        target_text = str(row[column])
        processed_target = re.sub(r'[^\w\s]', '', target_text).lower().strip()
        
        # Use SequenceMatcher for a simple similarity score
        score = SequenceMatcher(None, processed_query, processed_target).ratio()
        
        # Also check if the query is a substring of the target (useful for short queries)
        if processed_query in processed_target and len(processed_query) > 5:
            score = max(score, 0.9) # Boost score if it's a clear substring match

        if score > best_score:
            best_score = score
            best_match_index = index
            
    # Set a threshold for a "good enough" match
    if best_score > 0.7:
        return df.iloc[best_match_index], best_score
    else:
        return None, best_score

def route_call(customer_query, language='AR'):
    """
    Routes the call by finding the best matching scenario and providing a structured response.
    Language can be 'AR', 'FR', or 'EN'.
    """
    print(f"--- Analyzing Query (Language: {language}) ---")
    
    # Determine the correct query column based on the requested language
    query_column = f"Customer_Query_{language}"
    
    # Determine the correct response column, with FR as a fallback for EN since Agent_Response_EN was not generated
    if language == 'EN':
        response_column = "Agent_Response_FR"
    else:
        response_column = f"Agent_Response_{language}"
    
    match, score = get_best_match(customer_query, query_column)
    
    if match is not None:
        print(f"Match Found (Similarity Score: {score:.2f})")
        
        # Extract the structured business value
        result = {
            "Status": "Success",
            "Matched_Query": match[query_column],
            "Sector": match['Sector'],
            "Topic": match['Topic'],
            "Sentiment": match['Sentiment'],
            "Agent_Action": match['Agent_Action'],
            "Agent_Response": match[response_column]
        }
        return result
    else:
        print(f"No strong match found (Best Score: {score:.2f}).")
        return {
            "Status": "No Match",
            "Sector": "Unclassified",
            "Topic": "Unclassified",
            "Sentiment": "Neutral",
            "Agent_Action": "Escalate to Tier 2 Support",
            "Agent_Response": "أعتذر، لم أتمكن من تحديد طبيعة مشكلتك بدقة. سأقوم بتحويلك إلى مسؤول مختص فوراً. (Je m'excuse, je n'ai pas pu identifier la nature exacte de votre problème. Je vais vous transférer immédiatement à un responsable spécialisé.)"
        }

# --- Proof of Concept Demonstrations ---

# 1. Frustrated customer (Telecommunications)
query_1 = "الكونيكسيون ثقيلة بزاف، ما نقدر ندير والو."
print("\n[Scenario 1: Slow Internet (Darija)]")
print(route_call(query_1, 'AR'))

# 2. Urgent merchant issue (Payment Gateway)
query_2 = "My electronic payment terminal (POS) won't work today, it says a connection error."
print("\n[Scenario 2: Failed POS Transaction (English)]")
print(route_call(query_2, 'EN'))

# 3. B2B Critical Issue (Logistics)
query_3 = "Nous avons un conteneur bloqué au port à cause d'un problème de documents douaniers, nous avons besoin de votre soutien."
print("\n[Scenario 3: Customs Delay (French)]")
print(route_call(query_3, 'FR'))

# 4. Unmatched Query
query_4 = "I want to complain about the coffee machine in the office."
print("\n[Scenario 4: Unmatched Query (English)]")
print(route_call(query_4, 'EN'))

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib

labeled_df = pd.read_excel("updated_clustered_activities.xlsx")
test_df=pd.read_excel("15000-activities-propositions.xlsx")
test_df.rename(columns={"activity": "Text"}, inplace=True)

model = SentenceTransformer("sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
labeled_df["Embeddings"] = labeled_df["Text"].apply(lambda x: model.encode(str(x), convert_to_numpy=True))
test_df["Embeddings"] = test_df["Text"].apply(lambda x: model.encode(str(x), convert_to_numpy=True))

X_train = np.vstack(labeled_df["Embeddings"].values)
X_test = np.vstack(test_df["Embeddings"].values)
y = labeled_df["Label"]



clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(X_train, y)

y_pred = clf.predict(X_test)

test_df["Predicted_Label"] = y_pred 
test_df[["Text", "Predicted_Label"]].to_excel("15000_results.xlsx", index=False) 

print("Predictions saved to 15000_results.xlsx ✅")


joblib.dump(clf, "activity_classifier.pkl")

clf = joblib.load("activity_classifier.pkl")



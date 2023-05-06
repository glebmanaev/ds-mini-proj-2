import pandas
import pickle
from sklearn.ensemble import RandomForestRegressor

books = pandas.read_csv("ml-training-data.csv")
# Convert Genre to one-hot encoding
books = pandas.get_dummies(books, columns=["Genre"])
y = books["Price"]
X = books.drop(["Price"], axis=1)

model = RandomForestRegressor()
model.fit(X, y)

with open("ml-price-predicting-model.pkl", "wb") as f:
    pickle.dump(model, f)
print("Model saved to ml-price-predicting-model.pkl")

prediction = model.predict([[2010, 300, 1,0,0,0]])
print(f"Testing: \n{prediction[0]:.2f}")
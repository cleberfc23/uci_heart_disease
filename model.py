from ucimlrepo import fetch_ucirepo
from sklearn.model_selection import train_test_split
import xgboost as xgb
from sklearn.metrics import accuracy_score
import joblib 
print('\n>>> model.py\n')

heart_disease  = fetch_ucirepo(id=45)
data = heart_disease.data.features
data['disease'] = 1*(heart_disease.data.targets >1)

X = data.drop(columns = 'disease')
y = data['disease']

medians = X.median()
joblib.dump(medians, 'medians.pkl')

# print(X.head())
X_train, X_test, y_train, y_test = train_test_split(X,y,test_size=0.2, random_state=432, stratify=y)

model = xgb.XGBClassifier(objective ='binary:logistic')
model.fit(X_train, y_train)
predictions = model.predict(X_test)

model_accuracy = accuracy_score(y_test, predictions)
print(f'Accuracy: {model_accuracy:.2%}')

joblib.dump(model, 'xgboost_model.pkl')
print('\n')
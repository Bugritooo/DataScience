import pandas as pd
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV


# Create an imputer
imputer = SimpleImputer(strategy='mean')  # You can choose other strategies as well

# Load your CSV file
file_path = '/Users/bugrahan/Desktop/proje/test_data1.csv'
df = pd.read_csv(file_path)
df = df.drop(columns=['Unnamed: 0'])
print(df)

# Separate features (X) and target variable (y)
X = df.drop('tag', axis=1)
y = df['tag']

# Fit and transform the imputer on your entire dataset
X_imputed = imputer.fit_transform(X)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=0.2, random_state=42)

param_grid = {
    'n_estimators': [100, 500, 1000],
    'max_features': ['auto', 'sqrt', 'log2', None, 0.5, 0.7],
    'max_depth': [None, 10, 20, 30],
    'min_samples_split': [2, 5, 10],
    'min_samples_leaf': [1, 2, 4],
    'bootstrap': [True, False],
    'class_weight': [None, 'balanced', 'balanced_subsample']
}

grid_search = GridSearchCV(RandomForestClassifier(random_state=42), param_grid, cv=5, n_jobs=-1)
grid_search.fit(X_train, y_train)

# Make predictions on the test set
y_pred = grid_search.predict(X_test)

# Evaluate the accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f'Accuracy: {accuracy}')

# Use cross-validation to evaluate the model
cv_scores = cross_val_score(clf, X_imputed, y, cv=5)  # You can adjust the number of folds with the 'cv' parameter

# Print the cross-validation scores
print(f'Cross-Validation Scores: {cv_scores}')
print(f'Mean Accuracy: {cv_scores.mean()}')
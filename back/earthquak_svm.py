import pandas as pd
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import pickle


df = pd.read_csv('significant-earthquake-database.csv', usecols=['ID Earthquake', 'Mw Magnitude', 'Ms Magnitude', 'Mb Magnitude', 'Ml Magnitude', 'MFA Magnitude', 
                                                                   'Unknown Magnitude', 'Earthquake : Deaths', 'Earthquake : Damage Description', 'Coordinates_x', 'Coordinates_y'])

def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Filter the DataFrame to keep only rows where the column contains numeric values
    
string_to_numeric = {
    'SEVERE (~>$5 to $24 million)': 3,
    'MODERATE (~$1 to $5 million)': 2,
    'LIMITED (roughly corresponding to less than $1 million)': 1,
    'EXTREME (~$25 million or more)': 4,
    'Many (~101 to 1000 deaths)': 5
}

df['Earthquake : Damage Description'] = df['Earthquake : Damage Description'].map(string_to_numeric)

df = df[df['Coordinates_x'].apply(is_numeric)]
df = df[df['Coordinates_y'].apply(is_numeric)]
df = df[df['Earthquake : Deaths'].apply(is_numeric)]
df = df[df['Earthquake : Damage Description'].apply(is_numeric)]
df['Coordinates_x'] = pd.to_numeric(df['Coordinates_x'], errors='coerce')
df['Coordinates_y'] = pd.to_numeric(df['Coordinates_y'], errors='coerce')
df['Earthquake : Deaths'] = pd.to_numeric(df['Earthquake : Deaths'], errors='coerce')




magnitude_columns = ['Mw Magnitude', 'Ms Magnitude', 'Mb Magnitude', 'Ml Magnitude', 'MFA Magnitude', 'Unknown Magnitude']

df['mean_magnitude'] = df[magnitude_columns].mean(axis=1)

df = df[['mean_magnitude', 'Earthquake : Deaths', 'Earthquake : Damage Description', 'Coordinates_x', 'Coordinates_y']]

print(df.dtypes)
df = df.fillna(df.mean())


#Model processing
features = df[['Coordinates_x', 'Coordinates_y']] 
targets = df[['Earthquake : Deaths', 'Earthquake : Damage Description', 'mean_magnitude']]

X_train, X_test, y_train, y_test = train_test_split(features, targets, test_size=0.2, random_state=42)

svm_model_A = SVR(kernel='rbf')
svm_model_B = SVR(kernel='rbf')
svm_model_C = SVR(kernel='rbf')
svm_model_A.fit(X_train.values, y_train['Earthquake : Deaths'])
svm_model_B.fit(X_train.values, y_train['Earthquake : Damage Description'])
svm_model_C.fit(X_train.values, y_train['mean_magnitude'])

predictions_A = svm_model_A.predict(X_test)
predictions_B = svm_model_B.predict(X_test)
predictions_C = svm_model_C.predict(X_test)

mse_A = mean_squared_error(y_test['Earthquake : Deaths'], predictions_A)
mse_B = mean_squared_error(y_test['Earthquake : Damage Description'], predictions_B)
mse_C = mean_squared_error(y_test['mean_magnitude'], predictions_C)


with open('svm_model_dead.pkl', 'wb') as f:
    pickle.dump(svm_model_A, f)

with open('svm_model_dmg.pkl', 'wb') as f:
    pickle.dump(svm_model_B, f)

with open('svm_model_mag.pkl', 'wb') as f:
    pickle.dump(svm_model_C, f)

print("Mean Squared Error for column A:", mse_A)
print("Mean Squared Error for column B:", mse_B)
print("Mean Squared Error for column C:", mse_C)

# Testing infenences
X_test = [[-77, 43]]
predictions_C = svm_model_C.predict(X_test)

print(predictions_C)

new_df = pd.DataFrame({'AB_pair':list(zip(df['Coordinates_x'], df['Coordinates_y']))})

new_df.to_pickle('coords_tuple.pkl')
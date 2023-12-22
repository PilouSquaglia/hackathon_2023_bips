import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import numpy as np

# Load the Excel file
file_path = 'data.xlsx'
xls = pd.ExcelFile(file_path)

sheet_names = xls.sheet_names
print(sheet_names)


# Function to clean and structure data for each sheet (village)
def clean_and_structure_data(sheet_name):
    # Load data from the sheet
    df = pd.read_excel(xls, sheet_name=sheet_name)

    # Removing the first row which contains headers like GPS, remplissage, etc.
    df = df.drop(0)

    # Renaming the columns for clarity
    columns = ['Jour', 'Date']
    for i in range(1, int((df.shape[1] - 2) / 3) + 1):
        columns += [f'Poubelle_{i}_GPS', f'Poubelle_{i}_Remplissage', f'Poubelle_{i}_Coeff_Touriste']
    df.columns = columns

    # Filling the GPS coordinates down the column as they are constant for each poubelle
    for i in range(1, int((df.shape[1] - 2) / 3) + 1):
        df[f'Poubelle_{i}_GPS'] = df[f'Poubelle_{i}_GPS'].fillna(method='ffill')

    return df

# Clean and structure data for the first village "Olmeta di Tuda"
olmeta_di_tuda_data = clean_and_structure_data('olmeta di tuda')
print(olmeta_di_tuda_data.head())


# Consolidating data for all villages

# Initialize an empty DataFrame to store all data
all_villages_data = pd.DataFrame()

# Loop through each sheet (village) and clean, structure, then append the data
for sheet in sheet_names:
    village_data = clean_and_structure_data(sheet)
    # Adding a column to identify the village
    village_data['Village'] = sheet
    # Append to the global DataFrame
    all_villages_data = all_villages_data.append(village_data, ignore_index=True)

# Display the first few rows of the consolidated DataFrame
all_villages_data.head()

# Define the path for the new consolidated Excel file
consolidated_file_path = 'Consolidated_Village_Data.xlsx'


# Ensure the date format is correct
all_villages_data['Date'] = pd.to_datetime(all_villages_data['Date']).dt.strftime('%Y-%m-%d')

example_data = all_villages_data[['Date', 'Poubelle_1_Remplissage', 'Poubelle_1_Coeff_Touriste']].copy()

# Dropping rows with missing values for simplicity
example_data.dropna(inplace=True)

# Convert remplissage and coeff_touriste to numeric
example_data['Poubelle_1_Remplissage'] = pd.to_numeric(example_data['Poubelle_1_Remplissage'])
example_data['Poubelle_1_Coeff_Touriste'] = pd.to_numeric(example_data['Poubelle_1_Coeff_Touriste'])

# Adding day of week as a feature
example_data['DayOfWeek'] = pd.to_datetime(example_data['Date']).dt.dayofweek

# Target variable: Remplissage (fill level)
y = example_data['Poubelle_1_Remplissage']

# Features: Coeff_Touriste and DayOfWeek
X = example_data[['Poubelle_1_Coeff_Touriste', 'DayOfWeek']]

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize a Random Forest Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)

# Fit the model on the training data
model.fit(X_train, y_train)

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate the model using mean squared error
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
rmse




depot = 42.60080491507166, 9.322923935409024
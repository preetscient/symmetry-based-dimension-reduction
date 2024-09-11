# Processing Module

This module handles the main data processing tasks. It includes data cleaning, transformation, and validation.

## Functions

- `clean_data(data: pd.DataFrame)`: Cleans the data by removing invalid entries.
- `transform_data(data: pd.DataFrame)`: Transforms the data into the required format.

## Usage

```python
from processing import clean_data, transform_data

df = pd.read_csv('raw_data.csv')
clean_df = clean_data(df)
transformed_df = transform_data(clean_df)

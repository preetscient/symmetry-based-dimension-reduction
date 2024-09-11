# Lumping Module

Handles data aggregation and lumping processes. This is useful for condensing large datasets into more manageable forms.

## Functions

- `aggregate_data(data: pd.DataFrame)`: Aggregates data based on predefined rules.

## Usage

```python
from lumping import aggregate_data

df = pd.read_csv('data.csv')
aggregated_df = aggregate_data(df)

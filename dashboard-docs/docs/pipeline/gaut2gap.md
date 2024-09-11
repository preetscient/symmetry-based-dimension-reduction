# Gaut2Gap Module

This module is responsible for converting GAUT data formats into GAP-compatible formats. It ensures the data interoperability between different systems.

## Functions

- `convert_gaut_to_gap(gaut_data: pd.DataFrame)`: Converts GAUT data to GAP format.

## Usage

```python
from gaut2gap import convert_gaut_to_gap

gaut_df = pd.read_csv('gaut_data.csv')
gap_df = convert_gaut_to_gap(gaut_df)

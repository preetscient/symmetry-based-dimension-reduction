# Visualization Layout Module

The `viz_layout` module is responsible for defining the layout and design of visualizations. This includes setting up plots, axes, and other visual elements.

## Functions

- `setup_layout(figure, title: str)`: Configures the layout of a given figure with a specified title.
- `apply_theme(figure, theme_name: str)`: Applies a visual theme to a figure.

## Usage

```python
from viz_layout import setup_layout, apply_theme

fig, ax = plt.subplots()
setup_layout(fig, "My Chart Title")
apply_theme(fig, "dark_mode")
plt.show()

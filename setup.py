from setuptools import setup, find_packages

setup(
    name="your_module_name",
    version="0.1",
    description="A Dash app with Cytoscape visualization",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "dash>=2.0.0",
        "dash-cytoscape",
        "plotly",
    ],
    entry_points={
        'console_scripts': [
            'run-app=your_module_name.app:main',
        ],
    },
)
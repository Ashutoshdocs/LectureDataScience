# Project 1 — Business Sales Visualization

## Run
From the repository root:
```bash
pip install -r requirements.txt
python project_01_sales_visualization/main.py
```

## Data
`data/input/sales.csv` contains transaction rows with date, region, product, units, and unit price. `data/reference/regions.csv` describes the regions.

## Output
Charts and a summary CSV are written to `output/`. The script creates the output directory if it does not exist.

## Student tasks
- Add a chart for units sold by product.
- Add labels to the regional revenue bars.
- Change the monthly chart to show a rolling average.
- Export one chart as SVG.

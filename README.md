# Global Power Plant Explorer

Streamlit app to visualize the Global Power Plant Database with an interactive map, filters, and supporting visuals.

## Features
- Map explorer with Plotly Mapbox; points sized by `capacity_mw`, colored by `primary_fuel`, with hover details (country, name, capacity, fuels, commissioning year, owner).
- Filters for country and primary fuel via dropdowns.
- Table listing the plants currently shown on the map.
- Infographic tab showing `infographic.png` (if present).
- Estimating Power Plant Generation tab stacking `1.jpeg` through `8.jpeg` (shown if files exist).
- Footer with a logo (`logo.png` if present).

## Setup
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Place assets (optional, to enable visuals):
   - `logo.png` for the footer.
   - `infographic.png` for the Infographic tab.
   - `1.jpeg` … `8.jpeg` for the Estimating Power Plant Generation tab.
3. Run the app:
   ```bash
   streamlit run app.py
   ```

## Notes
- The app expects `global_power_plant_database.csv` in the project root.
- Missing optional assets simply show an info message instead of breaking the app.

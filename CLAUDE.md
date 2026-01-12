# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Linehaul.ai Network Dashboard - a Streamlit app that visualizes drop trailer freight markets and lane connections on an interactive US map using Plotly.

## Commands

### Run the app locally
```bash
uv run streamlit run app1.py
```

### Install dependencies
```bash
uv sync
```

### Docker
```bash
# Build
docker build -t streamlitnetwork:latest .

# Run
docker run -p 8501:8501 streamlitnetwork:latest
```

## Architecture

The entire application is contained in `app1.py`:

- **Hub data**: Static dictionary defining freight hub cities with coordinates and colors
- **Connected cities**: Mapping of which cities connect to each hub
- **Geocoding**: Uses geopy's Nominatim to look up coordinates for non-hub cities (cached with `@st.cache_data`)
- **Map visualization**: `create_network_map()` builds a Plotly Scattergeo figure with hub markers, connection lines, and destination markers
- **Session state**: Tracks the currently selected hub via `st.session_state.selected_hub`

Note: The README references `app.py` but the actual file is `app1.py`.

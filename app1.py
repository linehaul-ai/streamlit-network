import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# Set page config
st.set_page_config(page_title="Freight Network Dashboard", layout="wide")

# Initialize geocoder
geolocator = Nominatim(user_agent="freight_network_app")

# Initialize session state for selected hub
if 'selected_hub' not in st.session_state:
    st.session_state.selected_hub = "Chicago"

# Define hub data
hubs = {
    "Chicago": {"lat": 41.8781, "lon": -87.6298, "color": "#000000"},  # Black
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437, "color": "#fc0106"},  # Red
    "Stockton": {"lat": 37.9537, "lon": -121.2908, "color": "#3569be"},  # Light Blue
    "Greensboro": {"lat": 36.0726, "lon": -79.7915, "color": "#4fcc33"},  # Lime Green
    "Philadelphia": {"lat": 39.9526, "lon": -75.1652, "color": "#FFBE0B"},  # Yellow
    "Cleveland": {"lat": 41.4993, "lon": -81.6944, "color": "#FF006E"},  # Pink
    "St. Louis": {"lat": 38.6270, "lon": -90.1999, "color": "#8338EC"}  # Purple
}

# Define connected cities
connected_cities = {
    "Chicago": ["Greensboro", "St Louis", "Philadelphia", "Los Angeles", "Atlanta", "Stockton", "Cleveland", "Ft. Worth", "Madison"],
    "Los Angeles": ["Chicago", "Madison", "Charlotte"],
    "Stockton": ["Chicago", "Madison", "Charlotte"],
    "Philadelphia": ["Chicago"],
    "Greensboro": ["Chicago", "Philadelphia", "Atlanta", "Ft. Worth"],
    "Cleveland": ["Chicago"],
    "St. Louis": ["Chicago"],
}

# Cache geocoding results
@st.cache_data
def get_city_coordinates(city_name):
    try:
        location = geolocator.geocode(f"{city_name}, USA")
        return (location.latitude, location.longitude)
    except:
        return None

# Calculate city coordinates for all cities
all_cities = {}
for hub in hubs:
    all_cities[hub] = (hubs[hub]["lat"], hubs[hub]["lon"])
    for city in connected_cities[hub]:
        if city not in all_cities:
            coords = get_city_coordinates(city)
            if coords:
                all_cities[city] = coords

def create_network_map(selected_hub=None):
    fig = go.Figure()

    # Add base map
    fig.add_trace(go.Scattergeo(
        lon=[],
        lat=[],
        mode='markers',
        marker=dict(size=1),
        showlegend=False,
    ))

    # Plot all hubs
    for hub, data in hubs.items():
        if selected_hub is None or hub == selected_hub:
            # Plot hub with larger marker
            fig.add_trace(go.Scattergeo(
                lon=[data["lon"]],
                lat=[data["lat"]],
                mode='markers+text',
                text=[hub],
                textposition="top center",
                marker=dict(
                    size=20,  # Increased from 12
                    color=data["color"],
                    line=dict(width=2, color='white')  # Add white border
                ),
                name=hub,
                showlegend=True,
            ))

            # Plot connections and connected cities with smaller markers
            for city in connected_cities[hub]:
                if city in all_cities:
                    city_coords = all_cities[city]
                    # Add connection line
                    fig.add_trace(go.Scattergeo(
                        lon=[data["lon"], city_coords[1]],
                        lat=[data["lat"], city_coords[0]],
                        mode='lines',  # Removed markers from lines
                        line=dict(width=2, color=data["color"]),
                        showlegend=False,
                    ))
                    # Add connected city marker separately
                    fig.add_trace(go.Scattergeo(
                        lon=[city_coords[1]],
                        lat=[city_coords[0]],
                        mode='markers+text',
                        text=[city],
                        textposition="top center",
                        marker=dict(
                            size=10,  # Smaller than hub markers
                            color='white',  # Different color for connected cities
                            line=dict(width=1, color=data["color"])
                        ),
                        showlegend=False,
                    ))

    # Update layout
    fig.update_layout(
        geo=dict(
            scope='usa',
            projection_type='albers usa',
            showland=True,
            landcolor='#2f3037',  # Darker color for USA land
            countrycolor='#1a1a1d',  # Darker border color
            showlakes=True,
            lakecolor='#1f2024',  # Darker lake color
            showsubunits=True,
            subunitcolor='#1a1a1d',  # Darker state borders
            bgcolor='rgba(0,0,0,0)',
            center=dict(lat=39.5, lon=-98.35),
            lonaxis=dict(
                range=[-125, -65]
            ),
            lataxis=dict(
                range=[25, 49]
            ),
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=600,
    )

    return fig

# Streamlit app
st.title("linehaul.ai Network Dashboard")

# Display map using session state
fig = create_network_map(st.session_state.selected_hub)
st.plotly_chart(fig, use_container_width=True)

# Add horizontal hub selector below map
st.write("### Drop Trailer Markets")
cols = st.columns(len(hubs))

# Create horizontal buttons for hub selection
for idx, hub in enumerate(hubs.keys()):
    if cols[idx].button(hub, use_container_width=True):
        st.session_state.selected_hub = hub
        st.rerun()

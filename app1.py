import numpy as np
import plotly.graph_objects as go
import streamlit as st
from geopy.geocoders import Nominatim

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Drop Trailer Network | linehaul.ai",
    page_icon="favicon/favicon.ico",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ============================================================
# CSS STYLES
# ============================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Ubuntu:wght@300;400;500;700&display=swap');

/* Base */
.stApp {
    background-color: #0a0a0a !important;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

section[data-testid="stSidebar"] { display: none; }
#MainMenu, footer, header { visibility: hidden; }

/* Plotly */
[data-testid="stPlotlyChart"] {
    background-color: transparent !important;
    border: none !important;
    padding: 0 !important;
}

/* Floating header */
.floating-header {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 1000;
    padding: 1.25rem 2rem;
    background: linear-gradient(180deg, rgba(10,10,10,0.95) 0%, rgba(10,10,10,0.7) 60%, transparent 100%);
    display: flex;
    justify-content: space-between;
    align-items: center;
    pointer-events: none;
}

.floating-header * {
    pointer-events: auto;
}

.logo {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.logo-img {
    height: auto;
    width: auto;
}

.logo-accent { color: #4A7C59; }

.header-badge {
    font-family: 'Ubuntu', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: #ffffff;
    background: rgba(26, 26, 26, 0.9);
    padding: 0.5rem 1rem;
    border-radius: 100px;
    border: 1px solid #2a2a2a;
}

/* Info panel - bottom left */
.info-panel {
    position: fixed;
    bottom: 2rem;
    left: 2rem;
    z-index: 1000;
    background: rgba(26, 26, 26, 0.9);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid #2a2a2a;
    border-radius: 16px;
    padding: 1.5rem;
    width: 320px;
    height: 400px;
    overflow-y: auto;
}

.info-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.35rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.hub-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
    display: inline-block;
}

.info-subtitle {
    font-family: 'Ubuntu', sans-serif;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #4A7C59;
    margin-bottom: 1rem;
}

.info-stat {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.5rem 0;
    border-bottom: 1px solid #2a2a2a;
}

.info-stat:last-of-type { border-bottom: none; }

.info-stat-label {
    font-family: 'Ubuntu', sans-serif;
    font-size: 0.875rem;
    color: #d1d5db;
}

.info-stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1rem;
    font-weight: 600;
    color: #ffffff;
}

.info-connections {
    margin-top: 1rem;
    padding-top: 1rem;
    border-top: 1px solid #2a2a2a;
}

.info-connections-title {
    font-family: 'Ubuntu', sans-serif;
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: #666666;
    margin-bottom: 0.75rem;
}

.connection-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
}

.connection-tag {
    font-family: 'Ubuntu', sans-serif;
    font-size: 0.75rem;
    color: #d1d5db;
    background: rgba(255,255,255,0.05);
    padding: 0.3rem 0.6rem;
    border-radius: 4px;
    border: 1px solid #333333;
}

/* Hub selector container - fixed right side */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlockBorderWrapper"]:first-child button) {
    position: fixed !important;
    right: 2rem !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    z-index: 1000 !important;
    background: transparent !important;
    border: none !important;
}

/* Target the sidebar-like container we're creating */
section[data-testid="stSidebar"] {
    display: block !important;
    position: fixed !important;
    right: 0 !important;
    left: auto !important;
    top: 50% !important;
    transform: translateY(-50%) !important;
    width: auto !important;
    min-width: 0 !important;
    max-width: none !important;
    background: transparent !important;
    padding: 1rem !important;
    z-index: 1000 !important;
}

section[data-testid="stSidebar"] > div {
    background: transparent !important;
    padding: 0 !important;
}

section[data-testid="stSidebar"] [data-testid="stSidebarContent"] {
    background: transparent !important;
}

section[data-testid="stSidebar"] .stButton > button {
    font-family: 'Ubuntu', sans-serif !important;
    font-size: 0.85rem !important;
    font-weight: 400 !important;
    color: #d1d5db !important;
    background: rgba(26, 26, 26, 0.9) !important;
    backdrop-filter: blur(10px) !important;
    -webkit-backdrop-filter: blur(10px) !important;
    padding: 0.6rem 1rem !important;
    border-radius: 6px !important;
    border: 1px solid #333333 !important;
    transition: all 0.15s ease !important;
    width: 130px !important;
    min-width: 130px !important;
    max-width: 130px !important;
    min-height: 42px !important;
    height: 42px !important;
    margin-bottom: 0.35rem !important;
    box-sizing: border-box !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    white-space: nowrap !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
}

section[data-testid="stSidebar"] .stButton > button:hover {
    background: rgba(50, 50, 50, 0.95) !important;
    border-color: #4A7C59 !important;
    color: #ffffff !important;
}

section[data-testid="stSidebar"] .stButton > button[kind="primary"],
section[data-testid="stSidebar"] .stButton > button:focus {
    background: #4A7C59 !important;
    border-color: #4A7C59 !important;
    color: #ffffff !important;
    font-weight: 500 !important;
}

/* Responsive */
@media (max-width: 768px) {
    section[data-testid="stSidebar"] {
        top: auto !important;
        bottom: 1rem !important;
        right: 1rem !important;
        transform: none !important;
    }

    .info-panel { display: none; }
}
</style>
""",
    unsafe_allow_html=True,
)


# ============================================================
# DATA DEFINITIONS
# ============================================================

geolocator = Nominatim(user_agent="freight_network_app")

hubs = {
    "Chicago": {"lat": 41.8781, "lon": -87.6298, "color": "#ffffff"},
    "Los Angeles": {"lat": 34.0522, "lon": -118.2437, "color": "#fc0106"},
    "Stockton": {"lat": 37.9537, "lon": -121.2908, "color": "#3569be"},
    "Greensboro": {"lat": 36.0726, "lon": -79.7915, "color": "#4A7C59"},
    "Philadelphia": {"lat": 39.9526, "lon": -75.1652, "color": "#FFBE0B"},
    "Cleveland": {"lat": 41.4993, "lon": -81.6944, "color": "#FF006E"},
    "St. Louis": {"lat": 38.6270, "lon": -90.1999, "color": "#8338EC"},
    "Ft. Worth": {"lat": 32.7555, "lon": -97.3308, "color": "#FF8C00"},
    "Charlotte": {"lat": 35.2271, "lon": -80.8431, "color": "#00CED1"},
}

connected_cities = {
    "Chicago": [
        "Greensboro",
        "St Louis",
        "Philadelphia",
        "Los Angeles",
        "Atlanta",
        "Stockton",
        "Cleveland",
        "Ft. Worth",
        "Madison",
    ],
    "Los Angeles": ["Chicago", "Madison", "Charlotte", "Ridgefield, WA"],
    "Stockton": ["Chicago", "Madison", "Charlotte"],
    "Philadelphia": ["Chicago"],
    "Greensboro": ["Chicago", "Philadelphia", "Atlanta", "Ft. Worth"],
    "Cleveland": ["Chicago"],
    "St. Louis": ["Chicago"],
    "Ft. Worth": ["Aurora, CO", "Charlotte", "Ridgefield, WA"],
    "Charlotte": ["Lakeland", "Bayonne", "Boston", "Knoxville", "Los Angeles"],
}


@st.cache_data
def get_city_coordinates(city_name):
    try:
        location = geolocator.geocode(f"{city_name}, USA")
        return (location.latitude, location.longitude)
    except:
        return None


def get_all_city_coordinates():
    all_cities = {}
    for hub in hubs:
        all_cities[hub] = (hubs[hub]["lat"], hubs[hub]["lon"])
        for city in connected_cities.get(hub, []):
            if city not in all_cities:
                coords = get_city_coordinates(city)
                if coords:
                    all_cities[city] = coords
    return all_cities


# ============================================================
# CURVED LINE HELPER
# ============================================================


def get_curved_path(lat1, lon1, lat2, lon2, num_points=50):
    """Generate a curved path between two points using a quadratic bezier curve."""
    mid_lat = (lat1 + lat2) / 2
    mid_lon = (lon1 + lon2) / 2

    dist = np.sqrt((lat2 - lat1) ** 2 + (lon2 - lon1) ** 2)
    offset = dist * 0.15

    dx = lon2 - lon1
    dy = lat2 - lat1

    direction = 1 if lon1 < lon2 else -1
    ctrl_lat = mid_lat + direction * offset * (dx / (dist + 0.001))
    ctrl_lon = mid_lon - direction * offset * (dy / (dist + 0.001))

    t = np.linspace(0, 1, num_points)
    lats = (1 - t) ** 2 * lat1 + 2 * (1 - t) * t * ctrl_lat + t**2 * lat2
    lons = (1 - t) ** 2 * lon1 + 2 * (1 - t) * t * ctrl_lon + t**2 * lon2

    return lats.tolist(), lons.tolist()


# ============================================================
# MAP VISUALIZATION
# ============================================================


def create_map(selected_hub: str, all_cities: dict):
    fig = go.Figure()

    show_all = selected_hub == "ALL"

    if show_all:
        # Show all hubs and all connections
        for hub_name, hub_data in hubs.items():
            for city in connected_cities.get(hub_name, []):
                if city in all_cities:
                    city_coords = all_cities[city]
                    hub_coords = (hub_data["lat"], hub_data["lon"])

                    lats, lons = get_curved_path(
                        hub_coords[0], hub_coords[1], city_coords[0], city_coords[1]
                    )

                    fig.add_trace(
                        go.Scattergeo(
                            lon=lons,
                            lat=lats,
                            mode="lines",
                            line=dict(width=1.5, color=hub_data["color"]),
                            opacity=0.4,
                            showlegend=False,
                            hoverinfo="skip",
                        )
                    )

            fig.add_trace(
                go.Scattergeo(
                    lon=[hub_data["lon"]],
                    lat=[hub_data["lat"]],
                    mode="markers+text",
                    text=[hub_name],
                    textposition="top center",
                    textfont=dict(
                        family="Space Grotesk, sans-serif", size=12, color="#ffffff"
                    ),
                    marker=dict(
                        size=18,
                        color=hub_data["color"],
                        line=dict(width=2, color="#ffffff"),
                    ),
                    showlegend=False,
                    hovertemplate=f"<b>{hub_name}</b><br>Hub<extra></extra>",
                )
            )

        drawn_cities = set()
        for hub_name, hub_data in hubs.items():
            for city in connected_cities.get(hub_name, []):
                if city in all_cities and city not in hubs and city not in drawn_cities:
                    city_coords = all_cities[city]
                    drawn_cities.add(city)
                    fig.add_trace(
                        go.Scattergeo(
                            lon=[city_coords[1]],
                            lat=[city_coords[0]],
                            mode="markers+text",
                            text=[city],
                            textposition="top center",
                            textfont=dict(
                                family="Ubuntu, sans-serif", size=10, color="#666666"
                            ),
                            marker=dict(
                                size=8,
                                color="#1a1a1a",
                                line=dict(width=1.5, color="#666666"),
                            ),
                            showlegend=False,
                            hovertemplate=f"<b>{city}</b><extra></extra>",
                        )
                    )

    elif selected_hub in hubs:
        data = hubs[selected_hub]

        for city in connected_cities.get(selected_hub, []):
            if city in all_cities:
                city_coords = all_cities[city]
                lats, lons = get_curved_path(
                    data["lat"], data["lon"], city_coords[0], city_coords[1]
                )

                fig.add_trace(
                    go.Scattergeo(
                        lon=lons,
                        lat=lats,
                        mode="lines",
                        line=dict(width=2.5, color=data["color"]),
                        opacity=0.6,
                        showlegend=False,
                        hoverinfo="skip",
                    )
                )

        for city in connected_cities.get(selected_hub, []):
            if city in all_cities:
                city_coords = all_cities[city]
                fig.add_trace(
                    go.Scattergeo(
                        lon=[city_coords[1]],
                        lat=[city_coords[0]],
                        mode="markers+text",
                        text=[city],
                        textposition="top center",
                        textfont=dict(
                            family="Ubuntu, sans-serif", size=12, color="#888888"
                        ),
                        marker=dict(
                            size=14,
                            color="#1a1a1a",
                            line=dict(width=2, color=data["color"]),
                        ),
                        showlegend=False,
                        hovertemplate=f"<b>{city}</b><extra></extra>",
                    )
                )

        fig.add_trace(
            go.Scattergeo(
                lon=[data["lon"]],
                lat=[data["lat"]],
                mode="markers+text",
                text=[selected_hub],
                textposition="top center",
                textfont=dict(
                    family="Space Grotesk, sans-serif", size=16, color="#ffffff"
                ),
                marker=dict(
                    size=28, color=data["color"], line=dict(width=3, color="#ffffff")
                ),
                showlegend=False,
                hovertemplate=f"<b>{selected_hub}</b><br>Hub<extra></extra>",
            )
        )

    fig.update_layout(
        geo=dict(
            scope="usa",
            projection_type="albers usa",
            showland=True,
            landcolor="#141414",
            countrycolor="#2a2a2a",
            showlakes=True,
            lakecolor="#0a0a0a",
            showsubunits=True,
            subunitcolor="#1f1f1f",
            bgcolor="rgba(0,0,0,0)",
            center=dict(lat=39, lon=-98),
            lonaxis=dict(range=[-128, -65]),
            lataxis=dict(range=[23, 50]),
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=900,
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#1a1a1a",
            bordercolor="#404040",
            font=dict(family="Ubuntu, sans-serif", size=13, color="#ffffff"),
        ),
    )

    return fig


# ============================================================
# REUSABLE COMPONENTS
# ============================================================


def render_info_panel(selected: str) -> str:
    """Render the info panel HTML for any selection (ALL or specific hub)."""
    if selected == "ALL":
        total_connections = sum(len(c) for c in connected_cities.values())
        return f"""<div class="info-panel">
<div class="info-title">
<span class="hub-dot" style="background-color: #4A7C59;"></span>
All Networks
</div>
<div class="info-subtitle">Overview</div>
<div class="info-stat">
<span class="info-stat-label">Total Hubs</span>
<span class="info-stat-value">{len(hubs)}</span>
</div>
<div class="info-stat">
<span class="info-stat-label">Total Lanes</span>
<span class="info-stat-value">{total_connections}</span>
</div>
</div>"""

    if selected not in hubs:
        return ""

    hub_data = hubs[selected]
    connections = connected_cities.get(selected, [])
    connection_tags = "".join(
        [f'<span class="connection-tag">{c}</span>' for c in connections]
    )

    connections_html = ""
    if connections:
        connections_html = f"""<div class="info-connections">
<div class="info-connections-title">Connected Markets</div>
<div class="connection-tags">{connection_tags}</div>
</div>"""

    return f"""<div class="info-panel">
<div class="info-title">
<span class="hub-dot" style="background-color: {hub_data["color"]};"></span>
{selected}
</div>
<div class="info-subtitle">Hub City</div>
<div class="info-stat">
<span class="info-stat-label">Connections</span>
<span class="info-stat-value">{len(connections)}</span>
</div>
<div class="info-stat">
<span class="info-stat-label">Coordinates</span>
<span class="info-stat-value">{hub_data["lat"]:.1f}, {hub_data["lon"]:.1f}</span>
</div>
{connections_html}
</div>"""


# ============================================================
# MAIN APPLICATION
# ============================================================


def main():
    # Session state
    if "selected_hub" not in st.session_state:
        st.session_state.selected_hub = "ALL"

    # Floating header
    st.markdown(
        """
    <div class="floating-header">
        <div class="logo"><img src="data:image/png;base64,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" alt="inehaul"class="logo-img">linehaul<span class="logo-accent">.ai</span></div>
        <div class="header-badge">Drop Trailer Network</div>
    </div>
    """,
        unsafe_allow_html=True,
    )

    # Info panel
    selected = st.session_state.selected_hub
    st.markdown(render_info_panel(selected), unsafe_allow_html=True)

    # Hub selector in sidebar (positioned via CSS to right side)
    with st.sidebar:
        # ALL button
        if st.button(
            "ALL",
            key="hub_ALL",
            type="primary" if selected == "ALL" else "secondary",
        ):
            st.session_state.selected_hub = "ALL"
            st.rerun()

        # Hub buttons
        for hub_name in hubs.keys():
            is_selected = hub_name == selected
            if st.button(
                hub_name,
                key=f"hub_{hub_name}",
                type="primary" if is_selected else "secondary",
            ):
                st.session_state.selected_hub = hub_name
                st.rerun()

    # Map
    all_cities = get_all_city_coordinates()
    fig = create_map(st.session_state.selected_hub, all_cities)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


if __name__ == "__main__":
    main()

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static

# Load new_loc dataset
new_loc = pd.read_csv("new_loc.csv")  # Adjust the path as necessary

new_loc['Coordinates'] = new_loc['Latitude'].astype(str) + ", " + new_loc['Longitude'].astype(str)
coordinate_options = new_loc['Coordinates'].unique()

# Streamlit app title
st.title("Charging Point Analysis")

# User input for latitude and longitude
st.sidebar.header("User Input")
selected_coordinates = st.sidebar.selectbox("Select a Location:", coordinate_options)

latitude, longitude = map(float, selected_coordinates.split(", "))

# Find the corresponding row in the new_loc dataset
if st.sidebar.button("Get Details"):
    # Filter the dataset based on user input
    location_data = new_loc[
        (new_loc['Latitude'] == latitude) & (new_loc['Longitude'] == longitude)
    ]

    if not location_data.empty:
        col1, col2 = st.columns([0.5, 1])  # Adjust the ratio as needed

        with col1:
            # Points of Interest Section
            st.subheader("Points of Interest Metrics")
            st.write(f"**Number of POIs:** {location_data['POI Count'].values[0]}")
            st.write(f"**POIs Diversity:** {location_data['POI_Diversity'].values[0]:.2f}")
            st.write(f"**Convenience Score:** {location_data['Convenience_Score'].values[0]:.2f}")

            # Competitors Section
            st.subheader("Competitors")
            st.write(f"**Nearby Charging Stations:** {location_data['nearby_stations'].values[0]}")
            st.write(f"**Nearest Station Distance:** {location_data['nearest_station_distance (km)'].values[0]:.2f} km")

            # Traffic and Roads Section
            st.subheader("Traffic and Road Proximity")
            st.write(f"**Average Traffic Time (sec):** {location_data['avg_traffic_estimate (sec)'].values[0]:.1f}")
            st.write(f"**Highway Proximity:** {'Yes' if location_data['Highway_proximity'].values[0] == 1 else 'No'}")
            st.write(f"**Freeway Proximity:** {'Yes' if location_data['Freeway_proximity'].values[0] == 1 else 'No'}")

            st.subheader("Final Score")
            st.write(f"**Final Score:** {location_data['Score_normalized'].values[0]:.1f}")
        with col2:
            # Create a map
            st.subheader("Location on Map")
            map_center = [latitude, longitude]
            m = folium.Map(location=map_center, zoom_start=12, control_scale=True)
            folium.Marker(location=map_center, popup="Selected Location").add_to(m)

            # Increase the size of the map
            folium_static(m, width=700, height=580)
   
    else:
        st.error("No data found for the given coordinates.")

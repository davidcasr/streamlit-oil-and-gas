import geopandas as gpd
import streamlit as st
import folium
import welly
from shapely.geometry import Point
from streamlit_folium import folium_static

st.title("⛽ Streamlit for Oil and Gas Industry")

st.write(
    "The app simplifies the exploration and visualization of well log data. Users can upload LAS files to instantly access detailed well information, including header data and geospatial details. The application leverages GeoPandas and Folium to create interactive maps, pinpointing the well's location with markers for county and state information. Additionally, users can generate comprehensive well plots, both as an overall resume and selectively for specific curves of interest. The tool's streamlined interface provides professionals in the oil and gas sector with a user-friendly platform for efficient and insightful well log analysis, enhancing their ability to interpret and understand subsurface data."
)

st.markdown(
    '<div style="margin-top: 5px; margin-bottom: 15px;"><a href="https://www.buymeacoffee.com/davidcasr" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="41" width="174"></a></div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    Made with ❤️ by [@davidcasr](https://www.davidcasr.co)
    """
)

st.subheader("Upload a LAS file to plot the well log")

uploaded_file = st.file_uploader("Upload .las file")

if uploaded_file is not None:
    try:
        data_file = uploaded_file.read().decode("utf-8")
        well = welly.Well.from_las(data_file)
        st.success("LAS file loaded successfully.")
    except Exception as e:
        st.error(f"Error loading LAS file: {e}")
else:
    default_file = "files/1053428977.las"
    well = welly.Well.from_las(default_file)
    st.info("Using default LAS file.")

st.subheader("Well information")
st.write(well)

st.subheader("Well location")
if well.location and well.location.position:
    location_info = well.location

    gdf = gpd.GeoDataFrame(
        {
            "Well": [well.header.name],
            "County": [location_info.county],
            "State": [location_info.state],
        },
        geometry=[
            Point(location_info.position.longitude, location_info.position.latitude)
        ],
    )

    st.subheader("GeoSpatial Analysis")

    m = folium.Map(
        location=[location_info.position.latitude, location_info.position.longitude],
        zoom_start=12,
    )

    folium.Marker(
        location=[location_info.position.latitude, location_info.position.longitude],
        popup=f"County: {location_info.county}, State: {location_info.state}",
        icon=folium.Icon(color="blue"),
    ).add_to(m)

    folium.GeoJson(gdf).add_to(m)

    st.subheader("Location Map with GeoPandas Data")
    folium_static(m)
else:
    st.warning("Location information not available.")

st.subheader("Well Header")
st.write(well.header)

curve_names = well.data.keys()

resume = well.plot()
st.subheader("Well plot Resume")
st.pyplot(resume)

st.subheader("Well plot by tracks")

selected_curves = st.multiselect("Select curves to plot:", curve_names)

if selected_curves:
    fig = well.plot(tracks=selected_curves)
    st.pyplot(fig)
else:
    st.warning("Please select at least one curve.")

st.subheader("Curve Information")
for curve_name in selected_curves:
    st.markdown(f"**Curve '{curve_name}':**")
    st.write(well.data[curve_name], text_size="small")
    st.write("")

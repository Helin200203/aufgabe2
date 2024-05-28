import streamlit as st
from PIL import Image
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import read_data  # Ihr eigenes Modul

# Funktion zur Berechnung der Zonen basierend auf der Herzfrequenz
def calculate_zones(max_heart_rate, heart_rate_data, power_data):
    zones = {
        'Zone 1': (0, 0.5 * max_heart_rate),
        'Zone 2': (0.5 * max_heart_rate, 0.6 * max_heart_rate),
        'Zone 3': (0.6 * max_heart_rate, 0.7 * max_heart_rate),
        'Zone 4': (0.7 * max_heart_rate, 0.8 * max_heart_rate),
        'Zone 5': (0.8 * max_heart_rate, max_heart_rate)
    }
    zone_times = {zone: 0 for zone in zones}
    zone_power = {zone: [] for zone in zones}

    for hr, power in zip(heart_rate_data, power_data):
        for zone, (lower, upper) in zones.items():
            if lower <= hr < upper:
                zone_times[zone] += 1
                zone_power[zone].append(power)

    avg_power = {zone: (sum(powers)/len(powers)) if powers else 0 for zone, powers in zone_power.items()}
    
    return zone_times, avg_power

# Laden der Aktivitätsdaten
activity_data = pd.read_csv('activity.csv')

# Berechnungen
mean_power = activity_data['PowerOriginal'].mean()
max_power = activity_data['PowerOriginal'].max()

# Initialisierung von Session State Variablen
if 'current_user' not in st.session_state:
    st.session_state.current_user = 'None'

if 'picture_path' not in st.session_state:
    st.session_state.picture_path = 'data/pictures/none.jpg'

person_names = read_data.get_person_list()


st.markdown(
    """
    <style>
    body {
        background-color: #b0c4de;  /* Blaugrau */
        font-family: 'Arial', sans-serif;
    }
    h1, h2 {
        color: #000000;  /* Schwarz */
    }
    .stSelectbox select {
        background-color: #00008b;  /* Dunkelblau */
        color: #ffffff;  /* Weiße Schrift */
    }
    table thead th {
        background-color: #4682b4;  /* Stahlblau */
        color: white;  /* Weißer Text */
        font-size: 18px;
        font-weight: bold;
    }
    table tbody td {
        background-color: #b0c4de;  /* Blaugrauer Hintergrund */
        color: #000000;  /* Schwarzer Text */
        font-size: 16px;
    }
    .stButton button {
        background-color: #00008b;  /* Dunkelblau */
        color: white;  /* Weißer Text */
        font-size: 18px;
        font-weight: bold;
        border-radius: 8px;
    }
    .stTextInput input {
        background-color: #ffffff;  /* Weißer Hintergrund */
        color: #000000;  /* Schwarzer Text */
        font-size: 16px;
        border: 2px solid #00008b;  /* Dunkelblauer Rahmen */
        border-radius: 4px;
    }
    .stImage img {
        border: 2px solid #00008b;  /* Dunkelblauer Rahmen */
        border-radius: 8px;
    }
    .stSlider .stSliderBar {
        background-color: #00008b;  /* Dunkelblauer Hintergrund */
    }
    .stSlider .stSliderHandle {
        background-color: #4682b4;  /* Stahlblauer Griff */
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.write("# EKG APP")

col1, col2 = st.columns(2)

with col1:
    st.write("## Versuchsperson auswählen")
    st.session_state.current_user = st.selectbox(
        'Versuchsperson',
        options=person_names, key="sbVersuchsperson")

with col2:
    st.write("## Bild der Versuchsperson")
    if st.session_state.current_user in person_names:
        st.session_state.picture_path = read_data.find_person_data_by_name(st.session_state.current_user)["picture_path"]
    image = Image.open("./" + st.session_state.picture_path)
    st.image(image, caption=st.session_state.current_user)

# Anzeige der Leistungsdaten
st.title('Aktivitätsanalyse')
st.write(f"Durchschnittliche Leistung: {mean_power:.2f} W")
st.write(f"Maximale Leistung: {max_power:.2f} W")

# Interaktiver Plot
st.subheader('Leistung und Herzfrequenz über die Zeit')

fig = go.Figure()

fig.add_trace(go.Scatter(x=activity_data.index, y=activity_data['PowerOriginal'],
                         mode='lines', name='Leistung', line=dict(color='blue')))
fig.add_trace(go.Scatter(x=activity_data.index, y=activity_data['HeartRate'],
                         mode='lines', name='Herzfrequenz', line=dict(color='red')))

fig.update_layout(title='Leistung und Herzfrequenz über die Zeit',
                  xaxis_title='Zeit (s)',
                  yaxis_title='Wert',
                  legend=dict(x=0, y=1),
                  template='plotly_white')

st.plotly_chart(fig, use_container_width=True)

# Herzfrequenz-Zonen
max_heart_rate = st.number_input('Maximale Herzfrequenz', min_value=100, max_value=220, value=190, step=1)
zone_times, avg_power = calculate_zones(max_heart_rate, activity_data['HeartRate'], activity_data['PowerOriginal'])

# Zeit in Herzfrequenz-Zonen als Tabelle darstellen
st.subheader('Zeit in Herzfrequenz-Zonen')
zone_times_df = pd.DataFrame(list(zone_times.items()), columns=['Zone', 'Zeit (s)'])
st.table(zone_times_df)

# Durchschnittliche Leistung in den Zonen als Tabelle darstellen
st.subheader('Durchschnittliche Leistung in den Zonen')
avg_power_df = pd.DataFrame(list(avg_power.items()), columns=['Zone', 'Durchschnittliche Leistung (W)'])
st.table(avg_power_df)
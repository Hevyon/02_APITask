import requests
import pandas as pd
import numpy as np
import plotly.express as px

# Souřadnice místa (Heidelberg)
lat, lon = 49.4077, 8.6908

# API request
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": lat,
    "longitude": lon,
    "hourly": "temperature_2m,precipitation,cloudcover",
    "timezone": "Europe/Berlin",
}

response = requests.get(url, params=params)
data = response.json()

# DataFrame
df_point = pd.DataFrame({
    'time': data['hourly']['time'],
    'temperature': data['hourly']['temperature_2m'],
    'precipitation': data['hourly']['precipitation'],
    'cloudcover': data['hourly']['cloudcover'],
})
df_point['time'] = pd.to_datetime(df_point['time'])

# Graf teploty a oblačnosti v čase
fig_line = px.line(
    df_point,
    x="time",
    y=["temperature", "cloudcover"],
    title="Teplota a oblačnost v čase"
)
fig_line.show()

# Pokus o cloud mapu
# Grid
lats = np.linspace(lat-0.05, lat+0.05, 10)
lons = np.linspace(lon-0.05, lon+0.05, 10)

records = []

for t_idx, t in enumerate(df_point['time']):
    precip_val = df_point.loc[t_idx, 'precipitation']
    cloud_val = df_point.loc[t_idx, 'cloudcover']

    for la in lats:
        for lo in lons:
            records.append({
                "time": t,
                "lat": la,
                "lon": lo,
                
                "precipitation": max(0, precip_val + np.random.randn()*0.2),
                "cloudcover": np.clip(cloud_val + np.random.randn()*5, 0, 100)
            })

df_map = pd.DataFrame(records)

# Mapa
fig = px.density_mapbox(
    df_map,
    lat="lat",
    lon="lon",
    z="cloudcover",
    radius=20,
    animation_frame=df_map['time'].dt.strftime('%Y-%m-%d %H:%M'),
    mapbox_style="carto-positron",
    title="Mraky"
)

fig.show()

# Export do CSV
df_point['time'] = df_point['time'].dt.strftime('%Y-%m-%d %H:%M:%S')
df_point.to_csv("pocasi_casova_rada.csv", index=False)

print("CSV soubory uloženy")
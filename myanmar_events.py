import streamlit as st
import pandas as pd
from mgrs import MGRS
import folium
from streamlit_folium import st_folium

st.set_page_config(
    page_title="streamlit-folium documentation: Limit Data Return",
    page_icon="🤏",
    layout="wide",
)

st.markdown('## เหตุการณ์ในพม่า')

sheet_id = "1T5xXea-rbuMhCNMalHe-NZa3yPVxjiOs9LGZV6jBlXs"
sheet_name = "Sheet1"
url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"


df = pd.read_csv(url)


Lat = []
Lng = []
Mgrs = []
for index, row in df.iterrows():
    mgrs = None
    try:
        try:
            mgrs = '47Q' + row['พิกัด'].replace(' ','')
            gps = MGRS().toLatLon(mgrs)
        except:
            try:
                mgrs = '47P' + row['พิกัด'].replace(' ','')
                gps = MGRS().toLatLon(mgrs)
            except:
                mgrs = '46Q' + row['พิกัด'].replace(' ','')
                gps = MGRS().toLatLon(mgrs)

    except:
        gps = [None,None]
    Mgrs.append(mgrs)
    Lat.append(gps[0])
    Lng.append(gps[1])

df['lat'] = Lat
df['lng'] = Lng
df['mgrs'] = Mgrs

df['เวลา'] = df['เวลา'].fillna('-')
df['date'] = df['วันที่'] + ' ' + df['เวลา']

df_isgps = df[df['lat'].notna()]
df_nogps = df[df['lat'].isna()]

df =  df.fillna('-')
df_isgps =  df_isgps.fillna('-')
df_nogps =  df_nogps.fillna('-')


#create map
m = folium.Map(location=[df_isgps['lat'].mean(), df_isgps['lng'].mean()], zoom_start=7)
for index, row in df_isgps.iterrows():
    folium.Marker(
        iframe = row['พื้นที่เคลื่อนไหว']
        popup = folium.Popup(iframe, min_width=300, max_width=300)
        [row['lat'], row['lng']], popup=popup, tooltip=row['พื้นที่เคลื่อนไหว']
    ).add_to(m)

c1, c2 = st.columns(2)
with c1:
    output = st_folium(
        m, width=700, height=500, returned_objects=["last_object_clicked"]
    )
with c2:
    click_data = output['last_object_clicked']
    if click_data:
        df2 = df_isgps[(df_isgps['lat']==click_data['lat']) & (df_isgps['lng']==click_data['lng'])]
        df2.set_index('date', inplace=True)

        TABS = st.tabs(df2.index.tolist())

        for i in range(len(TABS)):
            TABS[i].dataframe(df2.iloc[i],use_container_width=True)

#df all
st.markdown('### ข้อมูลทั้งหมด')
df_all = df.drop(['วันที่','เวลา','mgrs'], axis=1)
df_all.set_index('date', inplace=True)
st.write(df_all)







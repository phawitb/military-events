import streamlit as st
import pandas as pd
from mgrs import MGRS
import folium
from streamlit_folium import st_folium
from folium import plugins

st.set_page_config(
    page_title="streamlit-folium documentation: Limit Data Return",
    page_icon="🤏",
    layout="wide",
)

st.markdown('## ปัญหาเส้นเขตแดนด้านเมียนมา')

sheet_id = "1T5xXea-rbuMhCNMalHe-NZa3yPVxjiOs9LGZV6jBlXs"
sheet_name = "Sheet2"
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

df_isgps = df[df['lat'].notna()]
df_nogps = df[df['lat'].isna()]

df =  df.fillna('-')
df_isgps =  df_isgps.fillna('-')
df_nogps =  df_nogps.fillna('-')

#create map
m = folium.Map(location=[df_isgps['lat'].mean(), df_isgps['lng'].mean()], zoom_start=7)
for index, row in df_isgps.iterrows():
    iframe = f"<h5>พื้นที่ : {row['พื้นที่']}</h5>"
    iframe += f"<h5>หน่วยรับผิดชอบ : {row['หน่วยรับผิดชอบ']}</h5>"  
    iframe += f"<h5>จังหวัด : {row['จังหวัด']}</h5>"    
    iframe += f"<h5>ประเภทปัญหา : {row['ประเภทปัญหา']}</h5>"
    iframe += f"<h5>รายละเอียดเหตุการณ์ : {row['รายละเอียดเหตุการณ์']}</h5>"   
    iframe += f"<h5>หมายเหตุ : {row['หมายเหตุ']}</h5>"
    iframe += f"<img src='{row['ลิ้งค์ภาพ']}' alt='Trulli' style='max-width:100%;max-height:100%'>"
    popup = folium.Popup(iframe, min_width=200, max_width=300)
    folium.Marker(
        [row['lat'], row['lng']], popup=popup, tooltip=row['พื้นที่']
    ).add_to(m)

plugins.Fullscreen(                                                         
    position = "topleft",                                   
    title = "Open full-screen map",                       
    title_cancel = "Close full-screen map",                      
    force_separate_button = True,                                         
).add_to(m) 

satellite_tiles = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
folium.TileLayer(tiles=satellite_tiles, attr="Esri World Imagery", name="Satellite").add_to(m)
# folium.TileLayer(tiles='Stamen Terrain',name="Satellite2").add_to(m)
folium.LayerControl(position='topleft').add_to(m)


c1, c2 = st.columns(2)
with c1:
    output = st_folium(
        m, width=700, height=500, returned_objects=["last_object_clicked"]
    )
with c2:
    click_data = output['last_object_clicked']
    if click_data:
        df2 = df_isgps[(df_isgps['lat']==click_data['lat']) & (df_isgps['lng']==click_data['lng'])]
        df2.set_index('พิกัด', inplace=True)
        st.write(df2.iloc[0])

        st.image(df2.iloc[0]['ลิ้งค์ภาพ'],use_column_width='auto')
        # 

        # TABS = st.tabs(df2.index.tolist())

        # for i in range(len(TABS)):
        #     TABS[i].dataframe(df2.iloc[i],use_container_width=True)

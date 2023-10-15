import pandas as pd
import requests
import io
import streamlit as st
from mgrs import MGRS
import folium
from streamlit_folium import st_folium

def get_data(province):
    # province = 'nonthaburi'
    url = f'https://raw.githubusercontent.com/phawitb/crawler-led3-window/main/df_{province}.csv'
    response = requests.get(url)
    df = pd.read_csv(io.StringIO(response.text))
    return df

province = 'nonthaburi'
df = get_data(province)
# st.write(df)

df_isgps = df[df['lat'].notna()]
df_nogps = df[df['lat'].isna()]

st.write(df_isgps)
st.write(df_nogps)
# null_values = df.isnull().sum()
# st.write(null_values)




#create map
m = folium.Map(location=[df_isgps['lat'].mean(), df_isgps['lon'].mean()], zoom_start=7)
for index, row in df_isgps.iterrows():
    # iframe = row['sell_order'] + row['case_id']
    # popup = folium.Popup(iframe, min_width=200, max_width=300)

    htm = ""

    # if row['lat']:
    #     decimal_coordinates = (row['lat'], row['lon'])
    #     formatted_coordinates = format_coordinates(*decimal_coordinates)
    #     map_url = f"https://www.google.com/maps/place/{formatted_coordinates}/@{row['lat']},{row['lon']},17z"
    
    try:
        htm += f"<h2>{row['type']}</h2>"
    except:
        pass
    try:
        htm += f"<h5><a href={map_url} target='_blank'>{row['tumbon']},{row['aumper']},{row['province']}</a></h5>"
    except:
        pass
    try:
        htm += f"<h5>{A}</h5>"
    except:
        pass
    try:
        txt = f"นัด{int(row['bid_time'])} : {datetime.datetime.strptime(str(int(row['lastSta_date'])), '%Y%m%d').strftime('%d/%m/%Y')} {row['lastSta_detail']}"
        if '-' in txt:
            c = 'green'
            fill_opacity = 0.8
        else:
            c = 'red'
            fill_opacity = 0.3
            fill_color = 'black'
        htm += f'<h5 style="color: {c};">{txt}</h5>'
    except:
        pass
    try:
        htm += f"<h5>{row['status']}</h5>"
    except:
        pass
    try:
        htm += f"<h4><a href='{row['link']}' target='_blank'>{'{:,}'.format(int(row['max_price']))}</a></h4>"
    except:
        pass
    try:
        htm += f"<img src='{row['img0']}' alt='Trulli' style='max-width:100%;max-height:100%'>"
    except:
        pass

    # row['user_id'] = st.session_state["current_id"]
    # row['province_eng'] = st.session_state["selected_province"]

    # ROW = {
    #     'user_id' : row['user_id'],
    #     'province_eng' : row['province_eng'],
    #     'link' : row['link']
    # }
    # encoded_text = base64.b64encode(json.dumps(ROW).encode('utf-8'))
    # encoded_text = base64.b64encode(json.dumps(dict(row)).encode('utf-8'))
    # htm += f"<h4><a href=http://localhost:8503/-/?name={encoded_text} target='_blank'>⭐</a></h4>"
    # htm += f"<h4><a href=https://ledmap.streamlit.app/api/?name={encoded_text} target='_blank'>⭐</a></h4>"

    

    popup=folium.Popup(htm, max_width=400)


    marker = folium.Circle(popup=popup,location=[float(row['lat']), float(row['lon'])], radius=200,weight=2, fill=True, color='red',fill_color='yellow',fill_opacity=1)
    marker.add_to(m)

    # folium.Marker(
    #     [row['lat'], row['lon']], popup=popup, tooltip=iframe
    # ).add_to(m)

c1, c2 = st.columns(2)
with c1:
    output = st_folium(
        m, width=700, height=500, returned_objects=["last_object_clicked"]
    )
with c2:
    click_data = output['last_object_clicked']
    if click_data:
        df2 = df_isgps[(df_isgps['lat']==click_data['lat']) & (df_isgps['lon']==click_data['lng'])]
        df2.set_index('link', inplace=True)

        TABS = st.tabs(df2.index.tolist())

        for i in range(len(TABS)):
            TABS[i].dataframe(df2.iloc[i],use_container_width=True)


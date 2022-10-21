import folium
import pandas

volcano=pandas.read_csv("Volcanoes.txt")
name=list(volcano["NAME"])
elev=list(volcano["ELEV"])
type=list(volcano["TYPE"])
lat=list(volcano["LAT"])
lon=list(volcano["LON"])

html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%s%%20volcano" target="_blank">%s</a><br>
Height: %s m<br>
Type: <a href="https://www.google.com/search?q=%s" target="_blank">%s</a>
"""


def volcano_color(elev):
    if elev<1000:
        return "green"
    elif 1000<=elev<3000:
        return "yellow"
    else:
        return "red"

map = folium.Map(location=[38,-120], zoom_start=6,tiles='Stamen Terrain')
featuregroup_vol=folium.FeatureGroup(name="Volcano")
for la,lo,nam,ele,typ in zip(lat,lon,name,elev,type):
    iframe = folium.IFrame(html=html % (nam, nam, str(ele), typ, typ), width=200, height=100)
    featuregroup_vol.add_child(folium.CircleMarker(location=[la,lo], radius=6,
                                                 popup=folium.Popup(iframe), fill_color=volcano_color(ele),
                                                 color="green", fill_opacity=0.7))
featuregroup_pop = folium.FeatureGroup(name='Population')
featuregroup_pop.add_child(folium.GeoJson(data=open('world.json', 'r', encoding= 'utf-8-sig ').read(),
style_function= lambda x: {'volcano_color':"green" if x['properties']['POP2005'] < 10000000
else "yellow" if 10000000<=x['properties']['POP2005']<20000000 else "red"}))


map.add_child(featuregroup_pop)
map.add_child(featuregroup_vol)
map.add_child(folium.LayerControl())
map.save("Map.html")

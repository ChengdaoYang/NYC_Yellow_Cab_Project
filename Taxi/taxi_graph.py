import networkx as nx
import pandas as pd
import geopandas as gpd
import numpy as np


import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly import tools


import shapefile
from shapely.geometry import Polygon
from descartes.patch import PolygonPatch

import matplotlib as mpl
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.pyplot import figure



######## Parameters #########

# please use you own mapbox token(acount) @ https://www.mapbox.com/
with open('/Users/chengdaoyang/Documents/Personal/Token/mapbox') as fp:
    mapbox_access_token = fp.readline()

center_lon = -73.97
center_lad = 40.71
zoom = 9.44

######## Parameters #########



######## Function Start ########
def graph_path(path):

    """
    graph_path draw straight line (edges) to represent a path or route
    of a taxi on NYC, between the TLCs zone center using NYC TLC data
    a interactive iplotly map via mapbox

    Args:
        path (list): list of zones as path
    
    Returns:
        None
        ' function simple graph a plotly grooh object
    """

    # Loading NYC TLC zone info
    taxi_zone_map = gpd.read_file('./Matrix/taxi_zones/taxi_zones.shp')
    taxi_zone_map_geo = taxi_zone_map.to_crs(epsg=4326)  # EPSG4326=WGS84 https://epsg.io/4326

    # create networkx Graph
    G=nx.Graph()
    
    # adding TLC zones' centriod as node to Graph and its lon lat cordinates
    for i in range(taxi_zone_map_geo.shape[0]):
        G.add_node(i, pos=(taxi_zone_map_geo['geometry'][i].centroid.xy[0][0],
                          taxi_zone_map_geo['geometry'][i].centroid.xy[1][0]))

    G.add_path(path) # add the taxi route as edges in Graph
    
    # create GeoJson objects to draw path on the map
    map_path = []
    for u in path:
        map_path.append(list(G.node[u]['pos']))
    
    the_geojson_type_dict = {
        "type": "LineString",
        "coordinates": map_path
    }

    # create zone object as scatter in the map
    zones = [
    go.Scattermapbox(
        lon=[str(taxi_zone_map_geo['geometry'][i].centroid.xy[0][0]) 
            for i in range(taxi_zone_map_geo.shape[0])],
        lat=[str(taxi_zone_map_geo['geometry'][i].centroid.xy[1][0]) 
            for i in range(taxi_zone_map_geo.shape[0])],
#         lon = [str(taxi_zone_map_geo['geometry'][i].centroid.xy[0][0]) for i in path ],
#         lat = [str(taxi_zone_map_geo['geometry'][i].centroid.xy[1][0]) for i in path ],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=4
        ),
        text=[f'zone{i}' for i in taxi_zone_map_geo.index],
        )
    ]
    path_zones = [
        go.Scattermapbox(
    #         lon=[str(taxi_zone_map_geo['geometry'][i].centroid.xy[0][0]) for i in range(taxi_zone_map_geo.shape[0])],
    #         lat=[str(taxi_zone_map_geo['geometry'][i].centroid.xy[1][0]) for i in range(taxi_zone_map_geo.shape[0])],
            lon = [str(taxi_zone_map_geo['geometry'][i].centroid.xy[0][0]) for i in path ],
            lat = [str(taxi_zone_map_geo['geometry'][i].centroid.xy[1][0]) for i in path ],
            mode='markers',
            marker=go.scattermapbox.Marker(
                size=14
            ),
            text=[f'zone{i}' for i in path],
        )
    ]
    
    
    # add the GeoJson path object as a layer offline
    layers=[dict(sourcetype = 'geojson',
             source =the_geojson_type_dict,
             color='rgb(5,170,35)',
             type = 'line',
             line=dict(width=4.5),
       )
         ]  
         
    # setting figure layout
    layout = dict(
    title="NYC zone to zone path",
    autosize=False,
    width=1000,
    height=800,
    hovermode='closest',
    
    # mapbpx info
    mapbox=dict(
        accesstoken=mapbox_access_token,
        layers=layers,
        bearing=0,
        pitch=0,
        center=go.layout.mapbox.Center(
                lon=center_lon,
                lat=center_lad
            ),
        zoom=zoom,
        #style='light'
    )
    )
    
    # plot
    fig = go.Figure(data=zones + path_zones, layout=layout)
    iplot(fig, filename='NYC_path')
    
    return None



def graph_nx(G):
     
    '''graph_nx draw a networkx Graph object
    by plotly.

    Args:
        G (networkx Garph): must has node and node's position 
            stored as an attribute of Graph's node, with attri
            named as 'pos'

    Return:
        None
        'simply graph a plotly object'
    '''


    edge_trace = go.Scatter(
        x=[],
        y=[],
        line=dict(width=0.5,color='#888'),
        hoverinfo='none',
        mode='lines')
    
    for edge in G.edges():
        x0, y0 = G.node[edge[0]]['pos']
        x1, y1 = G.node[edge[1]]['pos']
        edge_trace['x'] += tuple([x0, x1, None])
        edge_trace['y'] += tuple([y0, y1, None])
    
    node_trace = go.Scatter(
        x=[],
        y=[],
        text=[],
        mode='markers',
        hoverinfo='text',
        marker=dict(
            showscale=True,
            # colorscale options
            #'Greys' | 'YlGnBu' | 'Greens' | 'YlOrRd' | 'Bluered' | 'RdBu' |
            #'Reds' | 'Blues' | 'Picnic' | 'Rainbow' | 'Portland' | 'Jet' |
            #'Hot' | 'Blackbody' | 'Earth' | 'Electric' | 'Viridis' |
            colorscale='YlGnBu',
            reversescale=True,
            color=[],
            size=10,
            colorbar=dict(
                thickness=15,
                title='Node Connections',
                xanchor='left',
                titleside='right'
            ),
            line=dict(width=2)))
    
    for node in G.nodes():
        x, y = G.node[node]['pos']
        node_trace['x'] += tuple([x])
        node_trace['y'] += tuple([y])

    return None


######## Function End ########

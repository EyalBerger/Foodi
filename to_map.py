import pandas as pd
import numpy as np
import gmplot
from matplotlib import colors as mcolors

def draw_map(api_key, data, center, best_results, map_name):

    ### This function draws a google maps map of best volunteers allocation.
    ### Each volunteers group colored differntly with polylines representing the suggested points order per group.

    # @param api_key - String of google api key
    # @param data - Pandas DataFrame with columns of point's names, addresses, latitudes & longitudes
    # @param center - Dictionary with Center point name, address, latitude & longitude
    # @param best_results - Dictionary of the best volunteers allocation, with group numbers as Keys and lists of points names per group as Items
    # @param map_name - html file name for the map output
    # @retruns Series of groups colors per point in data


    gmap = gmplot.GoogleMapPlotter(data.Lat.mean(), data.Lng.mean(), 16, apikey=api_key)
    gmap.coloricon = "http://www.googlemapsmarkers.com/v1/%s/"

    # set colors for map points
    best_colors = ['blue', 'red', 'pink', 'green', 'purple', 'yellow', 'black', 'gray', 'white', 'brown']
    colors = best_colors + [c for c in list(mcolors.CSS4_COLORS.keys()) if c not in best_colors]
    colors = colors[:len(best_results['allocation']) + 1]

    names = data.Name.tolist()
    latitudes = data.Lat.tolist()
    longitudes = data.Lng.tolist()
    addresses = data.google_address.tolist()

    gmap.marker(center['Lat'], center['Lng'], color=colors[0], title=center['google_address'])

    data['color'] = np.nan

    for group, color in zip(best_results['allocation'], colors[1:]):
        group_names = best_results['allocation'][group][1:]
        for name in group_names:
            name_ix = names.index(name)
            name_lat, name_lng = latitudes[name_ix], longitudes[name_ix]

            gmap.marker(name_lat, name_lng, color=color,
                        title=addresses[name_ix].split(',')[0])

            if group_names.index(name) == 0:
                gmap.polygon([center['Lat'], name_lat],
                             [center['Lng'], name_lng], color=color)
            else:
                prev_name = group_names[group_names.index(name) - 1]
                prev_name_ix = names.index(prev_name)
                prev_name_lat, prev_name_lng = latitudes[prev_name_ix], longitudes[prev_name_ix]
                gmap.polygon([prev_name_lat, name_lat],
                             [prev_name_lng, name_lng], color=color)

        data['color'] = np.where(data.chosen_group == group, color, data.color)

    gmap.draw(map_name)

    return data['color']

import pandas as pd
import googlemaps

def set_distances(api_key, names_by_weeks, data, city, country, departure_time):

    ### This function is calculating the driving distance & duration between each two points
    ### on the uploaded file relatad to the same week, using googlemaps api

    # @param @api_key - String of google api key
    # @param @names_by_weeks - Dictionary with names (Lists) by weeks (Keys) of the points
    # @param @data - Pandas DataFrame with columns of point's names & addresses
    # @param @city - String of the city name of all points in the file
    # @param @country - String of the country name of all points in the file
    # @param @departure_time - Datetime of the next food baskets distribution
    # @returns Dictionary with names as Keys. Items are lists of tuples in the form of
    # (name, googlemaps results in one item list dictionary), orderd by driving duration

    gmaps = googlemaps.Client(key=api_key)

    names = data.Name.tolist()

    addresses = [", ".join([address, city, country]) for address in data.Address.tolist()]

    distance_matrix = {}

    for week in names_by_weeks:
        for base_name in names_by_weeks[week]:
            distance_matrix[base_name] = {}
            for destination_name in names_by_weeks[week]:
                if destination_name != base_name:
                    base_name_ix = names.index(base_name)
                    destination_name_ix = names.index(destination_name)
                    gmaps_res = gmaps.directions(origin=addresses[base_name_ix],
                                         destination=addresses[destination_name_ix],
                                         transit_mode='driving',
                                         departure_time=departure_time.timestamp())

                    distance_matrix[base_name][destination_name] = gmaps_res

            distance_matrix[base_name] = sorted(distance_matrix[base_name].items(),
                                                key=lambda x: x[1][0]['legs'][0]['duration_in_traffic']['value'])

    return distance_matrix



def get_center_distances(api_key, center, data, city, country, departure_time):

    ### This function is calculating the driving distance & duration between the center point and each point
    ### on the uploaded file, using googlemaps api

    # @param @api_key - String of google api key
    # @param @center - Dictionary with Center point name & address
    # @param @data - Pandas DataFrame with columns of point's names & addresses
    # @param @city - String of the city name of all points in the file
    # @param @country - String of the country name of all points in the file
    # @param @departure_time - Datetime of the next food baskets distribution
    # @returns Dictionary with names as Keys. Items are googlemaps results in one item list dictionary

    gmaps = googlemaps.Client(key=api_key)

    names = data.Name.tolist()

    addresses = [", ".join([address, city, country]) for address in data.Address.tolist()]

    center_address = ", ".join([center['Address'], city, country])

    center_distances = {}

    for name in names:
        name_ix = names.index(name)
        gmaps_res = gmaps.directions(origin=center_address,
                             destination=addresses[name_ix],
                             transit_mode='driving',
                             departure_time=departure_time.timestamp())

        center_distances[name] = gmaps_res

    return center_distances
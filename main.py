import pandas as pd

import distance_functions
import allocation_calc
import my_tools
import to_map

################ Start settings #############################

api_key = "***************************" #google developers api key

file = 'Foodi_example.xlsx' # data & settings file (see README file for further information)

################ Code #############################

##get data
data = pd.read_excel(file, names=['Week','Name','Address'], sheet_name='data')

#print (data.head())


## get settings

basic_settings = pd.read_excel(file, sheet_name='basic_settings')

city = basic_settings[basic_settings.name == 'distribution_city'].set_to.values[0].strip()
country = basic_settings[basic_settings.name == 'distribution_country'].set_to.values[0].strip()

center = {'Name': basic_settings[basic_settings.name == 'distribution_center_Name'].set_to.values[0].strip(),
         'Address': basic_settings[basic_settings.name == 'distribution_center_Address'].set_to.values[0].strip()}

weekday = basic_settings[basic_settings.name == 'distribution_weekday'].set_to.values[0].strip()
time = basic_settings[basic_settings.name == 'distribution_time'].set_to.values[0]

iterations = basic_settings[basic_settings.name == 'iterations'].set_to.values[0]
score = basic_settings[basic_settings.name == 'score'].set_to.values[0].strip()


groups_settings = pd.read_excel(file, sheet_name='groups_settings')

groups_size = {}
for week in groups_settings['week']:
    groups = groups_settings[groups_settings['week'] == week].group_size.tolist()
    groups_size[week.strip()] = groups

##check that groups_size dictionary fits the uploaded file
my_tools.groups_size_check(data.Week, groups_size)

##set departure_time by weekday and time
departure_time = my_tools.find_next_weekday(weekday, time)

#print (departure_time)

##set names_by_weeks Dict
names_by_weeks = my_tools.set_names_by_weeks(data)

##get distances between all the points and between the points and the center point
distance_matrix = distance_functions.set_distances(api_key,
                                                   names_by_weeks,
                                                   data,
                                                   city, country, departure_time)

center['center_distances'] = distance_functions.get_center_distances(api_key,
                                                                     center,
                                                                     data,
                                                                     city, country, departure_time)

center['google_address'] = center['center_distances'][list(center['center_distances'].keys())[0]][0]['legs'][0]['start_address'][0].split(',')[0]

center['Lat'] = \
    center['center_distances'][list(center['center_distances'].keys())[0]][0]['legs'][0]['start_location']['lat']
center['Lng'] = \
    center['center_distances'][list(center['center_distances'].keys())[0]][0]['legs'][0]['start_location']['lng']

## calcs the best volunteers allocation

res = allocation_calc.find_best_allocation(names_by_weeks,
                                           groups_size,
                                           distance_matrix,
                                           center,
                                           iterations,
                                           score)

print (res[0][1]['allocation'])
#print (res)

## add results to data DataFrame

data['google_address'] = data.apply(lambda point: distance_matrix[point.Name][0][1][0]['legs'][0]['start_address'], axis=1)
data['Lat'] = data.apply(lambda point: distance_matrix[point.Name][0][1][0]['legs'][0]['start_location']['lat'], axis=1)
data['Lng'] = data.apply(lambda point: distance_matrix[point.Name][0][1][0]['legs'][0]['start_location']['lng'], axis=1)

data['chosen_group'] = data.apply(lambda point: allocation_calc.set_best_allocation(point.Name, res[0][1], ret='chosen_group'),axis=1)
data['chosen_route'] = data.apply(lambda point: allocation_calc.set_best_allocation(point.Name, res[0][1], ret='chosen_route'),axis=1)
data['total_duration_minutes'] = data.apply(lambda point: allocation_calc.set_best_allocation(point.Name, res[0][1], ret='duration'),axis=1)


## draw a map of best volunteers allocation and add group color to data DataFrame

map_name = ".".join([file.split('.')[0] + '_map', 'html'])

data['color'] = to_map.draw_map(api_key, data, center, res[0][1], map_name)


## send results to Excel

data.to_excel(".".join([file.split('.')[0] + '_results', file.split('.')[1]]))



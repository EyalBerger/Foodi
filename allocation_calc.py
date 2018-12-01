import pandas as pd
import numpy as np

def find_closest_path(name, distance_matrix, counter_allocation, used_names, value):

    ### This function finds the closest point to name (which still didn't used in this iteration)
    ### and adds the duration value (seconds) to the total duration of this iteration

    ### @param name - String of point's name
    ### @param distance_matrix - Dictionary with names as Keys. Items are lists of tuples in the form of
    ###        (name, googlemaps results in one item list dictionary), orderd by driving duration
    ### @param counter_allocation - List of points representing a path in the checked allocation
    ### @param used_names - List of points names that are already allocated in this iteration
    ### @param value - Int of total driving duration (seconds) of this path

    ### @returns counter_allocation
    ### @return used_names
    ### @return value


    for destination_name, route_details in distance_matrix[name]:
        if destination_name not in used_names:
            duration_value = route_details[0]['legs'][0]['duration_in_traffic']['value']
            value = value + duration_value
            counter_allocation.append(destination_name)
            used_names.append(destination_name)
            break

    return counter_allocation, used_names, value


def find_best_allocation(names_by_weeks, groups_size, distance_matrix, center, iterations, score):

    ### This function calculates different volunteers allocations for finding the best allocation
    ### in terms of saving driving time.

    ### @param names_by_weeks - Dictionary with Lists of points names by weeks (Keys)
    ### @param groups_size - Dictionary with Lists of groups sizes by weeks (Keys)
    ### @param distance_matrix - Dictionary with names as Keys. Items are lists of tuples in the form of
    ###        (name, googlemaps results in one item list dictionary), orderd by driving duration
    ### @param center - Dictionary with Center point name, address &
    ###                                 driving duration between the center point and each point in the uploaded file
    ### @param iterations - Int of the number of random iterations for finding the best volunteers allocation
    ### @param score - String of the measure for choosing the best volunteers allocation ('min' or 'average')
    ### @returns List of tuples of iterations results (sorted from the best to worst) in the form of
    ###          (iteration_number, Dictionary of the volunteers allocation, with group numbers as Keys and lists of ordered points names per group as Items)


    iterations_results = {}

    for i in range(iterations):
        allocation = {}
        duration_values = []
        counter = 1

        for week in names_by_weeks:
            names = np.random.permutation(names_by_weeks[week])
            groups = np.random.permutation(groups_size[week])
            start_names = names[:len(groups)]
            used_names = list(start_names)
            for base_name, group_size in zip(start_names, groups):
                allocation[counter] = [center['Name'], base_name]
                value = center['center_distances'][base_name][0]['legs'][0]['duration_in_traffic']['value']

                for j in range(group_size - 1):
                    name = allocation[counter][-1:][0]
                    allocation[counter], used_names, value = find_closest_path(name,
                                                                    distance_matrix, allocation[counter],
                                                                    used_names, value)
                duration_values.append(value)
                counter += 1
            del used_names

        iterations_results[i] = {}
        iterations_results[i]['allocation'] = dict(allocation)
        iterations_results[i]['duration_values'] = list(duration_values)

        if score == 'average':
            iterations_results[i]['duration_score'] = np.mean(duration_values)
        elif score == 'min':
            iterations_results[i]['duration_score'] = np.max(duration_values)

        del allocation
        del duration_values
        del counter

    iterations_results = sorted(iterations_results.items(),
                                key=lambda x: x[1]['duration_score'])

    return iterations_results


def set_best_allocation(name, best_results, ret='chosen_group'):

    ### This function sets the chosen_group, chosen_route & total_duration for point,
    ### according to the best allocation results.

    ### @param name - String of point's name
    ### @param best_results - Dictionary of the best volunteers allocation, with group numbers as Keys and lists of points names per group as Items
    ### @param ret - String of the chosen returnd value - 'chosen_group' (default), 'chosen_route' or 'duration'
    ### @returns chosen group, chosen route or total driving duration in minutes


    for group, duration in zip(best_results['allocation'], best_results['duration_values']):
        group_names = best_results['allocation'][group][1:]
        if name in group_names:
            chosen_group = group
            chosen_route = "_".join(best_results['allocation'][group])
            total_duration_minutes = int(round(duration/60,0))
            break

    if ret=='chosen_route':
        return chosen_route
    elif ret=='chosen_group':
        return chosen_group
    elif ret=='duration':
        return total_duration_minutes
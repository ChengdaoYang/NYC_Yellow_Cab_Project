import numpy as np
import networkx as nx
import pandas as pd

## Loading data




######## Function Start ########

def Greedy_Algorithm(start_zone):
    '''Greedy algorithm search the at each states
    the minimized moving & wait time zone.
    return a path, total_trip_time & total_waste'''
    
    ## loading data
    matrix_PU_time= pd.read_csv('./Matrix/matrix_PU_time.csv',index_col=0)
    matrix_PU_time.columns =matrix_PU_time.columns.astype(float)

    matrix_PU_time.fillna(value=8*60, inplace=True)
    matrix_PU_wait_time = matrix_PU_time.set_index(matrix_PU_time.index.astype(int)).sort_index()
    
    matrix_zone_distance = pd.read_csv('./Matrix/full_zone_distance_matrix.csv',index_col=0)
    matrix_zone_distance.columns =matrix_zone_distance.columns.astype(int)
    matrix_zone_distance.index = matrix_zone_distance.index + 1
    temp_index = matrix_zone_distance.index
    matrix_zone_distance = matrix_zone_distance.T
    matrix_zone_distance.index = temp_index
    ind_dis = set(matrix_zone_distance.iloc[146].index)
    ind_wait_time = set(matrix_PU_wait_time[0].index)
    redundant_zones = list(ind_dis.difference(ind_wait_time))
    matrix_zone_distance = matrix_zone_distance.drop(redundant_zones, axis=1).drop(list(map(int, redundant_zones)))
    matrix_zone_distance[matrix_zone_distance.isna().any(axis=1)]
    
    matrix_prob_PU_DO_t0 = pd.read_csv('./Matrix/matrix_prob_PU_DO_t0.csv', index_col=0)
    matrix_prob_PU_DO_t0.index = matrix_prob_PU_DO_t0.index.astype(int)
    matrix_prob_PU_DO_t0.columns = matrix_prob_PU_DO_t0.columns.astype(int)
    top_dropoff_zone_t0 = pd.DataFrame(matrix_prob_PU_DO_t0.idxmax(axis=1))    

    result_path = list() # path with zone as node
    total_trip_time = 0 # total time that are making $
    total_waste_time = 0 # total time waste in move & wait
    total_time = 24*60 # time of a day
    temp_zone = start_zone # set current zone to starting zone
    
    while total_time >= 0:
        result_path.append(temp_zone)
        # compute highest pro drop off zone
        dropoff_zone = top_dropoff_zone_t0.iloc[temp_zone][0]
        result_path.append(dropoff_zone)
        
        # compute trip_time between pickup and dropoff zone
        dropoff_trip_time =  matrix_zone_distance.iloc[temp_zone,dropoff_zone]
        total_trip_time = total_trip_time + dropoff_trip_time # add trip time to total
        total_time = total_time - dropoff_trip_time # subtract the trip time from the day
        
        # compute moving_time to other zones and the wait time in other zones
        trip_wait_time_table = pd.DataFrame(np.array(matrix_zone_distance.iloc[260])
                                            + np.array(matrix_PU_wait_time[0])).sort_values(by=0)

        # looking for the min 
        local_min_cost_zone = trip_wait_time_table.idxmin()[0]
        local_min_cost_time = trip_wait_time_table.min()[0]
        
        # update current(temp) zone, total_waste time on moving and waiting, and day
        temp_zone = local_min_cost_zone
        total_waste_time = total_waste_time + local_min_cost_time
        total_time = total_time - local_min_cost_time
        
    return result_path, total_trip_time, total_waste_time




def Randomized_Greedy_Algorithm(start_zone, randomness=1, top=20):
    '''Randomized Greedy algorithm search the at each states
    the minimized moving & wait time zone. with some randomness
    return a path, total_trip_time & total_waste
    
    Args:
        start_zone(int): a int represent TLC zones as
        a starting zone of the alg
        
        randomness(float): between 0 and 1 to given some 
        randomness like entropy function, but with 1 the most
        random and 0 == Greedy Alg

        top(int): between 1 and 262 to given some 
        limitation on randomness, 1 == Greedy Alg

    Retrun:
        result_list(list): path of the taxi in a day
        
        total_trip_time(float): total time that taxi is making 
            money i.e. serving customers
        
        total_waste_time(float): time moving and waiting
        '''
    
    
        
    ## loading data
    matrix_PU_time= pd.read_csv('./Matrix/matrix_PU_time.csv',index_col=0)
    matrix_PU_time.columns =matrix_PU_time.columns.astype(float)

    matrix_PU_time.fillna(value=8*60, inplace=True)
    matrix_PU_wait_time = matrix_PU_time.set_index(matrix_PU_time.index.astype(int)).sort_index()
    
    matrix_zone_distance = pd.read_csv('./Matrix/full_zone_distance_matrix.csv',index_col=0)
    matrix_zone_distance.columns =matrix_zone_distance.columns.astype(int)
    matrix_zone_distance.index = matrix_zone_distance.index + 1
    temp_index = matrix_zone_distance.index
    matrix_zone_distance = matrix_zone_distance.T
    matrix_zone_distance.index = temp_index
    ind_dis = set(matrix_zone_distance.iloc[146].index)
    ind_wait_time = set(matrix_PU_wait_time[0].index)
    redundant_zones = list(ind_dis.difference(ind_wait_time))
    matrix_zone_distance = matrix_zone_distance.drop(redundant_zones, axis=1).drop(list(map(int, redundant_zones)))
    matrix_zone_distance[matrix_zone_distance.isna().any(axis=1)]
    
    matrix_prob_PU_DO_t0 = pd.read_csv('./Matrix/matrix_prob_PU_DO_t0.csv', index_col=0)
    matrix_prob_PU_DO_t0.index = matrix_prob_PU_DO_t0.index.astype(int)
    matrix_prob_PU_DO_t0.columns = matrix_prob_PU_DO_t0.columns.astype(int)
    top_dropoff_zone_t0 = pd.DataFrame(matrix_prob_PU_DO_t0.idxmax(axis=1))
    


    random_number = int(-0.2/(.000000000000001-(randomness+0.000001)) +0.812)
    if random_number > 20:
        random_number = 20
    elif random_number < 1:
        random_number = 1
    
    result_path = list() # path with zone as node
    total_trip_time = 0 # total time that are making $
    total_waste_time = 0 # total time waste in move & wait
    total_time = 24*60 # time of a day
    temp_zone = start_zone # set current zone to starting zone
    
    while total_time >= 0:
        result_path.append(temp_zone)
        # compute highest pro drop off zone
        dropoff_zone = top_dropoff_zone_t0.iloc[temp_zone][0]
        result_path.append(dropoff_zone)
        
        # compute trip_time between pickup and dropoff zone
        dropoff_trip_time =  matrix_zone_distance.iloc[temp_zone,dropoff_zone]
        total_trip_time = total_trip_time + dropoff_trip_time # add trip time to total
        total_time = total_time - dropoff_trip_time # subtract the trip time from the day
        
        # compute moving_time to other zones and the wait time in other zones
        trip_wait_time_table = pd.DataFrame(np.array(matrix_zone_distance.iloc[260])
                                            + np.array(matrix_PU_wait_time[0])).sort_values(by=0)

        # looking for the min 
        trip_wait_time_table = trip_wait_time_table[:top].sample(random_number)
        local_min_cost_zone = trip_wait_time_table.idxmin()[0]
        local_min_cost_time = trip_wait_time_table.min()[0]
        
        # update current(temp) zone, total_waste time on moving and waiting, and day
        temp_zone = local_min_cost_zone
        total_waste_time = total_waste_time + local_min_cost_time
        total_time = total_time - local_min_cost_time
        
    return result_path, total_trip_time, total_waste_time




######## Function End ########

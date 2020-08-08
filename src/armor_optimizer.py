import pandas as pd
from tqdm import tqdm
import itertools
from statistics import *

DATA_FILE = r'data\destinyArmor.csv'
# DATA_FILE = r'data\destinyArmorTest.csv'

ARMOR_MAP = {'helmet': 'Helmet',
             'chest_armor': 'Chest Armor',
             'gauntlets': 'Gauntlets',
             'leg_armor': 'Leg Armor'}

# ARMOR_PIN = {}
ARMOR_PIN = {'Helmet': '"6917529161428093246"'}


STATS = {'resilience': {'desired': True},
         'mobility': {'desired': True},
         'recovery': {'desired': True},
         'strength': {'desired': False},
         'intellect': {'desired': False},
         'discipline': {'desired': False}}

def combo_data(df_inv, row):
    ''' runs for each row and returns multiple values at once
    '''

    armor_lu = {}
    for armor in ARMOR_MAP:
        armor_lu[armor] = df_inv[armor].loc[row['{}_id'.format(armor)]]
    return armor_lu

def get_stat_sum(stat, row):
    ''' retrieve a stat from row's combo_data
    '''
    cd = row['combo_data']
    stat_base = '{}_base'.format(stat)
    sum = 0
    for armor in ARMOR_MAP:
        sum += cd[armor][stat_base]
    return sum

def get_inv_name(armor, row):
    ''' return the name value using the id from a dataframe
    '''
    return row['combo_data'][armor]['name']

def get_sub_min(row):
    ''' return the minimum value among the desired stats
    '''
    stats = []
    for stat in STATS:
        if STATS[stat]['desired']:
            stats.append(row[stat])
    return min(stats)

def get_min(row):
    ''' return the minimum value among all stats
    '''
    return min([row[stat] for stat in STATS])

def get_sub_mean(row):
    ''' return the mean value among the desired stats
    '''
    stats = []
    for stat in STATS:
        if STATS[stat]['desired']:
            stats.append(row[stat])
    return mean(stats)

def get_mean(row):
    ''' return the mean value among all stats
    '''
    return mean([row[stat] for stat in STATS])

def get_sub_med(row):
    ''' return the median value among the desired stats
    '''
    stats = []
    for stat in STATS:
        if STATS[stat]['desired']:
            stats.append(row[stat])
    return median(stats)

def get_med(row):
    ''' return the median value among all stats
    '''
    return median([row[stat] for stat in STATS])

def get_sub_total(row):
    ''' return the total among the desired stats
    '''
    stat_sum = 0
    for stat in STATS:
        if STATS[stat]['desired']:
            stat_sum += row[stat]
    return stat_sum

def get_total(row):
    ''' return the total among the all stats
    '''
    stat_sum = 0
    for stat in STATS:
            stat_sum += row[stat]
    return stat_sum

def check_keep(row, armor_id_keep):
    ''' determine if armor should be kept
    '''
    if row.name in armor_id_keep:
        return True
    return False

def main():
    tqdm.pandas()
    df = pd.read_csv(DATA_FILE, index_col=2)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
    df_inv = df[['name', 'type', 'equippable', 'tier', 'power_limit', 'mobility_base', 'resilience_base', 'recovery_base',
                'discipline_base', 'intellect_base', 'strength_base', 'total_base']]

    armor_inv = {}
    for armor in ARMOR_MAP:
        armor_type = ARMOR_MAP[armor]
        query_string = 'equippable == "Titan" & type == "{armor_type}" & (power_limit == "NaN" | power_limit >= 1260)'
        query_string = query_string.format(armor_type = armor_type)
        if armor_type in ARMOR_PIN:
            query_string += ' & Id == "{}"'.format(ARMOR_PIN[armor_type].replace('"', '\\"'))
        else:
            # assumes if not pinned, don't use exotic
            query_string += ' & tier != "Exotic"'
        armor_inv[armor] = df_inv.query(query_string)

    a = []
    for armor in armor_inv:
        a.append(list(armor_inv[armor].index.values))
    armor_combos = list(itertools.product(*a))
    df_ac = pd.DataFrame(armor_combos, columns =['helmet_id', 'chest_armor_id', 'gauntlets_id', 'leg_armor_id']) 

    df_ac['combo_data'] = df_ac.progress_apply(lambda row: combo_data(armor_inv, row), axis=1)
    
    for armor in ARMOR_MAP:
        df_ac['{}_name'.format(armor)] = df_ac.progress_apply(lambda row: row['combo_data'][armor]['name'], axis=1)

    for stat in STATS:
        df_ac[stat] = df_ac.progress_apply(lambda row: get_stat_sum(stat, row), axis=1)

    df_ac['sub_total'] = df_ac.progress_apply(lambda row: get_sub_total(row), axis=1)
    df_ac['total'] = df_ac.progress_apply(lambda row: get_total(row), axis=1)
    df_ac['sub_minimum'] = df_ac.progress_apply(lambda row: get_sub_min(row), axis=1)
    df_ac['minimum'] = df_ac.progress_apply(lambda row: get_min(row), axis=1)
    df_ac['sub_mean'] = df_ac.progress_apply(lambda row: get_sub_mean(row), axis=1)
    df_ac['mean'] = df_ac.progress_apply(lambda row: get_mean(row), axis=1)
    df_ac['sub_median'] = df_ac.progress_apply(lambda row: get_sub_med(row), axis=1)
    df_ac['median'] = df_ac.progress_apply(lambda row: get_med(row), axis=1)
    df_out = df_ac[['helmet_id','chest_armor_id','gauntlets_id','leg_armor_id','helmet_name','chest_armor_name','gauntlets_name',
                    'leg_armor_name','resilience','mobility','recovery','strength','intellect','discipline','sub_total',
                    'total','sub_minimum','minimum','sub_mean','mean','sub_median','median']]
    df_out.to_csv(r'data\out.csv') 

    total_max = df_ac['total'].max()
    total_min = df_ac['total'].min()
    total_mean = df_ac['total'].mean()
    total_75 = ((total_max - total_mean)/2) + total_mean

    query_string = 'total >= {}'
    query_string = query_string.format(total_75)
    df_high = df_ac.query(query_string)

    armor_id_keep = list(set(list(df_high['helmet_id']) + list(df_high['chest_armor_id']) + list(df_high['gauntlets_id']) + list(df_high['leg_armor_id'])))

    query_string = 'equippable == "Titan" & tier != "Exotic"'
    armor_inv = df_inv.query(query_string)
    armor_inv['keep'] =  armor_inv.progress_apply(lambda row: check_keep(row, armor_id_keep), axis=1) 
    armor_inv.to_csv(r'data\keep_trash.csv') 

    df_ac.head(10)
    df_ac.loc(0)

if __name__ == '__main__':
    main()
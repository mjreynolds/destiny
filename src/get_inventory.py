import pandas as pd
from tqdm import tqdm
# import itertools
# from statistics import *

DATA_FILE = r'data\destinyWeapons.csv'
# DATA_FILE = r'data\destinyArmorTest.csv'

godrolls = {'Auto Rifle': {'stats': ['Range', 'Stability'],
                           'perks': ['Outlaw', 'Kill Clip', 'Rampage', 
                                     'High-Impact Reserves']},
            'Combat Bow': {'stats': ['Accuracy', 'Draw Time'],
                           'perks': ["Archer's Tempo", 'Rampage']},
            'Fusion Rifle': {'stats': ['Range', 'Stability'],
                             'perks': ['Rangefinder', 'Backup Plan', 'Rampage']},
            'Grenade Launcher': {'stats': ['Blast Radius', 'Reload'],
                                 'perks': ['Quickdraw', 'Rampage', 'Proximity Grenades']},
            'Hand Cannon': {'stats': ['Range', 'Reload'],
                            'perks': ['Outlaw', 'Drop Mag', 'Kill Clip', 'Rampage']},
            'Linear Fusion Rifle': {'stats': ['Range', 'Charge Time'],
                                    'perks': ['Quickdraw', 'Snapshot Sights']},
            'Machine Gun': {'stats': ['Range', 'Stability'],
                            'perks': ['Outlaw', 'Rampage', 'Kill Clip', 
                                      'Zen Moment', 'Moving Target']},
            'Pulse Rifle': {'stats': ['Range', 'Stability'],
                            'perks': ['Rampage', 'Kill Clip', 'Outlaw']},
            'Rocket Launcher': {'stats': ['Blast Radius', 'Velocity', 'Reload'],
                                'perks': ['Cluster Bombs', 'Quickdraw', 'Tracking Module']},
            'Scout Rifle': {'stats': ['Range'],
                            'perks': ['Outlaw', 'Kill Clip', 'Dragonfly']},
            'Shotgun': {'stats': ['Range', 'Stability', 'Low Magnification'],
                        'perks': ['Snapshot Sights', 'Outlaw', 'Kill Clip']},
            'Sidearm': {'stats': ['Range', 'Stability'],
                        'perks': ['Rangefinder', 'Moving Target', 'Kill Clip']},
            'Sniper Rifle': {'stats': ['Range', 'Stability', 'Low Magnification'],
                             'perks': ['Snapshot Sights', 'Outlaw', 'Kill Clip']},
            'Submachine Gun': {'stats': ['Range', 'Stability'],
                               'perks': ['Outlaw', 'Rampage', 'Kill Clip', 
                                         'Zen Moment', 'Moving Target']},
            'Sword': {'stats': ['Impact', 'Range'],
                      'perks': ['Relentless Strikes', 'Whirlwind Blade']},
            'Trace Rifle': {},
            'Cold Denial': {'type': 'Pulse Rifle',
                            'perks': ['Smallbore', 'Ricochet Rounds',
                                      'Killing Wind', 'Swashbuckler']},
            'Falling Guillotine': {'type': 'Sword',
                                   'perks': ['Jagged Edge', 'Burst Guard',
                                             'Relentless Strikes', 'Whirlwind Blade']},
            'Death Adder': {'type': 'Submachine Gun',
                            'perks': ['Polygonal Rifling', 'Tactical Mag', 
                                      'Feeding Frenzy', 'Quickdraw', 'Dragonfly']},
            'IKELOS_SMG_v1.0.2': {'type': 'Submachine Gun',
                                  'perks': ['Corkscrew Rifling', 'Tactical Mag', 
                                            'Dynamic Sway Reduction', 'Vorpal Weapon']},
            'Truthteller': {'type': 'Grenade Launcher',
                            'perks': ['Linear Compensator', 'Proximity Grenades',
                                      'Auto-Loading Holster', 'Disruption Break']},                                      
            'Gnawing Hunger': {'type': 'Auto Rifle',
                               'perks': ['Arrowhead Break', 'Tactical Mag'
                                         'Subsistence', 'Multikill Clip']},
            'Nature of the Beast': {'type': 'Hand Cannon',
                                    'perks': ['Hitmark HCS', 'Accurized Rounds',
                                              'Quickdraw', 'Vorpal Weapon',
                                              'Demolitionist']},
            'IKELOS_SG_V1.0.2': {'type': 'Shotgun',
                                 'perks': ['Full Bore', 'Accurized Rounds',
                                           'Firmly Planted', 'Vorpal Weapon']},
            "Widow's Bite": {'type': 'Sniper Rifle',
                             'perks': ['Arrowhead Break', 'Tactical Mag', 
                                       'Slideshot', 'Opening Shot']},
            'Long Shadow': {'type': 'Sniper Rifle',
                            'perks': ['ATC Rex', 'Tactical Mag',
                                      'Snapshot Sights', 'Moving Target']}         
}

def main():
    tqdm.pandas()
    df = pd.read_csv(DATA_FILE, index_col=2)
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

if __name__ == '__main__':
    main()
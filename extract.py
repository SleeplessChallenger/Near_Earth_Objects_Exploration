"""

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

"""
import csv
import json
from pathlib import Path

from csv import DictReader
from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """Read near-Earth object information from a CSV file"""

    result = []
    with open(neo_csv_path, 'r') as file:
        reader = DictReader(file)
        for x in reader:
            result.append(NearEarthObject(designation = x['pdes'], name = x['name'], 
                            hazardous = x['pha'], diameter = x['diameter']))

    return result



def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.
    """


    bucket = []
    with open(cad_json_path, 'r') as file2:
        data = json.load(file2)
        for x in data['data']:
            bucket.append(CloseApproach(x[0], time = x[3], 
                                        distance = float(x[4]), velocity = float(x[7])))
    return bucket







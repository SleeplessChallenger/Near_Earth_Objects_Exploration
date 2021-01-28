"""

The main module calls these functions with the arguments provided at the command
line, and uses the resulting collections to build an `NEODatabase`.

"""
import csv
import json
from pathlib import Path

# Path(r'/Users/daniilslobodenuk/Desktop/Udacity/nd303-c1-advanced-python-techniques-project-starter/data/neos.csv')



from models import NearEarthObject, CloseApproach


def load_neos(neo_csv_path):
    """
        if you know only file name then use the following code:
            path = Path('file')
            result = path.resolve()
        or next one:
            path = Path.cwd() / 'file'
    """
    with open(neo_csv_path, 'r') as file:
        reader = list(csv.reader(file))
        with open('neo_ready.csv', 'w') as file2:
            writer = csv.writer(file2)
            for x in reader:
                writer.writerow([x[3], x[4], x[7], x[15]])

        return writer

# load_neos('/Users/daniilslobodenuk/Desktop/Udacity/nd303-c1-advanced-python-techniques-project-starter/data/neos.csv')


def load_approaches(cad_json_path):
    """Read close approach data from a JSON file.

    :param neo_csv_path: A path to a JSON file containing data about close approaches.
    :return: A collection of `CloseApproach`es.
    """
    with open(cad_json_path, 'r') as fl:
        content = json.load(fl)
        data1 = content['fields']
        data2 = content['data']
        dct = {}
        with open('cad_ready.json', 'w') as fl2:
            for x in range(len(data1)):
                if x == 0 or x == 3 or x == 4 or x == 7:
                    dct[data1[x]] = []
            for obj in data2:
                for var in range(len(obj)):
                    if var == 0:
                        dct['des'].append(obj[var])
                    if var == 3:
                        dct['cd'].append(obj[var])
                    if var == 4:
                        dct['dist'].append(obj[var])
                    if var == 7:
                        dct['v_rel'].append(obj[var])
            json.dump(dct, fl2)
        return dct

load_approaches('/Users/daniilslobodenuk/Desktop/Udacity/nd303-c1-advanced-python-techniques-project-starter/data/cad.json')







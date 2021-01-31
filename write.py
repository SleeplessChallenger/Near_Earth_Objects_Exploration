
import csv
import json
from csv import DictReader, DictWriter


def write_to_csv(results, filename):

    #1)'results' is data from limit (actually, list)
    #2)'filename' is Path which User specifies
    #3) to lessen the filesize let's use serialize()

    headers = ('datetime_utc', 'distance_au', 'velocity_km_s', 'designation', 'name', 'diameter_km', 'potentially_hazardous')
    with open(filename, 'w') as fl:
        writer = DictWriter(fl, fieldnames = headers)
        writer.writeheader()
        for obj in results:
            NeoD = obj.neo.serialize()
            ApprD = obj.serialize()
            #As data after serialize() will be in dict format, we are to use ** and merge via {}
            merged = {**NeoD, **ApprD}
            merged.pop('neo')
            writer.writerow(merged)
    
     

  
def write_to_json(results, filename):
    compressed_data = [data.serialize() for data in results]
    with open(filename, 'w') as file:
        json.dump(compressed_data, file, indent = 2)


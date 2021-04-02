# Near_Earth_Objects_Exploration


<h2>In this project Python allows to scrutinize various space objects' data taken from <i>NASA official site</i> </h2>

There are 7 files that will take data from csv & json, match the required parameters in Terminal. main.py is the glue of all the files as it connects them together. Also, requirements.txt was added so as you can install all the required packages.
The project is PEP 8 compliant and was checked with **pycodestyle**

<h3>For precise notes & explanation, please, look into files and <i># or ''' '''</i> things</h3>

1. extract.py will take data from csv & json, unpack it and provide into models.py 

2. models.py has 2 Classes: NearEarthObjects and CloseApproaches. They have one-to-many relationship where on one NearEarthObjects
there can be multiple CloseApproaches => former has self.approaches as list() to keep latter. And CloseApproaches is linked with upper class
via .neo

3. database.py is essential as it encapsulates two clases above, in other words the whole dataset. It has NEODatabase class which implements mentioned in the previous sentence feature. Also it enables user filters to work, i.e. query the dataset in other words by query(). Makes possible NearEarthObjects and CloseApproaches by designation or name retrieved. 

4. filters.py has cornucopia of filters which are input by users and are applied on NEODatabase in database.py. It has limit() function which put a constraint on the output as our dataset is very big.

5. write.py will write generated data from NEODatabase to either csv or json file.

*If you want more indepth walk by check a little bit below


**Notice**
In data folder I've uploaded shortened versions of .json and .csv
so as to ease testing. Otherwise, it took eternity to load all the data.


Commands to enter for testing:
`python3 main.py inspect --pdes 433` 
`python3 main.py inspect --verbose --name Ganymed`
have matching

`python3 main.py inspect --name Halley`
doesn't have one


**Some additional clarifications**
1) main.py triggers NEODatabase(load_neos(args.neofile), load_approaches(args.cadfile)) in database.py
2) .csv and .json firstly go into models.py and then into database.py
3) in models.py data is tweaked by classes and then *tweaked* data gets appended to *result* and *bucket*.
4) Then *result* and *bucket* find themselves into database.py 


**Explanation of the underhood of *filters.py*:**


1)User inputs some filter data like years, distance etc

2)filter() invokes some inherit class =>

operator is attached to 'op' and user's value is attached to 'value'

3)'get' in inherit class overrides the one in super class

=> otherwise Error is triggered. 'get' takes particular instance

of the CloseApproach instance or by .neo references NearEarthObject

4)__call__ is triggered: that 'op' from above, compares CloseApproach's attribute and 'value'

returning bool outcome

```bash
.
├── README.md
├── __pycache__
│   ├── database.cpython-37.pyc
│   ├── extract.cpython-37.pyc
│   ├── filters.cpython-37.pyc
│   ├── helpers.cpython-37.pyc
│   ├── models.cpython-37.pyc
│   └── write.cpython-37.pyc
├── data
│   ├── cad.json
│   └── neos.csv
├── database.py
├── extract.py
├── filters.py
├── helpers.py
├── main.py
├── models.py
└── write.py
```


# Near_Earth_Objects_Exploration


<h2>In this project Python allows to scrutinize various space objects' data taken from <i>NASA official site</i> </h2>

There are 7 files that will take data from csv & json, match the required parameters in Terminal. main.py is the glue of all the files as it connects them together. Also, **requirements.txt** was added so as you can install all the required packages.
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

1. At first, `main.py` triggers `create_filters(arguments...)` where filters from command line are supplied.

2. `filters.py -> create_filters()` will generate a list of filters that are classes: `filters` variable in main.py looks like [Date(op=operator.eq, value=2020-01-01)]. Where `op` will take place of `self.op` and `value` will be `self.value`. Due to the fact that Date/Distance etc classes are inherited ones => aforewritten stuff will go smoothly. 

3. Hence, `filters` variable in `main.py` is a list of `AttributeFilter` classes. It is supplied to `database.query(filters)`. `map(lambda x: x(approach), filters)` spits out something like [False], [True] etc, then there is a check that every thing in `temp` is True else skip this approach. 

**Note:** `map(lambda x: x(approach), filters)` here every `x` iterates over `filters` and then applied to `approach`: `x(approach)` where literally it means
          `x.__call__(approach)` as there is `__call__` in AttributeFilter. Thus it goes to AttributeFilter class and in `__call__` `get()` is triggered. As     every `x` is an inherited class of super class Attribute filter => `Date/Distance.get()` is triggered. So, it overrides `get()` classmethod in super class by
          the same method in inherited class. 
          After it receives value from return `approach.distance/return approach.velocity` etc, `self.op` compares 2 values and returns bool value.

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


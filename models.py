"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique),
    IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation="", name=None, diameter=None, hazardous='N'):
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} and {self.name}"\
        if isinstance(self.name, str) and self.name != ''\
        else f"{self.designation}"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, var):
        if var is '' or var is None:
            self._name = None
        else:
            self._name = var

    @property
    def diameter(self):
        return self._diameter

    @diameter.setter
    def diameter(self, var):
        if var is None or var is '':
            self._diameter = float("nan")
        else:
            self._diameter = float(var)

    @property
    def hazardous(self):
        return self._hazardous

    @hazardous.setter
    def hazardous(self, identifier):
        if identifier == 'Y':
            self._hazardous = True
        else:
            self._hazardous = False

    def __str__(self):
        """Return `str(self)`."""
        return f'''NearEarthObject: designation = {self.designation},
name = {self.name} with diameter = {self.diameter}'''

    def __repr__(self):
        return (f'''NearEarthObject(designation: {self.designation}, name={self.name},
diameter={self.diameter}, hazardous={self.hazardous})''')

    def serialize(self):
        name = self.name if self.name is not None else ''
        return {'designation': self.designation, 'name': name,
                'diameter_km': self.diameter,
                'potentially_hazardous': self.hazardous}


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the
    NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, designation, time, distance=float(0.0), velocity=float(0.0)):
        self._designation = designation
        self.time = cd_to_datetime(time)
        self.distance = distance
        self.velocity = velocity

        # reference NEO
        self.neo = None

    @property
    def time_str(self):
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`."""
        return (f'''CloseApproach: distance: {self.distance}, 
velocity: {self.velocity} 
NEO object: {self.neo}, time: {self.time}''')

    def __repr__(self):
        """Return `repr(self)`, a computer-readable
           string representation of this object."""
        return (f'''CloseApproach(time={self.time_str}, distance={self.distance:.2f}, 
velocity={self.velocity:.2f}, neo={self.neo})''')

    def serialize(self):
        return {'datetime_utc': datetime_to_str(self.time),
                'distance_au': self.distance,
                'velocity_km_s': self.velocity,
                'neo': self.neo.serialize()}

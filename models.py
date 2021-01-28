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
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, designation, name = None, diameter = None, hazardous = False):
        self.designation = designation
        self.name = name
        self.diameter = diameter
        self.hazardous = hazardous
        # Create an empty initial collection of linked approaches.
        self.approaches = []  #for now empty

    # @property
    # def fullname(self):
    #     """Return a representation of the full name of this NEO."""
    #     return f"{self.designation} and {self._name} hereeeee"

    @property
    def diameter(self):
        return self._diameter
    

    @diameter.setter
    def diameter(self, var = None):
        if not var:
            self._diameter = None   #this one is useless as diameter in __init__ is already None by default
        else:
            self._diameter = var

    @property
    def name(self):
        return self._name
    

    @name.setter
    def name(self, var = None):
        if var is None:
            self._name = float('Nan')
        else:
            self._name = var



    def __str__(self):
        """Return `str(self)`."""
        return f"NearEarthObject: designation = {self.designation}, name = {self._name} with diameter = {self.diameter}"


    def __repr__(self):
        return (f"NearEarthObject(designation: {self.designation}, name={self.name}, "
                f"diameter={self.diameter}, hazardous={self.hazardous})")


# neo = NearEarthObject('Comet', 'Leo', 542, True)
# print(neo)



class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initally, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """
    def __init__(self, designation, time, distance = 0.0, velocity = 0.0):        
        self._designation = designation
        self.time = cd_to_datetime(time) 
        self.distance = distance
        self.velocity = velocity

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None #should be refernces to NEO and implement fullname getter from class above

    @property
    def time_str(self):
        format_time = datetime_to_str(self.time)
      
        return (f"The {self._designation} comes to Earth on {format_time} at {self.velocity} "
                f"and will be on {self.distance} distance from our planet!")

    def __str__(self):
        """Return `str(self)`."""
        return (f"CloseApproach: distance: {self.distance}, velocity: {self.velocity} "
                f"NEO object: {self.neo}, time: {self.time}")

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return (f"CloseApproach(time={self.time_str!r}, distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, neo={self.neo!r})")

ca = CloseApproach('Asteroid', '2020-Dec-31 12:00', 65, 785)
print(ca.time)
print(ca.time_str)









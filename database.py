def UniteApprNeo(neos, approaches):
    '''
    Each `CloseApproach` has an attribute (`._designation`) that
    matches the `.designation` attribute of the corresponding NEO. This
    function modifies the supplied NEOs and close approaches to link them
    together and return linked neos, approaches collection.
    '''

    # Ex: NearEarthObject(designation: 1580, name=Betulia,
    #                     diameter=5.8, hazardous=False)

    # Ex: CloseApproach(time=1900-01-01 07:16, distance=0.39,
    #                   velocity=9.93, neo=None)
    Neos = {}
    Approaches = []
    for x in approaches:
        # CloseApproach: distance: 0.287066594994207,
        #                velocity: 18.9544162594432 NEO object: None,
        #                time: 1900-01-26 23:50:00
        for y in neos:
            # NearEarthObject: designation = 154991,
            #                  name = Vinciguerra with diameter = nan
            # NearEarthObject: designation = 154993,
            #                  name = None with diameter = 0.828
            if x._designation == y.designation:
                x.neo = y
                if y.designation in Neos:
                    Neos[y.designation].approaches.append(x)
                else:
                    # append those approaches  to
                    # NearEarthObject .approaches
                    y.approaches.append(x)

                    # key: designation (number)
                    # value: the whole object (including designation)
                    Neos[y.designation] = y
                    # Ex: {'170903': NearEarthObject(designation: 170903,
                    #                name=None, diameter=nan, hazardous=True)
                break

        Approaches.append(x)

    # populate with all the rest
    # 'neos' that didn't match
    # to approaches
    for x in neos:
        if x.designation not in Neos:
            Neos[x.designation] = x

    return (Neos.values(), Approaches)


class NEODatabase:

    def __init__(self, neos, approaches):

        self._neosNameDict = {}
        self._neosDesignDict = {}

        self._neos, self._approaches = UniteApprNeo(neos, approaches)
        # here (above) csv and json are supplied

        for x in self._neos:
            if x.name:
                self._neosNameDict[x.name] = x
            self._neosDesignDict[x.designation] = x

    def get_neo_by_designation(self, designation):

        if designation in self._neosDesignDict:
            return self._neosDesignDict[designation]
        return None

    def get_neo_by_name(self, name):

        if name in self._neosNameDict:
            return self._neosNameDict[name]
        return None

    def query(self, filters=()):
        for approach in self._approaches:
            # approach Ex: CloseApproach: distance: 0.363559619016314,
            # velocity: 18.9172998381067 NEO object:\
            # NearEarthObject: designation = 2010 YC1,
            # name = None with diameter = 0.227, time: 2020-12-30 04:57:00
            temp = map(lambda x: x(approach), filters)
            if all(x for x in temp) is True:
                # using generators if all values in
                # 'container [reference to filters]' are True => yield
                yield approach

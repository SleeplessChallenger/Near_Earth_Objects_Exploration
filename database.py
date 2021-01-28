
def UniteApprNeo(neos, approaches):
    Neos = {}
    Approaches = []
    for x in approaches:
        for y in neos:
            if x._designation == y.designation:
                x.neo = y #here .neo in CloseApproach is placed
                if y.designation in Neos:
                    Neos[y.designation].approaches.append(x) #if such object with such designation already exists, we take obj from hashmap
                                                            #[it's placed there as obj.designation = obj] => append approaches
                else:
                    y.approaches.append(x) #append to approaches of this object 
                    Neos[y.designation] = y #place object with designation in hashmap
                break
        Approaches.append(x)

    for x in neos:
        if x.designation not in Neos:
            Neos[x.designation] = x

    return (Neos.values(), Approaches)



class NEODatabase:
   
    def __init__(self, neos, approaches):

        self._neosNameDict = {} 
        self._neosDesignDict = {} 

        self._neos, self._approaches = UniteApprNeo(neos, approaches) #here csv and json are supplied 

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
                temp = map(lambda x: x(approach), filters)
                if all(x == True for x in temp) #using generators if all values in 'container [reference to filters]' are True =>yield
                    yield approach



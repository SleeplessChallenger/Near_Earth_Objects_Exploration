import operator
from itertools import islice


class UnsupportedCriterionError(NotImplementedError):
    """A filter criterion is unsupported."""


class AttributeFilter:
    """
    An `AttributeFilter` represents the search criteria pattern comparing some
    attribute of a close approach (or its attached NEO) to
    a reference value. It
    essentially functions as a callable predicate for whether a `CloseApproach`
    object satisfies the encoded criterion.

    It is constructed with a comparator operator and a reference value, and
    calling the filter (with __call__) executes `get(approach) OP value` (in
    infix notation).
    """
    def __init__(self, op, value):
        """
        The reference value will be supplied as the second (right-hand side)
        argument to the operator function. For example, an `AttributeFilter`
        with `op=operator.le` and `value=10` will, when called on an approach,
        evaluate `some_attribute <= 10`.
        """
        self.op = op
        # is just operator >/</<= etc
        self.value = value
        # value given by user

    def __call__(self, approach):
        """Invoke `self(approach)`."""
        return self.op(self.get(approach), self.value)
    # self.get() triggers 'get' method, but unless it mathces
    # one of the inherited classes => we'll trigger one of them

    @classmethod
    def get(cls, approach):
        raise UnsupportedCriterionError

    def __repr__(self):
        return f"{self.__class__.__name__}\
                 (op=operator.{self.op.__name__},\
                  value={self.value})"


class Date(AttributeFilter):

    @classmethod
    def get(cls, approach):
        return approach.time.date()


class Distance(AttributeFilter):

    @classmethod
    def get(cls, approach):
        return approach.distance


class Velocity(AttributeFilter):

    @classmethod
    def get(cls, approach):
        return approach.velocity


class Diameter(AttributeFilter):

    @classmethod
    def get(cls, approach):
        return approach.neo.diameter


class Hazardous(AttributeFilter):

    @classmethod
    def get(cls, approach):
        return approach.neo.hazardous


def create_filters(date=None, start_date=None, end_date=None,
                   distance_min=None, distance_max=None,
                   velocity_min=None, velocity_max=None,
                   diameter_min=None, diameter_max=None,
                   hazardous=None):

    container = []

    if date:
        container.append(Date(operator.eq, date))
    if start_date:
        container.append(Date(operator.ge, start_date))
    if end_date:
        container.append(Date(operator.le, end_date))
    if distance_min:
        container.append(Distance(operator.ge, distance_min))
    if distance_max:
        container.append(Distance(operator.le, distance_max))
    if velocity_min:
        container.append(Velocity(operator.ge, velocity_min))
    if velocity_max:
        container.append(Velocity(operator.le, velocity_max))
    if diameter_min:
        container.append(Diameter(operator.ge, diameter_min))
    if diameter_max:
        container.append(Diameter(operator.le, diameter_max))
    if hazardous is not None:
        container.append(Hazardous(operator.eq, hazardous))

    return container
    # has bool variables


def limit(iterator, n=None):
    # 1)create_filters create data with True/False
    # 2)it sends to query in database where it disects all the debris
    # 3) limit will put a confinment on this data
    # (which is placed in iterator); n is limit itself

    # start can be None == 0 => we need to verify that
    # if n == 0 then it equals to None
    # if we want to see the list itself: add list() before islice()

    if n == 0:
        n = None
        return islice(iterator, n)
    return islice(iterator, n)

    # without itertools
    # if n == 0 or n is None:
    #     return [x for x in iterator]
    # cont = list()
    # for idx, appr in enumerate(iterator):
    #     if idx > n:
    #         break
    #     cont.append(appr)
    # return cont

class UnexpectedResponse(Exception):
    """Raised if Label in the response doesn't match the given Statistic"""


class InvalidDimension(Exception):
    """Raised if an input dimension is of unexpected type"""


class InvalidMetricNamespace(Exception):
    """Raised if the given metric doesn't exist in the given namespace"""


class InvalidMetricType(Exception):
    """Raised if the given metric doesn't exist"""

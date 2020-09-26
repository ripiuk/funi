from enum import Enum

import trafaret as t


TIMESTAMP_FORMAT = '%Y-%m-%d'


class SCHEMAS(Enum):
    """Contains all the possible output data formats"""
    CSV_V1 = t.Dict({
        t.Key('timestamp'): t.Date(format=TIMESTAMP_FORMAT),
        t.Key('type'): t.String(allow_blank=False),
        t.Key('amount'): t.Float(gt=0),
        t.Key('from'): t.Int(gte=0),
        t.Key('to'): t.Int(gte=0),
    }, ignore_extra='*')

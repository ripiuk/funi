import datetime

import trafaret as t

from funi.formats import TIMESTAMP_FORMAT
from funi.providers._base import AbstractProvider


class Bank1(AbstractProvider):
    ident_schema = t.Dict({
        t.Key('timestamp'): t.Date(format='%b %d %Y'),
        t.Key('type'): t.Enum('remove', 'add'),
        t.Key('amount'): t.Float(gt=0),
        t.Key('from'): t.Int(gte=0),
        t.Key('to'): t.Int(gte=0),
    }, ignore_extra='*')

    @staticmethod
    def _transform_csv_v1(data: dict) -> dict:
        data['timestamp'] = datetime.datetime.strptime(
            data['timestamp'],
            '%b %d %Y',
        ).strftime(TIMESTAMP_FORMAT)
        return data


class Bank2(AbstractProvider):
    ident_schema = t.Dict({
        t.Key('date'): t.Date(format='%d-%m-%Y'),
        t.Key('transaction'): t.Enum('remove', 'add'),
        t.Key('amounts'): t.Float(gt=0),
        t.Key('from'): t.Int(gte=0),
        t.Key('to'): t.Int(gte=0),
    }, ignore_extra='*')

    @staticmethod
    def _transform_csv_v1(data: dict) -> dict:
        data['timestamp'] = datetime.datetime.strptime(
            data['date'],
            '%d-%m-%Y',
        ).strftime(TIMESTAMP_FORMAT)

        return t.Dict({
            t.Key('transaction', to_name='type'): t.Enum('remove', 'add'),
            t.Key('amounts', to_name='amount'): t.Float(gt=0),
        }, allow_extra='*').check(data)


class Bank3(AbstractProvider):
    ident_schema = t.Dict({
        t.Key('date_readable'): t.Date(format='%d %b %Y'),
        t.Key('type'): t.Enum('remove', 'add'),
        t.Key('euro'): t.Int(gte=0),
        t.Key('cents'): t.Int(gte=0),
        t.Key('to'): t.Int(gte=0),
        t.Key('from'): t.Int(gte=0),
    }, ignore_extra='*')

    @staticmethod
    def _transform_csv_v1(data: dict) -> dict:
        data['timestamp'] = datetime.datetime.strptime(
            data['date_readable'],
            '%d %b %Y',
        ).strftime(TIMESTAMP_FORMAT)
        data['amount'] = f'{data["euro"]}.{data["cents"]}'

        return data

import pytest
import trafaret as t

from funi.formats import SCHEMAS
from funi.providers.banks import Bank1, Bank2, Bank3
from tests.funi.const import BANK1_DATA_EXAMPLE, \
    BANK2_DATA_EXAMPLE, BANK3_DATA_EXAMPLE


# Bank1

@pytest.mark.parametrize('data', (
    BANK1_DATA_EXAMPLE,
    {
        'timestamp': 'Oct 2 2019',
        'type': 'add',
        'amount': 2000.20,
        'from': 188,
        'to': 198,
    },
))
def test_bank1_good_ident(data):
    assert data == Bank1.ident_schema.check(data)


@pytest.mark.parametrize('data', (
    # bad timestamp format
    {
        **BANK1_DATA_EXAMPLE,
        'timestamp': '2019-10-01',
    },
    # bad timestamp type
    {
        **BANK1_DATA_EXAMPLE,
        'timestamp': 123,
    },
    # wrong `type` field value
    {
        **BANK1_DATA_EXAMPLE,
        'type': 'bad value',
    },
    # bad amount type
    {
        **BANK1_DATA_EXAMPLE,
        'amount': 'some string',
    },
    # bad amount value
    {
        **BANK1_DATA_EXAMPLE,
        'amount': 0,
    },
    # bad `from` type
    {
        **BANK1_DATA_EXAMPLE,
        'from': 'some string',
    },
    # bad `from` value
    {
        **BANK1_DATA_EXAMPLE,
        'from': -1,
    },
    # bad `to` type
    {
        **BANK1_DATA_EXAMPLE,
        'to': 'some string',
    },
    # bad `to` value
    {
        **BANK1_DATA_EXAMPLE,
        'to': -1,
    },
))
def test_bank1_bad_ident(data):
    with pytest.raises(t.DataError):
        Bank1.ident_schema.check(data)


def test_bank1_csv_v1_transform():
    provider = Bank1()

    res = provider.transform(
        schema=SCHEMAS.CSV_V1,
        data=BANK1_DATA_EXAMPLE,
    )
    assert SCHEMAS.CSV_V1.value.check(res)


def test_bank1_csv_v1_without_transform_mapping():
    provider = Bank1()
    provider._transform_mapping = {}

    with pytest.raises(ValueError):
        provider.transform(
            schema=SCHEMAS.CSV_V1,
            data=BANK1_DATA_EXAMPLE,
        )


# Bank2

@pytest.mark.parametrize('data', (
    BANK2_DATA_EXAMPLE,
    {
        'date': '04-10-2019',
        'transaction': 'add',
        'amounts': 2123.40,
        'from': 198,
        'to': 188,
    },
))
def test_bank2_good_ident(data):
    assert data == Bank2.ident_schema.check(data)


@pytest.mark.parametrize('data', (
    # bad date format
    {
        **BANK2_DATA_EXAMPLE,
        'date': 'Oct 2 2019',
    },
    # bad date type
    {
        **BANK2_DATA_EXAMPLE,
        'date': 123,
    },
    # wrong transaction field value
    {
        **BANK2_DATA_EXAMPLE,
        'transaction': 'bad value',
    },
    # bad amounts type
    {
        **BANK2_DATA_EXAMPLE,
        'amounts': 'some string',
    },
    # bad amounts value
    {
        **BANK2_DATA_EXAMPLE,
        'amounts': 0,
    },
    # bad `from` type
    {
        **BANK2_DATA_EXAMPLE,
        'from': 'some string',
    },
    # bad `from` value
    {
        **BANK2_DATA_EXAMPLE,
        'from': -1,
    },
    # bad `to` type
    {
        **BANK2_DATA_EXAMPLE,
        'to': 'some string',
    },
    # bad `to` value
    {
        **BANK2_DATA_EXAMPLE,
        'to': -1,
    },
))
def test_bank2_bad_ident(data):
    with pytest.raises(t.DataError):
        Bank2.ident_schema.check(data)


def test_bank2_csv_v1_transform():
    provider = Bank2()

    res = provider.transform(
        schema=SCHEMAS.CSV_V1,
        data=BANK2_DATA_EXAMPLE,
    )
    assert SCHEMAS.CSV_V1.value.check(res)


# Bank3

@pytest.mark.parametrize('data', (
    BANK3_DATA_EXAMPLE,
    {
        'date_readable': '6 Oct 2019',
        'type': 'add',
        'euro': 1060,
        'cents': 6,
        'to': 198,
        'from': 188,
    },
))
def test_bank3_good_ident(data):
    assert data == Bank3.ident_schema.check(data)


@pytest.mark.parametrize('data', (
    # bad date_readable format
    {
        **BANK3_DATA_EXAMPLE,
        'date_readable': '06-10-2019',
    },
    # bad date_readable type
    {
        **BANK3_DATA_EXAMPLE,
        'date_readable': 123,
    },
    # wrong `type` field value
    {
        **BANK3_DATA_EXAMPLE,
        'type': 'bad value',
    },
    # bad euro type
    {
        **BANK3_DATA_EXAMPLE,
        'euro': 'some string',
    },
    # bad euro value
    {
        **BANK3_DATA_EXAMPLE,
        'euro': -1,
    },
    # bad cents type
    {
        **BANK3_DATA_EXAMPLE,
        'cents': 'some string',
    },
    # bad cents value
    {
        **BANK3_DATA_EXAMPLE,
        'cents': -1,
    },
    # bad `to` type
    {
        **BANK3_DATA_EXAMPLE,
        'to': 'some string',
    },
    # bad `to` value
    {
        **BANK3_DATA_EXAMPLE,
        'to': -1,
    },
    # bad `from` type
    {
        **BANK3_DATA_EXAMPLE,
        'from': 'some string',
    },
    # bad `from` value
    {
        **BANK3_DATA_EXAMPLE,
        'from': -1,
    },
))
def test_bank3_bad_ident(data):
    with pytest.raises(t.DataError):
        Bank3.ident_schema.check(data)


def test_bank3_csv_v1_transform():
    provider = Bank3()

    res = provider.transform(
        schema=SCHEMAS.CSV_V1,
        data=BANK3_DATA_EXAMPLE,
    )
    assert SCHEMAS.CSV_V1.value.check(res)

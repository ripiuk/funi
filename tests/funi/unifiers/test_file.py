from pathlib import Path
from unittest import mock

import pytest
import trafaret as t

from funi.formats import SCHEMAS
from funi.unifiers.file import CSVUnifier


# CSVUnifier

def test_csv_unifier_bad_schema():
    custom_schema = t.Dict({t.Key('test'): t.String})
    with pytest.raises(AssertionError):
        CSVUnifier(schema=custom_schema)


def test_csv_unifier_output_file_extension():
    unifier = CSVUnifier(
        schema=SCHEMAS.CSV_V1,
        output_filename='test_file'
    )
    assert Path(unifier.output_filename).suffix == \
        CSVUnifier.file_extension


@pytest.mark.parametrize('filename, suffix, expected', (
    ('test_file', '.csv', 'test_file.csv'),
    ('test_file', 'json', 'test_file.json'),
    ('test_file', None, 'test_file.txt'),
    ('test_file', '', 'test_file.txt'),
))
def test_csv_unifier_generate_filename(filename, suffix, expected):
    assert CSVUnifier._generate_filename(
        filename=filename,
        suffix=suffix,
    ) == expected


def test_csv_unifier_generate_random_filename():
    suffix = '.csv'
    generated_filename = Path(CSVUnifier._generate_filename(suffix=suffix))
    assert generated_filename.suffix == suffix
    assert len(generated_filename.name) >= 10
    # Check if generated filename contains only ASCII characters
    assert all(ord(char) < 128 for char in generated_filename.name)


def test_csv_unifier_can_not_get_provider():
    with mock.patch('funi.unifiers._base.PROVIDERS', new=[]):
        with pytest.raises(ValueError):
            CSVUnifier._get_provider(
                data={},
                file_path='test_file.csv',
            )


def test_csv_unifier_get_provider():
    expected = 'provider instance'

    provider1 = mock.MagicMock()
    provider1.ident_schema.check.side_effect = t.DataError('error')

    provider2 = mock.MagicMock()
    provider2.return_value = expected
    provider2.ident_schema.check.return_value = True

    with mock.patch(
            'funi.unifiers._base.PROVIDERS',
            new=[provider1, provider2],
    ):
        assert CSVUnifier._get_provider(
            data={},
            file_path='test_file.csv',
        ) == expected
        assert provider1.ident_schema.check.called


def test_csv_unifier_unify_bad_files(tmp_path):
    unifier = CSVUnifier(schema=SCHEMAS.CSV_V1)
    unifier._unify_files_data = mock.MagicMock()

    # directory instead of file
    directory = tmp_path / 'subdir'
    directory.mkdir()
    with pytest.raises(ValueError):
        unifier.unify(str(directory))

    # not existing file
    with pytest.raises(ValueError):
        unifier.unify('not_existing_file.csv')

    assert not unifier._unify_files_data.called


def test_csv_unifier_unify_good_files(tmp_path):
    unifier = CSVUnifier(schema=SCHEMAS.CSV_V1)
    unifier._unify_files_data = mock.MagicMock()

    file = tmp_path / 'test_file.csv'
    file.write_text('')

    assert unifier.unify(str(file)) is None
    unifier._unify_files_data.assert_called_with(str(file))


def test_csv_unifier_unify_files_empty_data(tmp_path):
    inp_file = tmp_path / 'inp_file.csv'
    inp_file.write_text('')
    res_file = tmp_path / 'res_file.csv'

    unifier = CSVUnifier(
        schema=SCHEMAS.CSV_V1,
        output_filename=str(res_file),
    )
    row = {
        key.name: 'test_value'
        for key in unifier.schema.value.keys
    }
    unifier._file_handler = mock.MagicMock()
    unifier._file_handler.return_value = [row]

    assert unifier._unify_files_data(str(inp_file)) is None
    unifier._file_handler.assert_called_with(str(inp_file))
    assert res_file.read_text() == \
        f"{','.join(row)}\n{','.join(row.values())}\n"

# TODO: Add tests for CSVUnifier._file_handler

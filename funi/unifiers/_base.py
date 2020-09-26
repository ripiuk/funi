import csv
import json
import typing as typ
from pathlib import Path
from random import choice
from string import hexdigits
from mimetypes import guess_type
from abc import ABC, abstractmethod

import trafaret as t

from funi.formats import SCHEMAS
from funi.providers import PROVIDERS, AbstractProvider


class AbstractUnifier(ABC):
    __slots__ = ('schema', )

    def __init__(self, schema: SCHEMAS):
        assert isinstance(schema, SCHEMAS), 'Wrong schema type'
        self.schema = schema

    @staticmethod
    def _get_provider(data: dict, file_path: str) -> AbstractProvider:
        """Search for provider by the data

        :param data: input data example
        :param file_path: local file path
        :return: provider for the data
        :raise ValueError: if can not find provider for the data
        """
        for provider in PROVIDERS:
            try:
                provider.ident_schema.check(data)
                return provider()
            except t.DataError:
                continue
        raise ValueError(
            f'Got unknown data structure for file: {file_path!r}'
        )

    def _file_handler(self, file_path: str) -> typ.Iterator[dict]:
        """Read file and transform data due to the provider logic

        :param file_path: local file path
        :return: transformed data
        """
        def _json_reader(file: typ.IO) -> typ.Iterator[dict]:
            try:
                yield json.load(file)
            except (AttributeError, json.JSONDecodeError) as error:
                raise TypeError(f'Can not read the json file. Error: {error}')

        _file_readers = {
            'text/csv': csv.DictReader,
            'text/plain': csv.DictReader,
            'application/json': _json_reader,
        }

        with open(file_path, 'r') as inp_f:
            file_type, _ = guess_type(file_path)
            reader = _file_readers.get(file_type)
            if not reader:
                raise TypeError(f'No reader found for the file: {file_path!r}')

            for row in reader(inp_f):
                # TODO: cache provider per file
                provider = AbstractFileUnifier._get_provider(row, file_path)
                try:
                    yield self.schema.value.check(
                        provider.transform(
                            schema=self.schema,
                            data=row,
                        )
                    )
                except t.DataError as err:
                    raise ValueError(
                        f'File content {row} does not fit '
                        f'the {self.schema.name} schema. Error: {err}'
                    )

    @abstractmethod
    def _unify_files_data(self, *files: str) -> None:
        """Unifying logic implementation"""

    def unify(self, *files: str) -> None:
        """Unify all the data from files due to the needed scheme"""
        for file in map(Path, files):
            if not file.is_file():
                raise ValueError(f'Got incorrect file type: {file.absolute()}')
            if not file.exists():
                raise ValueError(f'Can not find the file: {file.absolute()}')
        self._unify_files_data(*files)


class AbstractFileUnifier(AbstractUnifier, ABC):
    __slots__ = ('output_filename', )

    def __init__(self, schema: SCHEMAS, output_filename: str = None):
        super().__init__(schema=schema)
        self.output_filename = AbstractFileUnifier._generate_filename(
            filename=output_filename,
            suffix='.csv',
        )

    @staticmethod
    def _generate_filename(filename: str = None, suffix: str = None) -> str:
        """Generate new file name or validate existing one

        :param filename: file name
        :param suffix: file suffix (extension)
        :return: generated file name
        """
        suffix = suffix.lstrip('.') if suffix.startswith('.') else suffix
        filename = filename.rsplit('.', 1)[0] \
            if filename \
            else ''.join(choice(hexdigits) for _ in range(10))
        return f'{filename if filename else "res"}.{suffix}'

# TODO: Add AbstractDatabaseUnifier

from abc import ABC, abstractmethod

import trafaret as t

from funi.formats import SCHEMAS


class AbstractProvider(ABC):
    """Abstract base class for providers.

    :cvar ident_schema: trafaret schema that is used for provider identification.
    """

    __slots__ = ('_transform_mapping', )

    ident_schema: t.Dict = NotImplementedError

    def __init__(self):
        self._transform_mapping = {
            SCHEMAS.CSV_V1: self._transform_csv_v1,
        }

    @staticmethod
    @abstractmethod
    def _transform_csv_v1(data: dict) -> dict:
        """Data transformation logic for CSV_V1 output schema"""

    def transform(self, schema: SCHEMAS, data: dict) -> dict:
        """Transform input data due to the needed output schema

        :param schema: output schema
        :param data: input data for the provider
        :return: transformed data due to the output schema
        :raise ValueError: if transformation logic is not provided
        """
        if not (transform_func := self._transform_mapping.get(schema)):
            raise ValueError(f'Transformation logic is not implemented for {schema.name}')
        return transform_func(data)

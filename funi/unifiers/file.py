import csv

from funi.unifiers._base import AbstractFileUnifier


class CSVUnifier(AbstractFileUnifier):
    """Unify providers data and store it into a CSV file"""

    file_extension = '.csv'

    def _unify_files_data(self, *files: str) -> None:
        with open(self.output_filename, 'w+') as res_f:
            fieldnames = [key.name for key in self.schema.value.keys]
            writer = csv.DictWriter(res_f, fieldnames=fieldnames)
            writer.writeheader()

            for file in files:
                for row in self._file_handler(file):
                    writer.writerow(row)

# TODO: Add JSONUnifier
# TODO: Add XMLUnifier

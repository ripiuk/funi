import funi


if __name__ == '__main__':
    unifier = funi.CSVUnifier(
        schema=funi.SCHEMAS.CSV_V1,
        output_filename='res.csv',
    )

    unifier.unify(
        'data/bank1.csv',
        'data/bank2.csv',
        'data/bank3.csv',
    )

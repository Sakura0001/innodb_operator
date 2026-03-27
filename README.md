# innodb_suanzi

MySQL InnoDB DDL performance benchmark runner.

## Setup

```bash
python3 -m pip install --user .
cp config.example.yaml config.yaml
PYTHONPATH=src python3 -m innodb_suanzi
```

## Run Cases

```bash
PYTHONPATH=src python3 -m innodb_suanzi
PYTHONPATH=src python3 -m innodb_suanzi --operation alter_add_index
PYTHONPATH=src python3 -m innodb_suanzi --cases alter_add_index/dstore_test_case_001.sql
PYTHONPATH=src python3 -m innodb_suanzi --cases alter_add_index/dstore_test_case_001.sql,create_index/dstore_test_case_002.sql
PYTHONPATH=src python3 -m innodb_suanzi --case-range 1-5
```

## Project Files

- `config.example.yaml`: sample database config
- `schema.sql`: base table definition
- `test_cases/`: SQL benchmark cases grouped by operation directory
- `results/`: CSV output directory
- `src/innodb_suanzi/`: runner implementation
- `tests/`: automated tests

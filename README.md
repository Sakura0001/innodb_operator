# innodb_suanzi

MySQL InnoDB DDL performance benchmark runner.

## Setup

```bash
python3 -m pip install --user .
cp config.example.yaml config.yaml
python3 -m innodb_suanzi
```

## Run Specific Cases

```bash
python3 -m innodb_suanzi --cases dstore_test_case_001.sql
python3 -m innodb_suanzi --cases dstore_test_case_001.sql,dstore_test_case_002.sql
python3 -m innodb_suanzi --case-range 1-2
```

## Project Files

- `config.example.yaml`: sample database config
- `schema.sql`: base table definition
- `test_cases/`: SQL benchmark cases
- `results/`: CSV output directory
- `src/innodb_suanzi/`: runner implementation
- `tests/`: automated tests

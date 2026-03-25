from setuptools import find_packages, setup


setup(
    name="innodb_suanzi",
    version="0.1.0",
    description="A benchmark runner for MySQL InnoDB SQL operator performance tests.",
    python_requires=">=3.9",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "PyMySQL>=1.1.1",
        "PyYAML>=6.0.2",
    ],
)

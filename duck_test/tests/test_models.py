import subprocess

import duckdb
import pytest


@pytest.fixture(scope="session")
def dbt_compile():
    subprocess.run(["poetry", "run", "dbt", "compile", "--target", "test"], check=True)


@pytest.fixture
def duck_con(dbt_compile):
    con = duckdb.connect("test.duckdb")
    yield con
    con.close()


@pytest.fixture
def distro_using(duck_con):
    duck_con.sql("CREATE OR REPLACE TABLE linux_distro (id INTEGER, name VARCHAR)")
    duck_con.sql("COPY linux_distro FROM 'tests/data/linux_distro.csv' (HEADER)")
    yield duck_con
    duck_con.sql("DROP TABLE linux_distro")


def test_distro_using(distro_using):
    with open("./target/compiled/duck_test/models/distro_using.sql") as f:
        sql = f.read()

    expected = [(1, "Ubuntu")]
    result = distro_using.sql(sql).fetchall()

    assert result == expected

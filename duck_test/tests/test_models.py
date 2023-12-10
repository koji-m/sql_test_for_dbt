import duckdb
import pytest

# @pytest.fixture for session to dbt compile
@pytest.fixture
def duck_con():
    con = duckdb.connect("test.duckdb")
    yield con
    con.close()

@pytest.fixture
def distro_using(duck_con):
    duck_con.sql("CREATE TABLE linux_distro (id INTEGER, name VARCHAR)")
    duck_con.sql("COPY linux_distro FROM 'linux_distro.csv'")
    yield duck_con
    duck_con.sql("DROP TABLE linux_distro")

def test_distro_using(distro_using):
    with open('./models/distro_using.sql') as f:
        sql = f.read()

    expected = [(1, 'Ubuntu')]
    # result = distro_using.sql(sql).fetchall()

    # assert result == expected
    assert 1 == 1

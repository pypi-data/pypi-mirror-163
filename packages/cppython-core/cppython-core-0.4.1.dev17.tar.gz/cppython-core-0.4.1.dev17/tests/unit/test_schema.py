"""
TODO
"""

import pytest
from tomlkit import parse

from cppython_core.schema import PEP508, CPPythonData, PyProject


class TestSchema:
    """
    TODO
    """

    def test_cppython_data(self):
        """
        Ensures that the CPPython config data can be defaulted
        """
        CPPythonData()

    def test_cppython_table(self):
        """
        TODO
        """

        data = """
        [project]\n
        name = "test"\n
        version = "1.0.0"\n
        description = "A test document"\n

        [tool.cppython]\n
        target = "executable"\n
        """

        document = parse(data).value
        pyproject = PyProject(**document)
        assert pyproject.tool is not None
        assert pyproject.tool.cppython is not None

    def test_empty_cppython(self):
        """
        TODO
        """

        data = """
        [project]\n
        name = "test"\n
        version = "1.0.0"\n
        description = "A test document"\n

        [tool.test]\n
        """

        document = parse(data).value
        pyproject = PyProject(**document)
        assert pyproject.tool is not None
        assert pyproject.tool.cppython is None

    def test_508(self):
        """
        TODO
        """

        requirement = PEP508('requests [security,tests] >= 2.8.1, == 2.8.* ; python_version < "2.7"')

        assert requirement.name == "requests"

        with pytest.raises(ValueError):
            PEP508("this is not conforming")

from types import MappingProxyType

import pytest
from services import namelist_creator


class TestNamelistContentCreator:
    @pytest.fixture
    def namelist_content_creator(self):
        return namelist_creator.NamelistContentCreator("emission_vehicles")

    def test_create_namelist(
        self, namelist_content_creator: namelist_creator.NamelistContentCreator
    ):
        test_data = MappingProxyType({"co2_veic": "0.8"})

        created_data = namelist_content_creator.create_namelist(test_data)

        correct_content = """&emission_vehicles
    co2_veic = '0.8'
/
"""

        assert created_data == correct_content

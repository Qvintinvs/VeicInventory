from types import MappingProxyType

import pytest

from use_cases.namelist_serializer import NamelistSerializer


class TestNamelistContentCreator:
    @pytest.fixture
    def namelist_content_creator(self):
        return NamelistSerializer("emission_vehicles")

    def test_create_namelist(self, namelist_content_creator: NamelistSerializer):
        test_data = MappingProxyType({"co2_veic": 0.8})

        created_data = namelist_content_creator.create_namelist_through(test_data)

        correct_content = """&emission_vehicles
    co2_veic = 0.8
/
"""

        assert created_data == correct_content

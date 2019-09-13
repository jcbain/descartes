from context import dispatcher
from tests.data.tmp_input import tmp_string


class TestRemoveAll:

    def test_remove_one_item(self):
        x = ['james', 'bain', True, 1, 2]
        x = dispatcher.remove_all(x, 'james')
        assert 'james' not in x

    def test_remove_mult_items(self):
        x = ['james', 'bain', True, 1, 2]
        x = dispatcher.remove_all(x, 'james', 1)
        assert ('james' and 1) not in x


class TestParseOutput:

    def test_data_length(self):
        data_elements = dispatcher.parse_output(tmp_string, 0)[0]
        assert len(data_elements) == 8

    def test_data_extraction(self):
        data_elements = dispatcher.parse_output(tmp_string, 1)[0]
        assert data_elements[0] == '20001 -0.020159 0 283 370 1e-05 1e-05 1e-05 5 500 1'

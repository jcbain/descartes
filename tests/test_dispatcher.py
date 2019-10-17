from context import dispatcher
from tests.data.tmp_input2 import tmp_string2


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
        data_elements = dispatcher.parse_output(tmp_string2, 'm39', 0)[0]
        assert len(data_elements) == 6

    def test_data_extraction(self):
        data_elements = dispatcher.parse_output(tmp_string2, 'm39', 1)[0]
        assert data_elements[0] == '170001 0.0327583 0 0.0005 3997 1e-10 1e-05 1e-06 2 4000 1'

    def test_header_configuration(self):
        header_element = dispatcher.parse_output(tmp_string2, 'm39', 0)[1]
        assert header_element == 'position select_coef p1_freq p2_freq origin_gen migr_rate mut_rate recomb_rate ' \
                                 'fitness_width output_gen'


from context import dispatcher

def test_remove_all():
    x = [1, 'james', 'hello', 'james', True]
    x = dispatcher.remove_all(x, 'james')
    assert 'james' not in x


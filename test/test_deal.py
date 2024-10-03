from routers.deal import parse_order_num

def test_parse_order_num():
    assert parse_order_num("12312-label-id") == ("label", "id")
    assert parse_order_num("111111111") == (None, None)
    assert parse_order_num("") == (None, None)

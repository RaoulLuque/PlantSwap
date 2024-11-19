from app.models import Plant


def assert_if_trade_request_json_and_trade_request_data_match(
    outgoing_plant: Plant, incoming_plant: Plant, json_trade_request: dict[str, str]
) -> None:
    """
    Asserts if the request json and the request data match.
    :param outgoing_plant: Outgoing plant instance
    :param incoming_plant: Incoming plant instance
    :param json_trade_request: Response trade request as JSON dict
    :return: None
    """
    assert json_trade_request
    assert str(outgoing_plant.id) == json_trade_request["outgoing_plant_id"]
    assert str(incoming_plant.id) == json_trade_request["incoming_plant_id"]
    assert str(outgoing_plant.owner_id) == json_trade_request["outgoing_user_id"]
    assert str(incoming_plant.owner_id) == json_trade_request["incoming_user_id"]

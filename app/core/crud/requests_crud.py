import uuid

from sqlmodel import Session, select, or_

from app.models import TradeRequest, TradeRequestsPublic, User, Plant


def create_trade_request(session: Session, trade_request: TradeRequest) -> TradeRequest:
    """
    Create a new trade request.
    :param trade_request: Trade request to be added to the database
    :param session: Current database session
    :return: Created trade request
    """
    session.add(trade_request)
    session.commit()
    session.refresh(trade_request)
    return trade_request


def create_trade_request_from_plant_ids(
    session: Session,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
    message: str | None = None,
) -> TradeRequest:
    """
    Create a new trade request using the plant ids.

    Throws a value error if one of the plants does not exist.
    :param outgoing_plant_id: id of the plant the user wants to offer
    :param incoming_plant_id: id of the plant the user wants in return
    :param session: Current database session
    :param message: Optional message
    :return: Created trade request
    """
    outgoing_plant: Plant | None = session.get(Plant, outgoing_plant_id)
    incoming_plant: Plant | None = session.get(Plant, incoming_plant_id)
    if outgoing_plant is None or incoming_plant is None:
        raise ValueError("One of the plants does not exist.")
    trade_request = TradeRequest(
        outgoing_plant_id=outgoing_plant_id,
        incoming_plant_id=incoming_plant_id,
        outgoing_user_id=outgoing_plant.owner_id,
        incoming_user_id=incoming_plant.owner_id,
        message=message,
    )
    session.add(trade_request)
    session.commit()
    session.refresh(trade_request)
    return trade_request


def get_all_trade_requests(
    user: User,
    session: Session,
    skip: int,
    limit: int,
    outgoing_only: bool = False,
    incoming_only: bool = False,
) -> TradeRequestsPublic:
    """
    Retrieve all existing requests involving oneself up to the given limit with the given offset.
    Can be either outgoing or incoming only or all kinds of requests.

    Throws a ValueError  exception if both outgoing_only and incoming_only are true
    :param user: Currently logged-in user
    :param session: Current database session
    :param skip: Number of ads to skip
    :param limit: Limit of ads to retrieve
    :param outgoing_only: Whether to retrieve only outgoing requests
    :param incoming_only: Whether to retrieve only incoming requests
    :return: List of plant ads with number of ads as a PlantsPublic instance
    """
    if outgoing_only and incoming_only:
        raise ValueError("Cannot filter by both outgoing and incoming only.")
    elif outgoing_only:
        # noinspection Pydantic
        statement = (
            select(TradeRequest)
            .where(TradeRequest.outgoing_user_id == user.id)
            .offset(skip)
            .limit(limit)
        )
    elif incoming_only:
        # noinspection Pydantic
        statement = (
            select(TradeRequest)
            .where(TradeRequest.incoming_user_id == user.id)
            .offset(skip)
            .limit(limit)
        )
    else:
        # noinspection Pydantic
        statement = (
            select(TradeRequest)
            .where(
                or_(
                    TradeRequest.outgoing_user_id == user.id,
                    TradeRequest.incoming_user_id == user.id,
                )
            )
            .offset(skip)
            .limit(limit)
        )
    # noinspection PyTypeChecker
    trade_requests = session.exec(statement).all()
    count = len(trade_requests)
    return TradeRequestsPublic(data=list(trade_requests), count=count)


def delete_trade_request(session: Session, trade_request: TradeRequest) -> TradeRequest:
    """
    Delete an existing trade request.
    :param trade_request: Trade request to be deleted from the database
    :param session: Current database session
    :return: Deleted trade request as TradeRequest instance
    """
    session.delete(trade_request)
    session.commit()
    return trade_request

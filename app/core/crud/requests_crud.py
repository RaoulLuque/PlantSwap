from sqlmodel import Session, select, or_

from app.models import TradeRequest, TradeRequestsPublic, User


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
        raise ValueError("Cannot be both outgoing and incoming only.")
    elif outgoing_only:
        statement = (
            select(TradeRequest)
            .where(TradeRequest.outgoing_user_id == user.id)
            .offset(skip)
            .limit(limit)
        )
    elif incoming_only:
        statement = (
            select(TradeRequest)
            .where(TradeRequest.incoming_user_id == user.id)
            .offset(skip)
            .limit(limit)
        )
    else:
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
    trade_requests = session.exec(statement).all()
    count = len(trade_requests)
    return TradeRequestsPublic(data=list(trade_requests), count=count)



# Router for api endpoints regarding sending trade requests
import uuid

from fastapi import APIRouter, HTTPException, Form
from sqlalchemy.orm import selectinload
from sqlmodel import select

from app.api.dependencies import SessionDep, CurrentUserDep
from app.core.crud import requests_crud
from app.models import (
    TradeRequest,
    Plant,
    TradeRequestsPublic,
    Message,
    TradeRequestPublic,
)

router = APIRouter()


@router.post(
    "/requests/create/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequestPublic,
)
def create_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
    message: str | None = Form(None),
):
    """
    Create a new trade request.
    :param current_user: Currently logged-in user
    :param session: Current database session
    :param outgoing_plant_id: id of the plant the user wants to offer
    :param incoming_plant_id: id of the plant the user wants in return
    :param message: Optional message to the owner of the plant the user wants to trade with
    :return: Information about the created trade request as a TradeRequest instance
    """
    plant_owned_by_user: bool = False
    for plant in current_user.plants:
        if plant.id == outgoing_plant_id:
            plant_owned_by_user = True
            break
    if not plant_owned_by_user:
        raise HTTPException(
            status_code=401,
            detail="You cannot trade other people's plants (you do not own the plant you want to offer).",
        )
    incoming_plant: Plant | None = session.get(Plant, incoming_plant_id)
    if incoming_plant is None:
        raise HTTPException(
            status_code=404,
            detail="The plant you want does not exist.",
        )
    if current_user.id == incoming_plant.owner_id:
        raise HTTPException(
            status_code=418,
            detail="You cannot trade with yourself.",
        )
    # noinspection Pydantic
    possible_existing_trade = session.exec(
        select(TradeRequest)
        .where(TradeRequest.incoming_plant_id == incoming_plant_id)
        .where(TradeRequest.outgoing_plant_id == outgoing_plant_id)
    ).first()
    if possible_existing_trade is not None:
        raise HTTPException(
            status_code=409,
            detail="You already have a trade request for these two plants.",
        )
    possible_inverse_existing_trade = session.exec(
        select(TradeRequest)
        .where(TradeRequest.outgoing_plant_id == incoming_plant_id)
        .where(TradeRequest.incoming_plant_id == outgoing_plant_id)
    ).first()
    if possible_inverse_existing_trade is not None:
        raise HTTPException(
            status_code=409,
            detail="You already have a trade request for these two plants.",
        )
    messages = []
    if message is not None and message != "":
        messages.append(
            Message(
                sender_id=current_user.id,
                content=message,
                incoming_plant_id=incoming_plant_id,
                outgoing_plant_id=outgoing_plant_id,
            )
        )
    trade_request: TradeRequest = TradeRequest(
        outgoing_plant_id=outgoing_plant_id,
        incoming_plant_id=incoming_plant_id,
        outgoing_user_id=current_user.id,
        incoming_user_id=incoming_plant.owner_id,
        messages=messages,
    )
    trade_request = requests_crud.create_trade_request(session, trade_request)
    return trade_request


@router.get(
    "/requests/outgoing/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequestPublic,
)
def read_specific_outgoing_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
):
    """
    Retrieve specific outgoing trade request with the given plant ids if you are the owner of the outgoing plant.
    :param current_user: Currently logged-in user.
    :param session: Current database session
    :param outgoing_plant_id: id of the plant that is being offered
    :param incoming_plant_id: id of the plant that is wanted in return
    :return: Desired trade request if exists as a TradeRequest instance
    """
    plant_owned_by_user: bool = False
    for plant in current_user.plants:
        if plant.id == outgoing_plant_id:
            plant_owned_by_user = True
            break
    if not plant_owned_by_user:
        raise HTTPException(
            status_code=401,
            detail="You do not own a plant with the provided outgoing plant id.",
        )
    trade_request = session.get(TradeRequest, (outgoing_plant_id, incoming_plant_id))
    if trade_request is None:
        raise HTTPException(
            status_code=404,
            detail="No trade request with the given plant ids exists.",
        )
    return trade_request


@router.get(
    "/requests/incoming/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequestPublic,
)
def read_specific_incoming_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
):
    """
    Retrieve specific incoming trade request with the given plant ids if you are the owner of the incoming plant.
    :param current_user: Currently logged-in user.
    :param session: Current database session
    :param outgoing_plant_id: id of the plant that is being offered
    :param incoming_plant_id: id of the plant that is wanted in return
    :return: Desired trade request if exists as a TradeRequest instance
    """
    plant_owned_by_user: bool = False
    for plant in current_user.plants:
        if plant.id == incoming_plant_id:
            plant_owned_by_user = True
            break
    if not plant_owned_by_user:
        raise HTTPException(
            status_code=401,
            detail="You do not own a plant with the provided incoming plant id.",
        )
    trade_request = session.get(TradeRequest, (outgoing_plant_id, incoming_plant_id))
    if trade_request is None:
        raise HTTPException(
            status_code=404,
            detail="No trade request with the given plant ids exists.",
        )
    return trade_request


@router.get("/requests/outgoing/", response_model=TradeRequestsPublic)
def read_own_outgoing_trade_requests(
    current_user: CurrentUserDep, session: SessionDep, skip: int = 0, limit: int = 100
):
    """
    Retrieve all existing outgoing trade requests involving oneself.
    :param current_user: Currently logged-in user.
    :param session: Current database session
    :param skip: Number of requests to skip
    :param limit: Limit of requests to retrieve
    :return: List of trade requests with number of requests as a TradeRequestsPublic instance
    """
    trade_requests = requests_crud.get_all_trade_requests(
        current_user, session, skip, limit, outgoing_only=True
    )
    return trade_requests


@router.get("/requests/incoming/", response_model=TradeRequestsPublic)
def read_own_incoming_trade_requests(
    current_user: CurrentUserDep, session: SessionDep, skip: int = 0, limit: int = 100
):
    """
    Retrieve all existing incoming trade requests involving oneself.
    :param current_user: Currently logged-in user
    :param session: Current database session
    :param skip: Number of requests to skip
    :param limit: Limit of requests to retrieve
    :return: List of trade requests with number of requests as a TradeRequestsPublic instance
    """
    trade_requests = requests_crud.get_all_trade_requests(
        current_user, session, skip, limit, incoming_only=True
    )
    return trade_requests


@router.get("/requests/all/", response_model=TradeRequestsPublic)
def read_own_trade_requests(
    current_user: CurrentUserDep, session: SessionDep, skip: int = 0, limit: int = 100
):
    """
    Retrieve all existing trade requests involving oneself.
    :param current_user: Currently logged-in user
    :param session: Current database session
    :param skip: Number of requests to skip
    :param limit: Limit of requests to retrieve
    :return: List of trade requests with number of requests as a TradeRequestsPublic instance
    """
    trade_requests = requests_crud.get_all_trade_requests(
        current_user, session, skip, limit
    )
    return trade_requests


@router.post(
    "/requests/accept/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequestPublic,
)
def accept_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
):
    """
    Accept a trade request, if the user is owner of the incoming plant.
    :param current_user: Currently logged-in user.
    :param session: Current database session
    :param outgoing_plant_id: id of the plant that is being offered
    :param incoming_plant_id: id of the plant that is wanted in return
    :return: Desired changed trade request if exists as a TradeRequest instance
    """
    plant_owned_by_user: bool = False
    for plant in current_user.plants:
        if plant.id == incoming_plant_id:
            plant_owned_by_user = True
            break
    if not plant_owned_by_user:
        raise HTTPException(
            status_code=401,
            detail="You do not own a plant with the provided incoming plant id.",
        )
    trade_request = session.get(TradeRequest, (outgoing_plant_id, incoming_plant_id))
    if trade_request is None:
        raise HTTPException(
            status_code=404,
            detail="No trade request with the given plant ids exists.",
        )
    trade_request = requests_crud.accept_trade_request(session, trade_request)
    return trade_request


@router.post(
    "/requests/reject/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequestPublic,
)
def reject_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
):
    """
    Reject a trade request, if the user is owner of the incoming plant.
    :param current_user: Currently logged-in user.
    :param session: Current database session
    :param outgoing_plant_id: id of the plant that is being offered
    :param incoming_plant_id: id of the plant that is wanted in return
    :return: Desired changed trade request if exists as a TradeRequest instance
    """
    plant_owned_by_user: bool = False
    for plant in current_user.plants:
        if plant.id == incoming_plant_id:
            plant_owned_by_user = True
            break
    if not plant_owned_by_user:
        raise HTTPException(
            status_code=401,
            detail="You do not own a plant with the provided incoming plant id.",
        )
    trade_request = session.get(TradeRequest, (outgoing_plant_id, incoming_plant_id))
    if trade_request is None:
        raise HTTPException(
            status_code=404,
            detail="No trade request with the given plant ids exists.",
        )
    trade_request = requests_crud.reject_trade_request(session, trade_request)
    return trade_request


@router.post(
    "/requests/message/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequestPublic,
)
def add_message_to_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
    message: str | None = Form(None),
):
    """
    Write a message to the other user involved in the trade.
    :param current_user: Currently logged-in user.
    :param session: Current database session
    :param outgoing_plant_id: id of the plant that is being offered
    :param incoming_plant_id: id of the plant that is wanted in return
    :param message: Message to the other user involved in the trade
    :return: Desired changed trade request if exists as a TradeRequest instance
    """
    user_involved_in_trade: bool = False
    for plant in current_user.plants:
        if plant.id == incoming_plant_id or plant.id == outgoing_plant_id:
            user_involved_in_trade = True
            break
    if not user_involved_in_trade:
        raise HTTPException(
            status_code=404,
            detail="You do not own a plant with the given ids.",
        )
    trade_request = session.get(TradeRequest, (outgoing_plant_id, incoming_plant_id))
    if trade_request is None:
        raise HTTPException(
            status_code=404,
            detail="No trade request with the given plant ids exists.",
        )
    message_with_metadata = Message(
        sender_id=current_user.id,
        content=message,
        incoming_plant_id=incoming_plant_id,
        outgoing_plant_id=outgoing_plant_id,
    )
    trade_request = requests_crud.add_message_to_trade_request(session, trade_request, message_with_metadata)
    return trade_request


@router.post(
    "/requests/delete/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequestPublic,
)
def delete_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
):
    """
    Delete an existing trade request.
    :param current_user: Currently logged-in user
    :param session: Current database session
    :param outgoing_plant_id: id of the plant the user wants to offer
    :param incoming_plant_id: id of the plant the user wants in return
    :return: Information about the deleted trade request as a TradeRequest instance
    """
    # noinspection Pydantic
    trade_request = session.exec(
        select(TradeRequest)
        .options(
            # Eagerly load the relationships to avoid lazy loading error: DetachedInstanceError
            selectinload(TradeRequest.outgoing_plant),
            selectinload(TradeRequest.incoming_plant),
            selectinload(TradeRequest.messages),
        )
        .where(TradeRequest.incoming_plant_id == incoming_plant_id)
        .where(TradeRequest.outgoing_plant_id == outgoing_plant_id)
    ).first()
    if trade_request is None or (
        current_user.id != trade_request.outgoing_user_id
        and current_user.id != trade_request.incoming_user_id
    ):
        raise HTTPException(
            status_code=404,
            detail="No trade request with the given plant ids exists.",
        )
    trade_request = requests_crud.delete_trade_request(session, trade_request)
    return trade_request

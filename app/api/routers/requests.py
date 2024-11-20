# Router for api endpoints regarding sending trade requests
import uuid

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.dependencies import SessionDep, CurrentUserDep
from app.core.crud import requests_crud
from app.models import TradeRequest, Plant, TradeRequestsPublic

router = APIRouter()


@router.post(
    "/requests/create/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequest,
)
def create_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
    message: str | None = None,
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
    possible_existing_entry = session.exec(
        select(TradeRequest)
        .where(TradeRequest.incoming_plant_id == incoming_plant_id)
        .where(TradeRequest.outgoing_plant_id == outgoing_plant_id)
    ).first()
    if possible_existing_entry is not None:
        raise HTTPException(
            status_code=409,
            detail="You already have a trade request for this plant.",
        )
    trade_request: TradeRequest = TradeRequest(
        outgoing_plant_id=outgoing_plant_id,
        incoming_plant_id=incoming_plant_id,
        outgoing_user_id=current_user.id,
        incoming_user_id=incoming_plant.owner_id,
        message=message,
    )
    trade_request = requests_crud.create_trade_request(session, trade_request)
    return trade_request


@router.get(
    "/requests/{outgoing_plant_id}/{incoming_plant_id}", response_model=TradeRequest
)
def read_specific_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
):
    """
    Retrieve specific trade request with the given plant ids.
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
            detail="You cannot trade other people's plants (you do not own the plant you want to offer).",
        )
    trade_request = session.get(TradeRequest, (outgoing_plant_id, incoming_plant_id))
    if trade_request is None:
        raise HTTPException(
            status_code=404,
            detail="No trade request with the given plant ids exists.",
        )
    return trade_request


@router.get("/requests/outgoing", response_model=TradeRequestsPublic)
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


@router.get("/requests/incoming", response_model=TradeRequestsPublic)
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


@router.get("/requests/all", response_model=TradeRequestsPublic)
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
    "/requests/delete/{outgoing_plant_id}/{incoming_plant_id}",
    response_model=TradeRequest,
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

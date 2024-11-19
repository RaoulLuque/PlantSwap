# Router for api endpoints regarding sending trade requests
import uuid

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.api.dependencies import SessionDep, CurrentUserDep
from app.models import TradeRequest, Plant

router = APIRouter()


@router.post("/requests/create/{offering_id}/{wanting_id}", response_model=TradeRequest)
def create_trade_request(
    current_user: CurrentUserDep,
    session: SessionDep,
    outgoing_plant_id: uuid.UUID,
    incoming_plant_id: uuid.UUID,
    message: str | None = None,
):
    """
    Create a new trade request.
    :param current_user: Currently logged-in user.
    :param session: Current database session.
    :param outgoing_plant_id: id of the plant the user wants to offer.
    :param incoming_plant_id: id of the plant the user wants in return.
    :param message: Optional message to the owner of the plant the user wants to trade with.
    :return: Name, description, owner_id and id of the created plant.
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
    session.add(trade_request)
    session.commit()
    session.refresh(trade_request)
    return trade_request


# @router.get("/requests/outgoing", response_model=PublicTradeRequests)
# def read_own_outgoing_trade_requests(
#     session: SessionDep, skip: int = 0, limit: int = 100
# ) -> Any:
#     """
#     Retrieve all existing plant ads
#     :param session: Current database session
#     :param skip: Number of plant ads to skip
#     :param limit: Limit of plant ads to retrieve
#     :return: List of plants with number of plants as a PlantsPublic instance
#     """
#     statement = select(Plant).offset(skip).limit(limit)
#     plants = session.exec(statement).all()
#     count = len(plants)
#     return PlantsPublic(data=plants, count=count)

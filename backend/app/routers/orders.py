from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from backend.app.db import get_session
from backend.app.config import settings
from backend.app.models import Journey, Order, AppEvent
from backend.app.schemas import (
    OrderStatusResponse,
    OrderSimulateRequest,
    OtpRequest,
    OtpVerifyRequest,
    OtpVerifyResponse
)
from backend.app.services.tracker import (
    create_order_for_journey,
    advance_order_status,
    get_order_timeline
)

router = APIRouter(prefix="/api", tags=["Orders & Tracker"])

# Auth OTP endpoints
@router.post("/auth/otp/request")
def request_otp(req: OtpRequest):
    return {"status": "success", "message": f"Demo verification OTP is {settings.OTP_DEMO_CODE}"}

@router.post("/auth/otp/verify", response_model=OtpVerifyResponse)
def verify_otp(req: OtpVerifyRequest):
    if req.code.strip() == settings.OTP_DEMO_CODE:
        return OtpVerifyResponse(valid=True, token="demo_bearer_token_authenticated_user")
    else:
        raise HTTPException(status_code=400, detail="Invalid OTP. Use demo code 123456.")


# Orders endpoints
@router.post("/orders")
def create_order(payload: dict, session: Session = Depends(get_session)):
    journey_id = payload.get("journey_id")
    journey = session.get(Journey, journey_id)
    if not journey:
        raise HTTPException(status_code=404, detail="Journey not found")

    order = create_order_for_journey(journey, session)
    return {"order_id": order.id, "promised_date": order.promised_date}


@router.get("/orders/{order_id}", response_model=OrderStatusResponse)
def get_order_status(order_id: str, session: Session = Depends(get_session)):
    order = session.get(Order, order_id)
    if not order:
        # Check if journey_id was passed instead of order_id
        order = session.exec(select(Order).where(Order.journey_id == order_id)).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

    timeline_data = get_order_timeline(order, session)

    evt = AppEvent(event_name="status_checked", journey_id=order.journey_id)
    session.add(evt)
    session.commit()

    return OrderStatusResponse(**timeline_data)


@router.post("/orders/{order_id}/simulate-advance", response_model=OrderStatusResponse)
def simulate_advance_order(
    order_id: str,
    req: OrderSimulateRequest = OrderSimulateRequest(),
    session: Session = Depends(get_session)
):
    order = session.get(Order, order_id)
    if not order:
        order = session.exec(select(Order).where(Order.journey_id == order_id)).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")

    advance_count = req.days or 1
    advance_order_status(order, session, advance_count)
    timeline_data = get_order_timeline(order, session)
    return OrderStatusResponse(**timeline_data)

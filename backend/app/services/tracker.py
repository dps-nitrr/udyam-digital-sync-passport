from datetime import datetime, timedelta, date
from typing import List, Dict, Any, Optional
from sqlmodel import Session, select
from backend.app.config import settings
from backend.app.models import Order, OrderEvent, Notification, Journey, Quote, Product

STATUS_PIPELINE = [
    ("quote_accepted", "Quote Accepted", "Instant", 0),
    ("kyc_approved", "KYC Approved", "Instant", 0),
    ("order_booked", "Order Booked", "+0-1 Day", 1),
    ("feasibility_passed", "Field Feasibility Done", "+1 Day", 1),
    ("installed", "Equipment Installed", "+3-5 Days", 4),
    ("activated", "Service Active", "Live", 0)
]

NOTIFICATIONS_TEMPLATES = {
    "quote_accepted": {
        "en": "👋 Hello {name}! Your Accel Business order #{order_id} is confirmed. Estimated activation by {promised_date}.",
        "hi": "👋 नमस्ते {name}! आपका Accel Business ऑर्डर #{order_id} कन्फर्म हो गया है। एक्टिवेशन {promised_date} तक।"
    },
    "kyc_approved": {
        "en": "✅ KYC Approved: Business credentials verified against registry records in 3 seconds.",
        "hi": "✅ केवाईसी स्वीकृत: आपके व्यावसायिक दस्तावेज़ 3 सेकंड में सरकारी रिकॉर्ड से सत्यापित हो गए।"
    },
    "order_booked": {
        "en": "📦 Order Booked: Terminal hardware assigned at local distribution hub for {name}.",
        "hi": "📦 ऑर्डर बुक हुआ: {name} के लिए स्थानीय वितरण केंद्र पर हार्डवेयर आवंटित किया गया।"
    },
    "feasibility_passed": {
        "en": "📡 Site Feasibility: Signal coverage and fibre terminal confirmed for {address}.",
        "hi": "📡 साइट फ़ीजिबिलिटी: {address} पर नेटवर्क कवरेज और फ़ाइबर टर्मिनल की पुष्टि हो गई है।"
    },
    "installed": {
        "en": "🛠️ Setup Complete: Router and terminal devices tested with 99.9% signal strength.",
        "hi": "🛠️ सेटअप पूर्ण: राउटर और टर्मिनल डिवाइस का परीक्षण सफल, 99.9% सिग्नल स्ट्रेंथ।"
    },
    "activated": {
        "en": "🚀 Congratulations {name}! Your high-speed business line is now ACTIVE. Enjoy our delay-guarantee SLA.",
        "hi": "🚀 बधाई हो {name}! आपकी हाई-स्पीड बिज़नेस लाइन अब चालू है। हमारी गारंटी सेवा का आनंद लें।"
    }
}

def create_order_for_journey(journey: Journey, session: Session) -> Order:
    existing = session.exec(select(Order).where(Order.journey_id == journey.id)).first()
    if existing:
        return existing
        
    # Find quote to get promised date
    quote = session.exec(select(Quote).where(Quote.journey_id == journey.id)).first()
    promised_date = "2026-07-24"
    if quote and quote.bundle_json:
        try:
            bundle_data = json.loads(quote.bundle_json)
            max_inst = max([item.get("install_days", 3) for item in bundle_data], default=3)
            base_dt = datetime.strptime(settings.DEMO_TODAY, "%Y-%m-%d")
            promised_date = (base_dt + timedelta(days=1 + max_inst)).strftime("%Y-%m-%d")
        except:
            pass

    order = Order(
        journey_id=journey.id,
        status="quote_accepted",
        promised_date=promised_date
    )
    session.add(order)
    session.commit()
    session.refresh(order)

    # Initial event and notification
    event = OrderEvent(order_id=order.id, status="quote_accepted", message_key="order_created")
    session.add(event)

    cust_name = journey.business_name or "Partner"
    msg_tpl = NOTIFICATIONS_TEMPLATES["quote_accepted"].get(journey.language, NOTIFICATIONS_TEMPLATES["quote_accepted"]["en"])
    notif = Notification(
        order_id=order.id,
        channel="whatsapp_sim",
        body=msg_tpl.format(name=cust_name, order_id=order.id[:8].upper(), promised_date=promised_date),
        language=journey.language
    )
    session.add(notif)
    session.commit()

    return order


def advance_order_status(order: Order, session: Session, advance_count: int = 1) -> Order:
    status_keys = [k for k, _, _, _ in STATUS_PIPELINE]
    cur_idx = status_keys.index(order.status) if order.status in status_keys else 0
    next_idx = min(len(status_keys) - 1, cur_idx + advance_count)

    if next_idx > cur_idx:
        journey = session.get(Journey, order.journey_id)
        cust_name = journey.business_name if journey else "Partner"
        addr = journey.address if journey else "registered premises"
        lang = journey.language if journey else "en"

        for idx in range(cur_idx + 1, next_idx + 1):
            st = status_keys[idx]
            order.status = st
            
            # Event
            event = OrderEvent(order_id=order.id, status=st, message_key=f"status_{st}", simulated=True)
            session.add(event)

            # Notification
            tpl_dict = NOTIFICATIONS_TEMPLATES.get(st, {})
            body_template = tpl_dict.get(lang, tpl_dict.get("en", "Order status updated."))
            body_text = body_template.format(
                name=cust_name,
                order_id=order.id[:8].upper(),
                promised_date=order.promised_date,
                address=addr
            )
            notif = Notification(
                order_id=order.id,
                channel="whatsapp_sim",
                body=body_text,
                language=lang
            )
            session.add(notif)
            
        session.add(order)
        session.commit()
        session.refresh(order)

    return order


def get_order_timeline(order: Order, session: Session) -> Dict[str, Any]:
    status_keys = [k for k, _, _, _ in STATUS_PIPELINE]
    cur_idx = status_keys.index(order.status) if order.status in status_keys else 0
    
    events = session.exec(select(OrderEvent).where(OrderEvent.order_id == order.id)).all()
    event_map = {e.status: e.ts for e in events}

    timeline = []
    for idx, (s_key, label, eta_str, _) in enumerate(STATUS_PIPELINE):
        is_done = idx < cur_idx or order.status == "activated"
        is_current = (idx == cur_idx and order.status != "activated")
        
        timeline.append({
            "status_key": s_key,
            "label": label,
            "done": is_done,
            "current": is_current,
            "ts": event_map.get(s_key),
            "eta": eta_str
        })

    notifications = session.exec(
        select(Notification).where(Notification.order_id == order.id).order_by(Notification.ts)
    ).all()

    return {
        "order_id": order.id,
        "journey_id": order.journey_id,
        "status": order.status,
        "promised_date": order.promised_date,
        "timeline": timeline,
        "notifications": [
            {
                "id": n.id,
                "channel": n.channel,
                "body": n.body,
                "language": n.language,
                "ts": n.ts
            } for n in notifications
        ]
    }

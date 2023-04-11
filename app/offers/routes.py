from flask import Blueprint, request

from app.models import Item, Offer
from flask import (
    render_template,
)


offers_bp = Blueprint("offers", __name__)


@offers_bp.route("/<string:offer_title>")
def offer(offer_title):
    offer = Offer.query.filter_by(title=offer_title).first()
    offer_id = offer.id if offer else None
    offer = Offer.query.get_or_404(offer_id)
    page = request.args.get("page", 1, type=int)
    items = Item.query.filter_by(offer_id=offer_id).paginate(
        page=page, per_page=6
    )
    return render_template(
        "offer.html",
        title=offer.title,
        offer=offer,
        items=items,
    )


@offers_bp.route("/offers")
def offers():
    page = request.args.get("page", 1, type=int)
    offers = Offer.query.paginate(page=page, per_page=6)
    return render_template("offers.html", title="Offers", offers=offers)

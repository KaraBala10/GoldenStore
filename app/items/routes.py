from flask import Blueprint
from app.models import Item, Offer
from flask import (
    render_template,
    url_for,
    flash,
    redirect,
    request,
    session,
    abort,
)
from app.items.forms import (
    NewItemForm,
    ItemUpdateForm,
)
from app.offers.forms import NewOfferForm

from app import db
from flask_modals import render_template_modal
from flask_login import (
    login_required,
    current_user,
)
from app.helpers import save_picture
from app.items.helpers import get_previous_next_item, delete_picture

items = Blueprint("items", __name__)


@items.route("/dashboard/new_item", methods=["GET", "POST"])
@login_required
def new_item():
    new_item_form = NewItemForm()
    new_offer_form = NewOfferForm()
    form = ""
    flag = session.pop("flag", False)
    if "content" in request.form:
        form = "new_item_form"
    elif "description" in request.form:
        form = "new_offer_form"

    if form == "new_item_form" and new_item_form.validate_on_submit():
        if new_item_form.thumbnail.data:
            picture_file = save_picture(
                new_item_form.thumbnail.data, "static/item_thumbnails"
            )
        item_slug = str(new_item_form.slug.data).replace(" ", "-")
        offer = new_item_form.offer.data
        item = Item(
            title=new_item_form.title.data,
            content=new_item_form.content.data,
            slug=item_slug,
            author=current_user,
            offer_name=offer,
            thumbnail=picture_file,
        )
        db.session.add(item)
        db.session.commit()
        flash("Your item has been created!", "success")
        return redirect(url_for("items.new_item"))

    elif form == "new_offer_form" and new_offer_form.validate_on_submit():
        if new_offer_form.icon.data:
            picture_file = save_picture(
                new_offer_form.icon.data, "static/offer_icons", output_size=(150, 150)
            )
        offer_title = str(new_offer_form.title.data).replace(" ", "-")
        offer = Offer(
            title=new_offer_form.title.data,
            description=new_offer_form.description.data,
            price=new_offer_form.price.data,
            icon=picture_file,
        )
        db.session.add(offer)
        db.session.commit()
        session["flag"] = True
        flash("New Offer has been created!", "success")
        return redirect(url_for("users.dashboard"))

    modal = None if flag else "newOffer"
    return render_template_modal(
        "new_item.html",
        title="New item",
        new_item_form=new_item_form,
        new_offer_form=new_offer_form,
        active_tab="new_item",
        modal=modal,
    )


@items.route("/<string:offer>/<string:item_slug>")
def item(item_slug, offer):
    item = Item.query.filter_by(slug=item_slug).first()
    if item:
        previous_item, next_item = get_previous_next_item(item)
    item_id = item.id if item else None
    item = Item.query.get_or_404(item_id)
    return render_template(
        "item_view.html",
        title=item.title,
        item=item,
        previous_item=previous_item,
        next_item=next_item,
    )


@items.route("/dashboard/user_items", methods=["GET", "POST"])
@login_required
def user_items():
    return render_template(
        "user_items.html", title="Your Items", active_tab="user_items"
    )


@items.route("/<string:offer>/<string:item_slug>/update", methods=["GET", "POST"])
def update_item(item_slug, offer):
    item = Item.query.filter_by(slug=item_slug).first()
    if item:
        previous_item, next_item = get_previous_next_item(item)
    item_id = item.id if item else None
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        abort(403)
    form = ItemUpdateForm()
    if form.validate_on_submit():
        item.offer_name = form.offer.data
        item.title = form.title.data
        item.slug = str(form.slug.data).replace(" ", "-")
        item.content = form.content.data
        if form.thumbnail.data:
            delete_picture(item.thumbnail, "static/item_thumbnails")
            new_picture = save_picture(
                form.thumbnail.data, "static/item_thumbnails")
            item.thumbnail = new_picture
        db.session.commit()
        flash("Your item has been updated!", "success")
        return redirect(
            url_for("items.item", item_slug=item.slug,
                    offer=item.offer_name.title)
        )
    elif request.method == "GET":
        form.offer.data = item.offer_name.title
        form.title.data = item.title
        form.slug.data = item.slug
        form.content.data = item.content
    return render_template(
        "update_item.html",
        title="Update | " + item.title,
        item=item,
        previous_item=previous_item,
        next_item=next_item,
        form=form,
    )


@items.route("/item/<item_id>/delete", methods=["POST"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    if item.author != current_user:
        abort(403)
    db.session.delete(item)
    db.session.commit()
    flash("Your item has been deleted!", "success")
    return redirect(url_for("items.user_items"))

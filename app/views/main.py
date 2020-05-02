from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import current_user, login_required
from app import db
from app.models import User, Deck, Card
from app.forms.main import CreateDeckForm, EditDeckForm ,CreateCardForm, EditCardForm, EditUserForm

main = Blueprint('main', __name__)

@main.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()

# INDEX =============================================================
@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect( url_for('main.feed') )

    return render_template('main/landing.html')

# FEED ==============================================================
@main.route('/feed')
@login_required
def feed():
    # load users decks + followed users decks
    page = request.args.get('page', 1, type=int)
    decks = current_user.followed_decks().paginate(
        page, current_app.config['DECKS_PER_PAGE'], False
    )
    next_url = url_for('main.feed', page=decks.next_num) if decks.has_next else None
    prev_url = url_for('main.feed', page=decks.prev_num) if decks.has_prev else None

    return render_template(
        'main/feed.html',
        decks=decks.items,
        next_url=next_url, 
        prev_url=prev_url,
    )

# EXPLORE ===========================================================
@main.route('/explore')
@login_required
def explore():
    # load newest decks to render on explore page
    page = request.args.get('page', 1, type=int)
    decks = Deck.query.order_by(Deck.created.desc()).paginate(
        page, current_app.config['DECKS_PER_PAGE'], False
    )
    next_url = url_for('main.explore', page=decks.next_num) if decks.has_next else None
    prev_url = url_for('main.explore', page=decks.prev_num) if decks.has_prev else None

    return render_template(
        'main/explore.html',
        decks=decks.items,
        next_url=next_url, 
        prev_url=prev_url,
    )

# DECK NEW ==========================================================
@main.route('/decks/new', methods=['GET', 'POST'])
@login_required
def deck_new():
    # setup form for creation of new deck
    form=CreateDeckForm()
    if form.validate_on_submit():
        deck = Deck(
            name=form.name.data,
            description=form.description.data,
            author=current_user
        )
        db.session.add(deck)
        db.session.commit()
        flash('Deck created successfully')
        return redirect( url_for('main.deck_manage', deck_id=deck.id) )


    return render_template(
        'main/deck_new.html',
        form=form,
    )

# DECK VIEW =========================================================
@main.route('/decks/<deck_id>/view')
@login_required
def deck_view(deck_id):
    # load cards in the deck
    deck = Deck.query.filter_by(id=deck_id).first_or_404()

    # load cards in the deck
    cards = deck.cards.all()

    return render_template(
        'main/deck_view.html',
        deck=deck,
        cards=cards,
        num_cards=len(cards),
    )

# DECK MANAGE =======================================================
@main.route('/decks/<deck_id>/manage')
@login_required
def deck_manage(deck_id):
    # find deck model
    deck = Deck.query.filter_by(id=deck_id).first_or_404()

    # validate deck owner is logged in 
    if( deck.author != current_user ):
        flash('Access Denied.')
        return redirect( url_for('main.index') )

    # load cards in the deck
    cards = deck.cards.all()

    return render_template(
        'main/deck_manage.html',
        deck=deck,
        cards=cards,
        num_cards=len(cards),
    )

# DECK EDIT =========================================================
@main.route('/decks/<deck_id>/edit', methods=['GET', 'POST'])
@login_required
def deck_edit(deck_id):
    # find deck model 
    deck = Deck.query.filter_by(id=deck_id).first_or_404()

    # validate deck owner is logged in 
    if( deck.author != current_user ):
        flash('Access Denied.')
        return redirect( url_for('main.index') )

   # setup form for editing deck
    form = EditDeckForm()
    if form.validate_on_submit():
        deck.name = form.name.data
        deck.description = form.description.data
        deck.last_edited = datetime.utcnow()
        db.session.add(deck)
        db.session.commit()
        flash('Deck updated successfully.')
        return redirect( url_for('main.deck_manage', deck_id=deck.id) )
    elif request.method == 'GET':
        form.name.data = deck.name
        form.description.data = deck.description
    
    return render_template(
        'main/deck_edit.html',
        form=form,
    )

# DECK DELETE =======================================================
@main.route('/decks/<deck_id>/delete')
@login_required
def deck_delete(deck_id):
    # find deck model 
    deck = Deck.query.filter_by(id=deck_id).first_or_404()

    # validate deck owner is logged in 
    if( deck.author != current_user ):
        flash('Access Denied.')
        return redirect( url_for('main.index') )

    # remove deck and all cards from db
    db.session.delete(deck)
    db.session.commit()
    flash('Deck successfully deleted.')

    return redirect( url_for('main.user', username=current_user.username) )

# CARD NEW ==========================================================
@main.route('/decks/<deck_id>/cards/new', methods=['GET', 'POST'])
@login_required
def card_new(deck_id):
    # find deck model
    deck = Deck.query.filter_by(id=deck_id).first_or_404()

    # setup up form for creation of new card
    form = CreateCardForm()
    if form.validate_on_submit():
        card = Card(
            front=form.front.data,
            back=form.back.data,
            author=current_user,
            deck=deck
        )
        deck.last_edited = datetime.utcnow()
        db.session.add(card)
        db.session.commit()
        flash(f'Card succesfully created.')
        return redirect( url_for('main.deck_manage', deck_id=deck.id) )

    return render_template(
        'main/card_new.html',
        form=form,
    )

# CARD EDIT =======================================================
@main.route('/decks/<deck_id>/cards/<card_id>/edit', methods=['GET', 'POST'])
@login_required
def card_edit(deck_id, card_id):
    # find deck and card model
    deck = Deck.query.filter_by(id=deck_id).first_or_404()
    card = Card.query.filter_by(id=card_id).first_or_404()

    # validate deck owner is logged in 
    if( card.author != current_user ):
        flash('Access Denied.')
        return redirect( url_for('main.index') )

    # setup form for editing card
    form = EditCardForm()
    if form.validate_on_submit():
        card.front = form.front.data
        card.back = form.back.data
        deck.last_edited = datetime.utcnow()
        db.session.add(card)
        db.session.commit() 
        flash(f'Card succesfully updated.')
        return redirect( url_for('main.deck_manage', deck_id=deck_id) )
    elif request.method == 'GET':
        form.front.data = card.front
        form.back.data = card.back

    return render_template(
        'main/card_edit.html',
        form=form,
    )

# CARD DELETE =======================================================
@main.route('/decks/<deck_id>/cards/<card_id>/delete')
@login_required
def card_delete(deck_id, card_id):
    # find card model
    deck = Deck.query.filter_by(id=deck_id).first_or_404()
    card = Card.query.filter_by(id=card_id).first_or_404()

    # validate deck owner is logged in 
    if( card.author != current_user ):
        flash('Access Denied.')
        return redirect( url_for('main.index') )
    
    # remove card from db
    deck.last_edited = datetime.utcnow()
    db.session.delete(card)
    db.session.commit()
    flash('Card successfully deleted.')

    return redirect( url_for('main.deck_manage', deck_id=deck_id) )

# USER ==============================================================
@main.route('/users/<username>')
@login_required
def user(username):
    # load user and thier decks
    user = User.query.filter_by(username=username).first_or_404()

    page = request.args.get('page', 1, type=int)
    decks = user.decks.paginate(
        page, current_app.config['DECKS_PER_USER'], False
    )
    next_url = url_for('main.user', username=user.username, page=decks.next_num) if decks.has_next else None
    prev_url = url_for('main.user', username=user.username, page=decks.prev_num) if decks.has_prev else None

    return render_template(
        'main/user.html',
        user=user,
        decks=decks.items,
        next_url=next_url, 
        prev_url=prev_url,
    )

# EDIT USER =========================================================
@main.route('/edit_user', methods=['GET', 'POST'])
@login_required
def edit_user():
    # setup edit user form
    form = EditUserForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect( url_for('main.edit_user') )
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me

    return render_template(
        'main/edit_user.html',
        form=form,
    )

# FOLLOW ============================================================
@main.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(f'User {username} not found.')
        return redirect( url_for('main.index') )

    if user == current_user:
        flash('You cannot follow yourself!')
        return redirect( url_for('main.user', username=username) )

    current_user.follow(user)
    db.session.commit()
    flash(f'You are now following {username}!')

    return redirect( url_for('main.user', username=username) )

# UNFOLLOW ==========================================================
@main.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        flash(f'User {username} not found.')
        return redirect( url_for('main.index') )

    if user == current_user:
        flash('You cannot unfollow yourself!')
        return redirect( url_for('main.user', username=username) )

    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are no longer following {username}.')

    return redirect(url_for('main.user', username=username))
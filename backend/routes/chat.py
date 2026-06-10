from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from database import db
from models import Message, User
from sqlalchemy import or_, and_

chat_bp = Blueprint('chat', __name__)

@chat_bp.route('/conversations', methods=['GET'])
@jwt_required()
def get_conversations():
    user_id = int(get_jwt_identity())
    msgs = Message.query.filter(
        or_(Message.sender_id == user_id, Message.receiver_id == user_id)
    ).all()
    partner_ids = set()
    for m in msgs:
        partner_ids.add(m.receiver_id if m.sender_id == user_id else m.sender_id)
    partners = []
    for pid in partner_ids:
        partner = User.query.get(pid)
        if partner:
            last_msg = Message.query.filter(
                or_(
                    and_(Message.sender_id == user_id, Message.receiver_id == pid),
                    and_(Message.sender_id == pid, Message.receiver_id == user_id)
                )
            ).order_by(Message.created_at.desc()).first()
            unread = Message.query.filter_by(sender_id=pid, receiver_id=user_id, is_read=False).count()
            partners.append({
                'user': partner.to_dict(),
                'last_message': last_msg.to_dict() if last_msg else None,
                'unread_count': unread
            })
    return jsonify(partners)

@chat_bp.route('/messages/<int:other_id>', methods=['GET'])
@jwt_required()
def get_messages(other_id):
    user_id = int(get_jwt_identity())
    msgs = Message.query.filter(
        or_(
            and_(Message.sender_id == user_id, Message.receiver_id == other_id),
            and_(Message.sender_id == other_id, Message.receiver_id == user_id)
        )
    ).order_by(Message.created_at.asc()).all()
    # Mark as read
    Message.query.filter_by(sender_id=other_id, receiver_id=user_id, is_read=False).update({'is_read': True})
    db.session.commit()
    return jsonify([m.to_dict() for m in msgs])

@chat_bp.route('/messages', methods=['POST'])
@jwt_required()
def send_message():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    msg = Message(sender_id=user_id, receiver_id=data['receiver_id'], content=data['content'])
    db.session.add(msg)
    db.session.commit()
    return jsonify(msg.to_dict()), 201

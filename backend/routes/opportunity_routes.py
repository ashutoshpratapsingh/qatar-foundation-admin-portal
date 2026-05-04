from flask import Blueprint, request, jsonify
from models import Opportunity
from extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

opp_bp = Blueprint('opportunity', __name__)

# GET ALL
@opp_bp.route('', methods=['GET'])
@opp_bp.route('/', methods=['GET'])
@jwt_required()
def get_all():
    admin_id = int(get_jwt_identity())

    opps = Opportunity.query.filter_by(admin_id=admin_id).all()

    return jsonify([
        {
            "id": o.id,
            "name": o.name,
            "category": o.category,
            "duration": o.duration,
            "start_date": o.start_date,
            "description": o.description
        } for o in opps
    ])


# CREATE
@opp_bp.route('', methods=['POST'])
@opp_bp.route('/', methods=['POST'])
@jwt_required()
def create():
    admin_id = int(get_jwt_identity())
    data = request.json

    required_fields = [
        "name", "duration", "start_date",
        "description", "skills",
        "category", "future_opportunities"
    ]

    for field in required_fields:
        if not data.get(field):
            return jsonify({"error": f"{field} required"}), 400

    opp = Opportunity(
        admin_id=admin_id,
        name=data["name"],
        duration=data["duration"],
        start_date=data["start_date"],
        description=data["description"],
        skills=data["skills"],
        category=data["category"],
        future_opportunities=data["future_opportunities"],
        max_applicants=data.get("max_applicants")
    )

    db.session.add(opp)
    db.session.commit()

    return jsonify({"message": "Created", "id": opp.id})


# GET DETAILS
@opp_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def details(id):
    admin_id = int(get_jwt_identity())

    opp = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()

    if not opp:
        return jsonify({"error": "Not found"}), 404

    return jsonify({
    "id": opp.id,
    "name": opp.name,
    "duration": opp.duration,
    "start_date": opp.start_date,
    "description": opp.description,
    "skills": opp.skills,
    "category": opp.category,
    "future_opportunities": opp.future_opportunities,
    "max_applicants": opp.max_applicants
})


# UPDATE
@opp_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    admin_id = int(get_jwt_identity())

    opp = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()

    if not opp:
        return jsonify({"error": "Not found"}), 404

    data = request.json

    for key in data:
        setattr(opp, key, data[key])

    db.session.commit()

    return jsonify({"message": "Updated"})


# DELETE
@opp_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    admin_id = int(get_jwt_identity())

    opp = Opportunity.query.filter_by(id=id, admin_id=admin_id).first()

    if not opp:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(opp)
    db.session.commit()

    return jsonify({"message": "Deleted"})
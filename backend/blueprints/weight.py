from flask import jsonify, request, Blueprint
from models.weight_model import Weight  
from app import db

bp = Blueprint('weight', __name__, url_prefix='/weight')

@bp.route("/", methods=['GET'])
def get_all_weights():
    try:
        weights = Weight.query.all()
        weight_data = [
            {
                'id': weight.id,
                'date': weight.date.strftime('%Y-%m-%d'),  # Convert datetime to string
                'weight': weight.weight,
                'fat': weight.fat,
                'total_body_water': weight.total_body_water,
                'muscle_mass': weight.muscle_mass,
                'bone_density': weight.bone_density
            }
            for weight in weights
        ]
        return jsonify(weight_data), 200

    except Exception as e:
        return jsonify(error=f'Error retrieving weights: {str(e)}'), 500


@bp.route("/<int:weight_id>", methods=['GET'])
def get_weight(weight_id):
    try:
        weight = Weight.query.get_or_404(weight_id)
        weight_data = {
            'id': weight.id,
            'date': weight.date.strftime('%Y-%m-%d'),  # Convert datetime to string
            'weight': weight.weight,
            'fat': weight.fat,
            'total_body_water': weight.total_body_water,
            'muscle_mass': weight.muscle_mass,
            'bone_density': weight.bone_density
        }
        return jsonify(weight_data), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'Error retrieving weight: {str(e)}'), 500


@bp.route("/", methods=['POST'])
def add_weight():
    try:
        data = request.json
        date = data.get('date')
        weight = data.get('weight')
        fat = data.get('fat')
        total_body_water = data.get('total_body_water')
        muscle_mass = data.get('muscle_mass')
        bone_density = data.get('bone_density')

        new_weight = Weight(
            date=date,
            weight=weight,
            fat=fat,
            total_body_water=total_body_water,
            muscle_mass=muscle_mass,
            bone_density=bone_density
        )

        db.session.add(new_weight)
        db.session.commit()

        return jsonify(message='Weight entry created successfully'), 201

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'Error creating weight entry: {str(e)}'), 500


@bp.route("/<int:weight_id>", methods=['PUT'])
def update_weight(weight_id):
    try:
        weight = Weight.query.get_or_404(weight_id)

        data = request.json
        weight.date = data.get('date')
        weight.weight = data.get('weight')
        weight.fat = data.get('fat')
        weight.total_body_water = data.get('total_body_water')
        weight.muscle_mass = data.get('muscle_mass')
        weight.bone_density = data.get('bone_density')

        db.session.commit()

        return jsonify(message='Weight entry updated successfully'), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'Error updating weight entry: {str(e)}'), 500


@bp.route("/<int:weight_id>", methods=['DELETE'])
def delete_weight(weight_id):
    try:
        weight = Weight.query.get_or_404(weight_id)
        db.session.delete(weight)
        db.session.commit()

        return jsonify(message='Weight entry deleted successfully'), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(error=f'Error deleting weight entry: {str(e)}'), 500

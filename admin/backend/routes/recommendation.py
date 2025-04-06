from flask import Blueprint, jsonify, request
from models import db
from models.recommendation import RecommendationAlgorithmParam, RecommendationRule, RecommendationResult
from sqlalchemy import desc

recommendation_bp = Blueprint('recommendation', __name__)

@recommendation_bp.route('/recommendation/rules/list', methods=['GET'])
def get_rules_list():
    rules = RecommendationRule.query.filter_by(is_active=True).all()
    return jsonify([rule.to_dict() for rule in rules]) 
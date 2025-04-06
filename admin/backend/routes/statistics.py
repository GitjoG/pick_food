from flask import Blueprint, jsonify, request
from models import db
from models.statistics import NutritionGoalStatistics
from sqlalchemy import func

statistics_bp = Blueprint('statistics', __name__)

@statistics_bp.route('/statistics/nutrition-goals', methods=['GET'])
def get_nutrition_goals_statistics():
    stats = NutritionGoalStatistics.query.all()
    return jsonify([stat.to_dict() for stat in stats]) 
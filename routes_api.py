# routes_api.py
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import NewsRequestSchema, NewsResponseSchema
from models import NewsModel
from models import db
from sqlalchemy.exc import SQLAlchemyError
from logger import configure_logger  # Import logger configuration

# Use the logger configuration
logger = configure_logger()

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/news/search")
@api_bp.route("/news/search/")
class ApiNewsSeach(MethodView):

    @api_bp.response(200, NewsResponseSchema(many=True))
    @api_bp.arguments(NewsRequestSchema)
    def post(self, search_data):
        try:
            start_date = search_data['start_date']
            end_date = search_data['end_date']
            
            if start_date > end_date:
                return abort(400, message="Start date cannot be greater than end date")

            sentiment = search_data.get('type')
            if sentiment is None:
                items = NewsModel.query.filter(NewsModel.date.between(start_date, end_date)).all()
            else:
                items = NewsModel.query.filter(
                    NewsModel.date.between(start_date, end_date),
                    NewsModel.sentimentAnalysis.like(sentiment)
                ).all()
            return items
        except SQLAlchemyError as e:
            db.session.rollback()
            # Log the error for future reference
            logger.error(f"Database error: {str(e)}")
            return abort(500, message="An error occurred while processing the search request.")

@api_bp.route("/news")
@api_bp.route("/news/")
class ApiNewsAll(MethodView):

    @api_bp.response(200, NewsResponseSchema(many=True))
    def get(self):
        try:
            items = NewsModel.query.all()
            return items
        except SQLAlchemyError as e:
            db.session.rollback()
            # Log the error for future reference
            logger.error(f"Database error: {str(e)}")
            return abort(500, message="An error occurred while retrieving all news.")


@api_bp.route("/news/<int:news_id>")
@api_bp.route("/news/<int:news_id>/")
class NewsApiItem(MethodView):

    @api_bp.response(200, NewsResponseSchema)
    def get(self, news_id):
        try:
            item = NewsModel.query.get_or_404(str(news_id))
            return item
        except SQLAlchemyError as e:
            # Log the error for future reference
            logger.error(f"Database error: {str(e)}")
            return abort(500, message="An error occurred while retrieving a single news item.")

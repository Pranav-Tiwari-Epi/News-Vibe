# routes_frontend.py
from flask import request, render_template
from flask.views import MethodView
from flask_smorest import Blueprint
from models import NewsModel, db
from sqlalchemy.exc import SQLAlchemyError
from logger import configure_logger  # Import logger configuration

logger = configure_logger()
frontend_bp = Blueprint("frontend", __name__, template_folder="templates")

@frontend_bp.route("/", methods=["GET"])
class LandingPage(MethodView):
    def get(self):
        return render_template('index.html')
    
@frontend_bp.route("/news/search", methods=["GET", "POST"])
@frontend_bp.route("/news/search/", methods=["GET", "POST"])
class FrontendNewsSearch(MethodView):
    def get(self):
        return render_template('search_display.html')

    def post(self):
        try:
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            sentiment = request.form.get('type')

            if start_date > end_date:
                return render_template('search_display.html', error="Start date cannot be greater than end date")

            if sentiment is None:
                items = NewsModel.query.filter(NewsModel.date.between(start_date, end_date)).all()
            else:
                items = NewsModel.query.filter(
                    NewsModel.date.between(start_date, end_date),
                    NewsModel.sentimentAnalysis.like(sentiment)
                ).all()
            return render_template('search_display.html', items=items)
        except SQLAlchemyError as e:
            db.session.rollback()
            error_message = f"Database error: {str(e)}"
            logger.error(f"Database error: {str(e)}")  # Use the logger for error logging
            return render_template('search_display.html', error=error_message)

@frontend_bp.route("/news", methods=["GET"])
@frontend_bp.route("/news/", methods=["GET"])
class FrontendNewsAll(MethodView):
    def get(self):
        try:
            items = NewsModel.query.all()
            return render_template('news_list.html', items=items)
        except SQLAlchemyError as e:
            db.session.rollback()
            error_message = f"Database error: {str(e)}"
            logger.error(f"Database error: {str(e)}")  # Use the logger for error logging
            return render_template('news_list.html', error=error_message)

@frontend_bp.route("/news/<int:news_id>")
@frontend_bp.route("/news/<int:news_id>/")
class NewsItem(MethodView):
    def get(self, news_id):
        try:
            item = NewsModel.query.get_or_404(str(news_id))
            return render_template('news_item_display.html', item=item)
        except SQLAlchemyError as e:
            return render_template('news_item_display.html', error=f"Database error: {str(e)}")

from flask import request
from flask import render_template
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schema import NewsRequestSchema, NewsResponseSchema
from models import NewsModel
from models import db
from sqlalchemy.exc import SQLAlchemyError

frontend_bp = Blueprint("frontend", __name__, template_folder="templates")
api_bp = Blueprint("api", __name__, url_prefix="/api")


@frontend_bp.route("/news", methods=["GET", "POST"])
@frontend_bp.route("/news/", methods=["GET", "POST"])
class FrontendNews(MethodView):
    def get(self):
        try:
            items = NewsModel.query.all()
            return render_template('index.html', items=items)
        except SQLAlchemyError as e:
            db.session.rollback()
            error_message = f"Database error: {str(e)}"
            return render_template('index.html', error=error_message)
    def post(self):
        try:
            start_date = request.form.get('start_date')
            end_date = request.form.get('end_date')
            sentiment = request.form.get('type')

            if start_date > end_date:
                return render_template('index.html', error="Start date cannot be greater than end date")

            if sentiment is None:
                items = NewsModel.query.filter(NewsModel.date.between(start_date, end_date)).all()
            else:
                items = NewsModel.query.filter(
                    NewsModel.date.between(start_date, end_date),
                    NewsModel.sentimentAnalysis.like(sentiment)
                ).all()
            return render_template('index.html', items=items)
        except SQLAlchemyError as e:
            db.session.rollback()
            error_message = f"Database error: {str(e)}"
            return render_template('index.html', error=error_message)        

@frontend_bp.route("/news/<int:news_id>")
@frontend_bp.route("/news/<int:news_id>/")
class FrontendNewsItem(MethodView):
    def get(self, news_id):
        try:
            item = NewsModel.query.get_or_404(str(news_id))
            return render_template('news_item.html', item=item)
        except SQLAlchemyError as e:
            return render_template('news_item.html', error=f"Database error: {str(e)}")

        
@api_bp.route("/news")
@api_bp.route("/news/")
class ApiNews(MethodView):

    @api_bp.response(200, NewsResponseSchema(many=True))
    def get(self):
        try:
            items = NewsModel.query.all()
            return items
        except SQLAlchemyError as e:
            db.session.rollback()
            return abort(500, message=f"Database error: {str(e)}")

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
            return abort(500, message=f"Database error: {str(e)}")


@api_bp.route("/news/<int:news_id>")
@api_bp.route("/news/<int:news_id>/")
class ApiNewsItem(MethodView):

    @api_bp.response(200, NewsResponseSchema)
    def get(self, news_id):
        try:
            item = NewsModel.query.get_or_404(str(news_id))
            return item
        except SQLAlchemyError as e:
            return abort(500, message=f"Database error: {str(e)}")


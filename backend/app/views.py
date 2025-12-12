import os
import json
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.httpexceptions import HTTPBadRequest, HTTPInternalServerError
from pyramid.response import FileResponse
import os
from sqlalchemy.exc import SQLAlchemyError
from .models import Review
from .genai_helper import extract_key_points
from .huggingface_helper import analyze_sentiment  # buat helper
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def json_response(data, status=200):
    # ensure charset is set so WebOb accepts a text body
    return Response(json.dumps(data), content_type='application/json', charset='utf-8', status=status)


@view_config(route_name='home', request_method='GET')
def home(request):
    # if frontend build exists, serve its index.html for root
    dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'frontend', 'dist'))
    index_file = os.path.join(dist_path, 'index.html')
    if os.path.isfile(index_file):
        return FileResponse(index_file)
    return Response('API is running. Endpoints: /api/analyze-review, /api/reviews', content_type='text/plain')

@view_config(route_name='analyze_review', request_method='POST')
def analyze_review(request):
    try:
        body = request.json_body
        text = body.get('text', '').strip()
    except Exception:
        return HTTPBadRequest(json_response({"error": "Invalid JSON"}))

    if not text:
        return HTTPBadRequest(json_response({"error": "text is required"}))

    # sentiment via Hugging Face
    try:
        sentiment = analyze_sentiment(text)
    except Exception as e:
        return HTTPInternalServerError(json_response({"error": "sentiment error", "detail": str(e)}))

    # key points via Gemini
    try:
        key_points = extract_key_points(text)
    except Exception as e:
        return HTTPInternalServerError(json_response({"error": "keypoints error", "detail": str(e)}))

    # save to db
    DBSession = request.registry.DBSession
    try:
        review = Review(text=text, sentiment=sentiment, key_points=json.dumps(key_points))
        DBSession.add(review)
        DBSession.flush()  # to get id
        DBSession.commit()
    except SQLAlchemyError as e:
        DBSession.rollback()
        return HTTPInternalServerError(json_response({"error": "db error", "detail": str(e)}))

    return json_response({"result": review.to_dict()})

@view_config(route_name='get_reviews', request_method='GET')
def get_reviews(request):
    DBSession = request.registry.DBSession
    try:
        rows = DBSession.query(Review).order_by(Review.created_at.desc()).all()
        data = [r.to_dict() for r in rows]
    except SQLAlchemyError as e:
        return HTTPInternalServerError(json_response({"error": "db error", "detail": str(e)}))
    return json_response({"reviews": data})

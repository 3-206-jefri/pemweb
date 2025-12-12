import os
from pyramid.config import Configurator
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from .models import Base
from pyramid.response import FileResponse
import os
from dotenv import load_dotenv
load_dotenv()

# Use DATABASE_URL from environment if provided, otherwise fall back
# to a local SQLite file for development to avoid startup errors.
DB_URL = os.environ.get("DATABASE_URL") or "sqlite:///development.db"

def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('analyze_review', '/api/analyze-review')
    config.add_route('get_reviews', '/api/reviews')
    # add a simple root route so visiting `/` doesn't return 404
    config.add_route('home', '/')

    # DB session shared via registry
    # If a DATABASE_URL is provided but connection fails, fall back to local sqlite for development.
    env_db = os.environ.get("DATABASE_URL")
    if env_db:
        try:
            engine = create_engine(env_db)
            Base.metadata.create_all(engine)
        except Exception:
            # fallback to sqlite file when remote DB is unreachable or misconfigured
            engine = create_engine("sqlite:///development.db")
            Base.metadata.create_all(engine)
    else:
        engine = create_engine(DB_URL)
        Base.metadata.create_all(engine)

    DBSession = scoped_session(sessionmaker(bind=engine))
    config.registry.DBSession = DBSession

    config.scan()

    # Serve frontend built files if present (Vite build output `dist`)
    # Path: project_root/frontend/frontend/dist
    dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'frontend', 'frontend', 'dist'))
    if os.path.isdir(dist_path):
        # serve dist files at root (so built assets like /index.html and /assets/* work)
        config.add_static_view('', dist_path, cache_max_age=0)

        # fallback route for SPA: serve index.html for non-API GET requests
        def _spa_view(request):
            index_file = os.path.join(dist_path, 'index.html')
            return FileResponse(index_file)

        config.add_route('spa', '/*subpath')
        config.add_view(_spa_view, route_name='spa', request_method='GET')
    return config.make_wsgi_app()

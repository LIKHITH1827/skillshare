from app.db.base_class import Base

# Import models only for Alembic (not for runtime use)
from app.models import user, course, enrollment

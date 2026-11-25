from fastapi import APIRouter
from cyan.edition_routes import router as router_0
from cyan.strip_routes import router as router_1
from cyan.assay_routes import router as router_2
from cyan.recipe_routes import router as router_3
from cyan.seed import seed
from cyan.assay_job import run as run_job

router = APIRouter(prefix="/api")
router.include_router(router_0)
router.include_router(router_1)
router.include_router(router_2)
router.include_router(router_3)

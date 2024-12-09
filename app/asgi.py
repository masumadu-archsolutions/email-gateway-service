import os

from app import constants, create_app

assert (
    os.getenv("APP_ENV") != constants.TESTING_ENVIRONMENT
), "set APP_ENV=development|uat|production"
app = create_app()

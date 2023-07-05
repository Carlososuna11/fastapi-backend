from pathlib import Path
from utils import (
    get_env,
    bool_from_str
)

DEBUG = get_env('DEBUG', default=False)

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Project information
PROJECT_NAME = get_env('PROJECT_NAME', 'FastAPI Project')
PROJECT_DESCRIPTION = get_env('PROJECT_DESCRIPTION', 'FastAPI Project')
PROJECT_VERSION = get_env('PROJECT_VERSION', '1.0.0')

# Token Authorization
TOKEN_AUTHORIZATION = get_env(
    'TOKEN_AUTHORIZATION',
    'secret'
)

# CORS Settings
CORS_SETTINGS = {
    'allow_origins': list(
        filter(
            None,
            get_env(
                'CORS_ALLOW_ORIGINS',
                '*'
            ).split(',')
        )
    ),
    'allow_credentials': bool_from_str(
        get_env(
            'CORS_ALLOW_CREDENTIALS',
            'true'
        )
    ),
    'allow_methods': list(
        filter(
            None,
            get_env(
                'CORS_ALLOW_METHODS',
                '*'
            ).split(',')
        )
    ),
    'allow_headers': list(
        filter(
            None,
            get_env(
                'CORS_ALLOW_HEADERS',
                '*'
            ).split(',')
        )
    ),
}

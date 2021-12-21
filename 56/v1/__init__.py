from fastapi.templating import Jinja2Templates
from config import BASE_DIR

templates = Jinja2Templates(directory=BASE_DIR.as_posix() + '/v1/templates')

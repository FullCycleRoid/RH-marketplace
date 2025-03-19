import logging
import sys

logger = logging.getLogger("uvicorn.error")
FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
stdout_handler = logging.StreamHandler(stream=sys.stdout)
HANDLERS = [stdout_handler]
logging.basicConfig(format=FORMAT, level=logging.DEBUG, handlers=HANDLERS)

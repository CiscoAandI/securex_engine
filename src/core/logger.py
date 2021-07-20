import logging
import sys

logging.Formatter("%(asctime)s [%(levelname)-5.5s]  %(message)s")
logger = logging.getLogger('sxo_engine')

logger.addHandler(logging.StreamHandler(sys.stdout))
logging.basicConfig(filename='sxo.log', encoding='utf-8', level=logging.DEBUG)
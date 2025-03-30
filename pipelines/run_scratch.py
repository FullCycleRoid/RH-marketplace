from pprint import pprint
from time import time

from pipelines.connector import MarketplaceDBSession
from pipelines.utils import get_company_by_inn



with MarketplaceDBSession() as sess:
    start = time()
    company = get_company_by_inn(sess, '7804576823')
    pprint(company)
    print(time() - start)
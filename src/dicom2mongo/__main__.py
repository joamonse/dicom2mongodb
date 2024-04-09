import logging
import argparse

from functools import partial 

from dicom2mongo.database import Database
from dicom2mongo.dicom_extractor import DicomExtractor
from dicom2mongo.dicom_receptor import start_dicom_server

def on_c_store_event(event, db, upload_data_collection, dicom_extractor):
    logger.info('Recieved new dicom')
    
    ds = event.dataset
    ds.file_meta = event.file_meta

    data = dicom_extractor.extract_tags(ds)
    db.insert(data, upload_data_collection)

    return 0x0000


logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', level=logging.INFO)
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Run a dicom node that upload recied dicom\'s tags to a mongo database',prog='dicom2mongo')
parser.add_argument('dbname', help='Database name')
parser.add_argument('--searched_tags_collection', help='Table name containing the list of tags to be searched', default='tags')
parser.add_argument('--db_url', help='url of the database', default='localhost')
parser.add_argument('--db_port', help='port of the database', default=27017, type=int)
parser.add_argument('--upload_data_collection', help='Table name where the tags will be uploaded', default='data')
parser.add_argument('--host', help='Url hwere the program will listen. Set to 0.0.0.0 for online access', default='localhost')
parser.add_argument('--port', help='Port number of the program', type=int, default=11112)

args = parser.parse_args()

db = Database(args.db_url, args.db_port, args.dbname)

dicom_extractor = DicomExtractor(db.get_tags_list(args.searched_tags_collection))

filled_on_c_store = partial(on_c_store_event, 
                            db=db,
                            upload_data_collection=args.upload_data_collection, 
                            dicom_extractor=dicom_extractor)
logger.info(f'Started server. Listening on {args.host}:{args.port}. Database on {args.db_url}:{args.db_port} ')
start_dicom_server(filled_on_c_store, host=args.host, port=args.port)
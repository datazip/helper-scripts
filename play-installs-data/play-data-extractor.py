from google.cloud import storage
import os, os.path
from datetime import datetime, timedelta
import glob
import pandas as pd
import sys, getopt

def correctSubtitleEncoding(filename, newFilename, encoding_from='UTF-16LE', encoding_to='UTF-8'):
    with open(filename, 'r', encoding=encoding_from) as fr:
        with open(newFilename, 'w', encoding=encoding_to) as fw:
            for line in fr:
                fw.write(line[:-1]+'\r\n')


def main(argv):

    bucket_name = ''
    path = 'stats/installs/'
    target_bucket_name = ''

    try:
        opts, args = getopt.getopt(argv,"b:t:g:",["bucket_name=","target_bucket_name=", "gc_service_json_path="])
    except getopt.GetoptError:
        print ('play-data-extractor.py -b <google_play_bucket> -t <gcs_target_bucket> -g <gc_service_json_path> ')
        sys.exit(2)

    if len(opts) != 3:
        print ('play-data-extractor.py -b <google_play_bucket> -t <gcs_target_bucket> -g <gc_service_json_path> ')
        sys.exit()
    for opt, arg in opts:
        if opt not in ("-b", "-t", "-g", "--bucket_name", "--target_bucket_name", "--gc_service_json_path"):
            print ('play-data-extractor.py -b <google_play_bucket> -t <gcs_target_bucket> -g <gc_service_json_path> ')
            sys.exit()
        elif opt in ("-b", "--bucket_name"):
            bucket_name = arg
        elif opt in ("-t", "--target_bucket_name"):
            target_bucket_name = arg
        elif opt in ("-g", "--gc_service_json_path"):
            os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = arg
    print ('bucket_name "', bucket_name)
    print ('target_bucket_name "', target_bucket_name)
    print ('gc_service_json_path "', target_bucket_name)


    # Instantiates a client
    storage_client = storage.Client()

    target_bucket = storage_client.get_bucket(target_bucket_name)


    # path joining version for other paths
    DIR = './data_files'
    CONVERTED_DIR = './data_files_converted'
    FINAL_DIR = './final'
    if not os.path.exists(DIR):
        os.makedirs(f'{DIR}/{path}')
    if not os.path.exists(CONVERTED_DIR):
        os.makedirs(f'{CONVERTED_DIR}/{path}')
    if not os.path.exists(FINAL_DIR):
        os.makedirs(FINAL_DIR)

    installs_file_extension = ["country.csv","overview.csv","app_version.csv","os_version.csv","device.csv","carrier.csv","language.csv"]


    yesterday = datetime.now() - timedelta(1)

    yesterdayYearMonth = f'{yesterday.year}{yesterday.strftime("%m")}'
    todayYearMonth = f'{datetime.now().year}{datetime.now().strftime("%m")}'

    blobs = storage_client.list_blobs(bucket_name, prefix = path)
    for blob in blobs:
        if yesterdayYearMonth in  blob.name or todayYearMonth in blob.name : 
            if os.path.exists(f'{DIR}/{blob.name}'):
                os.remove(f'{DIR}/{blob.name}')
        if not os.path.exists(f'{DIR}/{blob.name}'):
            blob.download_to_filename(f"{DIR}/{blob.name}")
            correctSubtitleEncoding(f'{DIR}/{blob.name}', f'{CONVERTED_DIR}/{blob.name}')
                

    for file_extension in installs_file_extension :
        all_filenames = [i for i in glob.glob(f'{CONVERTED_DIR}/{path}/installs_*_{file_extension}')]
        combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
        combined_csv.to_csv( f'{FINAL_DIR}/{file_extension}', index=False, encoding='utf-8')
        blob = target_bucket.blob(f'{path}{file_extension}')
        blob.upload_from_filename(f'{FINAL_DIR}/{file_extension}')

if __name__ == "__main__":
   main(sys.argv[1:])
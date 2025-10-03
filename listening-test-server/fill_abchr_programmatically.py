from mongodbconnection import MongoDBConnection
import argparse
import csv
import uuid


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, required=True, help="Name of the ABCHR test. It should be already created on the platform")
    parser.add_argument("--audio_file_dir", type=str, required=True, help="Directory where audio files are stored")
    parser.add_argument("--input", type=str, required=True, help="Path to the input file containing ABCHR files with following format: <ref_audio_file>,<compressed_audio_file>")

    args = parser.parse_args()
    name = args.name
    audio_file_dir = args.audio_file_dir
    input_file = args.input

    connection = MongoDBConnection()
    db = connection.db
    collection = db['abchrTests']
    for doc in collection.find({'name': name}):
        print(f"Filling ABCHR test '{name}' with programmatically generated data...")
        if 'trials' in doc:
            print(f"Test '{name}' already has trials, aborting...")
            exit(1)
        nb_rows = 0
        with open(input_file, 'r') as f:
            reader = csv.reader(f)
            trials = []
            for row in reader:
                if len(row) != 2:
                    print(f"Invalid row format: {row}, skipping...")
                    continue
                ref_audio, compressed_audio = row
                current_id = uuid.uuid4().hex
                collection.update_one(
                    {'_id': doc['_id']},
                    {'$push': {'items': {
                        'id': current_id,
                        'type': 2,
                        'title': f'Trial {current_id}',
                        'example': {
                            'medias': [
                                {'src': f'{audio_file_dir}/{ref_audio}', 'filename': ref_audio},
                                {'src': f'{audio_file_dir}/{compressed_audio}', 'filename': compressed_audio}
                            ],
                            'fields': [
                                {
                                    'type': 'abchr',
                                    'title': 'Please rate the two proposed audio files compared to the reference audio',
                                    'value': None
                                }
                            ],
                            'mediaRef': {
                                'src': f'{audio_file_dir}/{ref_audio}',
                                'filename': ref_audio
                            },
                            'settings': {
                                'loopTimes': 0,
                                'requireClipEnded': False,
                                'sectionLooping': False,
                                'disablePlayerSlider': False,
                                'randomMedia': True,
                                'fixLastInternalQuestion': False,
                            }
                        }
                    }}}
                )
                nb_rows += 1
        print(f"Test '{name}' has been filled with {nb_rows} trials.")

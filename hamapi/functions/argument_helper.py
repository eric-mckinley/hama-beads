from argparse import ArgumentParser


def get_program_arguments():
    parser = ArgumentParser()
    parser.add_argument("-i", "--image",
                        required=True,
                        dest="image_path",
                        help="Path to image")
    parser.add_argument("-t", "--type",
                        default='remote',
                        dest="image_type",
                        help="Specify remote or local image type ")
    return parser.parse_args()

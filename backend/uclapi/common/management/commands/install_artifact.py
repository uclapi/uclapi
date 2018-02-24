from django.core.management.base import BaseCommand

import os
import tarfile

from io import BytesIO

import requests


class Command(BaseCommand):
    help = 'Installs frontend artifact files and updates statics'

    def add_arguments(self, parser):
        parser.add_argument('artifact_id', nargs=1)

    def extract_file(self, tar, file_obj, base_dir):
        split_path = file_obj.name.split('/')
        # Process frontend artifacts
        if (split_path[0] == "."):
            split_path = split_path[1:]
        if (split_path[0] == "frontend"):
            new_path = os.path.join(
                base_dir,
                "backend",
                "uclapi",
                split_path[1],
                "static",
                *split_path[2:]
            )
            print("Extracting {} to {}".format(file_obj.name, new_path))
            handle = tar.extractfile(file_obj.name)
            with open(new_path, mode='wb') as f:
                f.write(handle.read())

    def handle(self, *args, **options):
        artifact_id = options['artifact_id'][0]

        base_directory = os.path.abspath(os.getcwd())
        found = False
        while not found:
            dirs = os.listdir(base_directory)
            if "backend" in dirs and "frontend" in dirs:
                found = True
            else:
                base_directory = os.path.dirname(base_directory)

        print("Base UCL API Directory: " + base_directory)

        url = "{}/{}.tar.gz".format(
            os.environ["ARTIFACT_BASE_URL"],
            str(artifact_id)
        )
        print("Getting artifact from " + url)

        response = requests.get(url, stream=True)

        tmpfile = BytesIO()
        tmpfile.write(response.raw.read())
        tmpfile.seek(0)

        tar = tarfile.open(mode='r|gz', fileobj=tmpfile)
        members = tar.getmembers()
        tmpfile.seek(0)
        for m in members:
            if m.isfile():
                self.extract_file(tar, m, base_directory)


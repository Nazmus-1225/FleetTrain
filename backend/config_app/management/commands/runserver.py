from django.core.management.commands.runserver import Command as RunserverCommand
import os
from decouple import config
class Command(RunserverCommand):
    def run(self, *args, **options):
        directory=config('DIRECTORY')
        if not os.path.exists(directory):
            os.makedirs(directory)
        print(f"Central directory initialized at: {directory}")
        # Your custom startup code here
        super().run(*args, **options)

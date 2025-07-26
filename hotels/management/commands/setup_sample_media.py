import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Setup sample media files for the hotel booking system'

    def handle(self, *args, **options):
        # Create media directories if they don't exist
        media_root = settings.MEDIA_ROOT
        hotel_images_dir = os.path.join(media_root, 'hotel_images')
        room_images_dir = os.path.join(media_root, 'room_images')
        
        os.makedirs(hotel_images_dir, exist_ok=True)
        os.makedirs(room_images_dir, exist_ok=True)

        # Copy sample images from static to media
        static_samples = os.path.join(settings.STATIC_ROOT, 'img', 'sample')
        
        # Sample hotel images
        hotel_samples = {
            'sunrise_grand.jpg': 'hotel1.jpg',
            'oceanview.jpg': 'hotel2.jpg',
            'mountain_lodge.jpg': 'hotel3.jpg',
        }
        
        # Sample room images
        room_samples = {
            'deluxe1.jpg': 'room1.jpg',
            'suite1.jpg': 'room2.jpg',
            'double1.jpg': 'room3.jpg',
            'suite2.jpg': 'room4.jpg',
            'single1.jpg': 'room5.jpg',
        }

        # Copy hotel images
        for dest, src in hotel_samples.items():
            src_path = os.path.join(static_samples, src)
            dest_path = os.path.join(hotel_images_dir, dest)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                self.stdout.write(f'Copied {src} to {dest}')

        # Copy room images
        for dest, src in room_samples.items():
            src_path = os.path.join(static_samples, src)
            dest_path = os.path.join(room_images_dir, dest)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                self.stdout.write(f'Copied {src} to {dest}')

        self.stdout.write(self.style.SUCCESS('Successfully set up media files'))

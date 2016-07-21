from django.test import TestCase

from apps.tie_guard_radio.utils.metadata import fetch_song_data


class TieGuardRadioTestCase(TestCase):
    """
    Test the Tie Guard Radio application.
    """
    SONGS = (
        ('L\'Arc-en-Ciel', 'Driver\'s High'),
        ('Stromae', 'Alors on Danse'),
        ('Twenty One Pilots', 'Stressed'),
        ('Katy Perry', 'Firework'),
        ('Pharrell', 'Happy')
    )

    def setUp(self):
        pass

    def test_fetch_song_data(self):
        """
        Tests fetching various (artist, song) metadata.
        """
        for (artist, song_name) in self.SONGS:
            data = fetch_song_data(song_name, artist)
            self.assertTrue(data is not None)

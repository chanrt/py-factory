from random import shuffle
from os import path
import pygame as pg

from constants import consts as c


durations = {
    "epic_emotional_cinematic_trailer.mp3": 130,
    "impulse.mp3": 252,
    "quantum_sparks.mp3": 132,
    "time_travel.mp3": 195
}


class MusicPlayer:
    def __init__(self):
        self.file_location = "music"
        self.file_names = [
            "epic_emotional_cinematic_trailer.mp3",
            "impulse.mp3",
            "quantum_sparks.mp3",
            "time_travel.mp3"
        ]
        shuffle(self.file_names)

        pg.init()
        self.current_song = -1
        self.next_song_time = 0
        self.time = -c.music_padding

    def start_next_music(self):
        self.current_song = (self.current_song + 1) % len(self.file_names)
        song_name = self.file_names[self.current_song]
        self.next_song_time += durations[song_name] + c.music_padding

        pg.mixer.music.load(path.join(self.file_location, song_name))
        pg.mixer.music.play()

    def check_next_music(self):
        self.time += c.dt
        if self.time >= self.next_song_time:
            self.start_next_music()


music_player = MusicPlayer()
import pygame
import os

class MusicPlayer:
    def __init__(self, music_folder):
        pygame.mixer.init()
        self.playlist = []
        for file in os.listdir(music_folder):
            if file.endswith(".mp3") or file.endswith(".wav"):
                self.playlist.append(os.path.join(music_folder, file))
        self.current = 0
        self.is_playing = False
        self.start_time = 0

    def play(self):
        if len(self.playlist) == 0:
            return
        pygame.mixer.music.load(self.playlist[self.current])
        pygame.mixer.music.play()
        self.start_time = pygame.time.get_ticks()
        self.is_playing = True

    def stop(self):
        pygame.mixer.music.stop()
        self.is_playing = False

    def next(self):
        if len(self.playlist) == 0:
            return
        self.current += 1
        if self.current >= len(self.playlist):
            self.current = 0
        self.play()

    def back(self):
        if len(self.playlist) == 0:
            return
        self.current -= 1
        if self.current < 0:
            self.current = len(self.playlist) - 1
        self.play()

    def get_track_name(self):
        if len(self.playlist) == 0:
            return "No track"
        return os.path.basename(self.playlist[self.current])

    def get_position(self):
        if not self.is_playing:
            return 0
        return (pygame.time.get_ticks() - self.start_time) // 1000
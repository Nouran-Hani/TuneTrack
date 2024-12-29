import os

import imagehash

from audio_processing import Processing


class similarity_check:
    def __init__(self, directory_path):
        """
        Initialize the song database by loading all HDF5 files in the directory.
        :param directory_path: Path to the directory containing HDF5 files.
        """
        self.songs = []
        self.directory_path = directory_path
        self.load_songs()

    def load_songs(self, h5py=None):
        """
        Load all songs in the directory and their perceptual hashes.
        """
        for file_name in os.listdir(self.directory_path):
            if file_name.endswith('.h5'):
                song_path = os.path.join(self.directory_path, file_name)

                # Load the data from the HDF5 file
                with h5py.File(song_path, 'r') as hf:
                    # Load the spectrogram
                    spectrogram = hf['spectrogram'][:]

                    # Load the features
                    features = hf['features'][:]

                    # Load the perceptual hash
                    feature_hash = hf['feature_hash'][()].decode('utf-8')

                # Append the loaded data into the song list
                self.songs.append({
                    'title': file_name,  # Use file name as title
                    'feature_hash': feature_hash,
                    'features': features,
                    'spectrogram': spectrogram,
                    'file_path': song_path
                })

    def compare_with_query(self, query_file):
        """
        Compare a specific query song with all songs in the database and return a sorted list of similarities.

        :param query_file: Path to the query audio file.
        :return: List of tuples containing (song_title, similarity_index)
        """
        # Load query song features and perceptual hash
        query_song = Processing(query_file, "query_song")  # Create Processing instance for the query song
        query_feature_vector = query_song.compute_feature_vector()
        query_hash = query_song.compute_perceptual_hash()

        similarities = []

        for song in self.songs:
            # Compare feature hash similarity
            hash_similarity = self.compare_hashes(query_hash, song['feature_hash'])
            similarities.append((song['title'], hash_similarity))

        # Sort songs by similarity
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities

    def compare_hashes(self, query_hash, song_hash):
        """
        Compare perceptual hashes using Hamming distance.

        :param query_hash: Hash of the query song.
        :param song_hash: Hash of the song from the database.
        :return: Similarity index (lower distance means more similarity)
        """
        # Compute Hamming distance between the perceptual hashes
        query_hash_obj = imagehash.hex_to_hash(query_hash)
        song_hash_obj = imagehash.hex_to_hash(song_hash)
        return query_hash_obj - song_hash_obj  # Hamming distance is the measure

# Example Usage:

# Step 1: Save songs data to HDF5
processing_instance = Processing(audio_path='Music/Group1_Save-your-tears(instruments).wav', title="Instruments")
processing_instance.save_to_hdf5('songs/song1_data.h5')

# Step 2: Create the SongDatabase class with all songs stored in the directory
song_db = similarity_check(directory_path='songs')

# Step 3: Compare a target song's perceptual hash with all songs in the database
target_song = Processing(audio_path='Music/AnotherSong.wav', title="Another Song")
target_song_hash = target_song.compute_perceptual_hash()

# Compare and get similarity sorted list
sorted_songs = song_db.compare_song(target_song_hash)

# Step 4: Output the sorted songs and their similarity
for song in sorted_songs:
    print(f"Song: {song['title']}, Similarity Index: {song['similarity']:.4f}, File Path: {song['file_path']}")
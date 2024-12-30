# import json
# import imagehash
# import librosa
#
# from audio_processing import Processing
# import os
#
#
# class SimilarityCheck:
#     def __init__(self, json_file_path):
#         """
#         Initialize the song database by loading data from a JSON file.
#         :param json_file_path: Path to the JSON file containing song data.
#         """
#         self.json_file_path = os.path.join(os.path.dirname(__file__), '..', json_file_path)
#         self.songs = []
#         self.load_songs()
#
#     def load_songs(self):
#         """
#         Load songs from the JSON file into the class's song list.
#         """
#         if not os.path.exists(self.json_file_path):
#             raise FileNotFoundError(f"JSON file not found: {self.json_file_path}")
#
#         with open(self.json_file_path, 'r') as file:
#             data = json.load(file)
#             for entry in data:
#                 try:
#                     # Handle potential key typos dynamically
#                     self.songs.append({
#                         'title': entry['title'],
#                         'feature_hash': entry['features'],
#                         'spectrogram': entry.get('spectrogram') or entry.get('specrogram'),
#                         'other_features': {
#                             'zero crossing': entry['zero crossing'],
#                             'spectral bandwidth': entry.get('spectral bandwidth') or entry.get('spectral banwidth'),
#                             'spectral centroid': entry['spectral centroid'],
#                             'spectral contrast': entry['spectral contrast'],
#                             'spectral flatness': entry['spectral flatness'],
#                             'mfccs': entry['mfccs']
#                         }
#                     })
#                 except KeyError as e:
#                     print(f"Skipping entry due to missing key: {e}")
#
#         if not self.songs:
#             raise ValueError("No valid songs found in the JSON file.")
#
#     def compare_with_query(self, query_file):
#         """
#         Compare a specific query song with all songs in the database and return a sorted list of similarities.
#
#         :param query_file: Path to the query audio file.
#         :return: List of tuples containing (song_title, similarity_index)
#         """
#         # Load query song's audio and determine its sampling rate
#         audio, sr = librosa.load(query_file, sr=None)  # Load the query audio file with its original sampling rate
#
#         # Create a Processing instance for the query song
#         query_song = Processing(audio=audio, title="query_song", sr=sr)
#
#         # Extract query song's feature vector and hash
#         query_feature_vector = query_song.feature_vector
#         query_hash = query_song.get_hashed_features()
#
#         similarities = []
#
#         for song in self.songs:
#             # Compare feature hash similarity
#             print(f"Song hash:{query_hash}, hash of songs {song['feature_hash']}")
#             hash_similarity = self.compare_hashes(query_hash, song['feature_hash'])
#             similarities.append((song['title'], hash_similarity))
#
#         # Sort songs by similarity
#         similarities.sort(key=lambda x: x[1], reverse=False)
#         return similarities
#
#     def compare_hashes(self, query_hash, song_hash):
#         """
#         Compare perceptual hashes using Hamming distance.
#
#         :param query_hash: Hash of the query song.
#         :param song_hash: Hash of the song from the database.
#         :return: Similarity index (lower distance means more similarity)
#         """
#         # query_hash_obj = imagehash.hex_to_hash(query_hash)
#         # song_hash_obj = imagehash.hex_to_hash(song_hash)
#         # Convert the hex hash to a binary string
#         query_hash = bin(int(query_hash, 16))[2:].zfill(len(query_hash) * 4)  # Hex to binary (zero-padded)
#         song_hash = bin(int(song_hash, 16))[2:].zfill(len(song_hash) * 4)  # Hex to binary (zero-padded)
#
#         # Calculate Hamming distance by comparing corresponding bits
#         return sum(c1 != c2 for c1, c2 in zip(query_hash, song_hash))
#         # return query_hash_obj - song_hash_obj  # Hamming distance
#
# # Example Usage:
#
# # Step 1: Create the SimilarityCheck class with the JSON file
# song_db = SimilarityCheck(json_file_path='hashed_data.json')
#
# # Step 2: Compare a target song with the songs in the JSON database
# query_song_path = "../Music/Group8_AThousandYears(original).wav"
# sorted_songs = song_db.compare_with_query(query_song_path)
#
# # Step 3: Output the sorted songs and their similarity
# print("Similarity Results:")
# for song_title, similarity in sorted_songs:
#     print(f"Song: {song_title}, Similarity Index: {similarity}")

import json
import imagehash
import librosa
import os

class SimilarityCheck:
    def __init__(self):
        """
        Initialize the song database by loading data from a JSON file.
        :param json_file_path: Path to the JSON file containing song data.
        """
        self.json_file_path = 'TuneTrack/core/final_hashed_data.json'
        self.hashed = None
        self.songs = []
        self.similarities = []
        self.load_songs()

    def load_songs(self):
        if not os.path.exists(self.json_file_path):
            raise FileNotFoundError(f"JSON file not found: {self.json_file_path}")

        with open(self.json_file_path, 'r') as file:
            data = json.load(file)
            for entry in data:
                try:
                    # Handle missing keys and load relevant fields
                    self.songs.append({
                        'title': entry['title'],
                        'features': entry['features']

                    })
                except KeyError as e:
                    print(f"Skipping entry due to missing key: {e}")

        if not self.songs:
            raise ValueError("No valid songs found in the JSON file.")

    def compare_with_query(self):
        query_spectrogram_hash = self.hashed

        for song in self.songs:
            hash_similarity = self.compare_perceptual_hashes(query_spectrogram_hash, song['features'])
            self.similarities.append((song['title'], 100-hash_similarity))

        # Sort songs by similarity (lower is more similar)
        self.similarities.sort(key=lambda x: x[1], reverse=True)

    def compare_hashes(self, query_hash, song_hash):
        """
        Compare perceptual hashes using Hamming distance.

        :param query_hash: Hash of the query song's spectrogram.
        :param song_hash: Hash of the spectrogram of the song from the database.
        :return: Similarity index (lower distance means more similarity)
        """
        # Convert the hex hashes to binary strings
        query_hash_bin = bin(int(query_hash, 16))[2:].zfill(len(query_hash) * 4)  # Hex to binary (zero-padded)
        song_hash_bin = bin(int(song_hash, 16))[2:].zfill(len(song_hash) * 4)  # Hex to binary (zero-padded)

        # Calculate Hamming distance by comparing corresponding bits
        return sum(c1 != c2 for c1, c2 in zip(query_hash_bin, song_hash_bin))


    def compare_perceptual_hashes(self,hash1, hash2):
        """
        Compare two perceptual hashes using Hamming distance.

        :param hash1: First perceptual hash (in hex).
        :param hash2: Second perceptual hash (in hex).
        :return: Similarity score (lower distance means more similarity).
        """
        # Convert hex hash to imagehash object
        hash1_obj = imagehash.hex_to_hash(hash1)
        hash2_obj = imagehash.hex_to_hash(hash2)

        # Compute the Hamming distance between the two hashes
        hamming_distance = hash1_obj - hash2_obj

        # Return the Hamming distance (lower distance means more similarity)
        return hamming_distance

    def set_hashed_song(self, hashed):
        self.hashed = hashed
        self.compare_with_query()

    def get_similarities(self):
        return self.similarities  # Return the top 5 most similar songs


# Example Usage:
song_db = SimilarityCheck()

query_song_path = "9649a1563bcd13cb"
sorted_songs = song_db.set_hashed_song(query_song_path)
sort = song_db.get_similarities()

# Step 3: Output the sorted songs and their similarity
print("Similarity Results:")
for song_title, similarity in sort:
    print(f"Song: {song_title}, Similarity Index: {similarity}")

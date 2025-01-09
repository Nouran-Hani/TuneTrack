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
        self.json_file_path = 'TuneTrack/core/spectrohash.json'
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
        return self.similarities[:5] # Return the top 5 most similar songs


# Example Usage:
song_db = SimilarityCheck()

query_song_path = "d5d5cfcdc1c9c180"
sorted_songs = song_db.set_hashed_song(query_song_path)
sort = song_db.get_similarities()

# Step 3: Output the sorted songs and their similarity
print("Similarity Results:")
for song_title, similarity in sort:
    print(f"Song: {song_title}, Similarity Index: {similarity}")

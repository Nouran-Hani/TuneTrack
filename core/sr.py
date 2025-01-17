import os
import pprint
from load import Load
audio_folder = "TuneTrack/Music"

srdict = {}
for filename in os.listdir(audio_folder):
    file_path = os.path.join(audio_folder, filename)
    title = os.path.splitext(filename)[0]
    try:
        audio, sr = Load(file_path).get_audio_data()
        srdict[title] = sr
    except Exception as e:
        print(f"Failed to process {title}: {e}")

pprint.pprint(srdict)

{
 'Group19_ShadowOfMine_Full': 22050,
 'FE!N': 22050,
 'FE!N (Instruments)': 22050,
 'FE!N (Vocals)': 22050,
 'Group13_Let_Her_Go_Music': 22050,
 'Group13_Let_Her_Go_Original': 22050,
 'Group13_Let_Her_Go_Vocals': 22050,
 'Group20_HitTheRoadJack_Full': 22050,
 'Group20_HitTheRoadJack_Music': 22050,
 'Group20_HitTheRoadJack_Vocals': 22050,
 'Group7_SweetDreams_Full': 22050,
 'Group7_SweetDreams_Music': 22050,
 'Group7_SweetDreams_Vocals': 22050,
 'Group9_PleasePleasePlease_Full': 22050,
 'Group9_PleasePleasePlease_Music': 22050,
 'Group9_PleasePleasePlease_Vocals': 22050,
 'Something Just Like That(Instruments)': 22050,
 'Something Just Like That(Lyrics)': 22050,
 'Somthing Just Like That(Original)': 22050,
 'Ya Lala(instruments)': 22050,
 'Ya Lala(lyrics)': 22050,
 'Ya Lala(original)': 22050,
 'Group14_a sky full of stars_Full': 44100,
 'Group14_a sky full of stars_Music': 44100,
 'Group14_a sky full of stars_Vocals': 44100,
 'Group18_RollingInTheDeep_Music': 44100,
 'Group18_RollingInTheDeep_Original': 44100,
 'Group18_RollingInTheDeep_Vocals': 44100,
 'A Thousand Years(instruments)': 44100,
 'A Thousand Years(lyrics)': 44100,
 'Group19_ShadowOfMine_Music': 44100,
 'Group19_ShadowOfMine_Vocals': 44100,
 'Group5_NinaCriedPower_Full': 44100,
 'Group5_NinaCriedPower_Music': 44100,
 'Group5_NinaCriedPower_Vocals': 44100,
 'Group6_Alkanas_Full': 44100,
 'Group6_Alkanas_Music': 44100,
 'Group6_Alkanas_Vocals': 44100,
 'Save-your-tears(instruments)': 44100,
 'Save-your-tears(lyrcis)': 44100,
 'Shake It Out (instruments) (2)': 44100,
 'Shake It Out (lyrics) (2)': 44100,
 'Shake It Out (original) (2)': 44100,
 'wen_elkhael [music]': 44100,
 'wen_elkhael [vocals]': 44100,
 'A Thousand Years(original)': 48000,
 'Group3_SomeLikeYou_Full': 48000,
 'Group3_SomeLikeYou_Music': 48000,
 'Group3_SomeLikeYou_Vocal': 48000,
 'save-your-tears(original)': 48000,
 'wen_elkhael[music+vocals]': 48000}
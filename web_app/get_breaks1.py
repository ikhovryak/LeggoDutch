#required libraries
import math
import urllib.request
import scipy.io.wavfile
import matplotlib.pyplot as plt
import numpy as np

class SoundComparison:

    def __init__(self):
        self.input_sound_start_snip = 0
        self.result = {"too_little_breaks": False, "too_many_breaks": False,
                       "short_breaks": [], "long_breaks": [],
                       "short_pronunciation": [], "long_pronunciation": []}

    def compare_waves(self, speaker_sound, correct_sound, location):
        speaker_rate, pre_speaker_data = scipy.io.wavfile.read(speaker_sound)
        correct_rate, correct_data = scipy.io.wavfile.read(correct_sound)
        speaker_data = self.stereo_to_mono(pre_speaker_data)
        speaker_data, speaker_rate = self.convert_audio_data_to_chunk_audio_data(speaker_data, speaker_rate)
        correct_data, correct_rate = self.convert_audio_data_to_chunk_audio_data(correct_data, correct_rate)
        speaker_data = self.normalize_audio_data_wave(speaker_data)
        correct_data = self.normalize_audio_data_wave(correct_data)
        speaker_data_silence = self.calculate_silent_amplitude(speaker_data, speaker_rate)
        correct_data_silence = self.calculate_silent_amplitude(correct_data, correct_rate, 0)
        #speaker_sound must be snipped of silence after correct sound file
        correct_data = self.remove_audio_wave_silence(correct_data, correct_rate, 0)
        speaker_data = self.remove_audio_wave_silence(speaker_data, speaker_rate)
        speaker_silence = self.find_audio_chunk_breaks(speaker_data, speaker_rate, speaker_data_silence)
        correct_silence = self.find_audio_chunk_breaks(correct_data, correct_rate, correct_data_silence)


        # plot amplitude (or loudness) over time
        speaker_time = np.arange(0, len(speaker_data), 1) / speaker_rate
        correct_time = np.arange(0, len(correct_data), 1) / correct_rate
        self.check_sensibility_of_breaks(speaker_silence, correct_silence)

        long_breaks = self.result["long_breaks"]
        if(len(long_breaks)==0):
            self.plot_graphs(correct_time, correct_data, speaker_time, speaker_data, "#5cb85c", location)
        else:
            self.plot_graphs(correct_time, correct_data, speaker_time, speaker_data, "#f0ad4e", location)
        # print(long_breaks)

        return long_breaks

    def plot_graphs(self, correct_time, correct_data, speaker_time, speaker_data, color, location):
         # plot amplitude (or loudness) over time

        plt.subplot(211)
        plt.plot(correct_time, correct_data, linewidth=0.1, alpha=1, color=color)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Correct sound amplitude')

        plt.figure(1)

        plt.subplot(212)
        plt.plot(speaker_time, speaker_data, linewidth=0.1, alpha=1, color=color)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title("Your recording's amplitude")

        plt.subplots_adjust(hspace=0.7)
        plt.savefig(location)
        plt.clf()

    def stereo_to_mono(self, audio_data):
        audio_data = audio_data.astype(float)
        return audio_data.sum(axis=1) if not isinstance(audio_data[0], np.float64) else audio_data

    def normalize_audio_data_wave(self, original_audio_data):
        new_data = [abs(x) for x in original_audio_data]
        max_amplitude = max(new_data)
        final_audio_data = [abs(x / max_amplitude) for x in original_audio_data]
        return final_audio_data

    def find_audio_chunk_breaks(self, audio_data, rate, silence_amplitude):
        min_break_count = rate / 5
        counter = 0
        break_tuples = []
        start_break = 0
        while counter < len(audio_data):
            if audio_data[counter] <= silence_amplitude:
                if start_break == 0:
                    start_break = counter
            else:
                if start_break > 0:
                    if (counter - start_break) >= min_break_count:
                        break_tuples.append((start_break / rate, counter / rate))
                    start_break = 0
            counter += 1
        return break_tuples

    def check_sensibility_of_breaks(self, speaker_breaks, correct_breaks):
        #last_time_difference is used to track the interval between gaps so that past differences would not stack up
        last_time_difference = 0
        if len(speaker_breaks) > len(correct_breaks):
            self.result["too_many_breaks"] = True
        elif len(speaker_breaks) < len(correct_breaks):
            self.result["too_little_breaks"] = False
        else:
            for i in range(len(speaker_breaks)):
                speaker_start = speaker_breaks[i][0]
                speaker_end = speaker_breaks[i][1]
                speaker_break_time = speaker_end - speaker_start
                correct_start = correct_breaks[i][0]
                correct_end = correct_breaks[i][1]
                correct_break_time = correct_end - correct_start
                if (speaker_end - speaker_start) > 1.5:
                    self.result["long_breaks"].append(speaker_breaks[i])
                elif (speaker_break_time - correct_break_time) > 0.30:
                    self.result["long_breaks"].append((speaker_start + self.input_sound_start_snip, speaker_end + self.input_sound_start_snip))
                elif (correct_break_time - speaker_break_time) > 0.30:
                    self.result["short_breaks"].append((speaker_start + self.input_sound_start_snip, speaker_end + self.input_sound_start_snip))
                if (speaker_start - correct_start) > (last_time_difference + 0.5) and i > 0:
                    self.result["long_pronunciation"].append((speaker_breaks[i-1][1] + self.input_sound_start_snip, speaker_start + self.input_sound_start_snip))
                elif (correct_start - speaker_start) > (last_time_difference + 0.5) and i > 0:
                    self.result["short_pronunciation"].append((speaker_breaks[i-1][1] + self.input_sound_start_snip, speaker_start + self.input_sound_start_snip))
                last_time_difference = abs(correct_end - speaker_end)

    def remove_audio_wave_silence(self, audio_data, rate, min=None):
        start_counter = 0
        end_counter = 0
        reversed_audio_data = audio_data[::-1]
        while audio_data[start_counter] <= self.calculate_silent_amplitude(audio_data, rate, min):
            start_counter += 1
        while reversed_audio_data[end_counter] <= self.calculate_silent_amplitude(reversed_audio_data, rate, min):
            end_counter += 1
        self.input_sound_start_snip = start_counter / rate
        return audio_data[start_counter: (len(audio_data) - end_counter)]

    def calculate_silent_amplitude(self, audio_data, rate, min=None):
        end = int(rate/3)
        return max(max(audio_data[-end:]), 0.15) if min is None else 0.1

    # def check_for_long_breaks(self, audio_data, rate):
    #     counter = 0
    #     duration = 0
    #     while counter < len(audio_data):
    #         if audio_data[counter] < self.calculate_silent_amplitude(audio_data, rate):
    #             duration += 1
    #             if duration > (2.2 * rate):
    #                 return counter / rate
    #         else:
    #             duration = 0
    #         counter += 1
    #     return None

    # def check_for_amplitude_inconsistencies(self, audio_data1, rate1, audio_data2, rate2):
    #     chunk_audio1 = self.convert_audio_data_to_chunk_audio_data(audio_data1, rate1)
    #     chunk_audio2 = self.convert_audio_data_to_chunk_audio_data(audio_data2, rate2)
    #     for i in range(len(chunk_audio1)):
    #         if abs(chunk_audio1[i] - chunk_audio2[i]) > 0.2:
    #             return i
    #     return None

    def convert_audio_data_to_chunk_audio_data(self, audio_data, rate):
        data = audio_data[:]
        chunk_audio_data = [0] * ((len(data) // 10) + 1)
        for i in range(len(data)):
            index = int(i // 10)
            chunk_audio_data[index] = chunk_audio_data[index] + abs(data[i])
        for i in range(len(chunk_audio_data)):
            chunk_audio_data[i] = chunk_audio_data[i] / (int(rate) / 10)
        return chunk_audio_data, int(rate/10)

if __name__ == "__main__":
    # web_file="C:\Users\Samuel\PycharmProjects\speech_analysis\wave_comparison"
    #
    # #download file
    # input_sound, headers = urllib.request.urlretrieve("C:/Users/Samuel/PycharmProjects/speech_analysis/wave_comparison", "input_sound")
    # correct_sound, headers = urllib.request.urlretrieve("C:/Users/Samuel/PycharmProjects/speech_analysis/wave_comparison", "correct_sound")
    # wav_filename, headers = urllib.request.urlretrieve(web_file)
    # rate,audData=scipy.io.wavfile.read("C:\Users\Samuel\PycharmProjects\speech_analysis\wave_comparison")
    # time = np.arange(0, float(16000), 1) / rate
    # workable_data = []
    # string = ""
    # for data in audData[:16000]:
    #     workable_data.append(int(data))
    #     # string += str(data)
    #     # string += "."
    # # print(string)
    #
    # max = max(workable_data)
    #
    # happy = workable_data[:]
    # for i in range(len(happy)):
    #     happy[i] = abs(happy[i] / max)
    #     string += str(abs(happy[i] / max))
    #     string += "|"
    # print(happy[10400:15000])
    print(SoundComparison().compare_waves("C:/Users/Samuel/PycharmProjects/speech_analysis/wave_comparison/trial.wav", "C:/Users/Samuel/PycharmProjects/speech_analysis/wave_comparison/correct1.wav"))

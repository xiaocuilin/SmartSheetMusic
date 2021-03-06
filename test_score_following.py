import matplotlib.pyplot as plt
import score_following
# import ScoreClass
import corrupt_midi
import pretty_midi
import librosa as lb
import numpy as np
import utils_audio_transcript as utils
import pickle
import librosa.util
import importlib
import score_following_batch_evaluation
import pandas as pd 
import config
import music_detection
import librosa.display
import datetime
from scipy.signal import argrelmin
# from dtw_fast import dtw_fast
from scipy.spatial.distance import cdist
from pickle import load
from start_score_following import MatcherManager
import score_following 


# C = np.reshape(np.arange(1, 101), (20, 5)).astype(np.float) 
# dtw_fast(C, np.array([1.0, 1.0, 1.0]), 1, 1)
# 
# features1 = np.array([[1,2,3,4,5]]).T
# features2 = np.array([[1,1,2,2,2,3,4,5]]).T
# 
# C = cdist(features1, features2)
# 
# dtw_fast(C, np.array([1.0, 1.0, 1.0]), 1, 1)
# 
# a=1


# wd = utils.WD + '\Samples\TestScoreFollowing//'
wd = utils.WD + '\Samples\IMSLP//'

pkl_file = open(utils.WD + 'ScoreFollowingLogs\matcher.pkl', 'rb')
matcher_manager = load(pkl_file) #Only run in debug mode (i.e. Ctrl + Enter)
idxs_all = np.arange(0, matcher_manager.matcher.dtw.cum_distance.shape[1])
last_valid = idxs_all[np.all(np.isnan(matcher_manager.matcher.dtw.cum_distance), 0)][0]-1

#  idx_start = 800
#  idx_end = 1270
idx_start = 0
idx_end = last_valid

plt.figure()
# utils.plot_dtw_distance(matcher_manager.matcher.dtw.cum_distance[:, idx_start:idx_end])
plt.plot(range(0,idx_end-idx_start), matcher_manager.matcher.filter.positions_filtered[idx_start:idx_end])
plt.plot(range(0,idx_end-idx_start), matcher_manager.matcher.filter.positions_base[idx_start:idx_end])
plt.xlabel('Position in live')
plt.ylabel('Position in music sheet')

# wd = r"C:\Users\Alexis\Source\seescore\xml samples//"
# # filename_mid = r"35882-Fur_Elise_by_Ludwig_Van_Beethoven.mid"
# filename_mid = r"Waltz_in_A_MinorChopin.mid"
# matcher_new = score_following.Matcher(wd, filename_mid, utils.SR, utils.HOP_LENGTH)
# matcher_new.match_batch_online(matcher_manager.matcher.audio_data_all.astype('float32'))

matcher_manager.music_detecter.predictions 

# utils.write_wav(wd+r"Waltz_in_A_MinorChopin_recorded.wav", matcher_manager.matcher.audio_data_all.astype('float32'), rate = 11025)

plt.figure()
# plt.plot(matcher_new.positions_sec)
plt.plot(matcher_new.filter.positions_filtered)
plt.plot(matcher_new.filter.positions_base)
plt.xlabel('Position in live')
plt.ylabel('Position in music sheet')

a=1
# plt.figure()
# plt.plot(matcher_manager.matcher.dtw.cum_distance[:, 1140])

# filename_mid = "Chopin_Op028-01_003_20100611-SMD.mid"
filename_mid = 'Chopin-_Prelude_no._7_in_A_major.mid'
# filename_mid = "Beethoven_Moonlight_Sonata_Op._27_No._2_Mvt._2.mid"

# utils.convert_audio_file(wd+filename+'.mp3', wd+filename+'.wav', utils.SR)

# midi_obj = pretty_midi.PrettyMIDI(wd+filename_mid)
    
# length_sec = midi_obj._PrettyMIDI__tick_to_time[-1]
# times_ori_act = np.linspace(0.0, length_sec, int(length_sec/0.01))
# times_ori_act = [note.end for note in midi_obj.instruments[0].notes]

# filename_wav_corrupted ="Chopin_Op028-01_003_20100611-SMD_silence.wav"
# corrupt_midi.add_silence(midi_obj, start_silence=15.0, silence_length=3.0)
# times_cor_act = [note.end for note in midi_obj.instruments[0].notes]
# filename_wav_corrupted ="Chopin_Op028-01_003_20100611-SMD_cut.wav"
# filename_wav_corrupted ="Chopin_Op028-01_003_20100611-SMD_real.wav"
# filename_wav_corrupted = "Beethoven_Moonlight_Sonata_Op._27_No._2_Mvt._2_real.wav"
filename_wav_corrupted ="Chopin-_Prelude_no._7_in_A_major_real.wav"

# times_cor_act = corrupt_midi.remove_segment(midi_obj, times_ori_act, start_segment=5.0, remove_length=3.0)
      
# audio_data_cor = midi_obj.fluidsynth(utils.SR)
# utils.write_wav(wd+filename_wav_corrupted, audio_data_cor, rate=utils.SR)
audio_data_cor = lb.load(wd+filename_wav_corrupted, utils.SR)[0]

# audio_data_cor = audio_data_cor[5*1024:-1]

# matcher = score_following.Matcher(wd, filename_mid, utils.SR, utils.HOP_LENGTH,                                   
#                                   dtw_kwargs= {'alpha':0.97, 'diag_cost':1.0, 'light_run':False, 'positions_type':'adj_min'},
#                                   compute_chromagram_fcn_kwargs={'n_fft':utils.N_FFT, 'n_chroma':12},
#                                   )
matcher = score_following.Matcher(wd, filename_mid, utils.SR, utils.HOP_LENGTH,                                                                                                       
                                  compute_chromagram_fcn_kwargs={'n_fft':utils.N_FFT, 'n_chroma':12},
                                  )

t1 = datetime.datetime.now()
[times_cor_est, times_ori_est] = matcher.match_batch_online(audio_data_cor)
t2 = datetime.datetime.now()
print((t2-t1).total_seconds())
[times_cor_est_dtw, times_ori_est_dtw, res] = matcher.match_batch_offline(audio_data_cor)
utils.plot_alignment([(times_cor_est, times_ori_est)], times_cor_est_dtw, times_ori_est_dtw)#, matcher.positions_sec_filtered

plt.figure(); plt.plot(idxs.T[:,0])
plt.figure(); plt.plot(values.T)

plt.figure()
plt.plot(cum_distance_local)
plt.plot(argmins, cum_distance_local[argmins])


a=1
# plt.figure() 
# plt.plot(matcher.best_distance)
# 
# 
# times_cor_est = np.arange(chromagram_est.shape[0]) * matcher.hop_length_act / float(matcher.sr_act) 
# times_ori_est = np.array(matcher.position_sec)
# utils.plot_alignment(times_cor_est, times_ori_est, times_cor_act, times_ori_act)    
# 
# 
# plt.plot(matcher.best_paths_distance[-1])
# a=1
# 
# wd = utils.WD + '\Samples\TestScoreFollowing//'
# filename_mid = "Beethoven_Fur_Elise.mid"
# filename_wav = utils.change_file_format(filename_mid, 'mid', 'wav')
# filename_wav_corrupted = utils.change_file_format(filename_mid, '.mid', '.wav', append='_recorded')
# midi_obj = pretty_midi.PrettyMIDI(wd+filename_mid)
# audio_data = midi_obj.fluidsynth(utils.SR)
# utils.write_wav(wd+filename_wav, audio_data, rate=utils.SR)
# utils.start_and_record(wd + filename_wav,wd + filename_wav_corrupted, sr=utils.SR)
# 
# reload(score_following)
# matcher = score_following.Matcher(wd, filename_mid, utils.SR, utils.HOP_LENGTH, 
#                                   compute_chromagram_fcn_kwargs={'n_fft':utils.N_FFT, 'n_chroma':84},
#                                   use_low_memory=False)
# 
# audio_data_cor = lb.load(wd+filename_wav_corrupted, utils.SR)[0]
# [times_cor_est, times_ori_est] = matcher.match_batch(audio_data_cor)
# 
# length_sec = utils.get_length_wav(wd+filename_wav)
# times_ori_act = np.linspace(0.0, length_sec, int(length_sec/0.01))
# utils.plot_alignment(times_cor_est, times_ori_est, times_ori_act, times_ori_act)
# 
# [cum_distance, best_path] = matcher.match_offline(np.concatenate((audio_data_cor, audio_data_cor)))
# [times_cor_est_dtw, times_ori_est_dtw, res] = matcher.match_offline(audio_data_cor)
# 
# matcher.best_paths
# matcher.best_paths_distance[-1]
# 
# 
#                        
# a=1        
# midi_object = pretty_midi.PrettyMIDI(wd + filename1)
# matcher = MatcherMidi(wd, filename1, filename2)
# matcher.main_matcher()
# plt.plot(matcher.path[0], matcher.path[1])
# fig = plt.figure()
# fig.add_subplot(2,1,1)
# plt.imshow(midiread(wd + filename1, r=(0, 127)).piano_roll.T, origin='lower', aspect='auto', interpolation='nearest', cmap=plt.cm.gray_r)
# fig.add_subplot(2,1,2)
# plt.imshow(midiread(wd + filename2, r=(0, 127)).piano_roll.T, origin='lower', aspect='auto', interpolation='nearest', cmap=plt.cm.gray_r)
# utils.synthetise(wd + filename_midi1, wd + filename_wav1)


# wd = "C:\Users\Alexis\Business\SmartSheetMusic\Samples\Chopin_op28_3/"
#  
# filename_midi1 = "Chopin_Op028-01_003_20100611-SMD.mid"
# filename_midi2 = "Chopin_Op028-01_003_20100611-SMD_corrupt.mid"
# filename_wav1 = "Chopin_Op028-01_003_20100611-SMD.wav"
# filename_wav2 = "Chopin_Op028-01_003_20100611-SMD_corrupt.wav"

# midi_object = pretty_midi.PrettyMIDI(wd + filename_midi1)
# original_times = np.linspace(0.0, midi_object._PrettyMIDI__tick_to_time[-1], int(midi_object._PrettyMIDI__tick_to_time[-1]/0.05))
# adjusted_times,  diagnostics = corrupt_midi.corrupt_midi(midi_object, original_times)        
# midi_object.write(wd + filename_midi2)

# utils.write_wav(wd + filename_wav1, pretty_midi.PrettyMIDI(wd + filename_midi1).fluidsynth(44100), rate = 44100)
# utils.write_wav(wd + filename_wav2, pretty_midi.PrettyMIDI(wd + filename_midi2).fluidsynth(44100), rate = 44100)

# SR = 11025
# N_FFT = 2048
# HOP_LENGTH = 1024
# 
# win_len_smooth = 1
# tuning = 0.0
# chromagram_act = lb.feature.chroma_cens(y=audio_data_act, win_len_smooth=win_len_smooth, sr=SR, hop_length=HOP_LENGTH, chroma_mode='stft', n_fft=N_FFT, tuning=tuning).T
# audio_data_est = lb.core.load(wd + filename_wav2, sr = SR, offset=0.0, duration=None)[0]
# chromagram_est = lb.feature.chroma_cens(y=audio_data_est, win_len_smooth=win_len_smooth, sr=SR, hop_length=HOP_LENGTH, chroma_mode='stft', n_fft=N_FFT, tuning=tuning).T
# np.save( wd + 'chromagram_act.npy', chromagram_act)
# np.save( wd + 'chromagram_est.npy', chromagram_est)
# chromagram_act = np.load( wd + 'chromagram_act.npy')
# chromagram_est = np.load( wd + 'chromagram_est.npy')

# nb_frames_est = chromagram_est.shape[0]
# 
# matcher = score_following.Matcher(wd, filename_wav1, SR, N_FFT, HOP_LENGTH)
# 
# for n in range(nb_frames_est):
#     matcher.main_matcher(chromagram_est[n,:])
#     print n, matcher.position_sec 
# 
# plt.plot(matcher.best_paths[-1].rows, matcher.best_paths[-1].cols)

# filenames_mid = [ 
# "Bach_BWV871-02_002_20090916-SMD.mid",
# "Bach_BWV888-02_008_20110315-SMD.mid",
# # "Bartok_SZ080-02_002_20110315-SMD.mid",
# "Beethoven_Op027No1-02_003_20090916-SMD.mid",
# "Chopin_Op028-01_003_20100611-SMD.mid",
# ]
# wd = "C:\Users\Alexis\Business\SmartSheetMusic\Samples\TestScoreFollowing/" 
# 
# for filename_mid in filenames_mid:
#     filename_pkl = utils.change_file_format(filename_mid, '.mid', '.pkl', append = '_matcher_evaluator')
#     pkl_file = open(wd+filename_pkl, 'rb')
#     matcher_evaluator = pickle.load(pkl_file)
#     matcher_evaluator.plot_alignment_error()
    


# wd = "C:\Users\Alexis\Business\SmartSheetMusic\Samples\Chopin_op28_3/"
# pkl_file = open('C:\Users\Alexis\Business\SmartSheetMusic\Samples\TestScoreFollowing/alignments_stats.pkl', 'rb')
# alignment_stats = pickle.load(pkl_file)

# sr = 11025
# audio_data_est = lb.core.load("C:\Users\Alexis\Business\SmartSheetMusic\Samples\TestScoreFollowing/Chopin_Op028-01_003_20100611-SMD.wav", sr)[0]
# chroma_cqt = lb.feature.chroma_cqt(audio_data_est, sr=sr)
# chroma_stft = lb.feature.chroma_stft(audio_data_est, sr=sr, n_fft=4096)

# rests = utils.find_start_end_rests(audio_data_est, sr)


# wd = utils.WD + '\Samples\TestScoreFollowing//'
# # df_stats = score_following_batch_evaluation.format_alignment_stats(wd, 'alignments_stats.pkl')
# filename_mid = "Chopin_Op028-01_003_20100611-SMD.mid"
# midi_obj = pretty_midi.PrettyMIDI(wd+filename_mid)
# midi_obj.instruments[0].notes
# start_silence = 10.0
# silence_length = 10.0
# 
# corrupt_midi.add_silence(midi_obj, start_silence=start_silence, silence_length=silence_length)      
# audio_data = midi_obj.fluidsynth(utils.SR)
# utils.write_wav(wd+"Chopin_Op028-01_003_20100611-SMD_silence.wav", audio_data, rate=utils.SR)
# 
# filename_wav = "Chopin_Op028-01_003_20100611-SMD.wav"
# 
# audio_data_est = lb.core.load(wd + filename_wav, sr = utils.SR, offset=0.0, duration=None)[0]
#                                         
# chromagram = lb.feature.chroma_cqt(np.array(audio_data_est)[0:1023], sr=utils.SR, hop_length=utils.HOP_LENGTH)
#     
# with open(utils.WD_AUDIOSET + "all_data.pkl", 'rb') as handle:
#     all_data = pickle.load(handle)
#     
# music_detecter = music_detection.MusicDetecter(utils.WD_AUDIOSET, utils.SR, utils.HOP_LENGTH, 84, 4.0)    
# 
# music_detecter.detect(all_data["audio_data"][0])
# audio_data = utils.record(4.0, sr=utils.SR, save=True, filename_wav_out= wd + "file.wav")
# 
# utils.plot_chromagram(music_detection.chroma_cqt(all_data["audio_data"][0], utils.SR, utils.HOP_LENGTH, 84).T, sr=utils.SR, hop_length=utils.HOP_LENGTH)
# 
# 
# wd = "C:\Users\Alexis\Business\SmartSheetMusic\Samples/"
# 
# 
# S = np.abs(lb.spectrum.stft(audio_data_est, n_fft=utils.N_FFT, hop_length=utils.HOP_LENGTH))**2 
#         
# librosa.display.specshow(S, sr=utils.SR, hop_length=utils.HOP_LENGTH)
# librosa.onset.onset_strength
# 
# audio_data_mic = lb.core.load(wd + "file.wav", sr = utils.SR, offset=0.0, duration=None)[0]
# librosa.display.specshow(lb.amplitude_to_db(lb.stft(audio_data_est, n_fft=utils.N_FFT, hop_length=utils.HOP_LENGTH), ref=np.max), sr=utils.SR, hop_length=utils.HOP_LENGTH, y_axis='log')
# 
# audio_data_yt = lb.core.load(wd + "sample_0.wav", sr = utils.SR, offset=0.0, duration=4.0)[0]
# librosa.display.specshow(lb.amplitude_to_db(lb.stft(audio_data_yt, n_fft=utils.N_FFT, hop_length=utils.HOP_LENGTH), ref=np.max), sr=utils.SR, hop_length=utils.HOP_LENGTH, y_axis='log')
# 
# plt.colorbar(format='%+2.0f dB')

# midi_object = pretty_midi.PrettyMIDI(wd + filename_mid)
# run_matcher_evaluation(wd, filename_mid, {}, 0, [1], 0)

# filename_pkl = "Bach_BWV871-02_002_20090916-SMD_matcher_evaluator.pkl"
# pkl_file = open(wd+filename_pkl, 'rb')
# matcher_evaluator = pickle.load(pkl_file)

# config_matcher = config.configs_matcher[0]
# config_matcher = {'compute_chromagram_fcn': lb.feature.chroma_cqt, 
#                   'compute_chromagram_fcn_kwargs':{'bins_per_octave':24},
#                   'chromagram_mode':2}
# configs_corrupt = [config.configs_corrupt[0]]
# matcher_evaluator = score_following.MatcherEvaluator(wd, filenamce_mid, config_matcher=config_matcher, configs_corrupt=configs_corrupt)
# matcher_evaluator.filenames_wav_corrupt = ['Chopin_Op028-01_003_20100611-SMD.wav']
# matcher_evaluator.times_cor_act_all = [matcher_evaluator.times_ori_act] 
# matcher_evaluator.align()
# matcher_evaluator.evaluate()

# matcher_evaluator.main_evaluation()


# matcher_evaluator.plot_alignment_error()
# plt.plot(matcher_evaluator.alignement_stats[-1])
# utils.plot_chromagram(matcher_evaluator.matchers[0].chromagram_est[0:matcher_evaluator.matchers[0].idx_est,:])
# plt.plot(matcher_evaluator.times_est_all[0][:,0], matcher_evaluator.times_est_all[0][:,1])
# plt.plot(matcher_evaluator.times_cor_act_all[0], matcher_evaluator.times_ori_act)
# utils.to_clipboard(matcher_evaluator.matchers[3].cum_distance[0:1268, 0:1268])
# matcher_evaluator.matchers[6].plot_chromagrams()
# matcher_evaluator.matchers[0].plot_dtw_distance([455])
# plt.figure()




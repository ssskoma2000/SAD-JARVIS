using NAudio.Wave;
using System.IO;

namespace JarvisDesktop;

public class AudioService
{
    private WaveInEvent _waveIn;
    private MemoryStream _audioStream;
    private WaveFileWriter _waveWriter;

    public async Task StartRecordingAsync()
    {
        _audioStream = new MemoryStream();
        _waveIn = new WaveInEvent();

        // Configure audio recording
        _waveIn.WaveFormat = new WaveFormat(16000, 1); // 16kHz, mono
        _waveIn.DataAvailable += OnDataAvailable;
        _waveIn.RecordingStopped += OnRecordingStopped;

        _waveWriter = new WaveFileWriter(_audioStream, _waveIn.WaveFormat);

        _waveIn.StartRecording();
    }

    public async Task<byte[]> StopRecordingAsync()
    {
        if (_waveIn != null)
        {
            _waveIn.StopRecording();
            _waveIn.Dispose();
            _waveIn = null;
        }

        if (_waveWriter != null)
        {
            await _waveWriter.FlushAsync();
            _waveWriter.Dispose();
            _waveWriter = null;
        }

        if (_audioStream != null)
        {
            var audioData = _audioStream.ToArray();
            _audioStream.Dispose();
            _audioStream = null;
            return audioData;
        }

        return Array.Empty<byte>();
    }

    public async Task PlayAudioAsync(byte[] audioData)
    {
        using var stream = new MemoryStream(audioData);
        using var reader = new WaveFileReader(stream);
        using var outputDevice = new WaveOutEvent();

        outputDevice.Init(reader);
        outputDevice.Play();

        // Wait for playback to complete
        await Task.Run(() =>
        {
            while (outputDevice.PlaybackState == PlaybackState.Playing)
            {
                Thread.Sleep(100);
            }
        });
    }

    private void OnDataAvailable(object sender, WaveInEventArgs e)
    {
        if (_waveWriter != null)
        {
            _waveWriter.Write(e.Buffer, 0, e.BytesRecorded);
        }
    }

    private void OnRecordingStopped(object sender, StoppedEventArgs e)
    {
        // Cleanup will be handled in StopRecordingAsync
    }
}

using System.ComponentModel;
using System.Runtime.CompilerServices;

namespace JarvisDesktop;

public class JarvisViewModel : INotifyPropertyChanged
{
    private string _status;
    private bool _isRecording;
    private string _currentCommand;

    public string Status
    {
        get => _status;
        set
        {
            if (_status != value)
            {
                _status = value;
                OnPropertyChanged();
            }
        }
    }

    public bool IsRecording
    {
        get => _isRecording;
        set
        {
            if (_isRecording != value)
            {
                _isRecording = value;
                OnPropertyChanged();
            }
        }
    }

    public string CurrentCommand
    {
        get => _currentCommand;
        set
        {
            if (_currentCommand != value)
            {
                _currentCommand = value;
                OnPropertyChanged();
            }
        }
    }

    public event PropertyChangedEventHandler PropertyChanged;

    protected virtual void OnPropertyChanged([CallerMemberName] string propertyName = null)
    {
        PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(propertyName));
    }
}

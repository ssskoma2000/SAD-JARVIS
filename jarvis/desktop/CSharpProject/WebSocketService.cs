using System.Net.WebSockets;
using System.Text;
using System.Text.Json;

namespace JarvisDesktop;

public class WebSocketService
{
    private ClientWebSocket _webSocket;
    private CancellationTokenSource _cancellationTokenSource;
    private bool _isConnected;

    public event EventHandler<string> MessageReceived;
    public event EventHandler Connected;
    public event EventHandler Disconnected;

    public async Task ConnectAsync(string uri)
    {
        try
        {
            _webSocket = new ClientWebSocket();
            _cancellationTokenSource = new CancellationTokenSource();

            await _webSocket.ConnectAsync(new Uri(uri), _cancellationTokenSource.Token);
            _isConnected = true;

            Connected?.Invoke(this, EventArgs.Empty);

            // Start listening for messages
            _ = Task.Run(() => ReceiveMessagesAsync());
        }
        catch (Exception ex)
        {
            throw new Exception($"Failed to connect to WebSocket: {ex.Message}");
        }
    }

    public async Task DisconnectAsync()
    {
        if (_webSocket != null && _isConnected)
        {
            _cancellationTokenSource?.Cancel();
            await _webSocket.CloseAsync(WebSocketCloseStatus.NormalClosure, "Client disconnecting", CancellationToken.None);
            _isConnected = false;
            Disconnected?.Invoke(this, EventArgs.Empty);
        }
    }

    public async Task SendMessageAsync(string message)
    {
        if (!_isConnected || _webSocket.State != WebSocketState.Open)
        {
            throw new Exception("WebSocket is not connected");
        }

        var buffer = Encoding.UTF8.GetBytes(message);
        await _webSocket.SendAsync(new ArraySegment<byte>(buffer), WebSocketMessageType.Text, true, _cancellationTokenSource.Token);
    }

    private async Task ReceiveMessagesAsync()
    {
        var buffer = new byte[4096];

        try
        {
            while (_isConnected && !_cancellationTokenSource.Token.IsCancellationRequested)
            {
                var result = await _webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), _cancellationTokenSource.Token);

                if (result.MessageType == WebSocketMessageType.Close)
                {
                    await DisconnectAsync();
                    break;
                }
                else if (result.MessageType == WebSocketMessageType.Text)
                {
                    var message = Encoding.UTF8.GetString(buffer, 0, result.Count);
                    MessageReceived?.Invoke(this, message);
                }
            }
        }
        catch (Exception ex)
        {
            if (_isConnected)
            {
                _isConnected = false;
                Disconnected?.Invoke(this, EventArgs.Empty);
            }
        }
    }

    public bool IsConnected => _isConnected;
}

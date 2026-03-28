using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using Microsoft.Maui.Controls;
using Microsoft.Maui.Media;
using System.IO;
using NAudio.Wave;
using System.Diagnostics;

namespace JarvisDesktop;

public partial class MainPage : ContentPage
{
    private readonly WebSocketService _webSocketService;
    private readonly AudioService _audioService;
    private readonly JarvisViewModel _viewModel;
    private bool _isRecording = false;

    public MainPage(WebSocketService webSocketService, AudioService audioService, JarvisViewModel viewModel)
    {
        InitializeComponent();
        _webSocketService = webSocketService;
        _audioService = audioService;
        _viewModel = viewModel;

        // Setup WebSocket events
        _webSocketService.MessageReceived += OnWebSocketMessageReceived;
        _webSocketService.Connected += OnWebSocketConnected;
        _webSocketService.Disconnected += OnWebSocketDisconnected;

        // Connect to backend
        _ = _webSocketService.ConnectAsync("ws://localhost:8000/ws");

        // Setup Jarvis WebView
        SetupJarvisWebView();
    }

    private void SetupJarvisWebView()
    {
        // Load local HTML with 3D model
        var html = @"
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset='utf-8'>
            <script src='https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'></script>
            <script src='https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/loaders/GLTFLoader.js'></script>
            <style>
                body { margin: 0; background: transparent; overflow: hidden; }
                canvas { width: 100%; height: 100%; }
            </style>
        </head>
        <body>
            <script>
                // 3D Jarvis Model Setup
                const scene = new THREE.Scene();
                const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
                const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });

                renderer.setSize(window.innerWidth, window.innerHeight);
                renderer.setClearColor(0x000000, 0);
                document.body.appendChild(renderer.domElement);

                camera.position.z = 5;

                // Lighting
                const ambientLight = new THREE.AmbientLight(0x404040, 0.6);
                scene.add(ambientLight);

                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                directionalLight.position.set(1, 1, 1);
                scene.add(directionalLight);

                // Create Jarvis Model
                const jarvisGroup = new THREE.Group();

                // Head
                const headGeometry = new THREE.SphereGeometry(0.5, 32, 32);
                const headMaterial = new THREE.MeshPhongMaterial({
                    color: 0x4a90e2,
                    emissive: 0x001122,
                    shininess: 100
                });
                const head = new THREE.Mesh(headGeometry, headMaterial);
                jarvisGroup.add(head);

                // Eyes
                const eyeGeometry = new THREE.SphereGeometry(0.05, 16, 16);
                const eyeMaterial = new THREE.MeshBasicMaterial({ color: 0xffffff });

                const leftEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
                leftEye.position.set(-0.15, 0.1, 0.45);
                jarvisGroup.add(leftEye);

                const rightEye = new THREE.Mesh(eyeGeometry, eyeMaterial);
                rightEye.position.set(0.15, 0.1, 0.45);
                jarvisGroup.add(rightEye);

                // Mouth
                const mouthGeometry = new THREE.BoxGeometry(0.2, 0.05, 0.05);
                const mouthMaterial = new THREE.MeshBasicMaterial({ color: 0x333333 });
                const mouth = new THREE.Mesh(mouthGeometry, mouthMaterial);
                mouth.position.set(0, -0.15, 0.45);
                jarvisGroup.add(mouth);

                // Body
                const bodyGeometry = new THREE.CylinderGeometry(0.3, 0.4, 1, 32);
                const bodyMaterial = new THREE.MeshPhongMaterial({
                    color: 0x2c3e50,
                    emissive: 0x000011,
                    shininess: 50
                });
                const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
                body.position.y = -0.8;
                jarvisGroup.add(body);

                scene.add(jarvisGroup);

                // Animation variables
                let isSpeaking = false;
                let animationTriggers = {};

                // Animation loop
                function animate() {
                    requestAnimationFrame(animate);

                    if (isSpeaking) {
                        head.rotation.y += 0.01;
                        mouth.scale.y = 1 + Math.sin(Date.now() * 0.01) * 0.3;
                        jarvisGroup.rotation.y += 0.005;
                    } else {
                        head.rotation.y += 0.002;
                        mouth.scale.y = 1;
                        jarvisGroup.rotation.y += 0.001;
                    }

                    // Apply animation triggers
                    if (animationTriggers.nod_head) {
                        head.rotation.x = Math.sin(Date.now() * 0.005) * 0.2;
                    }
                    if (animationTriggers.mouth_open) {
                        mouth.scale.y = 1 + animationTriggers.mouth_open * 0.5;
                    }
                    if (animationTriggers.blink) {
                        leftEye.visible = rightEye.visible = Math.sin(Date.now() * 0.01) > -0.9;
                    }

                    renderer.render(scene, camera);
                }
                animate();

                // Handle window resize
                window.addEventListener('resize', () => {
                    camera.aspect = window.innerWidth / window.innerHeight;
                    camera.updateProjectionMatrix();
                    renderer.setSize(window.innerWidth, window.innerHeight);
                });

                // Expose functions for external control
                window.jarvis3D = {
                    setSpeaking: (speaking) => { isSpeaking = speaking; },
                    setAnimationTriggers: (triggers) => { animationTriggers = triggers; }
                };
            </script>
        </body>
        </html>";

        JarvisWebView.Source = new HtmlWebViewSource { Html = html };
    }

    private void OnVoiceButtonClicked(object sender, EventArgs e)
    {
        if (!_isRecording)
        {
            StartRecording();
        }
        else
        {
            StopRecording();
        }
    }

    private async void StartRecording()
    {
        _isRecording = true;
        VoiceButton.Text = "🔴 Recording...";
        StatusLabel.Text = "Listening...";
        StatusLabel.TextColor = Colors.Red;

        try
        {
            await _audioService.StartRecordingAsync();
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", $"Failed to start recording: {ex.Message}", "OK");
            StopRecording();
        }
    }

    private async void StopRecording()
    {
        _isRecording = false;
        VoiceButton.Text = "🎤 Speak to Jarvis";
        StatusLabel.Text = "Processing...";
        StatusLabel.TextColor = Colors.Yellow;

        try
        {
            var audioData = await _audioService.StopRecordingAsync();

            // Send audio to backend
            var message = new
            {
                type = "audio_command",
                audio_base64 = Convert.ToBase64String(audioData)
            };

            await _webSocketService.SendMessageAsync(JsonSerializer.Serialize(message));
        }
        catch (Exception ex)
        {
            await DisplayAlert("Error", $"Failed to process audio: {ex.Message}", "OK");
            StatusLabel.Text = "Ready";
            StatusLabel.TextColor = Colors.Green;
        }
    }

    private void OnAnimationClicked(object sender, EventArgs e)
    {
        if (sender is Button button && button.CommandParameter is string animationType)
        {
            var triggers = new Dictionary<string, object>();

            switch (animationType)
            {
                case "wave":
                    triggers["wave"] = true;
                    break;
                case "smile":
                    triggers["smile"] = true;
                    break;
                case "think":
                    triggers["think"] = true;
                    break;
            }

            // Send animation trigger to WebView
            JarvisWebView.EvaluateJavaScriptAsync($"window.jarvis3D?.setAnimationTriggers({JsonSerializer.Serialize(triggers)});");
        }
    }

    private void OnSettingsClicked(object sender, EventArgs e)
    {
        // Open settings page (to be implemented)
        DisplayAlert("Settings", "Settings panel coming soon!", "OK");
    }

    private void OnWebSocketMessageReceived(object sender, string message)
    {
        MainThread.BeginInvokeOnMainThread(async () =>
        {
            try
            {
                var response = JsonSerializer.Deserialize<JsonElement>(message);

                if (response.TryGetProperty("type", out var typeProperty))
                {
                    var type = typeProperty.GetString();

                    switch (type)
                    {
                        case "response":
                            var text = response.GetProperty("text").GetString();
                            var audioBase64 = response.GetProperty("audio_base64").GetString();
                            var animationTriggers = response.GetProperty("animation_triggers");

                            // Add to chat
                            AddMessageToChat("Jarvis", text, isUser: false);

                            // Play audio
                            if (!string.IsNullOrEmpty(audioBase64))
                            {
                                var audioData = Convert.FromBase64String(audioBase64);
                                await _audioService.PlayAudioAsync(audioData);
                            }

                            // Apply animations
                            JarvisWebView.EvaluateJavaScriptAsync($"window.jarvis3D?.setAnimationTriggers({animationTriggers});");
                            JarvisWebView.EvaluateJavaScriptAsync("window.jarvis3D?.setSpeaking(true);");

                            // Stop speaking after audio duration (approximate)
                            await Task.Delay(3000);
                            JarvisWebView.EvaluateJavaScriptAsync("window.jarvis3D?.setSpeaking(false);");

                            StatusLabel.Text = "Ready";
                            StatusLabel.TextColor = Colors.Green;
                            break;

                        case "stt_result":
                            var sttText = response.GetProperty("text").GetString();
                            AddMessageToChat("You", sttText, isUser: true);
                            break;
                    }
                }
            }
            catch (Exception ex)
            {
                await DisplayAlert("Error", $"Failed to process message: {ex.Message}", "OK");
            }
        });
    }

    private void OnWebSocketConnected(object sender, EventArgs e)
    {
        MainThread.BeginInvokeOnMainThread(() =>
        {
            StatusLabel.Text = "Connected";
            StatusLabel.TextColor = Colors.Green;
        });
    }

    private void OnWebSocketDisconnected(object sender, EventArgs e)
    {
        MainThread.BeginInvokeOnMainThread(() =>
        {
            StatusLabel.Text = "Disconnected";
            StatusLabel.TextColor = Colors.Red;
        });
    }

    private void AddMessageToChat(string sender, string message, bool isUser)
    {
        var messageFrame = new Frame
        {
            BackgroundColor = isUser ? Color.FromArgb("#4a90e2") : Color.FromArgb("#374151"),
            CornerRadius = 10,
            Padding = new Thickness(10),
            Margin = new Thickness(0, 5, 0, 0)
        };

        var messageLayout = new StackLayout { Spacing = 5 };

        var senderLabel = new Label
        {
            Text = sender,
            FontSize = 12,
            TextColor = Colors.LightGray,
            FontAttributes = FontAttributes.Bold
        };

        var messageLabel = new Label
        {
            Text = message,
            FontSize = 14,
            TextColor = Colors.White,
            LineBreakMode = LineBreakMode.WordWrap
        };

        messageLayout.Children.Add(senderLabel);
        messageLayout.Children.Add(messageLabel);
        messageFrame.Content = messageLayout;

        ChatStack.Children.Add(messageFrame);

        // Auto scroll to bottom
        var scrollView = ChatStack.Parent as ScrollView;
        scrollView?.ScrollToAsync(messageFrame, ScrollToPosition.End, true);
    }
}

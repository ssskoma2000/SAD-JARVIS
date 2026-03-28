using Microsoft.Extensions.DependencyInjection;
using Microsoft.Maui;
using Microsoft.Maui.Hosting;
using System;

namespace JarvisDesktop
{
    public static class MauiProgram
    {
        public static MauiApp CreateMauiApp()
        {
            var builder = MauiApp.CreateBuilder();
            builder
                .UseMauiApp<App>()
                .ConfigureFonts(fonts =>
                {
                    fonts.AddFont("OpenSans-Regular.ttf", "OpenSansRegular");
                    fonts.AddFont("OpenSans-Semibold.ttf", "OpenSansSemibold");
                });

            // Register services
            builder.Services.AddSingleton<WebSocketService>();
            builder.Services.AddSingleton<AudioService>();
            builder.Services.AddSingleton<JarvisViewModel>();

            return builder.Build();
        }
    }
}

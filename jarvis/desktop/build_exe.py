"""
🔨 BUILD SCRIPT - Convert Jarvis to Windows EXE
================================================
Uses PyInstaller to build standalone executable.

Usage:
    python build_exe.py
    
Output:
    dist/Jarvis.exe
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


class JarvisBuilder:
    """Build Jarvis executable."""
    
    def __init__(self):
        """Initialize builder."""
        self.script_dir = Path(__file__).parent
        self.backend_dir = self.script_dir.parent / "backend"
        self.dist_dir = self.script_dir / "dist"
        self.build_dir = self.script_dir / "build"
        self.main_script = self.script_dir / "jarvis_main.py"  # Asosiy kirish nuqtasi
        self.icon_path = self.script_dir / "jarvis.ico"
        
        print("🔨 Jarvis EXE Builder")
        print("=" * 60)
    
    def check_requirements(self) -> bool:
        """
        Check if all required tools are installed.
        
        Returns:
            True if all OK
        """
        
        print("\n📋 Checking requirements...")
        
        # Check Python version
        if sys.version_info < (3, 8):
            print("❌ Python 3.8+ required")
            return False
        
        print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor}")
        
        # Check PyInstaller
        try:
            import PyInstaller
            print("✅ PyInstaller installed")
        except ImportError:
            print("❌ PyInstaller not installed")
            print("\nInstall with: pip install PyInstaller")
            return False
        
        return True
    
    def create_icon(self) -> bool:
        """
        Create Jarvis icon if it doesn't exist.
        
        Returns:
            True if icon exists or created
        """
        
        if self.icon_path.exists():
            print(f"✅ Icon found: {self.icon_path}")
            return True
        
        print("\n🎨 Creating icon...")
        
        try:
            from PIL import Image, ImageDraw, ImageFont
            
            # Create 256x256 icon
            size = 256
            image = Image.new('RGB', (size, size), color=(73, 109, 137))
            draw = ImageDraw.Draw(image)
            
            # Draw "J" for Jarvis
            # Try to use a nice font
            try:
                font = ImageFont.truetype("arial.ttf", 180)
            except:
                font = ImageFont.load_default()
            
            draw.text((65, 40), "J", fill=(230, 126, 34), font=font)
            
            # Save as ICO
            image.save(self.icon_path, 'ICO')
            print(f"✅ Icon created: {self.icon_path}")
            return True
        
        except Exception as e:
            print(f"⚠️  Could not create icon: {e}")
            print("  Continuing without icon...")
            return False
    
    def clean_build(self):
        """Clean previous builds."""
        
        print("\n🧹 Cleaning previous builds...")
        
        for d in [self.build_dir, self.dist_dir]:
            if d.exists():
                shutil.rmtree(d)
                print(f"  Removed {d.name}")
    
    def build_exe(self) -> bool:
        """
        Build EXE using PyInstaller.
        
        Returns:
            True if build successful
        """
        
        print("\n🔨 Building EXE...")
        
        # PyInstaller command
        cmd = [
            sys.executable,
            "-m", "PyInstaller",
            "--onefile",  # Single executable
            "--windowed",  # No console window
            "--clean",  # Clean build
            "--name", "Jarvis",
            "--distpath", str(self.dist_dir),
            "--buildpath", str(self.build_dir),
        ]
        
        # Add icon if available
        if self.icon_path.exists():
            cmd.extend(["--icon", str(self.icon_path)])
        
        # Add hidden imports
        hidden_imports = [
            "pynput",
            "sounddevice",
            "soundfile",
            "numpy",
            "openai",
            "dotenv",
            "PyQt6",
            "PyQt6.QtCore",
            "OpenGL",
            "speech_recognition",
        ]
        
        for imp in hidden_imports:
            cmd.extend(["--hidden-import", imp])
        
        # Add main script
        cmd.append(str(self.main_script))
        
        print(f"\nRunning: {' '.join(cmd[:5])} ... (this may take 2-3 minutes)")
        
        try:
            result = subprocess.run(cmd, check=True, capture_output=False)
            
            if result.returncode == 0:
                print("\n✅ Build successful!")
                return True
            else:
                print("\n❌ Build failed!")
                return False
        
        except subprocess.CalledProcessError as e:
            print(f"\n❌ Build error: {e}")
            return False
    
    def copy_resources(self):
        """
        Copy resources to dist folder.
        """
        
        print("\n📦 Copying resources...")
        
        # Copy .env.example to dist
        env_example = self.backend_dir / ".env.example"
        env_dest = self.dist_dir / ".env.example"
        
        if env_example.exists():
            shutil.copy(env_example, env_dest)
            print(f"✅ Copied .env.example")
        
        # Copy config files
        commands_json = self.backend_dir / "commands.json"
        if commands_json.exists():
            shutil.copy(commands_json, self.dist_dir / "commands.json")
            print(f"✅ Copied commands.json")
    
    def create_installer_script(self):
        """
        Create NSIS installer script.
        """
        
        print("\n📝 Creating installer script...")
        
        nsis_script = """
; Jarvis Desktop Assistant Installer
; Auto-generated by build_exe.py

!include "MUI2.nsh"

Name "Jarvis Desktop Assistant"
OutFile "JarvisSetup.exe"
InstallDir "$PROGRAMFILES\\Jarvis"
RequestExecutionLevel admin

!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_LANGUAGE "English"

Section "Install"
  SetOutPath "$INSTDIR"
  
  ; Copy files
  File "Jarvis.exe"
  File ".env.example"
  File "commands.json"
  
  ; Create shortcuts
  CreateDirectory "$SMPROGRAMS\\Jarvis"
  CreateShortCut "$SMPROGRAMS\\Jarvis\\Jarvis.lnk" "$INSTDIR\\Jarvis.exe"
  CreateShortCut "$DESKTOP\\Jarvis.lnk" "$INSTDIR\\Jarvis.exe"
  
  ; Auto-start (optional)
  ; WriteRegStr HKCU "Software\\Microsoft\\Windows\\CurrentVersion\\Run" \\
  ;   "Jarvis" "$INSTDIR\\Jarvis.exe"
  
SectionEnd

Section "Uninstall"
  RMDir /r "$INSTDIR"
  Delete "$DESKTOP\\Jarvis.lnk"
  RMDir /r "$SMPROGRAMS\\Jarvis"
SectionEnd
"""
        
        nsis_path = self.dist_dir / "installer.nsi"
        with open(nsis_path, 'w') as f:
            f.write(nsis_script)
        
        print(f"✅ Created {nsis_path}")
    
    def build(self) -> bool:
        """
        Run full build process.
        
        Returns:
            True if successful
        """
        
        # Check requirements
        if not self.check_requirements():
            return False
        
        # Create icon
        self.create_icon()
        
        # Clean previous builds
        self.clean_build()
        
        # Build EXE
        if not self.build_exe():
            return False
        
        # Copy resources
        self.copy_resources()
        
        # Create installer script
        self.create_installer_script()
        
        # Print summary
        exe_path = self.dist_dir / "Jarvis.exe"
        
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            
            print("\n" + "=" * 60)
            print("✅ BUILD COMPLETE!")
            print("=" * 60)
            print(f"\n📁 Output: {exe_path}")
            print(f"📊 Size: {size_mb:.1f} MB")
            print("\n🚀 Next steps:")
            print(f"  1. Run: {exe_path}")
            print("  2. Set OPENAI_API_KEY in .env")
            print("  3. Test with: Ctrl+Space → speak command")
            print("\n💡 To create installer:")
            print("  1. Install NSIS: https://nsis.sourceforge.io")
            print(f"  2. Run: makensis {self.dist_dir / 'installer.nsi'}")
            print(f"  3. Output: {self.dist_dir / 'JarvisSetup.exe'}")
            print("\n" + "=" * 60)
            
            return True
        else:
            print("❌ EXE not found")
            return False


def main():
    """Main entry point."""
    
    builder = JarvisBuilder()
    
    if builder.build():
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

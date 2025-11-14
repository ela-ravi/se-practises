import streamlit as st
import subprocess
import os
import platform
from urllib.parse import urlparse
from pathlib import Path

# Initialize session state
if 'download_complete' not in st.session_state:
    st.session_state.download_complete = False
    st.session_state.downloaded_file = None
if 'download_dir' not in st.session_state:
    st.session_state.download_dir = ""

def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

def strip_wrappers(val: str) -> str:
    """Remove surrounding single or double quotes from a string, if present."""
    if val is None:
        return val
    s = val.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in ("'", '"'):
        return s[1:-1].strip()
    return s

def get_downloads_folder():
    """Get the Downloads folder path, fallback to current directory if not accessible"""
    try:
        home = str(Path.home())
        system = platform.system()
        
        if system == 'Windows':
            downloads_path = os.path.join(home, 'Downloads')
        elif system == 'Darwin':  # macOS
            downloads_path = os.path.join(home, 'Downloads')
        else:  # Linux and others
            downloads_path = os.path.join(home, 'Downloads')
        
        # Try to create the directory to check if it's writable
        os.makedirs(downloads_path, exist_ok=True)
        # Try to create a test file to verify write permissions
        test_file = os.path.join(downloads_path, '.write_test')
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return downloads_path
    except (OSError, PermissionError):
        # If any error occurs (folder doesn't exist, no permissions, etc.), use current directory
        return os.getcwd()

def download_video(video_url, output_name, download_dir: str = None):
    try:
        if not is_valid_url(video_url):
            return False, "Invalid URL format. Please enter a valid URL."
            
        if not output_name:
            return False, "Please enter an output filename."
            
        # Add .mp4 extension if not present
        if not output_name.lower().endswith(('.mp4', '.mkv', '.webm', '.mov')):
            output_name += '.mp4'
            
        # Decide target directory: user-provided or system Downloads
        if download_dir and download_dir.strip():
            target_dir = os.path.expanduser(download_dir.strip())
        else:
            target_dir = get_downloads_folder()

        # Ensure the directory exists
        os.makedirs(target_dir, exist_ok=True)

        output_path = os.path.join(target_dir, output_name)
        # Ensure no surrounding quotes remain on the final path
        output_path = strip_wrappers(output_path)
        
        # Check if file already exists
        if os.path.exists(output_path):
            return False, f"File '{output_path}' already exists. Please choose a different name."
        
        # Create a progress bar
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Run ffmpeg command
        command = [
            'ffmpeg',
            '-i', video_url,
            '-c', 'copy',
            output_path
        ]
        
        process = subprocess.Popen(
            command,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        # Monitor progress (this is a simplified version as ffmpeg progress is complex)
        while True:
            output = process.stderr.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                # Update progress based on time (simplified)
                if 'time=' in output:
                    progress_bar.progress(50)  # Just show some progress
                    status_text.text(f"Downloading... {output.strip()}")
        
        if process.returncode == 0:
            progress_bar.progress(100)
            status_text.text("Download completed successfully!")
            st.session_state.download_complete = True
            st.session_state.downloaded_file = output_path
            return True, f"Successfully downloaded as '{output_path}'"
        else:
            return False, "Error occurred during download. Please check the URL and try again."
            
    except Exception as e:
        return False, f"An error occurred: {str(e)}"

def main():
    st.set_page_config(
        page_title="Video Downloader",
        page_icon="🎬",
        layout="centered"
    )
    
    st.title("🎥 Video Downloader")
    st.markdown("Download videos from any URL using FFmpeg")
    
    # Inputs
    video_url = st.text_input("Enter Video URL:", placeholder="https://example.com/video.mp4")
    output_name = st.text_input("Output Filename (without extension):", placeholder="my_video")

    st.text_input(
        "Optional download folder",
        value=st.session_state.download_dir,
        placeholder="/path/to/folder (leave empty to use system Downloads)",
        key="download_dir",
        help="Provide an absolute path or use ~ for your home directory"
    )

    remove_wrap = st.checkbox("Remove wrappers", value=False, help="Strip surrounding 'single' or \"double\" quotes from URL and folder")
    
    # Download button
    if st.button("Download Video"):
        if not video_url or not output_name:
            st.warning("Please fill in all fields")
        else:
            # Optionally strip wrappers
            cleaned_url = strip_wrappers(video_url) if remove_wrap else video_url
            cleaned_dir = strip_wrappers(st.session_state.download_dir) if remove_wrap else st.session_state.download_dir
            cleaned_name = strip_wrappers(output_name) if remove_wrap else output_name
            with st.spinner("Downloading video..."):
                success, message = download_video(cleaned_url, cleaned_name, cleaned_dir)
                if success:
                    st.success(message)
                else:
                    st.error(message)
    
    # Show download button if file was downloaded successfully
    if st.session_state.download_complete and st.session_state.downloaded_file and os.path.exists(st.session_state.downloaded_file):
        file_name = os.path.basename(st.session_state.downloaded_file)
        with open(st.session_state.downloaded_file, 'rb') as f:
            st.download_button(
                label=f"Save Video to Downloads",
                data=f,
                file_name=file_name,
                mime="video/mp4",
                key="download_button"
            )
        st.info(f"Video saved to: {st.session_state.downloaded_file}")
    
    st.markdown("---")
    st.markdown("### Instructions:")
    st.markdown("""
    1. Enter the video URL in the input field
    2. Choose a name for the output file (without extension)
    3. Optionally type a download folder path; leave empty to use the system Downloads folder
    4. Click 'Download Video' to start the download
    5. Once downloaded, click the 'Save Video' button to save the file
    """)
    
    st.markdown("### Requirements:")
    st.code("pip install streamlit")
    st.markdown("Make sure FFmpeg is installed on your system.")

if __name__ == "__main__":
    main()
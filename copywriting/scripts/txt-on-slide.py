import os
import pysrt
from moviepy import (
    TextClip, 
    AudioFileClip, 
    CompositeVideoClip, 
    concatenate_videoclips
)

def create_text_slide(text, duration, width=1280, height=720, font_size=50, color='white', bg_color='black'):
    """
    Creates a MoviePy TextClip that centers the text in a solid background.
    """
    # Create the text clip using default system font
    text_clip = TextClip(
        text, 
        size=(width, height),
        method='caption',
        align='center',
        color=color,
        bg_color=bg_color,
        fontsize=font_size,
        font=None
    )
    
    # Set the duration for this slide
    text_clip = text_clip.with_duration(duration)
    
    return text_clip

def srt_time_to_seconds(srt_time):
    """
    Convert pysrt.SubRipTime to total seconds.
    """
    return srt_time.hours * 3600 + srt_time.minutes * 60 + srt_time.seconds + srt_time.milliseconds / 1000.0

def create_text_on_slide_video(srt_path, audio_path, output_path,
                               video_width=1280, video_height=720,
                               text_font_size=50, text_color='white',
                               background_color='black'):
    """
    Parse an SRT file, create text slides for each subtitle, 
    and combine them with an audio track into a final video.
    """
    # Check if files exist
    if not os.path.exists(srt_path):
        raise FileNotFoundError(f"SRT file not found: {srt_path}")
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Parse the SRT subtitles
    subs = pysrt.open(srt_path)
    
    if len(subs) == 0:
        raise ValueError("No subtitles found in the SRT file")
        
    print(f"Found {len(subs)} subtitles")
    
    # If you have a voiceover audio track, load it here
    voiceover = AudioFileClip(audio_path)
    
    # For each subtitle line, create a text clip that spans its duration
    clips = []
    for idx, sub in enumerate(subs):
        try:
            # Calculate start and end times (in seconds)
            start_seconds = srt_time_to_seconds(sub.start)
            end_seconds   = srt_time_to_seconds(sub.end)
            duration      = end_seconds - start_seconds
            
            print(f"Processing subtitle {idx+1}: Duration {duration:.2f}s")
            
            # Create a text slide for this subtitle line
            text_slide = create_text_slide(
                sub.text, 
                duration=duration,
                width=video_width,
                height=video_height,
                font_size=text_font_size,
                color=text_color,
                bg_color=background_color
            )
            
            clips.append(text_slide)
        except Exception as e:
            print(f"Error processing subtitle {idx+1}: {str(e)}")
    
    if not clips:
        raise ValueError("No valid clips were created from the subtitles")
        
    # Concatenate all text slides
    final_clip = concatenate_videoclips(clips, method='compose')
    
    # Get the audio duration
    audio_duration = voiceover.duration
    
    # Set the final clip duration to match the audio
    final_clip = final_clip.with_duration(audio_duration)
    
    # Set the audio
    final_clip = final_clip.set_audio(voiceover)
    
    # Export the final video
    final_clip.write_videofile(
        output_path,
        fps=24,
        codec='libx264',
        audio_codec='aac'
    )

if __name__ == '__main__':
    srt_file = "scripts/vo.srt"        # Path to your SRT file
    audio_file = "scripts/vo.mp3"      # Path to your voiceover audio file
    output_video = "output_slideshow.mp4"  # Final output file name
    
    try:
        create_text_on_slide_video(
            srt_path=srt_file,
            audio_path=audio_file,
            output_path=output_video
        )
    except Exception as e:
        print(f"Error creating video: {str(e)}")
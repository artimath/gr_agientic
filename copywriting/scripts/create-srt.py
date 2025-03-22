import pysrt

def create_sample_srt():
    subs = pysrt.SubRipFile()
    
    # Create some sample subtitles from the checkout page
    texts = [
        "Transform Your Ad Performance in Just 20 Minutes Per Day",
        "Special Launch Offer: $47 (Regular Price: $97)",
        "Here's Everything You're Getting Today:",
        "Core Program ($997 value)",
        "7 Daily Implementation Emails",
        "AI Pattern Multiplication Protocol™",
        "Complete Bonus Stack ($3,379 value)",
        "The \"All-Upside\" 365-Day Guarantee"
    ]
    
    # Add each subtitle with 3 seconds duration
    for i, text in enumerate(texts):
        start = pysrt.SubRipTime(seconds=i*3)
        end = pysrt.SubRipTime(seconds=(i+1)*3)
        sub = pysrt.SubRipItem(index=i+1, start=start, end=end, text=text)
        subs.append(sub)
    
    # Save the SRT file
    subs.save('scripts/vo.srt', encoding='utf-8')

if __name__ == '__main__':
    create_sample_srt() 
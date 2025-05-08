if __name__ == "__main__":
    emotion = input("Enter an emotion (e.g., happy, sad, angry): ")

    # Step 1: Get song recommendation from Hugging Face LLM
    print(f"Getting a song for emotion: {emotion}")
    song_text = get_song_recommendation(emotion)
    print(f"LLM Suggested: {song_text}")

    # Try to extract just the song name
    # You can add better parsing later if needed
    first_line = song_text.strip().split('\n')[0]
    print(f"Searching Spotify for: {first_line}")

    # Step 2: Search on Spotify
    song_data = search_song(first_line)

    if song_data:
        print("\n🎵 Song Details:")
        print(f"Title: {song_data['title']}")
        print(f"Artist: {song_data['artist']}")
        print(f"Album: {song_data['album']}")
        print(f"Preview URL: {song_data['preview_url']}")
        print(f"Album Art: {song_data['image_url']}")
    else:
        print("❌ No song found on Spotify.")

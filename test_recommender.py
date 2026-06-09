# if __name__ == "__main__":
#     emotion = input("Enter an emotion (e.g., happy, sad, angry): ")

#     # Step 1: Get song recommendation from Hugging Face LLM
#     print(f"Getting a song for emotion: {emotion}")
#     song_text = get_song_recommendation(emotion)
#     print(f"LLM Suggested: {song_text}")

#     # Try to extract just the song name
#     # You can add better parsing later if needed
#     first_line = song_text.strip().split('\n')[0]
#     print(f"Searching Spotify for: {first_line}")

#     # Step 2: Search on Spotify
#     song_data = search_song(first_line)

#     if song_data:
#         print("\n🎵 Song Details:")
#         print(f"Title: {song_data['title']}")
#         print(f"Artist: {song_data['artist']}")
#         print(f"Album: {song_data['album']}")
#         print(f"Preview URL: {song_data['preview_url']}")
#         print(f"Album Art: {song_data['image_url']}")
#     else:
#         print("❌ No song found on Spotify.")



from song_recommender import get_song_recommendation

if __name__ == "__main__":
    emotion = input("Enter an emotion (e.g., happy, sad, angry): ")

    # Step 1: Get song recommendation
    print(f"Getting a song for emotion: {emotion}")
    song_data = get_song_recommendation(emotion)

    if song_data:
        print("\n🎵 Song Details:")
        print(f"Title: {song_data.get('title', 'Unknown')}")
        print(f"Artist: {song_data.get('artist', 'Unknown')}")
        print(f"Preview URL: {song_data.get('preview_url', 'No preview available')}")
        print(f"Album Art: {song_data.get('image_url', 'No album art available')}")
        print(f"Spotify URL: {song_data.get('spotify_url', 'No Spotify link available')}")
    else:
        print("❌ No song found for the given emotion.")
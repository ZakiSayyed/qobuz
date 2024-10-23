import uiautomator2 as u2
import csv
import random
import time
import threading
import subprocess
import logging

from super_proxy import setup_proxy_main
from num_of_tracks import get_track_count

# Setup logging
logging.basicConfig(
    filename='activity_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(threadName)s - %(message)s'
)

# Global configuration for the script
config = {
    'stream_limit_min': 1,     # Minimum number of streams per account
    'stream_limit_max': 3,     # Maximum number of streams per account
    'play_time_min': 90,        # Minimum play time per track in seconds
    'play_time_max': 130,       # Maximum play time per track in seconds
    'content_distribution': {   # Percentage distribution for playing content
        'track': 30,
        'album': 30,
        'artist_search': 40
    },
    'track_interaction': {      # Interaction settings
        'like_percentage': 50,  # 100% chance to like the song
        'add_to_playlist': 50   # 100% chance to add the song to playlist
    }
}
# Load the inputs from CSV files
def load_inputs():
    accounts = []
    album_urls = []
    track_urls = []
    artist_songs = []

    # Load account details
    with open('accounts.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            accounts.append(row)

    # Load album URLs
    with open('albumn_urls.csv', mode='r') as file:
        reader = csv.reader(file)
        album_urls = list(reader)

    # Load track URLs
    with open('track_urls.csv', mode='r') as file:
        reader = csv.reader(file)
        track_urls = list(reader)

    # Load artist search keywords
    with open('artist_song.csv', mode='r') as file:
        reader = csv.reader(file)
        artist_songs = list(reader)

    return accounts, album_urls, track_urls, artist_songs

# Assign proxy for each account
def assign_proxy(device, account):

    proxyserver =  account['pserver']
    proxyport = account['pport']
    username = account['pusername']
    password = account['ppassword']

    logging.info(f"Assigning proxy : \nProxy Server : {proxyserver}\nProxy Port : {proxyport}\nUsername : {username}\nPassword : {password}")
    print(f"Assigning proxy : \nProxy Server : {proxyserver}\nProxy Port : {proxyport}\nUsername : {username}\nPassword : {password}")
    # Implement proxy binding logic here using third-party proxy app (e.g., super_proxy or oxy proxy manager)
    setup_proxy_main(proxyserver,proxyport,username,password,device)

# Log into Qobuz
def login_qobuz(d, account):
    d=u2.connect(d.serial)

    username = account['username']
    password = account['password']

    # Start the Qobuz app and navigate to login using uiautomator2 on the device 'd'
    d.app_start("com.qobuz.music", "com.qobuz.android.mobile.app.screen.home.MainActivity")
    time.sleep(5)

    if d(text="Discover"):
        print("Logged in Already")
        d.app_stop("com.qobuz.music")
        return

    logging.info(f"Logging into Qobuz with email: {account['username']} on device {d.serial}")
    print(f"Logging into Qobuz with email: {account['username']} on device {d.serial}")

    if d(text='Enter your email address').exists:
        d(text='Enter your email address').click()
        d.send_keys(username)
    else:
        print("Unable to click on Enter Email")

    time.sleep(3)

    if d(text='Continue').exists:
        d(text='Continue').click()

    time.sleep(3)

    if d(text='Enter your password').exists:
        d(text='Enter your password').click()
        d.send_keys(password)

    time.sleep(3)

    if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.view.View[1]').exists:
        d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.ScrollView/android.view.View[1]').click()
    else:
        print("Error")
    
    time.sleep(3)

    if d(text='YES').exists:
        d(text='YES').click()
        print("Clicked on YES")
        
    time.sleep(3)

    if d(text='Allow').exists:
        d(text='Allow').click()
        print("Clicked on Allow access")
        
    time.sleep(2)

# Randomly select content type based on percentage distribution
def select_content(album_urls, track_urls, artist_songs):
    content_type = random.choices(
        ['track', 'album', 'artist_search'],
        weights=[
            config['content_distribution']['track'],
            config['content_distribution']['album'],
            config['content_distribution']['artist_search']
        ],
        k=1
    )[0]

    if content_type == 'track':
        selected_content = random.choice(track_urls)
        logging.info(f"Selected track: {selected_content}")
        print(f"Selected track: {selected_content}")
    elif content_type == 'album':
        selected_content = random.choice(album_urls)
        logging.info(f"Selected album: {selected_content}")
        print(f"Selected album: {selected_content}")
    elif content_type == 'artist_search':
        selected_content = random.choice(artist_songs)
        logging.info(f"Selected artist/song search: {selected_content}")
        print(f"Selected artist/song search: {selected_content}")

    return content_type, selected_content

# Play selected content for a random duration
def play_content(device, content_type, content):
    selected_content = content[0]
    d = u2.connect(device.serial)
    print(device.serial)
    
    play_duration = random.randint(config['play_time_min'], config['play_time_max'])
    minutes = play_duration // 60
    seconds = play_duration % 60
    
    # Format the output to MM:SS
    duration = f"{minutes:02}:{seconds:02}"
    print(f"Play duration is : {duration}")
    # Set 100% chance for testing
    like_percentage = config['track_interaction']['like_percentage']  
    add_to_playlist_percentage = config['track_interaction']['add_to_playlist']  

    if content_type == 'track':
        time.sleep(5)
        d.shell(f"am start -a android.intent.action.VIEW -d '{selected_content}'")
        time.sleep(6)

        logging.info(f"Selected track: {selected_content}")
        print(f"Selected track: {selected_content}")

        if d(description='Play').exists:
            d(description='Play').click()
            print("Clicked on Play")    

        time.sleep(3)

        if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').exists:
            d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').click()
            print("Clicked on the Song being played")
        
        time.sleep(3)

        song_paused = False
        while not song_paused:
            if d(text=f'{duration}').exists():
                if d(resourceId='com.qobuz.music:id/playPauseBtn').exists:
                    d(resourceId='com.qobuz.music:id/playPauseBtn').click()
                    print("Song Paused")
                    song_paused = True  # Mark the song as paused but continue with rest of the logic

        # Since like_percentage and add_to_playlist_percentage are 100, both actions will always be triggered
        should_like = random.randint(1, 100) <= like_percentage
        should_add_to_playlist = random.randint(1, 100) <= add_to_playlist_percentage

        # Perform the like action
        if should_like:
            if d(resourceId='com.qobuz.music:id/addRemoveFavoritesImageView').exists:
                d(resourceId='com.qobuz.music:id/addRemoveFavoritesImageView').click()
                print("Song liked!")

        # Perform the add to playlist action
        if should_add_to_playlist:
            if d(resourceId='com.qobuz.music:id/optionsImage').exists:
                d(resourceId='com.qobuz.music:id/optionsImage').click()
                print("Clicked on Options")
                if d(text='Add to playlists').exists:
                    d(text='Add to playlists').click()
                    print("Clicked on Add to Playlists")
                time.sleep(3)
                if d(resourceId='com.qobuz.music:id/subtitleText', instance=1).exists:
                    d(resourceId='com.qobuz.music:id/subtitleText', instance=1).click()
                    print("Clicked on the Playlist")
                    time.sleep(5)

                print("Song added to playlist!")
        
        d.app_stop("com.qobuz.music")

    elif content_type == 'album':
        time.sleep(5)
        d.shell(f"am start -a android.intent.action.VIEW -d '{selected_content}'")
        time.sleep(6)

        logging.info(f"Selected album: {selected_content}")
        print(f"Selected album: {selected_content}")

        if d(description='Play').exists:
            d(description='Play').click()
            print("Clicked on Play")    
        
        time.sleep(3)

        if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').exists:
            d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').click()
            print("Clicked on the Song being played")
        
        time.sleep(3)

        numoftracks = get_track_count(selected_content)
        print(f"Number of tracks : {numoftracks}")

        count = 0
        print(f"Skipping {numoftracks} tracks")
        while count < numoftracks:
            if d(text=f'{duration}').exists():
                if d(resourceId='com.qobuz.music:id/skipNextBtn').exists:
                    d(resourceId='com.qobuz.music:id/skipNextBtn').click()
                    print("Song Skipped")
                    count += 1
                else:
                    print("Skip button not found.")
        
        time.sleep(3)

        d.app_stop("com.qobuz.music")

    elif content_type == 'artist_search':

        d.app_start("com.qobuz.music", "com.qobuz.android.mobile.app.screen.home.MainActivity")
        time.sleep(5)

        while True:
            if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.EditText/android.view.View[3]').exists:
                d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.EditText/android.view.View[3]').click()
                print("Removed the existing text in search")

            if d(text='Search').exists:
                d(text='Search').click()
                print("Clicked on Search")
                break
            else:
                subprocess.call(f"adb -s {device.serial} shell input keyevent 4")
                time.sleep(3)
                if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.EditText/android.view.View[3]').exists:
                    d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View/android.widget.EditText/android.view.View[3]').click()
                    print("Removed the existing text in search")

        time.sleep(3)

        if d(description='Search').exists:
            d(description='Search').click()
            print("Clicked on Search")

        d.send_keys(selected_content)    

        time.sleep(3)

        if d(text='Tracks').exists:
            d(text='Tracks').click()
            print("Clicked on Tracks")

        time.sleep(2)

        if d(description='Options', instance=0).exists:
            d(description='Options', instance=0).click()
            print("Clicked on Options")

        time.sleep(6)

        if d(description='Play').exists:
            d(description='Play').click()
            print("Clicked on Play")    

        if d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').exists:
            d.xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.RelativeLayout/android.widget.FrameLayout[2]/androidx.compose.ui.platform.ComposeView/android.view.View/android.view.View/android.view.View').click()
            print("Clicked on the Song being played")

        while True:
            if d(text=f'{duration}').exists():
                if d(resourceId='com.qobuz.music:id/playPauseBtn').exists:
                    d(resourceId='com.qobuz.music:id/playPauseBtn').click()
                    print("Song Paused")
                    break

        d.app_stop("com.qobuz.music")

# Interact with the content based on configured settings
def interact_with_content(d):
    like_percentage = config['track_interaction']['like_percentage']
    add_to_playlist = config['track_interaction']['add_to_playlist']

    # Randomly "like" a track
    if random.randint(1, 100) <= like_percentage:
        logging.info(f"Liking track on device {d.serial}")
        print(f"Liking track on device {d.serial}")
        # Add uiautomator2 action to like a track

    # Randomly add a track to playlist
    if random.randint(1, 100) <= add_to_playlist:
        logging.info(f"Adding track to playlist on device {d.serial}")
        print(f"Adding track to playlist on device {d.serial}")
        # Add uiautomator2 action to add track to playlist

# Log out and switch accounts
def logout_account(d):
    d=u2.connect(d.serial)
    d.app_start("com.qobuz.music", "com.qobuz.android.mobile.app.screen.home.MainActivity")
    time.sleep(5)
    logging.info(f"Logging out on device {d.serial}")
    print(f"Logging out on device {d.serial}")
    # Add uiautomator2 action to log out
    if d(description='Settings').exists:
        d(description='Settings').click()
        print("Clicked on Settings")
    
    time.sleep(3)
    
    if d(text='Log out').exists:
        d(text='Log out').click()
        print("Clicked on Logout")
    
    time.sleep(2)

    if d(text='OK').exists:
        d(text='OK').click()
        print("Clicked on OK")
        print("Successfully Logged out")
    time.sleep(5)
# Main bot execution function for each device
def bot_execution(udid):
    logging.info(f"Starting bot on device: {udid}")
    print(f"Starting bot on device: {udid}")
    d = u2.connect(udid)  # Connect to the device with specific UDID
    accounts, album_urls, track_urls, artist_songs = load_inputs()

    for account in accounts:
        assign_proxy(d, account)  # Step 2: Assign proxy and bind it

        login_qobuz(d, account)   # Step 3: Login to Qobuz

        stream_limit = random.randint(config['stream_limit_min'], config['stream_limit_max'])
        logging.info(f"Stream limit for account {account['username']} on device {udid}: {stream_limit}")
        print(f"Stream limit for account {account['username']} on device {udid}: {stream_limit}")

        streams = 0
        while streams < stream_limit:
            # Step 4: Select content type and play it
            content_type, selected_content = select_content(album_urls, track_urls, artist_songs)

            # Step 5: Play the content
            play_content(d, content_type, selected_content)

            # Step 6: Interact with the content
            # interact_with_content(d)

            streams += 1
            logging.info(f"Stream {streams} completed for account {account['username']} on device {udid}")
            print(f"Stream {streams} completed for account {account['username']} on device {udid}")

        # Step 7: Check stream limit and log out
        logout_account(d)

    logging.info(f"Bot execution completed on device {udid}")
    print(f"Bot execution completed on device {udid}")

# Function to get the list of connected devices
def get_device_udids():
    result = subprocess.run(['adb', 'devices'], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8').splitlines()

    udids = []
    for line in output[1:]:
        if line.strip() and 'device' in line:
            udid = line.split()[0]
            udids.append(udid)
    
    logging.info(f"Connected devices: {udids}")
    print(f"Connected devices: {udids}")
    return udids

# Main function to launch threads for each device
def main():
    device_udids = get_device_udids()

    threads = []
    for udid in device_udids:
        # Create a new thread for each device and start it
        t = threading.Thread(target=bot_execution, args=(udid,))
        threads.append(t)
        t.start()

    # Wait for all threads to complete
    for t in threads:
        t.join()

    logging.info("All devices have completed bot execution.")
    print("All devices have completed bot execution.")

# Entry point for the script
if __name__ == "__main__":
    main()

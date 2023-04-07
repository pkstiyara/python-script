

import time
import logging
import subprocess
from email.mime.text import MIMEText
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# Set up email settings
from_email = 'classroompragati@gmail.com'
to_email = 'pkstiyara@gmail.com'

# Define the directory to watch
watch_dir = '/home/opc/python-script/monitor.txt'

# Define the event handler
class FileChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Define the email message
        msg = MIMEText(event.src_path + ' has been modified.\n\n' +
                       'Changes:\n\n' +
                       event.src_path.read_text())
        msg['Subject'] = 'File change detected'
        msg['From'] = from_email
        msg['To'] = to_email

        # Send the email
        try:
            p = subprocess.Popen(['ssmtp', to_email], stdin=subprocess.PIPE)
            p.communicate(msg.as_bytes())
            logging.info('Email sent')
        except Exception as e:
            logging.error('Error sending email: %s' %e)

if __name__ == "__main__":
    # Set up the event handler and observer
    event_handler = FileChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_dir, recursive=True)

    # Start the observer
    observer.start()
    logging.info('Watching directory {watch_dir}')

    # Keep the script running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


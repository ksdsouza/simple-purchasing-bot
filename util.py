import subprocess


def send_notification(message: str):
    subprocess.Popen(['notify-send', message])

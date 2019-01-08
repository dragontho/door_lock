import os

hostname = "google.com"
def test_internet_connectivity():
    return os.system("ping -c 1 " + hostname)

if __name__ == "__main__":
    response = test_internet_connectivity()
    if response == 0:
        print(hostname + " is up")
    else:
        print(hostname + " is down")

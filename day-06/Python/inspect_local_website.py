from urllib.error import HTTPError, URLError
from urllib.request import urlopen

URL = "http://127.0.0.1:8000/"

def inspect_website():
    try:
        with urlopen(URL, timeout=5) as response:
            print("Request completed successfully.")
            print("Status code:", response.status)
            print("Content type:", response.headers.get("Content-Type"))
            print("Server header:", response.headers.get("Server"))

            content = response.read(500)
            print("\nFirst 500 bytes of response body:")
            print(content.decode("utf-8", errors="replace"))

    except HTTPError as error:
        print("HTTP error occurred:", error.code)
        print("Reason:", error.reason)

    except URLError as error:
        print("Could not reach the local server.")
        print("Reason:", error.reason)

    except TimeoutError:
        print("The request timed out.")

if __name__ == "__main__":
    inspect_website()

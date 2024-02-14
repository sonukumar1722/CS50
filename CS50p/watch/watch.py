import re
import sys


def main():
    # Prompt the user for input and print the parsed result
    print(parse(input("HTML: ")))


def parse(s):
    if s.startswith("<iframe") and s.endswith("</iframe>"):
        src = extract_src(s)
        if src and "youtube.com/embed/" in src:
            return short_link(src)
    return None


def extract_src(s):
    # Extract the URL from the src attribute of the <iframe> tag
    match = s.split("src=\"", 1)[-1].split("\"", 1)[0]
    return match


def short_link(url):
    # Replace the URL with a short HTTPS URL for YouTube videos
    url = url.replace("http://www.youtube.com/embed", "https://youtu.be")
    url = url.replace("http://youtube.com/embed", "https://youtu.be")
    url = url.replace("https://www.youtube.com/embed", "https://youtu.be")
    url = url.replace("https://youtube.com/embed", "https://youtu.be")
    return url


if __name__ == "__main__":
    main()

import os
import requests
from pathlib import Path

def download_file(url, path):
    """Download a file from a URL and save it to the specified path."""
    response = requests.get(url, stream=True)
    response.raise_for_status()
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(path), exist_ok=True)
    
    with open(path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

def main():
    # Base URL for the assets
    base_url = "https://raw.githubusercontent.com/creativetimofficial/soft-ui-dashboard/main/assets"
    
    # List of CSS files to download
    css_files = [
        "css/nucleo-icons.css",
        "css/nucleo-svg.css",
        "css/soft-ui-dashboard.css",
        "css/soft-ui-dashboard.min.css"
    ]
    
    # List of JS files to download
    js_files = [
        "js/core/popper.min.js",
        "js/core/bootstrap.min.js",
        "js/plugins/perfect-scrollbar.min.js",
        "js/plugins/smooth-scrollbar.min.js",
        "js/plugins/chartjs.min.js",
        "js/soft-ui-dashboard.min.js"
    ]
    
    # List of images to download
    image_files = [
        "img/logo-ct-dark.png",
        "img/logo-ct.png",
        "img/team-2.jpg",
        "img/team-3.jpg",
        "img/team-4.jpg",
        "img/bg-profile.jpg",
        "img/small-logos/logo-xd.svg",
        "img/small-logos/logo-slack.svg",
        "img/small-logos/logo-spotify.svg",
        "img/small-logos/logo-jira.svg",
        "img/small-logos/logo-invision.svg",
        "img/small-logos/logo-webdev.svg"
    ]
    
    # Download CSS files
    print("Downloading CSS files...")
    for css_file in css_files:
        url = f"{base_url}/{css_file}"
        path = os.path.join("static", "assets", css_file)
        print(f"Downloading {url} to {path}")
        try:
            download_file(url, path)
            print(f"Successfully downloaded {css_file}")
        except Exception as e:
            print(f"Error downloading {css_file}: {e}")
    
    # Download JS files
    print("\nDownloading JS files...")
    for js_file in js_files:
        url = f"{base_url}/{js_file}"
        path = os.path.join("static", "assets", js_file)
        print(f"Downloading {url} to {path}")
        try:
            download_file(url, path)
            print(f"Successfully downloaded {js_file}")
        except Exception as e:
            print(f"Error downloading {js_file}: {e}")
    
    # Download image files
    print("\nDownloading image files...")
    for img_file in image_files:
        url = f"{base_url}/{img_file}"
        path = os.path.join("static", "assets", img_file)
        print(f"Downloading {url} to {path}")
        try:
            download_file(url, path)
            print(f"Successfully downloaded {img_file}")
        except Exception as e:
            print(f"Error downloading {img_file}: {e}")
    
    print("\nAsset download complete!")

if __name__ == "__main__":
    main()

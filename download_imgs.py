from google_images_search import GoogleImagesSearch
import requests


if __name__ == "__main__":
    gis = GoogleImagesSearch('_', '_'
)
    gis.search(search_params={
        'q': 'pliers',
        'num': 10,
        'imgType': 'photo',
        'imgSize': 'large',
        'imgDominantColor': 'white',
        'fileType': 'jpg|png'
    })

    for i, image in enumerate(gis.results()):
        response = requests.get(image.url)

        with open(f'komb/z_image_{i}.png', 'wb') as f:
            f.write(response.content)

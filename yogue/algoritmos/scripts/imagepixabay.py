from pixabay import Image


def getImage(query,categ,num):
    API_KEY = '18748996-3847970326558aaeb79b99fe7'

    # image operations
    image = Image(API_KEY)

    # custom image search
    ims = image.search(q=query,
                lang='es',
                image_type='photo',
                orientation='horizontal',
                category=categ,#Accepted values: backgrounds, fashion, nature, science, education, feelings, health, people, religion, places, animals, industry, computer, food, sports, transportation, travel, buildings, business, music
                safesearch='true',
                order='latest',
                page=2,
                per_page=3)
    if ims['total'] == 0 or num > ims['totalHits']:
        return None
    else:
        return ims['hits'][0]['webformatURL']


import random

class NameGenerator(object):
    # From https://github.com/moby/moby/blob/master/pkg/namesgenerator/names-generator.go
    LEFT = ['admiring', 'adoring', 'affectionate', 'agitated', 'amazing', 'angry', 'awesome',
            'beautiful', 'blissful', 'bold', 'boring', 'brave', 'busy', 'charming', 'clever',
		    'cool', 'compassionate', 'competent', 'condescending', 'confident', 'cranky', 'crazy',
		    'dazzling', 'determined', 'distracted', 'dreamy', 'eager', 'ecstatic', 'elastic',
		    'elated', 'elegant', 'eloquent', 'epic', 'exciting', 'fervent', 'festive', 'flamboyant',
		    'focused', 'friendly', 'frosty', 'funny', 'gallant', 'gifted', 'goofy', 'gracious',
		    'great', 'happy', 'hardcore', 'heuristic', 'hopeful', 'hungry', 'infallible', 'inspiring',
		    'interesting', 'intelligent', 'jolly', 'jovial', 'keen', 'kind', 'laughing', 'loving',
		    'lucid', 'magical', 'mystifying', 'modest', 'musing', 'naughty', 'nervous', 'nice',
		    'nifty', 'nostalgic', 'objective', 'optimistic', 'peaceful', 'pedantic', 'pensive',
		    'practical', 'priceless', 'quirky', 'quizzical', 'recursing', 'relaxed', 'reverent',
		    'romantic', 'sad', 'serene', 'sharp', 'silly', 'sleepy', 'stoic', 'strange', 'stupefied',
		    'suspicious', 'sweet', 'tender', 'thirsty', 'trusting', 'unruffled', 'upbeat', 'vibrant',
		    'vigilant', 'vigorous', 'wizardly', 'wonderful', 'xenodochial', 'youthful', 'zealous', 'zen']
    # From https://en.wikipedia.org/wiki/List_of_modernist_poets
    RIGHT = ['Angus', 'Auden', 'Barnes', 'Bishop', 'Brooke', 'Bunting', 'Crane', 'Cummings', 'Doolittle',
             'Eliot', 'Frost', 'Graves', 'Hayden', 'Hopkins', 'Housman', 'Hughes', 'Jarrell', 'Jones',
             'Kipling', 'Lawrence', 'Lowell', 'Loy', 'MacDiarmid', 'MacLeish', 'Moore', 'Owen', 'Parker',
             'Plath', 'Pound', 'Robinson', 'Millay', 'Schwartz', 'Sitwell', 'Slessor', 'Stein', 'Stevens',
             'Tate', 'Williams', 'Yeats', 'Akhmatova', 'Apollinaire', 'Aragon', 'Benn', 'Breton', 'Cavafy',
             'Char', 'Baudelaire', 'Desnos', 'Ekelöf', 'Éluard', 'Heym', 'van Hoddis', 'Jacob', 'Kosovel',
             'Péret', 'Perse', 'Pessoa', 'Prévert', 'Reverdy', 'Rilke', 'Rimbaud', 'Lasker-Schüler', 'Lorca',
             'Lundkvist', 'Mallarmé', 'Martinson', 'Michaux', 'Sjöberg', 'Stramm', 'Seferis', 'Soupault',
             'Supervielle', 'Södergran', 'Trakl', 'Valéry']

    @staticmethod
    def generate():
        left = random.choice(NameGenerator.LEFT).title()
        right = random.choice(NameGenerator.RIGHT)
        return f'{left} {right}'

    @staticmethod
    def slugify(name):
        return '-'.join(name.lower().split())

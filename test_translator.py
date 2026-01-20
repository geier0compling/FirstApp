from dotenv import load_dotenv
from core.pipeline import german_nlp
from adapters.cache_sqlite import TranslationCache
from services.translator_google import GoogleTranslator
load_dotenv()

if __name__ == "__main__":
    text = """In seinem Büro im neunten Stock saß Mr Dursley immer mit dem Rücken zum
Fenster. Andernfalls wäre es ihm an diesem Morgen schwergefallen, sich auf die
Bohrer zu konzentrieren. Er bemerkte die Eulen nicht, die am helllichten Tage
vorbeischossen, wohl aber die Leute unten auf der Straße; sie deuteten in die Lüfte
und verfolgten mit offenen Mündern, wie eine Eule nach der andern über ihre Köpfe
hinwegflog. Die meisten von ihnen hatten überhaupt noch nie eine gesehen, nicht
einmal nachts. Mr Dursley jedoch verbrachte einen ganz gewöhnlichen, eulenfreien
Morgen. Er machte fünf verschiedene Leute zur Schnecke. Er führte mehrere
wichtige Telefongespräche und schrie dabei noch ein wenig lauter. Bis zur
Mittagspause war er glänzender Laune und wollte sich nun ein wenig die Beine
vertreten und beim Bäcker über der Straße einen Krapfen holen. """

    # get vocab from your pipeline
    _, vocab = german_nlp(text)
    print("Vocab:", vocab)

    # create cache + translator
    cache = TranslationCache("translations.db")
    translator = GoogleTranslator(cache)

    # translate words
    result = translator.translate(vocab, study_lang="de", native_lang="en")
    print("\nTranslations:", result)


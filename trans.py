from googletrans import Translator
translator = Translator(service_urls=['translate.googleapis.com'])
translation = translator.translate('안녕하세요.')
print(translation.text)
import re

URL = "https://www.toppreise.ch"


class Product:
    def __init__(self, config):
        self.config = config
        self.link = URL + config.attrs['data-link']
        self._price = 0
        self._name = ''

    @property
    def price(self):    # perhaps we want to refresh self.config for this.
        pattern = r"CHF\s+(\d{1,3}(?:\'\d{3})*(?:.\d{2})?)"
        res_string = self.config.text
        matches = re.findall(pattern, res_string)
        price = matches[0].replace("'", "")

        self._price = float(price)
        return self._price

    @property
    def name(self):
        pattern = r"^(.*?),"

        match = re.search(pattern, self.config.text.strip())
        if match:
            self._name = match.group(1).strip()
        return self._name

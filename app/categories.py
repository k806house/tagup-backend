import json


class Categories:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, filepath):
        with open(filepath) as f:
            data = json.load(f)
        categories = cls(data)
        return categories

    def find_by_category(self, query):
        result = []

        for name_lvl1, cat_lvl1 in self.data.items():
            if self._match(name_lvl1, query):
                result.append({
                    'match': name_lvl1,
                    'path': [name_lvl1],
                    'siblings': None
                })
                continue

            for name_lvl2, cat_lvl2 in cat_lvl1.items():
                if self._match(name_lvl2, query):
                    result.append({
                        'match': name_lvl2,
                        'path': [name_lvl1, name_lvl2],
                        'siblings': None #list(cat_lvl1.keys())
                    })
                    continue

                for name_lvl3, cat_lvl3 in cat_lvl2.items():
                    if self._match(name_lvl3, query):
                        result.append({
                            'match': name_lvl3,
                            'path': [name_lvl1, name_lvl2, name_lvl3],
                            'siblings': None#list(cat_lvl2.keys())
                        })
                        continue

                    for name_lvl4 in cat_lvl3:
                        if self._match(name_lvl4, query):
                            result.append({
                                'match': name_lvl4,
                                'path': [name_lvl1, name_lvl2, name_lvl3, name_lvl4],
                                'siblings': list(cat_lvl3)
                            })

        return result

    def get_top_level(self):
        return list(self.data.keys())

    @staticmethod
    def _match(category, query):
        return category.lower() == query.lower()

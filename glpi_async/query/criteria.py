class CriteriaBuilder:
    def __init__(self):
        self._criteria = []

    def where(self, field, value, searchtype="equals", link="AND"):
        index = len(self._criteria)
        self._criteria.append({
            f"criteria[{index}][field]": field,
            f"criteria[{index}][searchtype]": searchtype,
            f"criteria[{index}][value]": value,
        })
        if index > 0:
            self._criteria[-1][f"criteria[{index}][link]"] = link
        return self

    def build(self):
        out = {}
        for c in self._criteria:
            out.update(c)
        return out

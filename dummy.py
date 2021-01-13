class dummy:
    def __init__(self, first, last):
        self.first = first
        self.last = last
    
    def __str__(self):
        return (
            f'{self.first} '
            f'{self.last}'
        )

guyO = dummy('Guy Olivier', 'de Saint Albin')
print(guyO)

comedian = {"name": "Eric Idle", 'age': 74}
print(f'The comedian is {comedian["name"]}, aged {comedian["age"]}.')
print(f"The comedian is {comedian['name']}, aged {comedian['age']}.")
from marshmallow import *
to_exclude = ['fields']

for name in to_exclude:
    del globals()[name]

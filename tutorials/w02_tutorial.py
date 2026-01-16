import pandas as pd

person = pd.Series({'First': 'Hiroto', 'Last': 'Ikegami'})

print(f"Hello from {person['First']} {person['Last']}")
import pandas as pd

from utils.config import *


class DataLoader:

    def __init__(self):
        self.internal = None
        self.owners = None
        self.mygate = None

    def load(self):

        self.internal = pd.read_excel(INTERNAL_FILE)

        self.owners = pd.read_excel(OWNER_FILE)

        self.mygate = pd.read_csv(MYGATE_FILE)

        return self.internal, self.owners, self.mygate
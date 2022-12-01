class Card:
    _value = int()
    _symbol = int()
    _string_value = str()
    _string_symbol = str()

    def __init__(self, value, symbol):
        self._value = value
        self._symbol = symbol
        self.translateSymbol()
        self.translateValue()
    
    def translateValue(self):
        if self._value > 1 and self._value<11:
            self._string_value = str(self._value)
        else:
            if self._value == 1: 
                self._string_value = 'A'
            if self._value == 11:
                self._string_value = 'J'
            if self._value == 12:
                self._string_value = 'Q'
            if self._value == 13:
                self._string_value = 'K'

    def translateSymbol(self):
        if self._symbol == 0:
            self._string_symbol = 'Hearts'
        if self._symbol == 1:
            self._string_symbol = 'Tiles'
        if self._symbol == 2:
            self._string_symbol = 'Clovers'
        if self._symbol == 3:
            self._string_symbol = 'Pikes'
    
    def getSymbol(self):
        return self._symbol
    
    def getStringSymbol(self):
        return self._string_symbol
    
    def getValue(self):
        return self._value
    
    def getStringValue(self):
        return self._string_value
    
    def getFullName(self):
        return self._string_value + ' of ' + self._string_symbol

    def getInfo(self):
        return (self._value, self._symbol)
    
    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.getInfo() == other.getInfo():
            return True
        return False
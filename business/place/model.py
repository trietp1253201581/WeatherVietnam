# need download
import pycountry
from typing import Literal
class Country:
    def __init__(self, code: str, name: str|None = None):
        self.code = code
        self.name = name
        
    @property
    def code(self):
        return self.__code
    
    @property
    def name(self):
        return self.__name
    
    @code.setter
    def code(self, code: str):
        try:
            country_iso2 = pycountry.countries.get(alpha_2=code.upper())
            country_iso3 = pycountry.countries.get(alpha_3=code.upper())
            if country_iso2 is None and country_iso3 is None:
                raise ValueError("Invalid country code!")
            elif country_iso2 is not None:
                self.__code = country_iso2.alpha_2
                self.__name = country_iso2.name
            elif country_iso3 is not None:
                self.__code = country_iso3.alpha_2
                self.__name = country_iso3.name
        except ValueError as valueErr:
            raise ValueError("Invalid country code!")
        
    @name.setter
    def name(self, name: str|None = None):
        self.__name = name
            
    def switch_to(self, code_type: Literal['alpha_2', 'alpha_3']) -> str:
        try:
            country_iso = pycountry.countries.get(alpha_2=self.code)
            if country_iso is None:
                country_iso = pycountry.countries.get(alpha_3=self.code)
                if country_iso is None:
                    raise ValueError("Invalid!")
            if code_type == 'alpha_2':
                self.__code = country_iso.alpha_2
            else:
                self.__code = country_iso.alpha_3
            return self.__code
        except ValueError as e:
            raise e
        
    def get_iso_name(self) -> str:
        self.switch_to('alpha_2')
        try:
            country_iso = pycountry.countries.get(alpha_2=self.__code)
            return country_iso.name
        except ValueError as e:
            raise e
        
    def get_offical_name(self) -> str:
        self.switch_to('alpha_2')
        try:
            country_iso = pycountry.countries.get(alpha_2=self.__code)
            return country_iso.official_name
        except ValueError as e:
            raise e
        
    def __str__(self):
        s = f'Student(\n'
        s += f' code={self.code}\n'
        s += f' name={self.name}\n'
        s += f')\n'
        return s
    
if __name__ == '__main__':
    country = Country('VNM', "VVV")
    country.switch_to('alpha_3')
    print(country)
    print(country.get_iso_name())
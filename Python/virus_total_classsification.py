import json
from datetime import *
import enum

class site_categoization(enum.Enum):
    SAFE = 1
    RISK = 2

class virus_total_classification :
    _site: str = None
    _harmless: int = 0
    _malicious: int = 0
    _suspicious: int = 0
    _timeout: int = 0
    _undetected: int = 0
    _site_categoization: site_categoization = None
    _site_categoization_str : str = None
    _ttl: datetime = None
    _current_date_and_time: datetime = None
    _ttl_minutes: int = None

    def __init__(self, site : str, json_string: str, ttl_minutes: int):
        self._current_date_and_time = datetime.now()
        self._ttl_minutes = ttl_minutes
        self.parse(site, json_string)

#{'harmless': 76, 'malicious': 0, 'suspicious': 0, 'timeout': 0, 'undetected': 7}
    def parse(self, site, classification_for_site):

        self._harmless = classification_for_site["harmless"]
        self._malicious = classification_for_site["malicious"]
        self._suspicious = classification_for_site["suspicious"]
        self._timeout = classification_for_site["timeout"]
        self._undetected = classification_for_site["undetected"]
        self._site = site
        self._site_categoization = self.categoize()
        self._site_categoization_str = self.categoize_string()

        date_time_ttl = self._current_date_and_time + timedelta(minutes=self._ttl_minutes)
        self._ttl = date_time_ttl

    def get_ttl(self):
        return self._ttl

    def categoize(self):
        if self._harmless >= 1 or self._malicious >= 1 or self._suspicious >= 1:
            return site_categoization.RISK
        else:
            return site_categoization.SAFE

    def categoize_string(self):
        if self._harmless >= 1 or self._malicious >= 1 or self._suspicious >= 1:
            return 'RISK'
        else:
            return 'SAFE'

    # def toSQL(self):
    #     return f"insert into virustotal_clasification (site,date,insert_datetime,category,harmless,malicious,suspicious,timeout,undetected) valuues ('{self._site}',date(now()), now(),'{self._site_categoization}',{harmless},{malicious},{suspicious},{timeout},{undetected});"

    def to_row_in_array(self):
        return [self._site,
                datetime.now().strftime('%Y-%m-%d'),
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                self._ttl.strftime('%Y-%m-%d %H:%M:%S'),
                self._site_categoization_str,
                self._harmless,
                self._malicious,
                self._suspicious,
                self._timeout,
                self._undetected]


    def to_str(self):
        return str(self.torow_in_array())



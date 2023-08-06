import atexit
import json
import math
import uuid
from urllib.parse import quote

from oauthlib.oauth2 import BackendApplicationClient, TokenExpiredError, InvalidClientError
from oauthlib.oauth2.rfc6749.errors import CustomOAuth2Error
from requests_oauthlib import OAuth2Session


class SuiteCRM:

    def __init__(self, client_id: str, client_secret: str, url: str, logout_on_exit: bool = False):

        self.baseurl = url
        self._client_id = client_id
        self._client_secret = client_secret
        self._logout_on_exit = logout_on_exit
        self._headers = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                        '(KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
        self._login()
        self._modules()

    def _modules(self):
        self.Accounts = Module(self, 'Accounts')
        self.Bugs = Module(self, 'Bugs')
        self.Calendar = Module(self, 'Calendar')
        self.Calls = Module(self, 'Calls')
        self.Cases = Module(self, 'Cases')
        self.Campaigns = Module(self, 'Campaigns')
        self.Contacts = Module(self, 'Contacts')
        self.Documents = Module(self, 'Documents')
        self.Email = Module(self, 'Email')
        self.Emails = Module(self, 'Emails')
        self.Employees = Module(self, 'Employees')
        self.Leads = Module(self, 'Leads')
        self.Lists = Module(self, 'Lists')
        self.Meetings = Module(self, 'Meetings')
        self.Notes = Module(self, 'Notes')
        self.Opportunities = Module(self, 'Opportunities')
        self.Projects = Module(self, 'Projects')
        self.Spots = Module(self, 'Spots')
        self.Surveys = Module(self, 'Surveys')
        self.Target = Module(self, 'Target')
        self.Targets = Module(self, 'Targets')
        self.Tasks = Module(self, 'Tasks')
        self.Templates = Module(self, 'Templates')

    def _refresh_token(self) -> None:
        """
        Fetch a new token from from token access url, specified in config file.
        :return: None
        """
        try:
            self.OAuth2Session.fetch_token(token_url=self.baseurl[:-2] + 'access_token',
                                           client_id=self._client_id,
                                           client_secret=self._client_secret)
        except InvalidClientError:
            exit('401 (Unauthorized) - client id/secret')
        except CustomOAuth2Error:
            exit('401 (Unauthorized) - client id')
        # Update configuration file with new token'
        with open('AccessToken.txt', 'w+') as file:
            file.write(str(self.OAuth2Session.token))

    def _login(self) -> None:
        """
        Checks to see if a Oauth2 Session exists, if not builds a session and retrieves the token from the config file,
        if no token in config file, fetch a new one.

        :return: None
        """
        # Does session exist?
        if not hasattr(self, 'OAuth2Session'):
            client = BackendApplicationClient(client_id=self._client_id)
            self.OAuth2Session = OAuth2Session(client=client,
                                               client_id=self._client_id)
            self.OAuth2Session.headers.update({"User-Agent": self._headers,
                                               'Content-Type': 'application/json'})
            with open('AccessToken.txt', 'w+') as file:
                token = file.read()
                if token == '':
                    self._refresh_token()
                else:
                    self.OAuth2Session.token = token
        else:
            self._refresh_token()

        # Logout on exit
        if self._logout_on_exit:
            atexit.register(self._logout)

    def _logout(self) -> None:
        """
        Logs out current Oauth2 Session
        :return: None
        """
        url = '/logout'
        self.request(f'{self.baseurl}{url}', 'post')
        with open('AccessToken.txt', 'w+') as file:
            file.write('')

    def request(self, url: str, method, parameters='') -> dict:
        """
        Makes a request to the given url with a specific method and data. If the request fails because the token expired
        the session will re-authenticate and attempt the request again with a new token.

        :param url: (string) The url
        :param method: (string) Get, Post, Patch, Delete
        :param parameters: (dictionary) Data to be posted

        :return: (dictionary) Data
        """
        url = quote(url, safe='/:?=&')
        data = json.dumps({"data": parameters})
        try:
            the_method = getattr(self.OAuth2Session, method)
        except AttributeError:
            return

        try:
            if parameters == '':
                data = the_method(url)
            else:
                data = the_method(url, data=data)
        except TokenExpiredError:
            self._refresh_token()
            if parameters == '':
                data = the_method(url)
            else:
                data = the_method(url, data=data)

        # Revoked Token
        attempts = 0
        while data.status_code == 401 and attempts < 1:
            self._refresh_token()
            if parameters == '':
                data = the_method(url)
            else:
                data = the_method(url, data=data)
            attempts += 1
        if data.status_code == 401:
            exit('401 (Unauthorized) client id/secret has been revoked, new token was attempted and failed.')

        # Database Failure
        # SuiteCRM does not allow to query by a custom field see README, #Limitations
        if data.status_code == 400 and 'Database failure.' in data.content.decode():
            raise Exception(data.content.decode())

        return json.loads(data.content)


class Module:

    def __init__(self, suitecrm, module_name):
        self.module_name = module_name
        self.suitecrm = suitecrm

    def create(self, **attributes) -> dict:
        """
        Creates a record with given attributes
        :param attributes: (**kwargs) fields with data you want to populate the record with.

        :return: (dictionary) The record that was created with the attributes.
        """
        url = '/module'
        data = {'type': self.module_name, 'id': str(uuid.uuid4()), 'attributes': attributes}
        return self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'post', data)

    def delete(self, record_id: str) -> dict:
        """
        Delete a specific record by id.
        :param record_id: (string) The record id within the module you want to delete.

        :return: (dictionary) Confirmation of deletion of record.
        """
        # Delete
        url = f'/module/{self.module_name}/{record_id}'
        return self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'delete')

    def fields(self) -> list:
        """
        Gets all the attributes that can be set in a record.
        :return: (list) All the names of attributes in a record.
        """
        # Get total record count
        url = f'/module/{self.module_name}?page[number]=1&page[size]=1'
        return list(self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'get')['data'][0]['attributes'].keys())

    def get(self, fields: list = None, sort: str = None, **filters) -> list:
        """
        Gets records given a specific id or filters, can be sorted only once, and the fields returned for each record
        can be specified.

        :param fields: (list) A list of fields you want to be returned from each record.
        :param sort: (string) The field you want the records to be sorted by.
        :param filters: (**kwargs) fields that the record has that you want to filter on.
                        ie... date_start= {'operator': '>', 'value':'2020-05-08T09:59:00+00:00'}

        Important notice: we don’t support multiple level sorting right now!

        :return: (list) A list of dictionaries, where each dictionary is a record.
        """
        # Fields Constructor
        if fields:
            fields = f'?fields[{self.module_name}]=' + ','.join(fields)
            url = f'/module/{self.module_name}{fields}&filter'
        else:
            url = f'/module/{self.module_name}?filter'

        # Filter Constructor
        operators = {'=': 'EQ', '<>': 'NEQ', '>': 'GT', '>=': 'GTE', '<': 'LT', '<=': 'LTE'}
        for field, value in filters.items():
            if isinstance(value, dict):
                url = f'{url}[{field}][{operators[value["operator"]]}]={value["value"]}and&'
            else:
                url = f'{url}[{field}][eq]={value}and&'
        url = url[:-4]

        # Sort
        if sort:
            url = f'{url}&sort=-{sort}'

        # Execute
        return self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'get')['data']

    def get_all(self, record_per_page: int = 100) -> list:
        """
        Gets all the records in the module.
        :return: (list) A list of dictionaries, where each dictionary is a record.
                 Will return all records within a module.
        """
        # Get total record count
        url = f'/module/{self.module_name}?page[number]=1&page[size]=1'
        pages = math.ceil(self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'get')['meta']['total-pages'] /
                          record_per_page) + 1
        result = []
        for page in range(1, pages):
            url = f'/module/{self.module_name}?page[number]={page}&page[size]={record_per_page}'
            result.extend(self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'get'))
        return result

    def update(self, record_id: str, **attributes) -> dict:
        """
        updates a record.

        :param record_id: (string) id of the current module record.
        :param attributes: (**kwargs) fields inside of the record to be updated.

        :return: (dictionary) The updated record
        """
        url = '/module'
        data = {'type': self.module_name, 'id': record_id, 'attributes': attributes}
        return self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'patch', data)

    def get_relationship(self, record_id: str, related_module_name: str) -> dict:
        """
        returns the relationship between this record and another module.

        :param record_id: (string) id of the current module record.
        :param related_module_name: (string) the module name you want to search relationships for, ie. Contacts.

        :return: (dictionary) A list of relationships that this module's record contains with the related module.
        """
        url = f'/module/{self.module_name}/{record_id}/relationships/{related_module_name.lower()}'
        return self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'get')

    def create_relationship(self, record_id: str, related_module_name: str, related_bean_id: str) -> dict:
        """
        Creates a relationship between 2 records.

        :param record_id: (string) id of the current module record.
        :param related_module_name: (string) the module name of the record you want to create a relationship,
               ie. Contacts.
        :param related_bean_id: (string) id of the record inside of the other module.

        :return: (dictionary) A record that the relationship was created.
        """
        # Post
        url = f'/module/{self.module_name}/{record_id}/relationships'
        data = {'type': related_module_name.capitalize(), 'id': related_bean_id}
        return self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'post', data)

    def delete_relationship(self, record_id: str, related_module_name: str, related_bean_id: str) -> dict:
        """
        Deletes a relationship between 2 records.

        :param record_id: (string) id of the current module record.
        :param related_module_name: (string) the module name of the record you want to delete a relationship,
               ie. Contacts.
        :param related_bean_id: (string) id of the record inside of the other module.

        :return: (dictionary) A record that the relationship was deleted.
        """
        url = f'/module/{self.module_name}/{record_id}/relationships/{related_module_name.lower()}/{related_bean_id}'
        return self.suitecrm.request(f'{self.suitecrm.baseurl}{url}', 'delete')

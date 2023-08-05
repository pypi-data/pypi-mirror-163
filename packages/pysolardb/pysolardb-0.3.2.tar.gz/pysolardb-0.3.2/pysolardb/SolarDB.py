import requests
import json
import os
import logging
import outdated
import pandas as pd
from io import StringIO
from . import sample
from urllib3.exceptions import InsecureRequestWarning


class SolarDB():

    def __init__(self, token: str = None, logging_level: int = 10, apiURL: str = "solardb.univ-reunion.fr", skipSSL: bool = False):
        self.logger = logging.getLogger(__name__)
        self.setLoggerLevel(logging_level)
        self.checkIfOutdated()
        self.__baseURL = "https://" + apiURL + "/api/v1/"
        ## Used to ingore the SSL certification
        self.__verify = not skipSSL
        if skipSSL:
            requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
        self.__cookies = None
        ## Automatically logs in SolarDB if the token is saved in the '~/.bashrc' file
        if token is None:
            token = os.environ.get('SolarDBToken')
        self.login(token)

        ## Methods to log in SolarDB----------------------------------------------------------

    def login(self, token: str):
        """
        Gives access of SolarDB

        Parameters
        ----------
        token : str
            This string is used as a key to log in SolarDB.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem 
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        try:
            if token is not None:
                res = requests.get(self.__baseURL + "login?token=" + token, verify=self.__verify)
                res.raise_for_status()
                self.__cookies = res.cookies
                self.logger.debug(json.loads(res.content)["message"])
            else:
                self.logger.info("You will need to use your token to log in SolarDB")
        except requests.exceptions.HTTPError:
            self.logger.warning("login -> HTTP Error:\n%s\n",json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("login -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("login -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("login -> Request Error:\n%s\n", err)

    def register(self, email: str):
        """
        Sends a token via email.

        Parameters
        ----------
        email : str
            This string represents the user's mail address.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem 
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        try:
            res = requests.get(self.__baseURL + "register?email=" + email, verify=self.__verify)
            res.raise_for_status()
            self.logger.debug(json.loads(res.content)["message"])
        except requests.exceptions.HTTPError:
            self.logger.warning("register -> HTTP Error:\n%s%s", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("register -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("register -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("register -> Request Error:\n%s\n", err)

    def status(self):
        """
        This method is used to verify if you are still logged in.

        Returns
        -------

        A boolean representing the user's connection status.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        try:
            logged_in = False
            res = requests.get(self.__baseURL + "status", cookies=self.__cookies, verify=self.__verify)
            if json.loads(res.content)["message"] == "User connected":
                logged_in = True
            self.logger.info(json.loads(res.content)["message"])
            return logged_in
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("status -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("status -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("status -> Request Error:\n%s\n", err)

    def logout(self):
        """
        Logs out of SolarDB.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        try:
            res = requests.get(self.__baseURL + "logout", cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            self.logger.debug(json.loads(res.content)["message"])
            self.__cookies = None
        except requests.exceptions.HTTPError:
            self.logger.warning("logout -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("logout -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("logout -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("logout -> Request Error:\n%s\n", err)

    ## Methods to recover the data -------------------------------------------------------

    def getAllSites(self):
        """
        Returns all the alias sites accessible through SolarDB.

        Returns
        -------
            A list every alias site present in SolarDB.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        sites = []
        try:
            res = requests.get(self.__baseURL + "data/sites", cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            for i in range(len(json.loads(res.content)["data"])):
                sites.append(json.loads(res.content)["data"][i])
            self.logger.debug("All data sites successfully extracted from SolarDB")
            return sites
        except requests.exceptions.HTTPError:
            self.logger.warning("getAllSites -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getAllSites -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getAllSites -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getAllSites -> Request Error:\n%s\n", err)

    def getAllTypes(self):
        """
        Returns all the sensor types accessible through SolarDB.

        Returns
        -------
            A list every sensor type present in SolarDB.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        sensor_types = []
        try:
            res = requests.get(self.__baseURL + "data/types", cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            for i in range(len(json.loads(res.content)["data"])):
                sensor_types.append(json.loads(res.content)["data"][i])
            self.logger.debug("All data types successfully extracted from SolarDB")
            return sensor_types
        except requests.exceptions.HTTPError:
            self.logger.warning("getAllTypes -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getAllTypes -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getAllTypes -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getAllTypes -> Request Error:\n%s\n", err)

    def getSensors(self, sites: list = None, sensor_types: list = None):
        """
        Returns sensors present in SolarDB by sites and/or types.
        If no sites or types are given, returns all sensors present in SolarDB

        Parameters
        ----------
        sites : list (OPTIONAL)
            This list is used to specify the sites in which we will search the sensors.
        sensor_types : list (OPTIONAL)
            This list is used to specify sensor types to recover.

        Returns
        -------
        A list containing the sensors extracted from SolarDB

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """
        sensors = []
        query = self.__baseURL + "data/sensors"
        args = ""
        if sites is not None:
            args += "&site=" + ','.join(sites)
        if sensor_types is not None:
            args += "&type=" + ','.join(sensor_types)
        if args != "":
            query += "?" + args
        try:
            res = requests.get(query, cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            sensors = json.loads(res.content)["data"]
            self.logger.debug("All sensors successfully extracted from SolarDB")
            return sensors
        except requests.exceptions.HTTPError:
            self.logger.warning("getSensors -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getSensors -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getSensors -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getSensors -> Request Error:\n%s\n", err)

    def getData(
            self,
            sites: list = None,
            sensor_types: list = None,
            sensors: list = None,
            start: str = None,
            stop: str = None,
            aggrFn: str = None,
            aggrEvery: str = None
    ):
        """
        Extracts data associated to at least one site, sensor and/or type. The user can
        choose the time period on which the extraction is set (set on the last 24h by
        default) and define an aggregation for a better analysis.

        Parameters
        ----------
        sites : list
            This list is used to specify the sites for which we will search the data.
        sensor_types : list
            This list is used to specify sensor types used to recover the data.
        sensors : list
            This list is used to specify the sensors used to recover the data.
        start : str (OPTIONAL)
            This string specifies the starting date for the data recovery. It either follows
            a date format, an RFC3339 date format, or a duration unit respecting the '[N][T]'
            format, where [N] is an integer and [T] is one of the following strings:
            * 'y'   : year
            * 'mo'  : month
            * 'w'   : week
            * 'd'   : day
            * 'h'   : hour
            * 'm'   : minute
            Example: '-24d' == 24 days ago
        stop : str (OPTIONAL)
            This string specifies the ending date for the data recovery. It follows the same
            format as "start".
        aggrFn : str (OPTIONAL)
            This string represents the function to apply for the aggregation, such as:
            * 'mean'    : the average value
            * 'min'     : the minimum value
            * 'max'     : the maximum value
            * 'count'   : the number of non-null value
        aggrEvery : str (OPTIONAL)
            This string represents the period for the aggregation. It follows the duration
            unit format defined previously.

        Returns
        -------
            A dictionary containing the data per site and sensor. It is structured as 
            follows:
            {
                site{
                    sensor{
                        dates:  [...]
                        values: [...]
                    }
                }
            }

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """
        query = self.__baseURL + "data/json"
        args = ""
        if sites is not None:
            args += "&site=" + ','.join(sites)
        if sensor_types is not None:
            args += "&type=" + ','.join(sensor_types)
        if sensors is not None:
            args += "&sensorid=" + ','.join(sensors)
        if start is not None:
            args += "&start=" + start
        if stop is not None:
            args += "&stop=" + stop
        if aggrFn is not None:
            args += "&aggrFn=" + aggrFn
        if aggrEvery is not None:
            args += "&aggrEvery=" + aggrEvery
        if args != "":
            query += "?" + args

        try:
            res = requests.get(query, cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            data = json.loads(res.content)["data"]
            if data:
                self.logger.debug("Data successfully recovered")
            else:
                self.logger.info("There is no data for this particular request")
            return data
        except requests.exceptions.HTTPError:
            self.logger.warning("getData -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getData -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getData -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getData -> Request Error:\n%s\n", err)

    def getBounds(
            self,
            sites: list = None,
            sensor_types: list = None,
            sensors: list = None
    ):
        """
        Extracts the temporal bounds of each sensor associated to at least one site, sensor
        and/or type.

        Parameters
        ----------
        sites : list
            This list is used to specify the sites for which we will search the bounds.
        sensor_types : list
            This list is used to specify sensor types used to recover in SolarDB.
        sensors : list
            This list is used to specify the sensors used to recover the bounds.

        Returns
        -------
            A dictionary containing the bounds per site and sensor structured as follows:
            {
                site{
                    sensor{
                        start:  "..."
                        stop:   "..."
                    }
                }
            }

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        bounds = None
        query = self.__baseURL + "data/json/bounds"
        args = ""
        if sites is not None:
            args += "&site=" + ','.join(sites)
        if sensor_types is not None:
            args += "&type=" + ','.join(sensor_types)
        if sensors is not None:
            args += "&sensorid=" + ','.join(sensors)
        if args != "":
            query += "?" + args

        try:
            res = requests.get(query, cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            bounds = json.loads(res.content)["data"]
            if bounds:
                self.logger.debug("Bounds successfully recovered")
            else:
                self.logger.info("The bounds defined by this request are null")
            return bounds
        except requests.exceptions.HTTPError:
            self.logger.warning("getBounds -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getBounds -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getBounds -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getBounds -> Request Error:\n%s\n", err)

    ## Methods to recover the metadata ----------------------------------------------------

    def getCampaigns(
            self,
            ids: str = None,
            name: str = None,
            territory: str = None,
            alias: str = None
    ):
        """
        Extracts the different campaigns that took place during the IOS-Net project.
        Specifying the campaign id, name, territory and/or alias will narrow down the
        campaigns recovered.

        Parameters
        ----------
        ids : str (OPTIONAL)
            This string is the identity key. It corresponds to the '_id' field in the Mongo
            'campaigns' collection.
        name : str (OPTIONAL)
            This corresponds to the station official name and is associated to the 'name'
            field in the Mongo 'campaigns' collection.
        territory : str (OPTIONAL)
            This string represents the territory name and is associated to the 'territory'
            field in the Mongo 'campaigns' collection.
        alias : str (OPTIONAL)
            This string is the site practical name (which is used for data extraction) and
            is associated to the 'alias' field in the Mongo 'campaigns' collection.

        Returns
        -------
            A dictionary containing the campaigns' metadata.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        campaigns = None
        query = self.__baseURL + "metadata/campaigns"
        args = ""
        if ids is not None:
            args += "&id=" + ids
        if name is not None:
            args += "&name=" + name
        if territory is not None:
            args += "&territory=" + territory
        if alias is not None:
            args += "&alias=" + alias
        if args != "":
            query += "?" + args

        try:
            res = requests.get(query, cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            campaigns = json.loads(res.content)["data"]
            if campaigns:
                self.logger.debug("Campaign metadata successfully recovered")
            else:
                self.logger.info("The campaigns defined by this request do not exist")
            return campaigns
        except requests.exceptions.HTTPError:
            self.logger.warning("getCampaigns -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getCampaigns -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getCampaigns -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getCampaigns -> Request Error:\n%s\n", err)

    def getInstruments(
            self,
            ids: str = None,
            name: str = None,
            label: str = None,
            serial: str = None
    ):
        """
        Returns the different instruments used in the IOS-Net project. Specifying the id,
        name, label and/or serial number will narrow down the instruments recovered.

        Parameters
        ----------
        ids : str (OPTIONAL)
            This string is the identity key. It corresponds to the '_id' field in the Mongo
            'instruments' collection.
        name : str (OPTIONAL)
            This corresponds to the station official name and is associated to the 'name'
            field in the Mongo 'instruments' collection.
        label : str (OPTIONAL)
            This string represents the instrument's label and is associated to the 'label'
            field in the Mongo 'instruments' collection.
        serial : str (OPTIONAL)
            This string is the instrument's serial number and is associated to the 'serial'
            field in the Mongo 'instruments' collection.

        Returns
        -------
            A dictionary containing the instruments' metadata.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        instruments = None
        query = self.__baseURL + "metadata/instruments"
        args = ""
        if ids is not None:
            args += "&id=" + ids
        if name is not None:
            args += "&name=" + name
        if label is not None:
            args += "&label=" + label
        if serial is not None:
            args += "&serial=" + serial
        if args != "":
            query += "?" + args

        try:
            res = requests.get(query, cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            instruments = json.loads(res.content)["data"]
            if instruments:
                self.logger.debug("Instrument metadata successfully recovered")
            else:
                self.logger.info("The intstruments defined by this request do not exist")
            return instruments
        except requests.exceptions.HTTPError:
            self.logger.warning("getInstruments -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getInstruments -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getInstruments -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getInstruments -> Request Error:\n%s\n", err)

    def getMeasures(
            self,
            ids: str = None,
            names: list = None,
            measure_type: str = None,
            nested: bool = None
    ):
        """
        Extracts the different measure types used in the IOS-Net project. Specifying the id,
        name and/or data type will narrow down the measures recovered.

        Parameters
        ----------
        ids : str (OPTIONAL)
            This string is the identity key. It corresponds to the '_id' field in the Mongo
            'measures' collection.
        names : list (OPTIONAL)
            This corresponds to the sensor/s name/s and is associated to the 'name' field
            in the Mongo 'measures' collection.
        measure_type : list (OPTIONAL)
            This string represents the data type and is associated to the 'type' field in the
            Mongo 'measures' collection.
        nested : bool (OPTIONAL)
            This boolean, which is false by default, indicates whether the user wants to recieve
            all the metadata or only key metadata information associated to the measures.

        Returns
        -------
            A dictionary containing the measures' metadata

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        measures = None
        query = self.__baseURL + "metadata/measures"
        args = ""
        if ids is not None:
            args += "&id=" + ids
        if names is not None:
            args += "&name=" + ','.join(names)
        if measure_type is not None:
            args += "&type=" + measure_type
        if nested is not None:
            args += "&nested=" + str(nested)
        if args != "":
            query += "?" + args

        try:
            res = requests.get(query, cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            measures = json.loads(res.content)["data"]
            if measures:
                self.logger.debug("Measure metadata successfully recovered")
            else:
                self.logger.info("The measures defined by this request do not exist")
            return measures
        except requests.exceptions.HTTPError:
            self.logger.warning("getMeasures -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getMeasures -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getMeasures -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getMeasures -> Request Error:\n%s\n", err)

    def getModels(
            self,
            ids: str = None,
            name: str = None,
            model_type: str = None
    ):
        """
        Returns the models used in the IOS-Net project. Specifying the id, name and/or data
        type will narrow down the models recovered.

        Parameters
        ----------
        ids : str (OPTIONAL)
            This string is the identity key. It corresponds to the '_id' field in the Mongo
            'models' collection.
        name : str (OPTIONAL)
            This corresponds to the station official name and is associated to the 'name'
            field in the Mongo 'models' collection.
        model_type : str (OPTIONAL)
            This string represents the data type and is associated to the 'type' field in
            the Mongo 'models' collection.

        Returns
        -------
            A dictionary containing the models' metadata.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """

        models = None
        query = self.__baseURL + "metadata/models"
        args = ""
        if ids is not None:
            args += "&id=" + ids
        if name is not None:
            args += "&name=" + name
        if model_type is not None:
            args += "&type=" + model_type
        if args != "":
            query += "?" + args

        try:
            res = requests.get(query, cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            models = json.loads(res.content)["data"]
            if models:
                self.logger.debug("Models metadata successfully recovered")
            else:
                self.logger.info("The measures defined by this request do not exist")
            return models
        except requests.exceptions.HTTPError:
            self.logger.warning("getModels -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getModels -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getModels -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getModels -> Request Error:\n%s\n", err)

    ## Utils

    def getSiteDataframe(self, site: str, sensor_types: list = None, start: str = None, stop: str = None):
        """
        Extracts a CSV file containing the data associated to a site and converts it into
        a pandas dataframe object. The user can choose the time period on which the extraction
        is set (set on the last 24h by default).

        Parameters
        ----------
        site : str
            This string is used to specify the site chosen by the user.
        start : str (OPTIONAL)
            This string specifies the starting date for the data recovery. It either follows
            a date format, an RFC3339 date format, or a duration unit respecting the '[N][T]'
            format, where [N] is an integer and [T] is one of the following strings:
            * 'y'   : year
            * 'mo'  : month
            * 'w'   : week
            * 'd'   : day
            * 'h'   : hour
            * 'm'   : minute
            Example: '-24d' == 24 days ago
        stop : str (OPTIONAL)
            This string specifies the ending date for the data recovery. It follows the same
            format as "start".
        sensor_types : list
            This list is used to specify sensor types to recover in SolarDB.

        Returns
        -------
            A Pandas dataframe containing the data for each sensor of the site on the requested
            time period.

        Raises
        ------
        HTTPError
            If the responded HTTP Status is between 400 and 600 (i.e if there is a problem
            with the request or the server)
        ConnectionError
            If the program is unable to connect to SolarDB
        TimeOutError
            If the SolarDB response is too slow
        RequestException
            In case an error that is unaccounted for happens
        """
        query = self.__baseURL + "data/csv/" + site
        args = ""
        if start is not None:
            args += "&start=" + start
        if stop is not None:
            args += "&stop=" + stop
        if sensor_types is not None:
            args += "&type=" + ','.join(sensor_types)
        if args != "":
            query += "?" + args
        try:
            res = requests.get(query, cookies=self.__cookies, verify=self.__verify)
            res.raise_for_status()
            try:
                df = pd.read_csv(StringIO(res.text))
                self.logger.debug("pandas dataframe succesfully extracted")
                return df
            except pd.errors.EmptyDataError:
                self.logger.warning("There is no data for the given parameters. Please change your request.")
                return None
        except requests.exceptions.HTTPError:
            self.logger.warning("getData -> HTTP Error:\n%s\n", json.loads(res.content)["message"])
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("getData -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("getData -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("getData -> Request Error:\n%s\n", err)

    def setLoggerLevel(self, val: int):
        """
        Changes the logging level. It is used to enable and/or disable the messages.
        
        Parameters
        ----------
        val : str
            This integer represents the logging level as follows:
            - 0  : NOTSET
            - 10 (or logging.DEBUG)     : DEBUG
            - 20 (or logging.INFO)      : INFO
            - 30 (or logging.WARN)      : WARNING
            - 40 (or logging.ERROR)     : ERROR
            - 50 (ot logging.CRITICAL)  : CRITICAL
            The levels allow all the logging levels with a higher severity to appear
            (e.g a logging.INFO level will disable all messages marked with logging.DEBUG).
            If val is set to 0/logging.NOTSET, the logging level will be set to the root level,
            which is WARNING.
        """
        # remove all handlers
        while self.logger.hasHandlers():
            self.logger.removeHandler(self.logger.handlers[0])
        self.logger.setLevel(val)
        __ch = logging.StreamHandler()
        __ch.setLevel(val)
        self.logger.addHandler(__ch)

    def checkIfOutdated(self):
        """
        Checks if the current version of this package is the latest.
        """
        try:
            is_outdated, latest_version = outdated.check_outdated("pysolardb", sample.__version__)
            if is_outdated:
                self.logger.warning("A newer version (Version %s) of the pysolardb package is available on Pypi", latest_version)
        except ValueError as errv:
            self.logger.warning("Versionning error\n%s\n", errv)
        except requests.exceptions.HTTPError as errh:
            self.logger.warning("checkIfOutdated -> HTTP Error:\n%s\n", errh)
        except requests.exceptions.ConnectionError as errc:
            self.logger.warning("checkIfOutdated -> Connection Error:\n%s\n", errc)
        except requests.exceptions.Timeout as errt:
            self.logger.warning("checkIfOutdated -> Timeout Error:\n%s\n", errt)
        except requests.exceptions.RequestException as err:
            self.logger.warning("checkIfOutdated -> Request Error:\n%s\n", err)
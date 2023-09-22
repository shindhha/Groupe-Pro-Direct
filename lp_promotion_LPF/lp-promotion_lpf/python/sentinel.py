import configparser
import os
import requests
import pymssql
import psycopg2
import faulthandler
from hubspot import HubSpot
from hubspot.crm.contacts import PublicObjectSearchRequest, ApiException, ApiTypeError
from urllib3.exceptions import InsecureRequestWarning
import MySQLdb

hs_token = "pat-na1-48055e7d-c596-4917-bab8-8236ff3614c3"
hs_limite = 100
path = os.path.dirname(os.path.realpath(__file__))
configdir = '/'.join([path, 'config.cfg'])
config = configparser.ConfigParser()
if not config.read(configdir):
    print(f"Reading from File: {configdir} seems to return and empty object")
else:
    config.read(configdir)


faulthandler.enable()


def get_leads():
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
    api_client = HubSpot()
    api_client.access_token = hs_token

    id_hubspots = dict()
    hubspot_ids = []

    try:
        hs_after = 0
        while 1 == 1:
            public_object_search_request = PublicObjectSearchRequest(
                filter_groups=[{"filters": [{"value": "150071982", "propertyName": "hubspot_owner_id", "operator": "EQ"}]}],
                properties=["id_hubspot", "createdate"],
                limit=hs_limite,
                after=hs_after,
                sorts=["hubspot_owner_id"])

            api_response = api_client.crm.contacts.search_api.do_search(
                public_object_search_request=public_object_search_request)

            if len(api_response.results) == 0:
                print("arrêt")
                break

            for lead in api_response.results:
                properties = lead.properties

                id_hubspot = properties.get("hs_object_id")
                hubspot_created_at = properties.get("createdate")

                id_hubspots[id_hubspot] = hubspot_created_at
                hubspot_ids.append(id_hubspot)

            if api_response.paging is not None:
                hs_after = api_response.paging.next.after
            else:
                break

        return [id_hubspots, hubspot_ids]

    except ApiException as e:
        print("Exception when requesting contacts. %s\n" % e)
        return []
    except ApiTypeError as e:
        print("Exception when requesting contacts. %s\n" % e)
        return []
    except Exception as e:
        print("Exception when requesting contacts. %s\n" % e)
        return []


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    leads = get_leads()
    leads_hermes = []

    print(leads)
    # exit()

    sql = """
        SELECT hubspotId FROM VIVETIC_PROD.dbo.LP_PROMOTION_HUBSPOT x
WHERE hubspotId IN ({})
    """.format(', '.join(leads[1]))

    print(sql)

    conn = pymssql.connect('5.196.127.163', 'read_write', '0wY!3M8cQ#Kw', 'VIVETIC_PROD')
    cur = conn.cursor()
    cur.execute(sql)
    leads_hermes_list = cur.fetchall()
    conn.close()

    for lead in leads_hermes_list:
        leads_hermes.append(lead[0])

    diff = list(set(leads[1]) - set(leads_hermes))
    print(diff)

    conn2 = psycopg2.connect("host={} dbname={} user={} password={}".format(*config['TRACE'].values()))
    cur2 = conn2.cursor()

    for dif in diff:
        sql_trace = """
            INSERT INTO public.hubspot_inconnu_hermes (id_hubspot, date_creation_hubspot) 
            VALUES('{}', '{}') 
            ON CONFLICT (id_hubspot) DO NOTHING;
        """.format(dif, leads[0][dif])
        try:
            cur2.execute(sql_trace)
        except Exception as e:
            print(e)

    conn2.commit()
    conn2.close()

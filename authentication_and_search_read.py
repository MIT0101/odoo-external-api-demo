# https://www.odoo.com/documentation/16.0/developer/reference/external_api.html
import xmlrpc.client

# # online hrins Dev
# url = 'https://odoodev.hrins.net'
# db = 'HRiNS-Dev'
# username = 'admin'
# my_api_key = 'aF^_{s6mmWl.WHVH'

url = 'http://localhost:8070'
db = 'odoo-16-db'
username = 'admin'
# password = 'admin'
my_api_key = '332031b56386f219eea45687ff1df8b5fad9d49b'


common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
version_info = common.version()
print("Version Info : ", version_info)

# authenticate using username and password to get uid (user id )
# uid = common.authenticate(db, username, password, {})
# authentication using api key
uid = common.authenticate(db, username, my_api_key, {})

if uid:
    print(f"Authentication Successfully UID : {uid}")
else:
    print("Authentication Failed")

# search and read
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
# check if we have permission to read partner
can_access_read_partner = models.execute_kw(db, uid, my_api_key, 'res.partner', 'check_access_rights', ['read'],
                                            {'raise_exception': False})
if can_access_read_partner:
    # all partner with is_company
    # specify the db and uid and password or api-key then model name and method then params and options as dictionary
    partner_company_ids = models.execute_kw(db, uid, my_api_key, 'res.partner', 'search', [[['is_company', '=', True]]])

    partner_company_count = models.execute_kw(db, uid, my_api_key, 'res.partner', 'search_count',
                                              [[['is_company', '=', True]]])

    partner_company_pagination_ids = models.execute_kw(db, uid, my_api_key, 'res.partner', 'search',
                                                       [[['is_company', '=', True]]], {'offset': 1, "limit": 5})

    partner_email_ids = models.execute_kw(db, uid, my_api_key, 'res.partner', 'search',
                                          [[["email", "=", "colleen.diaz83@example.com"]]])

    partner_company_search_read_recs = models.execute_kw(db, uid, my_api_key, "res.partner", "search_read",
                                                         [[['is_company', '=', True]]],
                                                         {"fields": ["id", "name"], "limit": 5})

    print("Partners Company Ids : ", partner_company_ids)
    print("Partners Company Count : ", partner_company_count)
    print("Partners Company Pagination (offset 1 & limit 5) Ids : ", partner_company_pagination_ids)
    print("Partners Company Pagination (search_read) (limit 5) (fields id ,name ) : ", partner_company_search_read_recs)
    print("Partners Email Ids : ", partner_email_ids)
    print("--------------")
    # get records values
    # this will get all fields of partner model
    # partner_recs = models.execute_kw(db, uid, password, 'res.partner', 'read', [partner_company_ids])
    # print("Partners Company : ", partner_recs)
    # get specific fields (id , name , company id)
    partner_sp_fields_recs = models.execute_kw(db, uid, my_api_key, 'res.partner', 'read', [partner_company_ids], {
        "fields": ["id", "name", "country_id"]
    })

    print("Partners Company (Specific Fields) : ", partner_sp_fields_recs)


else:
    print("Can't Access Partner")

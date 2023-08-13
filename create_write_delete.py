import xmlrpc.client

url = 'http://localhost:8070'
db = 'odoo-16-db'
username = 'admin'
my_api_key = '332031b56386f219eea45687ff1df8b5fad9d49b'

common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
version_info = common.version()
print("Version Info : ", version_info)
# authentication using api key
uid = common.authenticate(db, username, my_api_key, {})

if uid:
    print(f"Authentication Successfully UID : {uid}")
else:
    print("Authentication Failed")

# create , write and delete
models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
# check if we have permission to read partner
can_access_read_partner = models.execute_kw(db, uid, my_api_key, 'res.partner', 'check_access_rights', ['read'],
                                            {'raise_exception': False})
if can_access_read_partner:

    #######################--------- CREATE --------#################################
    # create new record
    new_partner_data = {
        "name": "Mohammed From External"
    }
    exist_partner_ids = models.execute_kw(db, uid, my_api_key, "res.partner", "search",
                                          [[["name", "=", new_partner_data["name"]]]])

    if not exist_partner_ids:
        created_id = models.execute_kw(db, uid, my_api_key, "res.partner", "create", [new_partner_data])
        exist_partner_ids = created_id
        print(f"Created Id : {created_id}")
    else:
        print(f"Partner Already Created : {exist_partner_ids}")

    #######################--------- UPDATE (write) --------#################################

    # update records based on id return Boolean
    # take array with two items first list of ids and then dictionary of values
    to_update_id = 68
    update_result = models.execute_kw(db, uid, my_api_key, "res.partner", "write",
                                      [[to_update_id], {"phone": "1010123"}])
    print("Update Result : ", update_result)
    #######################--------- DELETE --------#################################
    # can be got using search
    to_delete_id = 69
    try:
        # return boolean
        # if not exists Error will be thrown
        delete_result = models.execute_kw(db, uid, my_api_key, 'res.partner', 'unlink', [[to_delete_id]])
        print("Delete Result : ", delete_result)

    except:

        print(f"Error when Deleting item with id ({to_delete_id}) , It May be not exist or already deleted ")

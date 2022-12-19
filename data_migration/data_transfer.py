import xmlrpc.client
from xmlrpc import client


url_db1 = "http://localhost:8015"
db_1 = 'odoo15'
username_db_1 = 'dazzildavid@gmail.com'
password_db_1 = 'admin'
common_1 = client.ServerProxy('{}/xmlrpc/2/common'.format(url_db1))
models_1 = client.ServerProxy('{}/xmlrpc/2/object'.format(url_db1))
version_db1 = common_1.version()

url_db2 = "http://cybrosys-thinkpad-e15-gen-2:8069"
db_2 = 'odoo16_1'
username_db_2 = '1'
password_db_2 = '1'
common_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url_db2))
models_2 = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url_db2))
version_db2 = common_2.version()

uid_db1 = common_1.authenticate(db_1, username_db_1, password_db_1, {})
uid_db2 = common_2.authenticate(db_2, username_db_2, password_db_2, {})
print("rdk78754rfgb")

db_1_cust = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [[]],
                                {'fields': ['id', 'name', 'type', 'email']})
field_id16 = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search_read', [[]])
field_id15 = models_1.execute_kw(db_1, uid_db1, password_db_1, 'res.partner', 'search_read', [[]], {'fields': ['id']})

model_crm = models_2.execute_kw(db_2, uid_db2, password_db_2, 'ir.model', 'search_read',
                                [[['model', '=', 'res.partner']]], {'fields': ['id']})
a = model_crm[0]['id']
# local = models_2.execute_kw(db_2, uid_db2, password_db_2, 'ir.model.fields', 'create',
#                             [{
#                                 'name': 'x_main_id',
#                                 'model_id': model_crm[0]['id'],
#                                 'model': 'res_partner',
#                                 'ttype': 'integer',
#                                 'store': True,
#                             }])
for rec in db_1_cust:
    field_ids = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'search_read', [[['x_main_id', '=', rec['id']]]], {'fields': ['id']})
    if not field_ids:
        db_2_cust = models_2.execute_kw(db_2, uid_db2, password_db_2, 'res.partner', 'create', [{
                        'name': rec['name'],
                        'type': rec['type'],
                        'email': rec['email'],
                        'x_main_id': rec['id']
                    }])
        print(234567890, field_ids)

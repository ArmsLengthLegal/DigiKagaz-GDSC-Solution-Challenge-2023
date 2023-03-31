from docassemble.webapp import db_object
import psycopg2

__all__ = ['update', 'fetch', 'add', 'add_multiple', 'delete', 'add_cases', 'fetch_client_by_case', 'fetch_case_cnr_details', 'raw_query']

table_columns = {
  'case_details' : ['id', 'cnr', 'updated_title', 'updated_petitioner', 'updated_respondent', 'updated_clients', 'representing', 'approved', 'adv_id', 'misc'],
  'cnr_details': ['cnr', 'reg_no', 'case_type', 'petitioner', 'respondent', 'party', 'next_heading_date', 'case_stage', 'acts_and_sections', 'fir_no', 'fir_station', 'fir_year', 'court_complex', 'court_name', 'court_name_hi', 'active', 'petitioner_advocates', 'respondent_advocates', 'filing_date', 'updated_at'],
  'client_details': ['id', 'name', 'name_hi', 'father_name', 'father_name_hi', 'caste', 'caste_hi', 'age', 'mobile', 'email', 'address', 'auth_rep', 'adv_id', 'address_hi'],
  'client_case_map': ['client_id', 'case_id'],
  'case_cnr_details': ['id', 'cnr ', 'updated_title', 'updated_petitioner', 'updated_respondent', 'updated_clients', 'representing', 'approved', 'adv_id', 'misc', 'cnr ', 'reg_no', 'case_type', 'petitioner', 'respondent', 'party', 'next_heading_date', 'case_stage', 'acts_and_sections', 'fir_no', 'fir_station', 'fir_year', 'court_complex', 'court_name', 'court_name_hi', 'active', 'petitioner_advocates', 'respondent_advocates', 'filing_date', 'updated_at']
}

def convert_arr_to_dict(table, data, cols=None):
  arr = []
  for x in data:
    dic = {}
    for i in range(len(x)):
      if cols:
        dic[cols[i]] = x[i]
      else:
        dic[table_columns[table][i]] = x[i]
    arr.append(dic)
  return arr

def update(table_name, dic, where):
    try:
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        bs = "'" #backslash not allowed in f'string
        cur.execute(f'UPDATE {table_name} SET {",".join([f"{x[0]}={bs}{x[1]}{bs}" for x in dic.items()])} WHERE {where};')
        connection.commit()
        cur.close()
        return True, 'OK'
    except Exception as err:
        return False, err

def fetch(table_name,columns = [], where = ""):
    try:
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        cur.execute(f'SELECT {",".join(columns) if len(columns) else "*"} FROM {table_name} {"WHERE " + where if where else ""};')
        rows = cur.fetchall()
        cur.close()
        if len(columns):
          return True, convert_arr_to_dict(table_name, rows, columns)
        elif table_name in table_columns:
          return True, convert_arr_to_dict(table_name, rows)
        return True, rows
    except Exception as err:
        return False, err

def fetch_case_cnr_details(adv_id, cnr=None, columns = [], where=None):
    try:
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        bs = "'" #backslash not allowed in f'string
        cur.execute(f"select {','.join(columns) if len(columns) else '*'} from case_details left join cnr_details on case_details.cnr = cnr_details.cnr where {f'case_details.cnr = {bs}{cnr}{bs} and ' if cnr else ''}adv_id = '{adv_id}' {' and '+where if where else ''};")
        rows = cur.fetchall()
        cur.close()
        if len(columns):
            return True , convert_arr_to_dict('case_cnr_details', rows, columns)
        return True, convert_arr_to_dict('case_cnr_details', rows)
    except Exception as err:
        return False, err
      
def fetch_client_by_case(case_id):
    try:
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        cur.execute(f"select client_details.* from client_details inner join client_case_map on client_details.id = client_id where case_id = {case_id};")
        rows = cur.fetchall()
        cur.close()
        return True, convert_arr_to_dict('client_details', rows)
    except Exception as err:
        return False, err

def add(table_name, dic, return_val=None):
    try:
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        bs = "'" #backslash not allowed in f'string
        cur.execute(f'INSERT INTO {table_name} ({",".join(dic.keys())}) VALUES ({",".join([bs+str(x)+bs for x in dic.values()])}) {"returning "+return_val if return_val else ""};')
        if return_val:
          rows = cur.fetchall()
        connection.commit()
        cur.close()
        if return_val:
          return True, rows[0]
        else:
          return True, "OK"
    except Exception as err:
        return False, err

def add_multiple(table_name, arr, return_val=None):
    try:
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        bs = "'" #backslash not allowed in f'string
        cur.execute(f'INSERT INTO {table_name} ({",".join(arr[0].keys())}) VALUES ({ "),(".join( [ ",".join([bs+str(x)+bs  for x in dic.values()])  for dic in arr])}) ON CONFLICT DO NOTHING {"returning "+return_val if return_val else ""};')
        rows = cur.fetchall()
        connection.commit()
        cur.close()
        return True, rows
    except Exception as err:
        return False, err
      
def delete(table_name, where):
    try:
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        cur.execute(f'DELETE FROM {table_name} WHERE {where};')
        connection.commit()
        cur.close()
        return True, 'OK'
    except Exception as err:
        return False, err
      
def raw_query(query, isRead = False):
    try:
        resp = "OK"
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        cur.execute(query)
        if isRead:
          resp = cur.fetchall()
        else:
          connection.commit()
        cur.close()
        return True, resp
    except Exception as err:
        return False, err
      

def add_cases(arr, adv_id):
    try:
        connection = db_object.db.engine.raw_connection()
        cur = connection.cursor()
        bs = "'" #backslash not allowed in f'string
        cur.execute(f'INSERT INTO case_details ({",".join(arr[0].keys())}) VALUES ({ "),(".join( [ ",".join([bs+str(x)+bs  for x in dic.values()])  for dic in arr])}) ON CONFLICT DO NOTHING returning id;')
        rows = cur.fetchall()
        if len(rows):
          cur.execute(f'INSERT INTO adv_case_map (adv_id, case_id) VALUES ({ "),(".join( [f"{adv_id},{x[0]}" for x in rows])});')
        connection.commit()
        cur.close()
        return True, 'OK'
    except Exception as err:
        return False, err
equipment_data = {"name":"Dell Desktop", "serial_number":"DT40055","product_template_id":25}
print("before", equipment_data)
equipment_data['template_id'] = equipment_data.pop('product_template_id')
print("after",equipment_data)

list_num = [4,23,5,1,17,2,6,9,7]
print("Original", list_num)
print("Ascending Order", sorted(list_num))
print("Descending Order", sorted(list_num, reverse=True))

############################## SQL ###############################
import psycopg2
from tabulate import tabulate

def run_sql_query(query, db_config):
    """
    Execute an SQL query and print the result as a table.

    Parameters:
        query (str): The SQL query to execute.
        db_config (dict): Dictionary with DB connection details.
    """
    conn = None
    cursor = None
    try:
        conn = psycopg2.connect(**db_config)
        cursor = conn.cursor()

        cursor.execute(query)

        if cursor.description:
            rows = cursor.fetchall()

           # Get column names dynamically
            headers = [desc[0] for desc in cursor.description]

            # Print formatted result
            print(tabulate(rows, headers=headers, tablefmt='psql'))
        else:
            conn.commit()
            print(f"Query executed successfully. Rows affected: {cursor.rowcount}")
        
    except Exception as e:
        print("Error:", e)

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

###############################################################

db_config = {
    'dbname': 'web_learns',
    'user': 'tarek-ashry',
    'password': ' ',
    'host': 'localhost',
    'port': 5432
}

# sq l= """
#     SELECT name,
#         email,
#         phone
#         FROM res_partner
#         Where supplier_rank > 0 and active = True;
# """
# ---------------------------------------------------
# sql = """
#     SELECT rp.name,
#         po.name as purchase_order_reference,
#         po.amount_total,
#         po.date_order
#         From purchase_order po 
#         JOIN res_partner rp ON po.partner_id = rp.id
#         WHERE po.date_order >= (CURRENT_DATE - INTERVAL '30 days')
#         ORDER BY po.date_order DESC;
# """
# ------------------------------------------------------
# sql = """
# SELECT
#     pt.name,
#     pt.default_code,
#     COALESCE(SUM(sol.product_uom_qty), 0) AS total_qty_sold
#     FROM product_product pp
#     JOIN product_template pt ON pp.product_tmpl_id = pt.id
#     LEFT JOIN sale_order_line sol ON sol.product_id = pp.id
#     LEFT JOIN sale_order so ON so.id = sol.order_id AND so.state IN ('sale', 'done')
#     GROUP BY pt.name, pt.default_code
#     ORDER BY total_qty_sold DESC
#     LIMIT 5;
# """
# -------------------------------------------------------
# sql = """
#     SELECT  rp.name as Customer_name,
#         count(so.id) as Order_count 
#         FROM res_partner rp
#         JOIN sale_order so ON so.partner_id = rp.id 
#         WHERE so.amount_total > (SELECT avg(amount_total) FROM sale_order WHERE state = 'sale') and so.state = 'sale'
#         GROUP BY Customer_name 
#         ORDER BY Order_count DESC;
# """
# -------------------------------------------------------
# sql = """
#     SELECT 
#         count(id)
#         FROM purchase_order
#         WHERE state = 'draft' AND date_order < (CURRENT_DATE - INTERVAL '3 days');
# """
sql = """
    UPDATE purchase_order 
        SET state = 'cancel'
        WHERE state = 'draft' AND date_order < (CURRENT_DATE - INTERVAL '3 days');
"""

run_sql_query(sql,db_config)
#!/usr/bin/python3
from mysql.connector import connect, Error
from datetime import datetime
from decimal import Decimal


def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
    except Error as e:
        pass
    return connection

def close_connection(connection):
    if connection:
        connection.close()

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        pass

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        pass

def get_current_debt(user):
    debt_db_conn = create_connection(
        host_name="localhost",
        user_name="root",
        user_password="",
        db_name="debt_db"
    )
    debt_query = f"SELECT * FROM debts WHERE user_id = {user}"
    exec = execute_read_query(debt_db_conn, debt_query)
    if len(exec) == 0:
        return None
    close_connection(debt_db_conn)
    return exec[0][2:]


def get_user_data_helper(user):
    user_db_conn = create_connection(
        host_name="localhost",
        user_name="root",
        user_password="",
        db_name="user_db"
    )
    user_query = f"SELECT * FROM users WHERE user_id = {user}"
    exec = execute_read_query(user_db_conn, user_query)
    if len(exec) == 0:
        return {"error": "User not found"}
    iscore_var = iscore(user)
    last_payment_var = last_payment(user)
    get_current_debt_var = get_current_debt(user)

    close_connection(user_db_conn)

    return {"user_data": exec[0],"iscore": iscore_var, "last_payment": last_payment_var, "current_debt": get_current_debt_var}

def iscore(user):
    paymentScore = float(paymentScore_fn(user)).__round__(3)
    debtScore = float(debtScore_fn(user)).__round__(3)
    historyScore = float(historyScore_fn(user)).__round__(3)
    mixScore = float(mixScore_fn(user)).__round__(3)
    return {
        "paymentScore": paymentScore,
        "debtScore": debtScore,
        "historyScore": historyScore,
        "mixScore": mixScore,
        "iscore": (0.35 * paymentScore + 0.30 * debtScore + 0.15 * historyScore + 0.20 * mixScore).__round__(3)
    }    

def paymentScore_fn(user):
    payment_db_conn = create_connection(
        host_name="localhost",
        user_name="root",
        user_password="",
        db_name="payments_db"
    )
    payment_query = f"SELECT * FROM payments WHERE user_id = {user}"
    exec = execute_read_query(payment_db_conn, payment_query)
    den = len(exec)
    if den == 0:
        return 0.0
    nom = 0
    for i in exec:
        if i[-1] == "completed":
            nom += 1
    close_connection(payment_db_conn)
    return nom/den

def debtScore_fn(user):
    exec = get_current_debt(user)
    if exec is None:
        return 0
    return exec[0] / exec[1]

def historyScore_fn(user):
    history_db_conn = create_connection(
        host_name="localhost",
        user_name="root",
        user_password="",
        db_name="history_db"
    )
    history_query = f"SELECT * FROM histories WHERE user_id = {user}"
    exec = execute_read_query(history_db_conn, history_query)
    if len(exec) == 0:
        return 0
    close_connection(history_db_conn)
    return (datetime.today().year - exec[0][2].year)/10

def mixScore_fn(user):
    mixscore_db_conn = create_connection(
        host_name="localhost",
        user_name="root",
        user_password="",
        db_name="mix_reference_db"
    )
    mixscore_query = f"SELECT * FROM credit_references WHERE user_id = {user}"
    exec = execute_read_query(mixscore_db_conn, mixscore_query)
    close_connection(mixscore_db_conn)
    return len(exec)/5

def last_payment(user):
    payment_db_conn = create_connection(
        host_name="localhost",
        user_name="root",
        user_password="",
        db_name="payments_db"
    )
    payment_query = f"select * from payments where user_id = {user} order by payment_date desc"
    exec = execute_read_query(payment_db_conn, payment_query)
    if len(exec) == 0:
        return None
    close_connection(payment_db_conn)
    return exec[0][2:]


if __name__ == "__main__":
    # Example usage
    user_id = 1  # Replace with the actual user ID you want to test
    # print("Payment Score:", paymentScore_fn(user_id))
    # print("Debt Score:", debtScore_fn(user_id))
    # print("History Score:", historyScore_fn(user_id))
    # print("Mix Score:", mixScore_fn(user_id))
    # print("Iscore:", iscore(user_id))
    # print("Last Payment:", last_payment(user_id))
    print("User Data:", get_user_data_helper(user_id))
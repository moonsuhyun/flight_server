import sqlite3
import random
import string
import models.Notification


class Reservation:
    def __init__(self, id, name, dept_flight, dept_date):
        self.dept_date = dept_date
        self.dept_flight = dept_flight
        self.name = name
        self.id = id


def get_reservation_id():
    connect = sqlite3.connect('flight.sqlite')
    cursor = connect.cursor()
    id = ""
    while 1:
        for i in range(6):
            id += str(random.choice(string.ascii_uppercase + string.digits))
        cursor.execute(f"select * from reservation where id='{id}'")
        rows = cursor.fetchall()
        if len(rows) == 0:
            break
    connect.close()
    return id


def make_reservation(reservation: Reservation, phone):
    connect = sqlite3.connect('flight.sqlite')
    cursor = connect.cursor()
    cursor.execute(f"""
        insert into reservation(id, name, dept_flight, dept_date)
        values ('{reservation.id}', '{reservation.name}', '{reservation.dept_flight}', '{reservation.dept_date}') 
    """)
    connect.commit()
    connect.close()

    sms_data = f"{reservation.name}님,\n항공권 {reservation.dept_flight}편이 예약 되었습니다.\n예약 번호: {reservation.id}"
    models.Notification.send_sms(phone, sms_data)


def get_reservation(id):
    connect = sqlite3.connect('flight.sqlite')
    cursor = connect.cursor()
    cursor.execute(f"select * from reservation where id='{id}'")
    rows = cursor.fetchall()
    connect.close()
    if len(rows) == 0:
        return None
    reservation = Reservation(
        id=rows[0][0],
        name=rows[0][1],
        dept_flight=rows[0][2],
        dept_date=rows[0][3]
    )
    return reservation

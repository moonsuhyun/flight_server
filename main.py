#
# INHA TECHNICAL COLLAGE
# DEPARTMENT OF COMPUTER SCIENCE
# 2022-1 TCP/IP FINAL TEST
# 3-A 201844012 문수현
# MOON@ITC.AC.KR
#
# FLIGHT_SERVER
# DEVELOPMENT ENVIRONMENT
# OS: APPLE MAC OS 12.4
# IDE: JETBRAINS PYCHARM PROFESSIONAL 2022.1.2
# PYTHON 3.9.13
#
# DEPENDENCY:
# REQUESTS
#

from socket import *
import threading
import datetime

import models.Reservation
import models.FlightSchedule

port = 10001

server_socket = socket(AF_INET, SOCK_STREAM)
server_socket.bind(('', port))
server_socket.listen(5)

client_list = []
count = 0

mutex = threading.Lock()

def wait_for_answer(client_socket: socket):
    while True:
        data = client_socket.recv(1024)
        return data.decode()

def service(client_socket: socket, addr):
    print(f"thread {threading.get_ident()} start")
    try:
        while True:
            client_socket.send("[항공권 예약 시스템] Send /q to exit.\n1. 항공권 조회\n2. 예약 조회\nAnswer: ".encode())
            answer = wait_for_answer(client_socket)
            if answer == "1":
                client_socket.send("[항공권 조회] Send /q to exit.\n목적지 공항 Code (e.g., JFK, CDG, NRT, HKG ...):".encode())
                answer = wait_for_answer(client_socket).upper()

                if answer == "/q": break
                dest = answer

                client_socket.send(f"[항공권 조회] Send /q to exit.\n{answer}로 가시는 출발 일자 (e.g., 20220615):".encode())
                answer = wait_for_answer(client_socket)
                if answer == "/q": break

                schedule = datetime.datetime.strptime(answer, "%Y%m%d")
                schedule_date = answer
                day = schedule.weekday()
                flights = models.FlightSchedule.get_departure_schedule(dest)
                results = []
                if day == 0:
                    for flight in flights:
                        if flight.day.mon:
                            results.append(flight)
                elif day == 1:
                    for flight in flights:
                        if flight.day.tue:
                            results.append(flight)
                elif day == 2:
                    for flight in flights:
                        if flight.day.wed:
                            results.append(flight)
                elif day == 3:
                    for flight in flights:
                        if flight.day.thu:
                            results.append(flight)
                elif day == 4:
                    for flight in flights:
                        if flight.day.fri:
                            results.append(flight)
                elif day == 5:
                    for flight in flights:
                        if flight.day.sat:
                            results.append(flight)
                elif day == 6:
                    for flight in flights:
                        if flight.day.sun:
                            results.append(flight)
                client_socket.send(f"[항공권 조회] Send /q to exit.\nICN -> {dest} 출발 일자: {answer}\n".encode())
                for index, result in enumerate(results):
                    client_socket.send(f"[{index}] 항공사: {result.airline}, 편명: {result.flight}, 출발시간: {result.time}\n".encode())
                client_socket.send(f"예약할 항공편의 index를 입력해주세요 :".encode())
                answer = wait_for_answer(client_socket)
                if answer == "/q": break
                flight = results[int(answer)]
                client_socket.send(f"선택한 항공편: {flight.flight}\n".encode())
                client_socket.send("탑승객 이름을 입력해주세요: ".encode())

                answer = wait_for_answer(client_socket)
                if answer == "/q": break
                name = answer

                client_socket.send("탑승객 휴대전화 번호를 입력해주세요. (e.g., 01012345678): ".encode())

                answer = wait_for_answer(client_socket)
                if answer == "/q": break
                phone = answer

                mutex.acquire()
                print(f"Locked by {threading.get_ident()}")

                resv = models.Reservation.Reservation(
                    id=models.Reservation.get_reservation_id(),
                    name=name,
                    dept_date=schedule_date,
                    dept_flight=flight.flight
                )
                models.Reservation.make_reservation(resv, phone)
                mutex.release()
                print(f"UnLocked by {threading.get_ident()}")

                client_socket.send("예약되었습니다.\n".encode())


            elif answer == "2":
                client_socket.send("[예약 조회] Send /q to exit. 예약 번호:".encode())
                answer = wait_for_answer(client_socket)
                if answer == "/q": break
                resv = models.Reservation.get_reservation(answer.upper())
                if resv is None:
                    client_socket.send("해당 예약이 존재하지 않습니다.\n".encode())
                else:
                    client_socket.send(f"예약 번호: {resv.id} / 탑승객: {resv.name} / 편명: {resv.dept_flight} / 탑승일자: {resv.dept_date}\n".encode())

            elif answer == "\q":
                break

    finally:
        client_socket.close()
        print(f"thread {threading.get_ident()} finished")

while True:
    client_socket, addr = server_socket.accept()
    client_list.append(client_socket)
    receive_thread = threading.Thread(target=service, args=(client_socket, addr))
    receive_thread.start()


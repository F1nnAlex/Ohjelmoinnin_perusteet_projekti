import Functions
import GUI

def check_in():
    name = GUI.get_guest_name()
    phone = GUI.get_guest_phone()
    email = GUI.get_guest_email()
    room_type = GUI.get_room_type()
    Functions.assign_guest(name, phone, email, room_type)

def check_out():
    Functions.checkout_guest()
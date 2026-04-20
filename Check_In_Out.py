import Functions


def check_in(name,phone, email,room_type):
    assigned_data = Functions.assign_guest(name, phone, email, room_type)
    if assigned_data is not None:
        customer_id = assigned_data[0]
        room_number = assigned_data[1]
        return f"Success! ID:  {customer_id} | Room: {room_number} "
    else:
        return "Error"

def check_out(customer_id):
    success = Functions.checkout_guest(customer_id)
    if success:
        return "Successfully checked out!"
    else:
        return "Error: invalid customer ID"
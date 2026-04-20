import Functions

def fetch_guest_list_data(admin_key=None):
    """Hakee listan kaikista vieraista. Purkaa salauksen, jos admin_key on oikea."""
    raw_guests = Functions.get_all_active_guests()
    processed_list = []
    
    for g in raw_guests:
        # Tuplen rakenne: (id, name, phone_enc, email_enc, type, room)
        c_id, name, p_enc, e_enc, r_type, r_num = g
        
        if admin_key == Functions.DECRYPTION_KEY:
            # Käytetään Functions.py:n purkutoimintoa
            phone = Functions.decrypt_cipher(p_enc, admin_key)
            email = Functions.decrypt_cipher(e_enc, admin_key)
        else:
            # Oletuksena tiedot ovat piilotettu
            phone = "********"
            email = "********"
            
        processed_list.append((c_id, name, phone, email, r_type, r_num))
    
    return processed_list

# Pidetään vanha komentorivikäyttöliittymä erillään
if __name__ == "__main__":
    Functions.setup_database()
    Functions.list_active_guests()
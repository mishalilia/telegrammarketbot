from os import environ


token = environ["TOKEN"]
email = environ["EMAIL"]
password = environ["PASS"]

'''
firebase_account = {
    "type": environ["type"],
    "project_id": environ["project_id"],
    "private_key_id": environ["private_key_id"],
    "private_key": environ["private_key"],
    "client_email": environ["client_email"],
    "client_id": environ["client_id"],
    "auth_uri": environ["auth_uri"],
    "token_uri": environ["token_uri"],
    "auth_provider_x509_cert_url": environ["auth_provider_x509_cert_url"],
    "client_x509_cert_url": environ["client_x509_cert_url"]
}
'''

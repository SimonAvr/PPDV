from recorder import fetch_data

def init_patients():
        for i in range(1,6):
            r=fetch_data(i)
            requests.post(f'http://127.0.0.1:5000/be/patient/{i}',json=r)
init_patients()

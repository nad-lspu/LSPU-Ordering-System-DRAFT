import pyrebase

firebaseConfig = {
    "apiKey": "AIzaSyC6WJzNijzPO8Bmg4mWEb_MIoJioj7xtJc",
    "authDomain": "grab-piyu-d.firebaseapp.com",
    "databaseURL": "https://grab-piyu-d-default-rtdb.asia-southeast1.firebasedatabase.app",
    "projectId": "grab-piyu-d",
    "storageBucket": "grab-piyu-d.appspot.com",  # fixed the storageBucket domain
    "messagingSenderId": "77622540773",
    "appId": "1:77622540773:web:df19e6b5e6dac23e61170c",
    "measurementId": "G-07KFHQ70WY"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

# import pyrebase

# config = {
#   'apiKey': "AIzaSyDndPGQ8G-XQX6eFpHGUoAfvqXUhpgMc0U",
#   'authDomain': "ypg-risk-ffc53.firebaseapp.com",
#   'databaseURL': "https://ypg-risk-ffc53-default-rtdb.asia-southeast1.firebasedatabase.app",
#   'projectId': "ypg-risk-ffc53",
#   'storageBucket': "ypg-risk-ffc53.appspot.com",
#   'messagingSenderId': "711063614327",
#   'appId': "1:711063614327:web:07adb4f7462c7cc9b7e772",
# }

# firebase   = pyrebase.initialize_app(config)
# auth       = firebase.auth()
# fdatabase  = firebase.database()




import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "ypg-security",
  "private_key_id": "e37de4f6b003d78bf095546469ee59c286ca04da",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCKBE9Xe4R2/t/1\nxANJ+1S5n44B573Z/JOenRAQoqkLcm9w1uFNIlIGNWUWpieRb2hmDtgXpC1cgvwv\n8O0m928bwVDKrgQEjvqaCALCSLdcMEBS60rLQFksTFHCQS+BPdEkDLaqvbxPxVQ6\ngsVefeppcqdL/ePPjeiccZ44U/i4F4OgXWBYZr/V1pwRH8ZHHLI/413qHbkOg2rd\nLUFHL0heiXmcFtC/mNhmIJBoPuNESzlenKWYZynSXXLm2+ldqtz+KedhMAerQpiB\na2dVjmRROpvMpwXAYWVXsO2dTRjGEFX0PzKReTzzb15ib0WT6Bid1qGu4xv5rLCp\nqv4AVZcVAgMBAAECggEAB7iBAGmqTzEn3IA9bNyQm0eyh9HBHETVtI2gZ0XU2Lfr\nRa/c76syqnfp3UVTOP63TjTuCriGScK8En8oTRc8vHE+hfALzSjQb7XGAxH9S+du\nbxUMMeg6H3vE0RiYweKa5KjfaRgZxN6gPRuxUygOaR1fACXGTNyT6CMvpi1bCwqU\nrHmPahpYLaPqiyjtNzOfwXAyy9dym5g1ULKhnxKRAlF2VTcNijsrFdAezEB2uLGL\nmZOsGr+PKdDYfxBtCEiSDn4YpgAlfBMhjKERSzA71y2XR0z2LY0D8ybBL+RzllHO\nbkMLmJTysynI1vX/7llCSGKde+lDH3xj2uk6bKxamwKBgQC8LNxZSa8py9+GDlCL\nsa9Sp8dFtvDiRfCcm7VuPuAmGqf3JMfF3YiMopLuleqthf+8JV7ZsN0fjxZZ5Po1\nnIh5bJ44pSngkdVUwMBiCEb3ZBVDeVOCz9rBfqqoz1l0ZBgNg4t6ZtG0eAExe7Oh\nw6gaOqTUWjiqAdQm5ybKTHC7JwKBgQC7w0cIIOCl/uEWzAsaaE50USgHw6qjG6hy\namQNbdlIQm2bvjEde+Qki5hjtQeTbfN8Wpagwahr2xIlgExqWdQlgrVNOZasgFhC\n2Zaf8NNA4gNdgBSlD6fU1/CEX1LFq+zBbHG4B5wG3M5i2W4scSScsD6xxS0LO/k3\nijq+OXdxYwKBgQCvTOd1sqQgvtGb9CfrC3u196E3e+bKFLfDXXdWnfJ47Oo+3Z/R\n38A+q5FP/I9kWenU38eN6ysEJGuBEURav1mQLLT1NkBd+d2QGAThDq719uGsOxGm\nUnaLPbJEku3V9Q1HQZ2lSLXhds49x+yfLUOkM6+sN+SD1DJMj5hea3m1jwKBgGim\n/wBY0t2yomLCd63QVWofkeBB/unKkKi1A+84OtM7szwLVfTJCPAVnmp0jDRwJDY7\nh5kyV11GTWb5i537U3NU1xij8IdVQdyAyqN650RStO14ZglaIIFRmo0tVEU4/k0Q\n1JFuLFjm2WHfLrk2luF+mnMbI3APjWiXcwZzoU9hAoGADZdvUpHQiZtqBF24u+DS\n/rCbHd3+y8yIKT2d3vKK+qiqsMlCq0i081RAD+Vi0imTZTmwzxElR2hy5IVALd4O\nx53hpCRaNlrCgEpk+sEs8Ivj381PaFKd+LKILzcVlOPG+8jNd6Sp9x7W2aaHWsov\nXMAb2a1bzKugTgo9Bwb2mpI=\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-70o1p@ypg-security.iam.gserviceaccount.com",
  "client_id": "115144072705706582837",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-70o1p%40ypg-security.iam.gserviceaccount.com"
})
firebase_app = firebase_admin.initialize_app(cred, name="Django Web App")

fdatabase = firestore.client(app=firebase_app)

import face_recognition as fr
import os
"""
Takes : images that are in the  dataset folder( Image file name : <e_ticket_no.jpg>)
Do : extracts facial encodings from all the images
And : save it using a dict called data where encodings key has all encodings in a list and ticket_id key has all the known ticket_id as a list
Returns : data, a dict
"""
def encodings():
    path = 'dataset'
    imagePaths = os.listdir(path)
    images = []
    known_face_encodings = []
    known_ticket_id = []
    for iPath in imagePaths:
        images.append(f'{path}/{iPath}')

    total_face_processed = 0

    for (i, imagePath) in enumerate(images):
        ticket_id = imagePath.split('.')[0]
        ticket_id = ticket_id.split('/')[-1]
        known_ticket_id.append(ticket_id)
        
        image_file = fr.load_image_file(imagePath)
        known_face_encodings.append(fr.face_encodings(image_file)[0])
        total_face_processed += 1

    data = {"encodings" : known_face_encodings, "ticket_id": known_ticket_id}
    
    return data
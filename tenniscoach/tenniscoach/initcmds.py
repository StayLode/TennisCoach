from essential.models import Profile, Course, Lesson

def erase_db():
    print("Cancello il DB")
    Course.objects.all().delete()
    Profile.objects.all().delete()
    Lesson.objects.all().delete()

def init_db():
    
    if len(Libro.objects.all()) != 0:
        return

    libridict = {
        "autori" : ["Alessandro Manzoni", "George Orwell", "Omero", "George Orwell", "Omero"],
        "titoli" : ["Promessi Sposi", "1984", "Odissea", "La Fattoria degli Animali", "Iliade"],
        "pagine" : [832,328,414,141,263],
    }

    for i in range(5):
        l = Libro()
        for k in libridict:
            if k == "autori":
                    l.autore = libridict[k][i]
            if k == "titoli":
                    l.titolo = libridict[k][i]
            if k == "pagine":
                    l.pagine = libridict[k][i] 
        l.save()
        for _ in range(2):
            c = Copia()
            c.libro = l
            c.save()
    
    print("DUMP DB")
    print(Libro.objects.all()) #controlliamo
    print(Copia.objects.all())

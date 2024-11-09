from django.db import models
from datetime import datetime
# Create your models here.

class Voter(models.Model):
    '''A model to represent a voter'''
    first_name = models.TextField()
    last_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()
    dob = models.DateField()
    year_of_birth = models.IntegerField()
    date_of_registration = models.TextField()
    party_affiliation = models.TextField()
    precinct_number = models.CharField(max_length=6)
    v20state = models.TextField()
    v21town = models.TextField()
    v21primary = models.TextField()
    v22general = models.TextField()
    v23town = models.TextField()
    voter_score = models.IntegerField()

    def __str__(self):
        '''Return a string representation of this model instance.'''
        return f'{self.first_name} {self.last_name}'

def load_data():
    '''function to load data recrods from csv file into Django model instances'''
    # Delete all
    Voter.objects.all().delete()

    filename = '/Users/rongc/Downloads/newton_voters.csv'
    f = open(filename)
    headers = f.readline() # discard headers

    for line in f:
        try:
            fields = line.split(',')
            dob = datetime.strptime(fields[7], '%m/%d/%Y').date()
            year_of_birth = dob.year
            # create a new instance of Voter object with this record from CSV
            voter = Voter(first_name=fields[1],
                          last_name=fields[2],
                          street_number=fields[3],
                          street_name=fields[4],
                          apartment_number=fields[5],
                          zip_code=fields[6],
                          dob=dob,
                          year_of_birth=year_of_birth,
                          date_of_registration=fields[8],
                          party_affiliation=fields[9],
                          precinct_number=fields[10],
                          v20state=fields[11],
                          v21town=fields[12],
                          v21primary=fields[13],
                          v22general=fields[14],
                          v23town=fields[15],
                          voter_score=fields[16]
                        )
            voter.save()
        except Exception as e:
            print(f'Exception occured: {e}')
            break
    print("Done")

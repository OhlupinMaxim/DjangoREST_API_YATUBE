from review.models import Review

with open('users.csv', newline='') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    next(reader, None)
    for row in reader:
        Review.objects.create(
            id=int(row[0]),
            title_id=row[1],
            text=row[2],
            author_id=row[3],
            score=row[4],
            pub_date=row[5]
        )
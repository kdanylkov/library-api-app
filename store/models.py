from django.db import models


class Book(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    author_name = models.CharField(max_length=255)
    owner = models.ForeignKey(
        to='auth.User', on_delete=models.SET_NULL, null=True, related_name='my_books')
    readers = models.ManyToManyField(
        to='auth.User', through='UserBookRelation', related_name='books')

    def __str__(self) -> str:
        return f'ID {self.pk}: {self.name}'


class UserBookRelation(models.Model):
    RATING_CHOICES = (
        (1, 'Ok'),
        (2, 'Fine'),
        (3, 'Good'),
        (4, 'Excellent'),
        (5, 'Amazing'),
    )

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    in_bookmarks = models.BooleanField(default=False)
    rate = models.PositiveSmallIntegerField(choices=RATING_CHOICES, null=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f'{self.book.name} | User: {self.user.username} | RATING: {self.rate}'

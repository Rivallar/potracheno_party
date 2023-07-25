from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Sum


class Party(models.Model):

    """Represents a party event. Gathers all participants and all spares altogether."""

    description = models.CharField(max_length=255)
    date = models.DateField()
    is_active = models.BooleanField(default=True)

    def delete(self, is_soft=True, *args, **kwargs):
        if is_soft:
            self.is_active = False
            self.save()
        else:
            super().delete(*args, **kwargs)

    def __str__(self):
        return self.description

    class Meta:
        verbose_name_plural = "Parties"


class Member(models.Model):

    """Represents a participant of a party. Shows how much money he had spent."""

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='members')

    name = models.CharField(max_length=25, unique=True)
    money_spent = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)])

    def __str__(self):
        return self.name


class SpareItem(models.Model):

    """Represents a single spare item of a party with its price and members, who consumed this item."""

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='items')

    item_name = models.CharField(max_length=100, unique=True)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    count = models.PositiveSmallIntegerField(blank=True, null=True)
    one_item_price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, validators=[MinValueValidator(0)])

    members = models.ManyToManyField(Member, through='SharePart', related_name='spares', blank=True)

    def __str__(self):
        return self.item_name


class SharePart(models.Model):

    """Represents relations between a member of a party and a spare item. Shows how much (in %) a member consumed an item."""

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    item = models.ForeignKey(SpareItem, on_delete=models.CASCADE, related_name='parts')

    share = models.FloatField(default=0, validators=[MinValueValidator(0)])

    def save(self, *args, **kwargs):

        """Need to check that Sum of all shares <= 1 (100%)"""

        curr_shares = SharePart.objects.filter(item=self.item).exclude(member=self.member).aggregate(total=Sum('share'))['total']
        if not curr_shares:
            curr_shares = 0
        if curr_shares + self.share <= 1:
            super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.member.name}: {self.share}'

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['member', 'item'], name='Must be unique')
        ]


class Exchange(models.Model):

    """To show how much money who gives whom."""

    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name="exchanges")
    giver = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="gives")
    taker = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="takes")

    amount = models.DecimalField(max_digits=6, decimal_places=2, validators=[MinValueValidator(0)])

    def __str__(self):
        return f'{self.giver} gives {self.taker} {self.amount}'
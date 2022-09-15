from django.db import models
from django.utils import timezone

from django.contrib.auth.models import User


class Injury(models.Model):
    RELATION_CHOICES = [
        ('JTI Employee', 'JTI Employee (permanent, temporary/seasonal)'),
        ('Outsourced', 'Outsourced personnel /Supervised employee (JTI direct supervision)'),
        ('Contractor', 'Contractor'),
        ('Public', 'Member of public (no direct contractual relationship between JTI and injured person)'),
    ]
    relation_to_business = models.CharField(
        'Relation to Business',
        choices=RELATION_CHOICES,
        max_length=100,
    )
    SEVERITY_CHOICES = [
        ('Fatality', 'Fatality'),
        ('LTI', '(LTI) Lost time injury'),
        ('RWC', '(RWC) Restricted work case'),
        ('MTC', '(MTC) Medical treatment case'),
        ('First aid', 'First aid'),
    ]
    severity = models.CharField(
        'Severity',
        choices=SEVERITY_CHOICES,
        max_length=100,
    )
    CAUSE_CHOICES = [
        ('1', 'Road incident'),
        ('2', 'Cut by sharp object'),
        ('3', 'Exposure to or contact with compressed Air'),
        ('4', 'Exposure to fumes'),
        ('5', 'Exposure to or contact chemical substance'),
        ('6', 'Exposure to or contact with electric current'),
        ('7', 'Exposure to or contact with extreme temperatures'),
        ('8', 'Exposure to or contact with harmful substances or radiations'),
        ('9', 'Fall from height'),
        ('10', 'Fall on same level'),
        ('11', 'Hit by an industrial vehicle'),
        ('12', 'Improper body movement'),
        ('13', 'Injured by animal/insect'),
        ('14', 'Overexertion or strenuous movement'),
        ('15', 'Running into object'),
        ('16', 'Struck by falling or moving object'),
        ('17', 'Trapped my moving machinery or equipment'),
    ]
    immediate_cause = models.CharField(
        'Immediate Cause - Safety',
        choices=CAUSE_CHOICES,
        max_length=100,
    )
    VEHICLE_CHOICES = [
        ('Car', 'Car'),
        ('Motorcycle', 'Motorcycle'),
        ('Van', 'Van'),
        ('Rickshaw', 'Rickshaw'),
        ('Other', 'Other'),
    ]
    vehicle = models.CharField(
        'Vehicle Type',
        choices=VEHICLE_CHOICES,
        max_length=50,
        blank=True,
        null=True,
    )
    
    incident = models.ForeignKey(
        'HS_incident',
        verbose_name='Incident',
        related_name='injuries',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name_plural = 'Injuries'


class Illness(models.Model):
    RELATION_CHOICES = [
        ('JTI Employee', 'JTI Employee (permanent, temporary/seasonal)'),
        ('Outsourced', 'Outsourced personnel /Supervised employee (JTI direct supervision)'),
        ('Contractor', 'Contractor'),
        ('Public', 'Member of public (no direct contractual relationship between JTI and injured person)'),
    ]
    relation_to_business = models.CharField(
        'Relation to Businesss',
        choices=RELATION_CHOICES,
        max_length=100,
    )
    SEVERITY_CHOICES = [
        ('Fatality', 'Fatality'),
        ('LTI', '(LTI) Lost time injury'),
        ('RWC', '(RWC) Restricted work case'),
        ('MTC', '(MTC) Medical treatment case'),
        ('First aid', 'First aid'),
    ]
    severity = models.CharField(
        'Severity',
        choices=SEVERITY_CHOICES,
        max_length=100,
    )
    CONSEQUENCE_CHOICES = [
        ('1', 'Respiratory disease (eg Green tobacco sickness, Asthma, Chronic pulmonary disease)'),
        ('2', 'Skin disease (eg Dermatitis, Urticaria)'),
        ('3', 'Musculoskeletal disorder (eg Carpal tunnel syndrome, Hernia, Back pains)'),
        ('4', 'Hearing loss/impairment'),
        ('5', 'Mental and behavioral disorder (eg Burnout, Post-traumatic stress, Anxiety)'),
        ('6', 'Other (please specify)'),
    ]
    consequence = models.CharField(
        'Consequence',
        choices=CONSEQUENCE_CHOICES,
        max_length=100,
    )
    CAUSE_CHOICES = [
        ('1', 'Exposure to physical agents (Noise, Vibration, Ionizing radiations, Heat radiation, Ultraviolet radiation, Extreme temperature, Intense light etc.)'),
        ('2', 'Exposure to chemical agents (Allergic provoking agents, Irritants agents from work activities such as organic solvents, ammonia, Cadmium, phosphorus, lead and their compounds….)'),
        ('3', 'Exposure to biological agents and infectious or parasitic diseases (Viruses, Bacteria, Fungi etc.)'),
        ('4', 'Long term exposure to repetitive movements or long hours in a static position'),
        ('5', 'Long term exposure to heavy workload'),
        ('6', 'Other (please specify)'),
    ]
    immediate_cause = models.CharField(
        'Immediate Cause - Occ. Health',
        choices=CAUSE_CHOICES,
        max_length=100,
    )
    age = models.IntegerField(
        'Age',
    )
    GENDER_CHOICES = [
        (1, 'Male'),
        (2, 'Female'),
    ]
    gender = models.CharField(
        'Gender',
        choices=GENDER_CHOICES,
        max_length=100,
    )
    incident = models.ForeignKey(
        'HS_incident',
        verbose_name='Incident',
        related_name='illnesses',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )


class HS_incident(models.Model):
    ACTIVITY_CHOICES = [
        ('Manufacturing', 'Manufacturing Operations'),
        ('Leaf', 'Leaf Origins'),
        ('Market', 'Market'),
        ('R&D', 'R&D'),
        ('GBS', 'GBS'),
        ('CSS', 'CSS')
    ]
    business_activity = models.CharField(
        'Business Activity',
        choices=ACTIVITY_CHOICES,
        max_length=50,
    )
    CLASSIFICATION_CHOICES = [
        ('Safety', 'Safety'),
        ('Health', 'Occupational Health'),
    ]
    incident_classification = models.CharField(
        "Incident Classification",
        choices=CLASSIFICATION_CHOICES,
        default=None,
        max_length=50,
    )
    YES_NO = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]
    work_related = models.CharField(
        "Work related",
        choices=YES_NO,
        default=None,
        max_length=50,
    )
    auth_notified = models.CharField(
        "Ext. Auth. notification?",
        choices=YES_NO,
        default=None,
        max_length=50,
    )
    description = models.TextField(
        'Incident Description',
    )
    LOCATION_CHOICES = [
        ('Onsite', 'ON-site'),
        ('Offsite', 'OFF-site'),
    ]
    location = models.CharField(
        'Incident Location',
        choices=LOCATION_CHOICES,
        default=None,
        max_length=50,
    )
    JTI_SITES = [
        ('1419', '🏠 Babol, Iran: Office cat. B'),
        ('934', '📦Zanjan, Iran: NTM WH cat. C Machinery WH'),
        ('933', '🏠Tehran, Iran: Office cat. B (South Tehran)'),
        ('932', '🏠Tehran, Iran: Office cat. B (West Tehran)'),
        ('931', '🏠Karaj, Iran: Office cat. B'),
        ('930', '🏠Tehran, Iran: Office cat. B'),
        ('929', '🏠Hakimiyeh, Iran: Office cat. B'),
        ('928', '🏠Zanjan, Iran: Office cat. B'),
        ('927', '🏠Zahedan, Iran: Office cat. B'),
        ('926', '🏠Yazd, Iran: Office cat. B'),
        ('925', '🏠Tabriz, Iran: Office cat. B'),
        ('924', '🏠Shiraz, Iran: Office cat. B'),
        ('923', '🏠Shahroud, Iran: Office cat. B'),
        ('922', '🏠Shahrekord, Iran: Office cat. B'),
        ('921', '🏠Semnan, Iran: Office cat. B'),
        ('920', '🏠Sari, Iran: Office cat. B'),
        ('919', '🏠Sanandaj, Iran: Office cat. B'),
        ('918', '🏠Rasht, Iran: Office cat. B'),
        ('917', '🏠Qom, Iran: Office cat. B'),
        ('916', '🏠Urmia, Iran: Office cat. B'),
        ('915', '🏠Mashahd, Iran: Office cat. B'),
        ('914', '🏠Bandar Mahshahr, Iran: Office cat. B'),
        ('913', '🏠Khoy, Iran: Office cat. B'),
        ('912', '🏠Khoramabad, Iran: Office cat. B'),
        ('911', '🏠Kermanshah, Iran: Office cat. B'),
        ('910', '🏠Kerman, Iran: Office cat. B'),
        ('908', '🏠Isfahan, Iran: Office cat. B'),
        ('907', '🏠Hamedan, Iran: Office cat. B'),
        ('906', '🏠Gorgan, Iran: Office cat. B'),
        ('904', '🏠Qazvin, Iran: Office cat. B'),
        ('903', '🏠Chaloos, Iran: Office cat. B'),
        ('902', '🏠Bojnourd, Iran: Office cat. B'),
        ('901', '🏠Birjand, Iran: Office cat. B'),
        ('900', '🏠Bandar Abbas, Iran: Office cat. B'),
        ('898', '🏠Ardebil, Iran: Office cat. B'),
        ('897', '🏠Arak, Iran: Office cat. B'),
        ('896', '🏠Andimeshk, Iran: Office cat. B'),
        ('895', '🏠 Ahvaz, Iran: Office cat. B'),
        ('401', '📦🚬Mahdi Shahr, Iran: FG WH cat. A'),
        ('399', '📦🍂Jolfa, Iran: Leaf WH cat. B (ITC)'),
        ('92', '🏠Tehran, Iran: Office cat. A (HQ)'),
        ('28', '🏭Zanjan, Iran: Factory cat. A (JTI Parsian)'),
    ]

    jti_site = models.CharField(
        'JTI Site',
        max_length=50,
        choices=JTI_SITES,
        null=True,
        blank=True,
    )
    latitude = models.FloatField(
        'Latitude',
        null=True,
        blank=True,
    )
    longitude = models.FloatField(
        'Longitude',
        null=True,
        blank=True,
    )
    date_occurred = models.DateField(
        'Date Occurred',
        default=timezone.now,
    )
    date_reported = models.DateField(
        'Date Reported to Local H&S',
        default=timezone.now,
    )
    description = models.CharField(
        'Description',
        max_length=50,
        blank=True,
    )
    unique_id = models.IntegerField(
        'SIMP unique id',
        null=True,
        blank=True,
    )
    object_id = models.IntegerField(
        'SIMP object id',
        null=True,
        blank=True,
    )
    date_created = models.DateField(
        'Date created',
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        blank=True,
        null=True,
    )

    def __str__(self):
        if self.date_created:
            return f'H&S INC #{self.date_created.year}-{self.unique_id}'
        else:
            return f'H&S INC #{self.id}'


class SimpLogin(models.Model):
    token = models.TextField(
        'токен'
    )
    expiration = models.IntegerField(
        'срок истечения',
    )

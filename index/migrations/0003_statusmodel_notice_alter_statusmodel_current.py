# Generated by Django 4.1.5 on 2024-03-19 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0002_statusmodel_delete_mypagemodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='statusmodel',
            name='notice',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='statusmodel',
            name='current',
            field=models.CharField(choices=[('PREPARE', '동아리 홍보 기간'), ('FIRST_FORM', '1차 서류 지원'), ('FIRST_RESULT', '1차 서류합격 발표'), ('SECOND_INTERVIEW', '2차 면접 기간'), ('SECOND_RESULT', '최초합 발표'), ('ADD_FIRST_RESULT', '1차 추가합격 발표'), ('ADD_SECOND_RESULT', '2차 추가합격 발표'), ('ADD_THIRD_RESULT', '3차 추가합격 발표'), ('ADD_FOURTH_RESULT', '4차 추가합격 발표'), ('ADDITIONAL', '추가모집 기간'), ('FINISH', '상설동아리 모집 종료')], default='PREPARE', max_length=20),
        ),
    ]

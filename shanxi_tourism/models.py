# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Attraction(models.Model):
    attraction_id = models.IntegerField(primary_key=True)
    attraction_name = models.CharField(max_length=255)
    attraction_en_name = models.CharField(max_length=255, blank=True, null=True)
    attraction_img = models.CharField(max_length=255, blank=True, null=True)
    attraction_desc = models.CharField(max_length=10240, blank=True, null=True)
    attraction_tele = models.CharField(max_length=255, blank=True, null=True)
    attraction_site = models.CharField(max_length=255, blank=True, null=True)
    attraction_use_time = models.CharField(max_length=255, blank=True, null=True)
    attraction_traffic = models.CharField(max_length=1023, blank=True, null=True)
    attraction_ticket = models.CharField(max_length=255, blank=True, null=True)
    attraction_open_time = models.CharField(max_length=255, blank=True, null=True)
    attraction_hotel_url_1 = models.CharField(max_length=255, blank=True, null=True)
    attraction_hotel_url_2 = models.CharField(max_length=255, blank=True, null=True)
    attraction_travels_url = models.CharField(max_length=255, blank=True, null=True)
    attraction_rank = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'attraction'


class Hotel(models.Model):
    hotel_id = models.IntegerField(primary_key=True)
    attraction = models.ForeignKey(Attraction, models.DO_NOTHING)
    hotel_name = models.CharField(max_length=255, blank=True, null=True)
    hotel_position = models.CharField(max_length=255, blank=True, null=True)
    hotel_img_src = models.CharField(max_length=255, blank=True, null=True)
    hotel_in_time = models.CharField(max_length=255, blank=True, null=True)
    hotel_out_time = models.CharField(max_length=255, blank=True, null=True)
    hotel_size = models.CharField(max_length=255, blank=True, null=True)
    hotel_build_time = models.CharField(max_length=255, blank=True, null=True)
    hotel_house_name = models.CharField(max_length=255, blank=True, null=True)
    hotel_price = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel'


class HotelComment(models.Model):
    hotel_comment_id = models.AutoField(primary_key=True)
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    hotel_comment_content = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    hotel_comment_date = models.DateField(auto_now=True)
    hotel_comment_mfw_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel_comment'


class HotelOrder(models.Model):
    hotel_order_id = models.AutoField(primary_key=True)
    id_card = models.CharField(max_length=255, blank=True, null=True)
    tele_num = models.BigIntegerField(blank=True, null=True)
    hotel_type = models.CharField(max_length=255, blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.CharField(max_length=255, blank=True, null=True)
    end_time = models.CharField(max_length=255, blank=True, null=True)
    hotel = models.ForeignKey(Hotel, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'hotel_order'


class Route(models.Model):
    route_id = models.IntegerField(primary_key=True)
    route_name = models.CharField(max_length=255, blank=True, null=True)
    route_price = models.CharField(max_length=255, blank=True, null=True)
    route_img_src = models.CharField(max_length=255, blank=True, null=True)
    route_has_saled = models.CharField(max_length=255, blank=True, null=True)
    route_tag = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route'


class RouteComment(models.Model):
    route_comment_id = models.AutoField(primary_key=True)
    route = models.ForeignKey(Route, models.DO_NOTHING)
    route_comment_content = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    route_comment_date = models.DateField(auto_now=True)
    route_comment_mfw_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route_comment'


class RouteOrder(models.Model):
    route_order_id = models.AutoField(primary_key=True)
    id_card = models.CharField(max_length=255, blank=True, null=True)
    tel_num = models.BigIntegerField(blank=True, null=True)
    description = models.CharField(max_length=255, blank=True, null=True)
    route = models.ForeignKey(Route, models.DO_NOTHING)
    user = models.ForeignKey('User', models.DO_NOTHING, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'route_order'


class Travels(models.Model):
    travels_id = models.IntegerField(primary_key=True)
    attraction = models.ForeignKey(Attraction, models.DO_NOTHING)
    travels_name = models.CharField(max_length=255)
    travels_content_cut = models.CharField(max_length=255, blank=True, null=True)
    travels_content = models.CharField(max_length=10384, blank=True, null=True)
    travels_view_num = models.IntegerField(blank=True, null=True)
    travels_img_url = models.CharField(max_length=255, blank=True, null=True)
    travels_scr = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'travels'


class User(models.Model):
    user_id = models.CharField(primary_key=True, max_length=255)
    user_nick = models.CharField(max_length=255)
    user_password = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'user'

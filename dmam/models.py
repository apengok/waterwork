# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class District(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=128, blank=True, null=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'district'

    def __unicode__(self):
        return '%s%s'%(self.name)


class Alarm(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    alarmtime = models.CharField(db_column='AlarmTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    alarmevent = models.IntegerField(db_column='AlarmEvent', blank=True, null=True)  # Field name made lowercase.
    alarmtype = models.IntegerField(db_column='AlarmType', blank=True, null=True)  # Field name made lowercase.
    alarmlevel = models.IntegerField(db_column='AlarmLevel', blank=True, null=True)  # Field name made lowercase.
    alarmcontent = models.CharField(db_column='AlarmContent', max_length=128, blank=True, null=True)  # Field name made lowercase.
    alarmstate = models.IntegerField(db_column='AlarmState', blank=True, null=True)  # Field name made lowercase.
    dealtime = models.CharField(db_column='DealTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dealcontent = models.CharField(db_column='DealContent', max_length=128, blank=True, null=True)  # Field name made lowercase.
    dealjob = models.CharField(db_column='DealJob', max_length=30, blank=True, null=True)  # Field name made lowercase.
    alarmobj = models.IntegerField(db_column='AlarmObj', blank=True, null=True)  # Field name made lowercase.
    communityid = models.CharField(db_column='CommunityId', max_length=30, blank=True, null=True)  # Field name made lowercase.
    waterid = models.CharField(db_column='WaterId', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alarm'

    def __unicode__(self):
        return '%s%s'%(self.alarmcontent)


class AlarmProcess(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    alarmstate = models.IntegerField(db_column='AlarmState', blank=True, null=True)  # Field name made lowercase.
    dealtime = models.CharField(db_column='DealTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dealcontent = models.CharField(db_column='DealContent', max_length=128, blank=True, null=True)  # Field name made lowercase.
    dealjob = models.CharField(db_column='DealJob', max_length=30, blank=True, null=True)  # Field name made lowercase.
    alarmid = models.IntegerField(db_column='AlarmId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'alarm_process'

    def __unicode__(self):
        return '%s%s'%(self.DealContent)

class Amrsparam(models.Model):
    paramkey = models.CharField(db_column='paramKey', primary_key=True, max_length=64)  # Field name made lowercase.
    paramvalue = models.CharField(db_column='paramValue', max_length=128)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'amrsparam'


class Bigmeter(models.Model):
    username = models.CharField(db_column='UserName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='UserType', max_length=128, blank=True, null=True)  # Field name made lowercase.
    userid = models.CharField(db_column='UserId', max_length=128, blank=True, null=True)  # Field name made lowercase.
    installationsite = models.CharField(db_column='InstallationSite', max_length=128, blank=True, null=True)  # Field name made lowercase.
    metertype = models.CharField(db_column='MeterType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=30, blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dn = models.CharField(db_column='Dn', max_length=30, blank=True, null=True)  # Field name made lowercase.
    material = models.CharField(db_column='Material', max_length=30, blank=True, null=True)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    madedate = models.CharField(db_column='MadeDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lng = models.CharField(db_column='Lng', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lat = models.CharField(db_column='Lat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    coortype = models.CharField(db_column='CoorType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', primary_key=True, max_length=30)  # Field name made lowercase.
    simid = models.CharField(db_column='SIMID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    # districtid = models.IntegerField(db_column='DistrictId', blank=True, null=True)  # Field name made lowercase.
    districtid = models.ForeignKey(District,db_column='DistrictId',blank=True, null=True,on_delete=models.CASCADE) 
    field_metabinding = models.CharField(db_column='\r\nMetaBinding', max_length=20, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    gpflow = models.CharField(db_column='GPFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    uplimitflow = models.CharField(db_column='UpLimitFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    monthupflow = models.CharField(db_column='MonthUpFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    monthdownflow = models.CharField(db_column='MonthDownFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commstate = models.IntegerField(db_column='CommState', blank=True, null=True)  # Field name made lowercase.
    meterstate = models.CharField(db_column='MeterState', max_length=30, blank=True, null=True)  # Field name made lowercase.
    gprsv = models.CharField(db_column='GprsV', max_length=30, blank=True, null=True)  # Field name made lowercase.
    meterv = models.CharField(db_column='MeterV', max_length=30, blank=True, null=True)  # Field name made lowercase.
    downlimitv = models.CharField(db_column='DownLimitV', max_length=30, blank=True, null=True)  # Field name made lowercase.
    t = models.CharField(db_column='T', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hearttime = models.CharField(db_column='HeartTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    signlen = models.CharField(db_column='SignLen', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastonlinetime = models.CharField(db_column='LastOnLineTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    createdate = models.CharField(db_column='CreateDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    alarmoffline = models.IntegerField(db_column='AlarmOffLine', blank=True, null=True)  # Field name made lowercase.
    alarmonline = models.IntegerField(db_column='AlarmOnLine', blank=True, null=True)  # Field name made lowercase.
    alarmgprsvlow = models.IntegerField(db_column='AlarmGprsVLow', blank=True, null=True)  # Field name made lowercase.
    alarmmetervlow = models.IntegerField(db_column='AlarmMeterVLow', blank=True, null=True)  # Field name made lowercase.
    alarmuplimitflow = models.IntegerField(db_column='AlarmUpLimitFlow', blank=True, null=True)  # Field name made lowercase.
    alarmgpflow = models.IntegerField(db_column='AlarmGPFlow', blank=True, null=True)  # Field name made lowercase.
    pressure = models.CharField(db_column='Pressure', max_length=64, blank=True, null=True)  # Field name made lowercase.
    plustotalflux = models.CharField(db_column='PlusTotalFlux', max_length=64, blank=True, null=True)  # Field name made lowercase.
    reversetotalflux = models.CharField(db_column='ReverseTotalFlux', max_length=64, blank=True, null=True)  # Field name made lowercase.
    flux = models.CharField(db_column='Flux', max_length=64, blank=True, null=True)  # Field name made lowercase.
    totalflux = models.CharField(db_column='TotalFlux', max_length=64, blank=True, null=True)  # Field name made lowercase.
    pressurereadtime = models.CharField(db_column='PressureReadTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fluxreadtime = models.CharField(db_column='FluxReadTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pressurealarm = models.IntegerField(db_column='PressureAlarm', blank=True, null=True)  # Field name made lowercase.
    pressureup = models.CharField(db_column='PressureUp', max_length=64, blank=True, null=True)  # Field name made lowercase.
    pressuredown = models.CharField(db_column='PressureDown', max_length=64, blank=True, null=True)  # Field name made lowercase.
    dosagealarm = models.IntegerField(db_column='DosageAlarm', blank=True, null=True)  # Field name made lowercase.
    dosageup = models.CharField(db_column='DosageUp', max_length=64, blank=True, null=True)  # Field name made lowercase.
    dosagedown = models.CharField(db_column='DosageDown', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bigmeter'

    def __unicode__(self):
        return '%s%s'%(self.username)


class BindBigmeter(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupId', blank=True, null=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bind_bigmeter'


class BindCommunity(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupId', blank=True, null=True)  # Field name made lowercase.
    communityid = models.CharField(db_column='CommunityId', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bind_community'


class BindGroupRole(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupId', blank=True, null=True)  # Field name made lowercase.
    grouprolekey = models.CharField(db_column='GroupRoleKey', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bind_group_role'


class BindMenuGroupRole(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    usermenuid = models.IntegerField(db_column='UserMenuId', blank=True, null=True)  # Field name made lowercase.
    grouprolekey = models.CharField(db_column='GroupRoleKey', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bind_menu_group_role'


class BindMenuUserRole(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    usermenuid = models.IntegerField(db_column='UserMenuId', blank=True, null=True)  # Field name made lowercase.
    userrolekey = models.CharField(db_column='UserRoleKey', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bind_menu_user_role'


class BindUserGroup(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    groupid = models.IntegerField(db_column='GroupId', blank=True, null=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bind_user_group'


class BindUserRole(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    userid = models.IntegerField(db_column='UserId', blank=True, null=True)  # Field name made lowercase.
    userrolekey = models.CharField(db_column='UserRoleKey', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'bind_user_role'


class Changewatermeter(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    changedt = models.CharField(db_column='ChangeDt', max_length=30, blank=True, null=True)  # Field name made lowercase.
    oldmetervalue = models.CharField(db_column='OldMeterValue', max_length=128, blank=True, null=True)  # Field name made lowercase.
    newmetervalue = models.CharField(db_column='NewMeterValue', max_length=128, blank=True, null=True)  # Field name made lowercase.
    oldnodeaddr = models.CharField(db_column='OldNodeAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    oldwateraddr = models.CharField(db_column='OldWaterAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    newnodeaddr = models.CharField(db_column='NewNodeAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    newwateraddr = models.CharField(db_column='NewWaterAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    job = models.CharField(db_column='Job', max_length=30, blank=True, null=True)  # Field name made lowercase.
    waterid = models.IntegerField(db_column='WaterId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'changewatermeter'


class Community(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=128, blank=True, null=True)  # Field name made lowercase.
    metabinding = models.CharField(db_column='MetaBinding', max_length=20, blank=True, null=True)  # Field name made lowercase.
    districtid = models.IntegerField(db_column='DistrictId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'community'

    def __unicode__(self):
        return '%s%s'%(self.name)


class Concentrator(models.Model):
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    installationsite = models.CharField(db_column='InstallationSite', max_length=128, blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=64, blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=64, blank=True, null=True)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    madedate = models.CharField(db_column='MadeDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lng = models.CharField(db_column='Lng', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lat = models.CharField(db_column='Lat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    coortype = models.CharField(db_column='CoorType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', primary_key=True, max_length=30)  # Field name made lowercase.
    simid = models.CharField(db_column='SIMID', max_length=30, blank=True, null=True)  # Field name made lowercase.
    gpflow = models.CharField(db_column='GPFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    uplimitflow = models.CharField(db_column='UpLimitFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    monthupflow = models.CharField(db_column='MonthUpFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    monthdownflow = models.CharField(db_column='MonthDownFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commstate = models.IntegerField(db_column='CommState', blank=True, null=True)  # Field name made lowercase.
    gprsv = models.CharField(db_column='GprsV', max_length=30, blank=True, null=True)  # Field name made lowercase.
    downlimitv = models.CharField(db_column='DownLimitV', max_length=30, blank=True, null=True)  # Field name made lowercase.
    t = models.CharField(db_column='T', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hearttime = models.CharField(db_column='HeartTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    signlen = models.CharField(db_column='SignLen', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastonlinetime = models.CharField(db_column='LastOnLineTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    createdate = models.CharField(db_column='CreateDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    communityid = models.IntegerField(db_column='CommunityId', blank=True, null=True)  # Field name made lowercase.
    alarmoffline = models.IntegerField(db_column='AlarmOffLine', blank=True, null=True)  # Field name made lowercase.
    alarmonline = models.IntegerField(db_column='AlarmOnLine', blank=True, null=True)  # Field name made lowercase.
    alarmgprsvlow = models.IntegerField(db_column='AlarmGprsVLow', blank=True, null=True)  # Field name made lowercase.
    alarmuplimitflow = models.IntegerField(db_column='AlarmUpLimitFlow', blank=True, null=True)  # Field name made lowercase.
    alarmgpflow = models.IntegerField(db_column='AlarmGPFlow', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'concentrator'

    def __unicode__(self):
        return '%s%s'%(self.name)



class FireHydrant(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=128, blank=True, null=True)  # Field name made lowercase.
    metabinding = models.CharField(db_column='MetaBinding', max_length=20, blank=True, null=True)  # Field name made lowercase.
    lng = models.CharField(db_column='Lng', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lat = models.CharField(db_column='Lat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    coortype = models.CharField(db_column='CoorType', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'fire_hydrant'

    def __unicode__(self):
        return '%s%s'%(self.name)

class HdbCommunityRdc(models.Model):
    hdate = models.CharField(db_column='HDate', primary_key=True, max_length=30)  # Field name made lowercase.
    community = models.CharField(db_column='Community', max_length=30)  # Field name made lowercase.
    totalnum = models.CharField(db_column='TotalNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    normalnum = models.CharField(db_column='NormalNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    nodefaultnum = models.CharField(db_column='NodeFaultNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    waterfaultnum = models.CharField(db_column='WaterFaultNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    abnormalnum = models.CharField(db_column='AbnormalNum', max_length=30, blank=True, null=True)  # Field name made lowercase.
    readdatacount = models.CharField(db_column='ReadDataCount', max_length=30, blank=True, null=True)  # Field name made lowercase.
    sortidx = models.IntegerField(db_column='SortIdx', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_community_rdc'
        unique_together = (('hdate', 'community'),)


    def __unicode__(self):
        return '%s%s'%(self.community)

class HdbFlowData(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    readtime = models.CharField(db_column='ReadTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    meterstate = models.CharField(db_column='MeterState', max_length=30, blank=True, null=True)  # Field name made lowercase.
    flux = models.CharField(db_column='Flux', max_length=64, blank=True, null=True)  # Field name made lowercase.
    plustotalflux = models.CharField(db_column='PlusTotalFlux', max_length=64, blank=True, null=True)  # Field name made lowercase.
    reversetotalflux = models.CharField(db_column='ReverseTotalFlux', max_length=64, blank=True, null=True)  # Field name made lowercase.
    totalflux = models.CharField(db_column='TotalFlux', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gprsv = models.CharField(db_column='GprsV', max_length=64, blank=True, null=True)  # Field name made lowercase.
    meterv = models.CharField(db_column='MeterV', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_flow_data'
        unique_together = (('commaddr', 'readtime'),)

    def __unicode__(self):
        return '%s%s'%(self.commaddr)


class HdbFlowDataDay(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hdate = models.CharField(db_column='HDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dosage = models.CharField(db_column='Dosage', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_flow_data_day'
        unique_together = (('commaddr', 'hdate'),)

    def __unicode__(self):
        return '%s%s'%(self.commaddr)


class HdbFlowDataHour(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hdate = models.CharField(db_column='HDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dosage = models.CharField(db_column='Dosage', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_flow_data_hour'
        unique_together = (('commaddr', 'hdate'),)

    def __unicode__(self):
        return '%s%s'%(self.commaddr)

class HdbFlowDataMonth(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hdate = models.CharField(db_column='HDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dosage = models.CharField(db_column='Dosage', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_flow_data_month'
        unique_together = (('commaddr', 'hdate'),)

    def __unicode__(self):
        return '%s%s'%(self.commaddr)


class HdbPressureData(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    readtime = models.CharField(db_column='ReadTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    meterstate = models.CharField(db_column='MeterState', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pressure = models.CharField(db_column='Pressure', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gprsv = models.CharField(db_column='GprsV', max_length=64, blank=True, null=True)  # Field name made lowercase.
    meterv = models.CharField(db_column='MeterV', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_pressure_data'
        unique_together = (('commaddr', 'readtime'),)

    def __unicode__(self):
        return '%s%s'%(self.commaddr)


class HdbSimflow(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hdate = models.CharField(db_column='HDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    monthupflow = models.CharField(db_column='MonthUpFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.
    monthdownflow = models.CharField(db_column='MonthDownFlow', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_simflow'

    def __unicode__(self):
        return '%s%s'%(self.commaddr)


class HdbWatermeterDay(models.Model):
    waterid = models.IntegerField(db_column='WaterId', primary_key=True)  # Field name made lowercase.
    rvalue = models.CharField(db_column='RValue', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fvalue = models.CharField(db_column='FValue', max_length=30, blank=True, null=True)  # Field name made lowercase.
    meterstate = models.CharField(db_column='MeterState', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commstate = models.CharField(db_column='CommState', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rtime = models.CharField(db_column='RTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hdate = models.CharField(db_column='HDate', max_length=30)  # Field name made lowercase.
    dosage = models.CharField(db_column='Dosage', max_length=30, blank=True, null=True)  # Field name made lowercase.
    communityid = models.IntegerField(db_column='CommunityId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_watermeter_day'
        unique_together = (('waterid', 'hdate', 'communityid'),)


class HdbWatermeterMonth(models.Model):
    waterid = models.IntegerField(db_column='WaterId', primary_key=True)  # Field name made lowercase.
    hdate = models.CharField(db_column='HDate', max_length=30)  # Field name made lowercase.
    dosage = models.CharField(db_column='Dosage', max_length=30, blank=True, null=True)  # Field name made lowercase.
    communityid = models.IntegerField(db_column='CommunityId')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'hdb_watermeter_month'
        unique_together = (('waterid', 'hdate', 'communityid'),)


class Imexport(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commtype = models.IntegerField(db_column='CommType', blank=True, null=True)  # Field name made lowercase.
    protocol = models.CharField(db_column='Protocol', max_length=64, blank=True, null=True)  # Field name made lowercase.
    driver = models.CharField(db_column='Driver', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dbname = models.CharField(db_column='DbName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    hostname = models.CharField(db_column='Hostname', max_length=30, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=30, blank=True, null=True)  # Field name made lowercase.
    port = models.IntegerField(db_column='Port', blank=True, null=True)  # Field name made lowercase.
    opedate = models.IntegerField(db_column='OpeDate', blank=True, null=True)  # Field name made lowercase.
    opetime = models.CharField(db_column='OpeTime', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'imexport'


class Metercomm(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commtype = models.IntegerField(db_column='CommType', blank=True, null=True)  # Field name made lowercase.
    tcpport = models.CharField(db_column='TcpPort', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commprotocol = models.CharField(db_column='CommProtocol', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'metercomm'

    def __unicode__(self):
        return '%s%s'%(self.name)

class Meterprotocol(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commtype = models.IntegerField(db_column='CommType', blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'meterprotocol'

    def __unicode__(self):
        return '%s%s'%(self.name)


class PipeMapNode(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    nodetype = models.IntegerField(db_column='NodeType', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=128, blank=True, null=True)  # Field name made lowercase.
    lng = models.CharField(db_column='Lng', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lat = models.CharField(db_column='Lat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    coortype = models.CharField(db_column='CoorType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    zoommin = models.IntegerField(db_column='ZoomMin', blank=True, null=True)  # Field name made lowercase.
    nodestate = models.CharField(db_column='NodeState', max_length=64, blank=True, null=True)  # Field name made lowercase.
    nodestatetype = models.IntegerField(db_column='NodeStateType', blank=True, null=True)  # Field name made lowercase.
    nodestateshow = models.IntegerField(db_column='NodeStateShow', blank=True, null=True)  # Field name made lowercase.
    prop1 = models.CharField(db_column='Prop1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop1type = models.IntegerField(db_column='Prop1Type', blank=True, null=True)  # Field name made lowercase.
    prop1show = models.IntegerField(db_column='Prop1Show', blank=True, null=True)  # Field name made lowercase.
    prop2 = models.CharField(db_column='Prop2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop2type = models.IntegerField(db_column='Prop2Type', blank=True, null=True)  # Field name made lowercase.
    prop2show = models.IntegerField(db_column='Prop2Show', blank=True, null=True)  # Field name made lowercase.
    prop3 = models.CharField(db_column='Prop3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop3type = models.IntegerField(db_column='Prop3Type', blank=True, null=True)  # Field name made lowercase.
    prop3show = models.IntegerField(db_column='Prop3Show', blank=True, null=True)  # Field name made lowercase.
    prop4 = models.CharField(db_column='Prop4', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop4type = models.IntegerField(db_column='Prop4Type', blank=True, null=True)  # Field name made lowercase.
    prop4show = models.IntegerField(db_column='Prop4Show', blank=True, null=True)  # Field name made lowercase.
    prop5 = models.CharField(db_column='Prop5', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop5type = models.IntegerField(db_column='Prop5Type', blank=True, null=True)  # Field name made lowercase.
    prop5show = models.IntegerField(db_column='Prop5Show', blank=True, null=True)  # Field name made lowercase.
    prop6 = models.CharField(db_column='Prop6', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop6type = models.IntegerField(db_column='Prop6Type', blank=True, null=True)  # Field name made lowercase.
    prop6show = models.IntegerField(db_column='Prop6Show', blank=True, null=True)  # Field name made lowercase.
    prop7 = models.CharField(db_column='Prop7', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop7type = models.IntegerField(db_column='Prop7Type', blank=True, null=True)  # Field name made lowercase.
    prop7show = models.IntegerField(db_column='Prop7Show', blank=True, null=True)  # Field name made lowercase.
    prop8 = models.CharField(db_column='Prop8', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop8type = models.IntegerField(db_column='Prop8Type', blank=True, null=True)  # Field name made lowercase.
    prop8show = models.IntegerField(db_column='Prop8Show', blank=True, null=True)  # Field name made lowercase.
    prop9 = models.CharField(db_column='Prop9', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop9type = models.IntegerField(db_column='Prop9Type', blank=True, null=True)  # Field name made lowercase.
    prop9show = models.IntegerField(db_column='Prop9Show', blank=True, null=True)  # Field name made lowercase.
    prop10 = models.CharField(db_column='Prop10', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop10type = models.IntegerField(db_column='Prop10Type', blank=True, null=True)  # Field name made lowercase.
    prop10show = models.IntegerField(db_column='Prop10Show', blank=True, null=True)  # Field name made lowercase.
    visible = models.IntegerField(db_column='Visible', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pipe_map_node'

    def __unicode__(self):
        return '%s%s'%(self.name)

class PipeMapNodeType(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    nodetype = models.IntegerField(db_column='NodeType', blank=True, null=True)  # Field name made lowercase.
    prop1 = models.CharField(db_column='Prop1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit1 = models.CharField(db_column='Unit1', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop2 = models.CharField(db_column='Prop2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit2 = models.CharField(db_column='Unit2', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop3 = models.CharField(db_column='Prop3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit3 = models.CharField(db_column='Unit3', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop4 = models.CharField(db_column='Prop4', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit4 = models.CharField(db_column='Unit4', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop5 = models.CharField(db_column='Prop5', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit5 = models.CharField(db_column='Unit5', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop6 = models.CharField(db_column='Prop6', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit6 = models.CharField(db_column='Unit6', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop7 = models.CharField(db_column='Prop7', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit7 = models.CharField(db_column='Unit7', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop8 = models.CharField(db_column='Prop8', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit8 = models.CharField(db_column='Unit8', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop9 = models.CharField(db_column='Prop9', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit9 = models.CharField(db_column='Unit9', max_length=64, blank=True, null=True)  # Field name made lowercase.
    prop10 = models.CharField(db_column='Prop10', max_length=64, blank=True, null=True)  # Field name made lowercase.
    unit10 = models.CharField(db_column='Unit10', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pipe_map_node_type'


class PipePressure(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=128, blank=True, null=True)  # Field name made lowercase.
    pressuretag = models.CharField(db_column='PressureTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    pressureup = models.CharField(db_column='PressureUp', max_length=64, blank=True, null=True)  # Field name made lowercase.
    pressuredown = models.CharField(db_column='PressureDown', max_length=64, blank=True, null=True)  # Field name made lowercase.
    isbigmeter = models.IntegerField(db_column='IsBigMeter', blank=True, null=True)  # Field name made lowercase.
    lng = models.CharField(db_column='Lng', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lat = models.CharField(db_column='Lat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    coortype = models.CharField(db_column='CoorType', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'pipe_pressure'

    def __unicode__(self):
        return '%s%s'%(self.name)


class SecondDistrict(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=128, blank=True, null=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'second_district'

    def __unicode__(self):
        return '%s%s'%(self.name)


class SecondWater(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=128, blank=True, null=True)  # Field name made lowercase.
    metabinding = models.CharField(db_column='MetaBinding', max_length=20, blank=True, null=True)  # Field name made lowercase.
    districtid = models.IntegerField(db_column='DistrictId', blank=True, null=True)  # Field name made lowercase.
    lng = models.CharField(db_column='Lng', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lat = models.CharField(db_column='Lat', max_length=30, blank=True, null=True)  # Field name made lowercase.
    coortype = models.CharField(db_column='CoorType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    waterinpresstag = models.CharField(db_column='WaterInPressTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    wateroutpresstag = models.CharField(db_column='WaterOutPressTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    watersetpresstag = models.CharField(db_column='WaterSetPressTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    freqtag = models.CharField(db_column='FreqTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    lowfreqtag = models.CharField(db_column='LowFreqTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    fluxtag = models.CharField(db_column='FluxTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    totalfluxtag = models.CharField(db_column='TotalFluxTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    chlorinetag = models.CharField(db_column='ChlorineTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    leveltag = models.CharField(db_column='LevelTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    phtag = models.CharField(db_column='PhTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    utag = models.CharField(db_column='UTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    i1tag = models.CharField(db_column='I1Tag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    i2tag = models.CharField(db_column='I2Tag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    i3tag = models.CharField(db_column='I3Tag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    s1tag = models.CharField(db_column='S1Tag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    s2tag = models.CharField(db_column='S2Tag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    s3tag = models.CharField(db_column='S3Tag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commtag = models.CharField(db_column='CommTag', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'second_water'

    def __unicode__(self):
        return '%s%s'%(self.name)


class StnAlarmBind(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    bindtype = models.CharField(db_column='BindType', max_length=32, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'stn_alarm_bind'

    def __unicode__(self):
        return '%s%s'%(self.name)

class Syncscada(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pressuretag = models.CharField(db_column='PressureTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    plustotalfluxtag = models.CharField(db_column='PlusTotalFluxTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    reversetotalfluxtag = models.CharField(db_column='ReverseTotalFluxTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    fluxtag = models.CharField(db_column='FluxTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    totalfluxtag = models.CharField(db_column='TotalFluxTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    commstatetag = models.CharField(db_column='CommStateTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    meterstatetag = models.CharField(db_column='MeterStateTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    gprsvtag = models.CharField(db_column='GprsVTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    metervtag = models.CharField(db_column='MeterVTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    pressurereadtimetag = models.CharField(db_column='PressureReadTimeTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    fluxreadtimetag = models.CharField(db_column='FluxReadTimeTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    ttag = models.CharField(db_column='TTag', max_length=64, blank=True, null=True)  # Field name made lowercase.
    syncdis = models.IntegerField(db_column='SyncDis', blank=True, null=True)  # Field name made lowercase.
    offset = models.IntegerField(db_column='Offset', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'syncscada'

    def __unicode__(self):
        return '%s%s'%(self.name)

class SystemLog(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    logtime = models.CharField(db_column='LogTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    logtype = models.IntegerField(db_column='LogType', blank=True, null=True)  # Field name made lowercase.
    logcontent = models.CharField(db_column='LogContent', max_length=128, blank=True, null=True)  # Field name made lowercase.
    job = models.CharField(db_column='Job', max_length=30, blank=True, null=True)  # Field name made lowercase.
    logobj = models.IntegerField(db_column='LogObj', blank=True, null=True)  # Field name made lowercase.
    communityid = models.CharField(db_column='CommunityId', max_length=30, blank=True, null=True)  # Field name made lowercase.
    waterid = models.CharField(db_column='WaterId', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commaddr = models.CharField(db_column='CommAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'system_log'


class User(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=30, blank=True, null=True)  # Field name made lowercase.
    job = models.CharField(db_column='Job', max_length=30, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=64, blank=True, null=True)  # Field name made lowercase.
    tel = models.CharField(db_column='Tel', max_length=64, blank=True, null=True)  # Field name made lowercase.
    sex = models.IntegerField(db_column='Sex', blank=True, null=True)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=64, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=64, blank=True, null=True)  # Field name made lowercase.
    platformname = models.CharField(db_column='PlatformName', max_length=64, blank=True, null=True)  # Field name made lowercase.
    logintime = models.CharField(db_column='LoginTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    loginip = models.CharField(db_column='LoginIp', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user'


class UserGroup(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=64, blank=True, null=True)  # Field name made lowercase.
    platformname = models.CharField(db_column='PlatformName', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_group'


class UserGroupRole(models.Model):
    grouprolekey = models.CharField(db_column='GroupRoleKey', primary_key=True, max_length=64)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_group_role'


class UserMenu(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=32, blank=True, null=True)  # Field name made lowercase.
    icon = models.CharField(db_column='Icon', max_length=128, blank=True, null=True)  # Field name made lowercase.
    url = models.CharField(db_column='Url', max_length=128, blank=True, null=True)  # Field name made lowercase.
    alarmapi = models.CharField(db_column='AlarmApi', max_length=128, blank=True, null=True)  # Field name made lowercase.
    alarmurl = models.CharField(db_column='AlarmUrl', max_length=128, blank=True, null=True)  # Field name made lowercase.
    sortmenuno = models.IntegerField(db_column='SortMenuNo', blank=True, null=True)  # Field name made lowercase.
    parentid = models.IntegerField(db_column='ParentId', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_menu'


class UserRole(models.Model):
    userrolekey = models.CharField(db_column='UserRoleKey', primary_key=True, max_length=64)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=64, blank=True, null=True)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=64, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'user_role'


class Watermeter(models.Model):
    id = models.AutoField(db_column='Id', primary_key=True)  # Field name made lowercase.
    numbersth = models.CharField(db_column='NumberSth', max_length=30, blank=True, null=True)  # Field name made lowercase.
    buildingname = models.CharField(db_column='BuildingName', max_length=128, blank=True, null=True)  # Field name made lowercase.
    roomname = models.CharField(db_column='RoomName', max_length=128, blank=True, null=True)  # Field name made lowercase.
    nodeaddr = models.CharField(db_column='NodeAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    wateraddr = models.CharField(db_column='WaterAddr', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rvalue = models.CharField(db_column='RValue', max_length=30, blank=True, null=True)  # Field name made lowercase.
    fvalue = models.CharField(db_column='FValue', max_length=30, blank=True, null=True)  # Field name made lowercase.
    metertype = models.CharField(db_column='MeterType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    meterstate = models.CharField(db_column='MeterState', max_length=30, blank=True, null=True)  # Field name made lowercase.
    commstate = models.CharField(db_column='CommState', max_length=30, blank=True, null=True)  # Field name made lowercase.
    rtime = models.CharField(db_column='RTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastrvalue = models.CharField(db_column='LastRValue', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastrtime = models.CharField(db_column='LastRTime', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dosage = models.CharField(db_column='Dosage', max_length=30, blank=True, null=True)  # Field name made lowercase.
    islargecalibermeter = models.IntegerField(db_column='IsLargeCaliberMeter', blank=True, null=True)  # Field name made lowercase.
    communityid = models.IntegerField(db_column='CommunityId', blank=True, null=True)  # Field name made lowercase.
    metabinding = models.CharField(db_column='MetaBinding', max_length=20, blank=True, null=True)  # Field name made lowercase.
    commaddrbig = models.CharField(db_column='CommAddrBig', max_length=30, blank=True, null=True)  # Field name made lowercase.
    metercontrol = models.IntegerField(db_column='MeterControl', blank=True, null=True)  # Field name made lowercase.
    valvestate = models.IntegerField(db_column='ValveState', blank=True, null=True)  # Field name made lowercase.
    usertype = models.CharField(db_column='UserType', max_length=30, blank=True, null=True)  # Field name made lowercase.
    username = models.CharField(db_column='UserName', max_length=30, blank=True, null=True)  # Field name made lowercase.
    usertel = models.CharField(db_column='UserTel', max_length=30, blank=True, null=True)  # Field name made lowercase.
    serialnumber = models.CharField(db_column='SerialNumber', max_length=30, blank=True, null=True)  # Field name made lowercase.
    model = models.CharField(db_column='Model', max_length=30, blank=True, null=True)  # Field name made lowercase.
    dn = models.CharField(db_column='Dn', max_length=30, blank=True, null=True)  # Field name made lowercase.
    material = models.CharField(db_column='Material', max_length=30, blank=True, null=True)  # Field name made lowercase.
    manufacturer = models.CharField(db_column='Manufacturer', max_length=30, blank=True, null=True)  # Field name made lowercase.
    installationsite = models.CharField(db_column='InstallationSite', max_length=30, blank=True, null=True)  # Field name made lowercase.
    madedate = models.CharField(db_column='MadeDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastwritedate = models.CharField(db_column='LastWriteDate', max_length=30, blank=True, null=True)  # Field name made lowercase.
    lastwritevalue = models.CharField(db_column='LastWriteValue', max_length=30, blank=True, null=True)  # Field name made lowercase.
    meterv = models.CharField(db_column='MeterV', max_length=30, blank=True, null=True)  # Field name made lowercase.
    pntno = models.CharField(db_column='PntNo', max_length=30, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'watermeter'
        unique_together = (('communityid', 'nodeaddr', 'wateraddr'),)

    def __unicode__(self):
        return '%s%s'%(self.buildingname)
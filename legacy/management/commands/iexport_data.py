from django.core.management.base import BaseCommand, CommandError

from legacy.models import HdbFlowData,HdbFlowDataDay,HdbFlowDataHour,HdbFlowDataMonth,HdbPressureData,Bigmeter
import time

class Command(BaseCommand):
    help = 'import data from A to B'

    def add_arguments(self, parser):
        # parser.add_argument('sTime', type=str)

        parser.add_argument(
            '--hdb_flow_data',
            action='store_true',
            dest='hdb_flow_data',
            default=False,
            help='import hdb_flow_data to new db'
        )

        parser.add_argument(
            '--test',
            action='store_true',
            dest='test',
            default=False,
            help='test'
        )

        parser.add_argument(
            '--hdb_flow_data_day',
            action='store_true',
            dest='hdb_flow_data_day',
            default=False,
            help='import hdb_flow_data_day to new db'
        )

        parser.add_argument(
            '--hdb_flow_data_hour',
            action='store_true',
            dest='hdb_flow_data_hour',
            default=False,
            help='import hdb_flow_data_hour to new db'
        )

        parser.add_argument(
            '--hdb_flow_data_month',
            action='store_true',
            dest='hdb_flow_data_month',
            default=False,
            help='import hdb_flow_data_month to new db'
        )

        parser.add_argument(
            '--bigmeter',
            action='store_true',
            dest='bigmeter',
            default=False,
            help='import bigmeter to new db'
        )

        

    def handle(self, *args, **options):
        # sTime = options['sTime']
        t1=time.time()
        count = 0
        if options['test']:
            
            commaddr = '15720596623'
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=HdbFlowData.objects.using("zncb").filter(commaddr=commaddr).all()
            count = data_qset.count()
            zncb_last = HdbFlowData.objects.using("zncb").filter(commaddr=commaddr).last()
            last_readtime = zncb_last.readtime
            print(zncb_last,zncb_last.id,zncb_last.readtime,zncb_last.flux,zncb_last.plustotalflux)
            print(last_readtime)
            data_shexian=HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).all()
            count_sx = data_shexian.count()
            sx_last = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(readtime=last_readtime).first()
            print('sx_last',sx_last.id,sx_last.readtime,sx_last.flux,sx_last.plustotalflux)
            added = HdbFlowData.objects.using("shexian").filter(commaddr=commaddr).filter(id__gt=sx_last.id).all()
            print('added',added.count())
            for d in added:
                d.save(using='zncb')
            # 

        if options['hdb_flow_data']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=HdbFlowData.objects.using("zncb").all()
            count = data_qset.count()
            for d in data_qset:
                d.save(using='zncb2')

        if options['hdb_flow_data_day']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=HdbFlowDataDay.objects.using("zncb").all()
            count = data_qset.count()
            for d in data_qset:
                d.save(using='zncb2')

        if options['hdb_flow_data_hour']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=HdbFlowDataHour.objects.using("zncb").all()
            count = data_qset.count()
            for d in data_qset:
                d.save(using='zncb2')

        if options['hdb_flow_data_month']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=HdbFlowDataMonth.objects.using("zncb").all()
            count = data_qset.count()
            for d in data_qset:
                d.save(using='zncb2')

        aft=0
        if options['bigmeter']:
            
            
            # data_qset=HdbFlowData.objects.using("virvo").filter(readtime__range=[sTime,'2018-09-20'])
            data_qset=Bigmeter.objects.using("zncb").all()
            count = data_qset.count()
            for d in data_qset:
                commaddr = d.commaddr
                d2=Bigmeter.objects.using("zncb2").filter(commaddr=commaddr)
                if not d2.exists():
                    d.save(using='zncb2')
                    aft+=1

        
                
        t2 = time.time() - t1
        self.stdout.write(self.style.SUCCESS(f'total {count}  Affected {aft} row(s)!,elapsed {t2}'))

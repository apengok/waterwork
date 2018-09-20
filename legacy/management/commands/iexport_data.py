from django.core.management.base import BaseCommand, CommandError

from legacy.models import HdbFlowData
import time

class Command(BaseCommand):
    help = 'import data from A to B'

    def add_arguments(self, parser):
        parser.add_argument('sTime', type=str)

        # parser.add_argument(
        #     '--clear',
        #     action='store_true',
        #     dest='clear',
        #     default=False,
        #     help='Clear all existing products first'
        # )

    def handle(self, *args, **options):
        sTime = options['sTime']
        # if options['clear']:
        #     models.Product.objects.all().delete()
        # factories.ProductFactory.create_batch(size=count)
        t1=time.time()
        data_qset=HdbFlowData.objects.using("shex").filter(readtime__range=[sTime,'2018-09-20'])
        count = data_qset.count()
        for d in data_qset:
            d.save(using='zncb')
        t2 = time.time() - t1
        self.stdout.write(self.style.SUCCESS(f'Affected {count} row(s)!,elapsed {t2}'))

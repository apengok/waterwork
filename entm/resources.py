# -*- coding:utf-8 -*-
from import_export import resources
from accounts.models import User,MyRoles
from entm.models import Organizations

class UserResource(resources.ModelResource):
    class Meta:
        model = User
        import_id_fields = ['user_name']
        fields = ('user_name', 'real_name', 'sex','phone_number','email','is_active','expire_date','belongto','Role')
        export_order = fields

    def before_import(self, dataset, using_transactions, dry_run, **kwargs):
        print('before_import:',dataset.dict)

    # def before_import(self, dataset, dry_run):
    #     """
    #     Make standard corrections to the dataset
    #     """

    #     # Convert headers to lower case
    #     if dataset.headers:
    #         dataset.headers = [str(header).lower().strip() for header in dataset.headers]

    #     # Skip rows before the table headers
    #     while not dataset.headers or not (set(dataset.headers) & set(self.fields.keys())):
    #         dataset.headers = [str(item).lower() for item in dataset[0]]
    #         del dataset[0]
    #         logger.warning('Deleting non-header line from start of Dataset')

    #     if 'id' not in dataset.headers and 'other_col' in dataset.headers:
    #         dataset.headers[dataset.headers.index('other_col')] = 'id'  # Rename a column
    #     if 'id' not in dataset.headers:
    #         dataset.insert_col(0, lambda row: dict(zip(dataset.headers, row))['accno'] * 10, header='id')  # or use a lambda to calculate the id

    def dehydrate_sex(self,user):
        print('dehydrate_sex:',user.sex)
        # #export
        # if user.sex == '1':
        #     return '男'
        # if user.sex == '2':
        #     return '女'

        # #import
        # if user.sex == '男':
        #     return '1'
        # if user.sex == '女':
        #     return '2'
        return '男' if user.sex == '1' else '女'

    def dehydrate_is_active(self,user):
        print('dehydrate_is_active:',user.is_active)
        #export
        
        return '启用' if user.is_active else '停用'

    def dehydrate_belongto(self,user):
        print('dehydrate_belongto',user.belongto)
        if user.belongto:
            return user.belongto.name
        else:
            raise Exception(" belongto is none ")
            # return ''

    def dehydrate_Role(self,user):
        print('dehydrate_Role',user.Role)
        if user.Role:
            return user.Role.name
        else:
            return ''

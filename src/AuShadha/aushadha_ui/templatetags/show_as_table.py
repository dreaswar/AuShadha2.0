#######################################################################################
# PROJECT      : AuShadha
# Description  : Custom Template Tags for Data Display
# Author       : Dr. Easwar T R
# Date         : 16-09-2018
# Licence      : GNU GPL V3. Please see AuShadha/LICENSE.txt
#######################################################################################


from django import template
from django.utils.safestring import mark_safe

register = template.Library()

# variables
table_open = "<table class='content_pane_table'>"
table_row_open = "<tr>"
table_row_close = "</tr>"
table_header_row_open = "<thead>"
table_header_row_close = "</thead>"
table_header_open = "<th>"
table_header_close = "</th>"
table_cell_open = "<td>"
table_cell_close = "</td>"
table_close = "</table>"


@register.simple_tag
def show_as_table(m_queryset):
    ''' Return formatted data as mark_safe HTML table '''

    print("Calling function to print data as table")
    # print(m_queryset)

    def build_header(obj):
        _str_obj = table_header_row_open
        _str_obj += table_row_open
        for o in obj:
            if o.__class__.__name__ not in ['AutoField', 'ForeignKey']:
                _str_obj += table_header_open
                field_name = (o.name).replace('_', ' ').title()
                # print(field_name)
                _str_obj += field_name
                _str_obj += table_header_close
        _str_obj += table_row_close
        _str_obj += table_header_row_close
        return _str_obj

    try:
        if len(m_queryset) > 0:
            for x in m_queryset:
                x._field_list()
            str_obj = ''
            #str_obj += table_open
            str_obj += build_header(m_queryset[0].field_list)
            # print(str_obj)

            # build table body

            for query_instance in m_queryset:
                str_obj += table_row_open
                #print("now running instances")
                # print(query_instance.base_condition)
                for obj in query_instance.field_list:
                    if obj.__class__.__name__ not in ['AutoField', 'ForeignKey']:
                        str_obj += table_cell_open
                        field_value = (obj.value_to_string(
                            query_instance)).replace('_', ' ').title()
                        #print("Field value is : ")
                        # print(field_value)
                        if field_value in['', None]:
                            field_value = '--'

                        if field_value == True:
                            field_value = "Yes"
                        elif field_value == False:
                            field_value = "No"

                        str_obj += field_value
                        str_obj += table_cell_close
                        # print(str_obj)

                    else:
                        continue
                str_obj += table_row_close

            # close table <row>, <body> and <table>
            #str_obj += table_close
            # print(str_obj)
            return mark_safe(str_obj)

    except (Exception) as e:
        print(e)
        raise e

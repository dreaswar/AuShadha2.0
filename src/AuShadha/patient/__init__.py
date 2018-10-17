################################################################################
# Project : AuShadha
# Description: Patient Module Vars
# Date : 08-10-2013
# License : GNU-GPL Version 3, see LICENSE.txt
# Author : Dr. Easwar T.R
################################################################################

MODULE_IDENTIFIER = 'aushadha-patient'
<<<<<<< HEAD
MODULE_LABEL      = 'Patient'
VERSION           = 0.01
MODULE_TYPE       = 'main_module'
PARENT_MODULE     = 'aushadha'
DEPENDS_ON        = ['aushadha','search']
=======
MODULE_LABEL = 'Patient'
VERSION = 0.01
MODULE_TYPE = 'main_module'
PARENT_MODULE = 'aushadha'
DEPENDS_ON = ['aushadha',]
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0

ui_sections = {'app_type'  : 'main_module',
               'load_after': 'search',
               'load_first': False,
<<<<<<< HEAD
               'layout'    :['trailing','top','center'],
               'widgets'   :{ 'tree'   : '',
                              'summary': True,
                              'grid'   : '',
                              'search' : ''
                            }
=======
               'layout'  :['trailing','top','center'],
               'widgets' :{ 'tree'   : '',
                            'summary': True,
                            'grid'   : '',
                            'search' : ''
                          }
>>>>>>> 7267bc2cae01b0396f99de8b8af48c7397d820e0
              }

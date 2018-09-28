################################################################################
# Project : AuShadha
# Description: Search Module Vars
# Date : 13-09-2018
# License : GNU-GPL Version 3, see LICENSE.txt
# Author : Dr. Easwar T.R
################################################################################

from django.urls import reverse

MODULE_IDENTIFIER = 'aushadha-search'
MODULE_LABEL      = 'Search'
VERSION           = 0.01
MODULE_TYPE       = 'main_module'
PARENT_MODULE     = 'aushadha'
DEPENDS_ON        = ['aushadha']

ui_sections = {'app_type'  : 'main_module',
               'load_after': '',   #Explicitly specify this to load after a particular module
               'load_first': True, #Does this UI load before any other ? 
               'layout'    :['trailing','top','center'],
               'widgets'   :{ 'tree'   : ''  , #Does UI get its own tree widget ?
                              'summary': True, #Does UI get its own summary widget ?
                              'grid'   : ''  , #Does UI get its own grid widget ? 
                              'search' : True, #Does UI get its own search widget ?
                              'pane'   : '/AuShadha/search/pane' #Does UI get its own dedicated pane ? 
                          }
              }

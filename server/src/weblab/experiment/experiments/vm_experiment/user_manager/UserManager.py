#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2005-2009 University of Deusto
# All rights reserved.
#
# This software is licensed as described in the file COPYING, which
# you should have received as part of this distribution.
#
# This software consists of contributions made by many individuals, 
# listed below:
#
# Author: Luis Rodriguez <luis.rodriguez@opendeusto.es>
# 

class ConfigureError(Exception):
    """ Configure error of any kind """
    pass

class PermanentConfigureError(ConfigureError):
    """ Configure error that would most likely occur again should we retry """
    pass

class TemporaryConfigureError(ConfigureError):
    """ Configure error that is likely to not be permanent """
    pass

class UserManager(object):
    
    def __init__(self, cfg_manager):
        """
        Creates the UserManager.
        @param cfg_manager Config Manager which will be used to read configuration parameters
        """
        self.cfg = cfg_manager
    
    def configure(self, sid):
        """
        Configures the Virtual Machine for use.
        @note This method may block for a long time. It might hence be advisable to account for this delay
        and to call it from a worker thread. 
        @note Implementations might require additional information, which should generally be provided
        through the configuration script and accessed through the UserManager's config reader.
        @param sid Unique session id of the user.
        @return None
        @raise ConfigureError If the configure attempt failed. Failure and the ConfigureError may be either
        a PermanentConfigureError or a TemporaryConfigureError.
        """
        pass
    
        
        
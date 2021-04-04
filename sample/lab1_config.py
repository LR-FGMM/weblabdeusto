##################################
# Laboratory Server configuration #
##################################

laboratory_assigned_experiments = {
        'exp1:dummy@Dummy experiments' : {
                'coord_address' : 'experiment1:laboratory1@core_host',
                'checkers' : ()
            },
        'exp1:simulador@Simulador experiments' : {
                'coord_address' : 'simulador:laboratory1@core_host',
                'checkers' : (),
                'api' : 2,
                'manages_polling' : True
            },
    }

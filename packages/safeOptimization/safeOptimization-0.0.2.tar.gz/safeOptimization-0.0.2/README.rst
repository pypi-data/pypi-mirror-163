Safe Logarithmic Barrier Method
===============
This package is an implementation of the sLMB in https://arxiv.org/pdf/1912.09478.pdf and the SAFW algorithm. The original paper of SAFW has not published yet. 


Usage
=====

.. code-block:: bash

    >>> import safeOpt
    
    >>> def ask_constraints(x):
        '''will return a list of the values of constraints at x_t'''
        y = [-5 - x[0], -5 - x[1], x[0] - 5, x[1] - 5]
        return y
        
    >>> def ask_objective_func(x):
        '''will return the value of objective function at x_t'''
        y = -1*(x[0] - 1)**3 + 2 -1*(x[0] - 1)**2
        return y**2
        
    >>> model = safeOpt.logBarrier.sLBM(ask_objective_func, ask_constraints, dimension = 2, constraints_number = 4, x_0 = np.array([0,0]))
    >>> model.run()
        

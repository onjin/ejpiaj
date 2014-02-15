Assertions
==========

Assertions are used to check extracted variables against your tests.

Builtin assertions
------------------


### equals / notequals

Example::

    assertions:
      response:
        - 'status_code equals 200'
        - 'status_code notequals 500'

### in / notin

Example::

    assertions:
      response:
        - 'status_code in 200,301,302'
        - 'status_code notin 404,500'

## empty / notempty

Example::

    assertions:
      response:
        - 'contentText empty'
        - 'contentText notempty'

## contains / notcontains

Example::

    assertions:
      response:
        - 'contentText contains Hello'
        - 'contentText notcontains World'

Custom assertions
-----------------

You can easily create your own assertions::


    from ejpiaj.decorators import assertion

    @assertion('equals')
    def equals_assertion(value, params):
        return str(value) == str(params)


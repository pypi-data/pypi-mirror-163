import re as _re
import pregex.pre as _pre
import pregex.exceptions as _exceptions


class __Group(_pre.Pregex):
    '''
    Constitutes the base class for classes "Capture" and "Group".
    '''
    def __init__(self, pre: _pre.Pregex or str, transform) -> _pre.Pregex:
        pattern = transform(__class__._to_pregex(pre))
        super().__init__(pattern, escape=False)


class Capture(__Group):
    '''
    Creates a capturing group out of the provided pattern.

    :param Pregex | str pre: The pattern out of which the capturing group is created.
    :param str name: The name that is assigned to the captured group for backreference purposes. \
        A value of "''" indicates that no name is to be assigned to the group. Defaults to "''".

    :raises NonStringArgumentException: Parameter 'name' is not a string.
    :raises InvalidCapturingGroupNameException: Parameter 'name' is not a valid \
        capturing-group name. Such name must contain word characters only and start \
        with a non-digit character.

    :note:
        - Creating a capturing group out of a capturing group does nothing to it.
        - Creating a capturing group out of a non-capturing group converts it to a capturing group.
        - Creating a named capturing group out of an unnamed capturing group, assigns a name to it.
        - Creating a named capturing group out of a named capturing group, changes the group's name.
    '''

    def __init__(self, pre: _pre.Pregex or str, name: str = ''):
        '''
        Creates a capturing group out of the provided pattern.

        :param Pregex | str pre: The pattern out of which the capturing group is created.
        :param str name: The name that is assigned to the captured group for backreference purposes. \
            A value of "''" indicates that no name is to be assigned to the group. Defaults to "''".

        :raises NonStringArgumentException: Parameter 'name' is not a string.
        :raises InvalidCapturingGroupNameException: Parameter 'name' is not a valid \
            capturing-group name. Such name must contain word characters only and start \
            with a non-digit character.

        :note:
            - Creating a capturing group out of a capturing group does nothing to it.
            - Creating a capturing group out of a non-capturing group converts it to a capturing group.
            - Creating a named capturing group out of an unnamed capturing group, assigns a name to it.
            - Creating a named capturing group out of a named capturing group, changes the group's name.
        '''
        if not isinstance(name, str):
            raise _exceptions.NonStringArgumentException()
        if name != '' and _re.fullmatch("[A-Za-z_]\w*", name) is None:
            raise _exceptions.InvalidCapturingGroupNameException(name)
        super().__init__(pre, lambda pre: pre._capturing_group(name))
        self.name = name


class Group(__Group):
    '''
    Creates a non-capturing group out of the provided pattern.

    :param Pregex | str pre: The expression out of which the non-capturing group is created.

    :note:
        - Creating a non-capturing group out of a non-capturing group does nothing to it.
        - Creating a non-capturing group out of a capturing group converts it to a non-capturing group.
    '''

    def __init__(self, pre: _pre.Pregex or str):
        '''
        Creates a non-capturing group out of the provided pattern.

        :param Pregex | str pre: The expression out of which the non-capturing group is created.

        :note:
            - Creating a non-capturing group out of a non-capturing group does nothing to it.
            - Creating a non-capturing group out of a capturing group converts it to a non-capturing group.
        '''
        super().__init__(pre, lambda pre: pre._non_capturing_group())


class Backreference(__Group):
    '''
    Creates a backreference to some previously declared named capturing group.\
    A backreference matches the same text as the text that was most recently \
    matched by the capturing group with the specified name.

    :param str name: The name of the referenced capturing group.

    :raises NonStringArgumentException: Parameter 'name' is not a string.
    :raises InvalidCapturingGroupNameException: Parameter 'name' is not a valid \
        capturing-group name. Such name must contain word characters only and start \
        with a non-digit character.
    '''

    def __init__(self, name: str):
        '''
        Creates a backreference to some previously declared named capturing group.\
        A backreference matches the same text as the text that was most recently \
        matched by the capturing group with the specified name.

        :param str name: The name of the referenced capturing group.

        :raises NonStringArgumentException: Parameter 'name' is not a string.
        :raises InvalidCapturingGroupNameException: Parameter 'name' is not a valid \
            capturing-group name. Such name must contain word characters only and start \
            with a non-digit character.
        '''
        if not isinstance(name, str):
            raise _exceptions.NonStringArgumentException()
        if _re.fullmatch("[A-Za-z_][A-Za-z_0-9]*", name) is None:
            raise _exceptions.InvalidCapturingGroupNameException(name)
        super().__init__(name, lambda s : f"(?P={s})")

    
class Conditional(__Group):
    '''
    Given the name of a capturing group, matches 'pre1' only if said capturing group has \
    been previously matched. Furthermore, if a second pattern 'pre2' is provided, then this \
    pattern is matched in case the referenced capturing group was not matched, though one \
    should be aware that for this to be possible, the referenced capturing group must be optional.

    :param str name: The name of the referenced capturing group.
    :param Pregex | str pre1: The pattern that is to be matched in case condition is true.
    :param Pregex | str pre2: The pattern that is to be matched in case condition is false. \
        Defaults to "''".

    :raises NonStringArgumentException: Parameter 'name' is not a string.
    :raises InvalidCapturingGroupNameException: Parameter 'name' is not a valid \
        capturing-group name. Such name must contain word characters only and start \
        with a non-digit character.
    '''

    def __init__(self, name: str, pre1: _pre.Pregex or str, pre2: _pre.Pregex or str = ''):
        '''
        Given the name of a capturing group, matches 'pre1' only if said capturing group has\
        been previously matched. Furthermore, if a second pattern 'pre2' is provided, then this \
        pattern is matched in case the referenced capturing group was not matched, though one \
        should be aware that for this to be possible, the referenced capturing group must be optional.

        :param str name: The name of the referenced capturing group.
        :param Pregex | str pre1: The pattern that is to be matched in case condition is true.
        :param Pregex | str pre2: The pattern that is to be matched in case condition is false. \
            Defaults to "''".

        :raises NonStringArgumentException: Parameter 'name' is not a string.
        :raises InvalidCapturingGroupNameException: Parameter 'name' is not a valid \
            capturing-group name. Such name must contain word characters only and start \
            with a non-digit character.
        '''
        if not isinstance(name, str):
            raise _exceptions.NonStringArgumentException()
        if _re.fullmatch("[A-Za-z_][\w]*", name) is None:
            raise _exceptions.InvalidCapturingGroupNameException(name)
        super().__init__(name, lambda s: f"(?({s}){pre1}{'|' + str(pre2) if pre2 != '' else ''})")
from actions import BaseAction

class Action(BaseAction):
    def execute(self, input_string, replace_list):
        # WARNING: Has the potential for cascading replacements. I.E.
        # TODO: Does SXO Also have this behavior?? Find out.
        #
        # replace d with f
        # replace f with x
        # flood -> floof -> xloox
        # Rather than what users probably want which is
        # flood -> floof -> xloof

        for replacement in replace_list:
            input_string = input_string.replace(replacement['replaced_string'], replacement['replacement_string'])

        return {
            'result_string': input_string
        }

    def export(self, input_string, replace_list):
        return ""
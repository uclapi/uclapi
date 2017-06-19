# Storage of the scope map
# The purpose of this setup is that the OAuth scope of any app can be stored in a single field,
# and it can be added to in the future.
# We have a BigIntegerField to work with, which means 64 bits of storage. This translates into
# 64 types of scope, each of which can be checked with a bit mask.
# E.g. roombookings has scope 0, which is 0000000000000000000000000000000000000000000000000000000000000001b.
# This is because the 0th bit (LSB) is set to 1.
# Room bookings + UCLU = 1001b, or a scope number of 11

class Scopes:
    SCOPE_MAP = {
        "roombookings": (0, "Private room bookings data"),
        "timetable": (1, "Private timetable data"),
        "uclu": (2, "Private UCLU data"),
        "moodle": (3, "Private Moodle data")
    }

    # Add a scope to the scope number given and return the new number
    def add_scope(self, current, scope_name):
        try:
            scope_shift = self.SCOPE_MAP[scope_name][0]
        except KeyError:
            return current

        return (current | (1 << scope_shift))

    # Check whether a scope is present in the current scope number given
    def check_scope(self, current, scope_name):
        try:
            scope_shift = self.SCOPE_MAP[scope_name][0]
        except KeyError:
            return False

        return ((1 << scope_shift) & current) > 0

    # Remove a scope from the current scope number
    def remove_scope(self, current, scope_name):
        try:
            scope_shift = self.SCOPE_MAP[scope_name][0]
        except KeyError:
            return current

        if current & 1 << scope_shift > 0:
            return ~(~current + (1 << scope_shift))
        else:
            return current

    # Produce a dictionary with the scope information. Example:
    # {
    #    "roombookings": True,
    #    "timetable": False,
    #    ...
    # }
    def scope_dict(self, current, pretty_print=True):
        scopes = []
        for x in self.SCOPE_MAP.keys():
            if self.check_scope(current, x):
                if pretty_print:
                    scope = {
                        "name": x,
                        "description": self.SCOPE_MAP[x][1]
                    }
                else:
                    scope = {
                        "name": x,
                        "description": self.SCOPE_MAP[x][0]
                    }

                scopes.append(scope)
        return scopes

    # Get available scopes for showing to the user
    def get_all_scopes(self, pretty_print=True):
        scopes = []
        for x in self.SCOPE_MAP.keys():
            if pretty_print:
                scope = {
                    "name": x,
                    "description": self.SCOPE_MAP[x][1]
                }
            else:
                scope = {
                    "name": x,
                    "description": self.SCOPE_MAP[x][0]
                }

            scopes.append(scope)
        return scopes
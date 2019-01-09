"""
UCL Academic Modelling Project
Fast Code Processing
"""

STUDENT_TYPES = {
    'A': "Campus-based, numeric mark scheme",
    'B': "Campus-based, non-numeric mark scheme",
    'C': "Distance learner, numeric mark scheme",
    'D': "Distance learner, non-numeric mark scheme",
    'E': "MBBS Resit"
}


class InvalidAMPCodeException(Exception):
    pass


class ModuleDelivery:
    def __init__(self, delivery_code):
        # Sanity check the code we have
        if len(delivery_code) != 3:
            raise InvalidAMPCodeException("Delivery code is too long")
        if delivery_code[0] in STUDENT_TYPES:
            self.student_type = STUDENT_TYPES[delivery_code[0]]
        else:
            raise InvalidAMPCodeException("Student type is not valid")
        self.fheq_level = int(delivery_code[1])
        self.undergraduate = delivery_code[2] == 'U'

    def get_delivery(self):
        return {
            "fheq_level": self.fheq_level,
            "is_undergraduate": self.undergraduate,
            "student_type": self.student_type
        }


class ModulePeriods:
    # Default Attributes
    term_1 = False
    term_2 = False
    term_3 = False
    term_4 = False  # Term 1 of the next academic year
    summer = False  # Summer Teaching Period
    summer_school = False  # UCL Summer School
    summer_school_1 = False  # UCL Summer School Session 1
    summer_school_2 = False  # UCL Summer School Session 2
    lsr = False  # Late Summer Resit period
    year = False  # Whole year module

    def __init__(self, periods_code):
        if periods_code == 'YEAR':
            self.term_1 = True
            self.term_2 = True
            self.term_3 = True
            self.year = True
        elif periods_code == 'SUMMER':
            self.summer = True
        elif periods_code == 'LSR':
            self.lsr = True
        elif periods_code[0] == 'S':
            # Summer School periods start with an S.
            # S1, S2, S1+2
            self.summer_school = True
            if periods_code == 'S1':
                self.summer_school_1 = True
            elif periods_code == 'S2':
                self.summer_school_2 = True
            elif periods_code == 'S1+2':
                self.summer_school_1 = True
                self.summer_school_2 = True
            else:
                raise InvalidAMPCodeException(
                    "An invalid AMP code was found: " + periods_code
                )
        elif periods_code[0] == 'T':
            # Normal classes start with a T for Term
            if periods_code == 'T1':
                self.term_1 = True
            elif periods_code == 'T1/2':
                self.term_1 = True
                self.term_2 = True
            elif periods_code == 'T1/2/3':
                self.term_1 = True
                self.term_2 = True
                self.term_3 = True
            elif periods_code == 'T1/3':
                self.term_1 = True
                self.term_3 = True
            elif periods_code == 'T2':
                self.term_2 = True
            elif periods_code == 'T2/3':
                self.term_2 = True
                self.term_3 = True
            elif periods_code == 'T2/3/S' or periods_code == 'T2/3/4':
                self.term_2 = True
                self.term_3 = True
                self.summer = True
            elif periods_code == 'T3':
                self.term_3 = True
            elif periods_code == 'T3/1':
                self.term_3 = True
                self.term_4 = True
            elif periods_code == 'T3/S' or periods_code == 'T3/4':
                self.term_3 = True
                self.summer = True
            elif periods_code == 'T4':
                self.term_4 = True
            else:
                raise InvalidAMPCodeException(
                    "AMP Periods Code contained an invalid term element"
                )
        else:
            raise InvalidAMPCodeException(
                "An invalid AMP code was found: " + periods_code
            )

    def get_periods(self):
        return {
            "teaching_periods": {
                "term_1": self.term_1,
                "term_2": self.term_2,
                "term_3": self.term_3,
                "term_1_next_year": self.term_4,
                "summer": self.summer
            },
            "year_long": self.year,
            "lsr": self.lsr,
            "summer_school": {
                "is_summer_school": self.summer_school,
                "sessions": {
                    "session_1": self.summer_school_1,
                    "session_2": self.summer_school_2
                }
            }
        }


class ModuleInstance:
    def __init__(self, amp_code):
        """
        An AMP Code is stored as the INSTID in CMIS.
        It looks something like this: A6U-T1/2
        """
        parts = amp_code.split('-')
        module_delivery_code = parts[0]  # A6U
        periods_code = parts[1]  # T1/2

        self.delivery = ModuleDelivery(module_delivery_code)
        self.periods = ModulePeriods(periods_code)

#
# Protocol class
#

# What to do:
# - give a delivery = "subcutaneous" or "intravenous" 
# - The dose function Dose(t) = dose_function, which could consist of :
#                                                                       - instantaneous doses of X ng of the drug at one or more time points 
#                                                                       - steady application of X ng per hour over a given time period, 
#                                                                       - or some combination.


class Protocol:
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------

    type_dosing: string, optional
                 "intravenous" or "subcutaneous"
                 Defines the way we inject the drug: intravenous or subcutaneous 

                 
    instantaneous_application: dictionnary, optionnal
                               {time point : dose injected at this timepoint}
                               Defines the instantaneous injections of specific doses of X ng of the drug at one or more time points


    steady_application: list, optionnal
                        [Timepoint_0, Timepoint_1]
                        Defines the timepoints of the beginning and the end of the steady application
    
                        
    steady_dose = numeric, optionnal
                   Defines the amount of drug injected through the steady application, between Timepoint_0 and Timepoint_1

    """
    def __init__(self, type_dosing = "intravenous", instantaneous_application = {}, steady_application = [0, 1], steady_dose = 0):
        self.type_dosing = type_dosing
        self.instantaneous_application = instantaneous_application
        self.steady_application = steady_application
        self.steady_dose = steady_dose


    def __call__(self, t):
        """ A method giving the Dose(t) function

        Parameters
        ----------
        t: float
           time
        """

        if self.steady_application[0] < t < self.steady_application[1] :
            return self.steady_dose
        else:
            return 0
        

        


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

                 
    instantaneous_application: list of tuples, optionnal
                               [(time point : dose injected at this timepoint)]
                               Defines the instantaneous injections of specific doses of X ng of the drug at one or more time points


    steady_application: list, optionnal
                        [Timepoint_0, Timepoint_1]
                        Defines the timepoints of the beginning and the end of the steady application
    
                        
    steady_dose = numeric, optionnal
                   Defines the amount of drug injected through the steady application, between Timepoint_0 and Timepoint_1

    """
    def __init__(self, type_dosing = "intravenous", instantaneous_application = [], steady_application = [t0 = 0, t1 = 1], steady_dose = 0):
        self.type_dosing = type_dosing
        self.instantaneous_application = instantaneous_application
        self.steady_application = steady_application
        self.steady_dose = steady_dose


    def sort_instanteneous_application(self, t0 = 0):
        """ A method to sort the instantenous application list according to the time 
            and giving the index of the current application in this list 

        Parameters
        ----------

        t0: float, optionnal
            beginning of the experiement
        
        
        """

        self.instantaneous_application.sort()
        while self.instantaneous_application[0] < t0:
            self.current += 1
    

    def next_application(self):
        """ A method updating the index of the application from the instantaneous_application list over time
            
        """

        if self.current >= len(self.instantaneous_application):
            return (None, None)
        self.current += 1
        return self.instantaneous_application[self.current-1]
    


    def dose_function(self, t):
        """ A method giving the Dose(t) function for the steady application 

        Parameters
        ----------
        t: float
           time
        """

        if self.steady_application[0] < t < self.steady_application[1] :
            return self.steady_dose
        else:
            return 0
        

        


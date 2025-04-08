# --------------------------------------------------
#  Optimization Model for School Demostrator
#  Barbosa, J. (2025)
#  mail@juliabarbosa.net
# --------------------------------------------------

# Importing Libraries
import pyomo.environ as pyo
from pyomo.dataportal import DataPortal
from pathlib import Path
import json, os

import pandas as pd

OPT_DEBUG = False  # Debugging flag


def get_abstract_pyomo_model(fix_capacities=False):
    # TODO: Debug storage euqations once ir can be run with storage.

    model = pyo.AbstractModel()

    ## Sets
    model.T = pyo.Set(ordered=True)  # Times
    model.N = pyo.Set()  # Nodes

    model.H = pyo.Set()  # Technologies

    model.U = pyo.Set(within=model.H * model.N)  # Technologies at nodes

    ## Parameters ##
    model.is_consumer = pyo.Param(model.H, default=0)  # Is Consumer
    model.is_producer = pyo.Param(model.H, default=0)  # Is Generator
    model.is_storage = pyo.Param(model.H, default=0) # Is Storage
    model.record_curtailment = pyo.Param(model.H, default=0)  # Record curtailment 

    model.capacity_cost = pyo.Param(model.H, default=0)  # Capacity Cost
    model.operational_cost = pyo.Param(model.H, default=0)  # Operational Cost
    model.operational_lifetime = pyo.Param(model.H, default=100)  # Operational Lifetime
    model.energy_capacity = pyo.Param(model.H, model.N, default=0) # Storage energy capacity! Energy units
 
    model.demand_profile = pyo.Param(model.H, model.T)  # Demand Profile
    model.yearly_demand = pyo.Param(model.H, default=0)  # Yearly Demand

    model.availability_profile = pyo.Param(
        model.H, model.T, default=1
    )  # Availability Profile

    model.installed_capacity = pyo.Param(
        model.H, model.N, default=0
    )  # Installed Capacity --> rhis are the sliders values in the frontend

    ## Dynamic Sets
    model.Ug = pyo.Set(
        within=model.U,
        initialize=lambda model: [(h, n) for (h, n) in model.U if model.is_producer[h]],
    )  # Generators
    model.Uc = pyo.Set(
        within=model.U,
        initialize=lambda model: [(h, n) for (h, n) in model.U if model.is_consumer[h]],
    )  # Consumers

    model.Us = pyo.Set(
        within=model.U, 
        initialize=lambda model: [(h,n) for (h,n) in model.U if model.is_storage[h]],
    ) # Storage Units

    model.UgRE = pyo.Set(
        within=model.Ug,
        initialize=lambda model: [(h, n) for (h, n) in model.Ug if model.record_curtailment[h]],
    )  # Generators that record curtailment --> Renewable Energy!

    ## Variables ##

    # Cost Variables
    model.OPEX = pyo.Var()  # Operational Expenditure
    model.CAPEX = pyo.Var()  # Capital Expenditure
    model.TOTEX = pyo.Var()  # Total Expenditure #send to frontend
    model.PENALTY = pyo.Var()  # Penalty for not satisfying demand

    # Power Variables
    model.YearFactor = pyo.Var() # Year factor
    model.Pg = pyo.Var(model.Ug|model.Us, model.T, within=pyo.NonNegativeReals) 
    model.Pd = pyo.Var(model.Uc|model.Us, model.T, within=pyo.NonNegativeReals)  
    
    # Demand not satisfied
    model.nSPd = pyo.Var(model.Uc, model.T, within=pyo.NonNegativeReals) # Curtailed demand
    model.nSPg = pyo.Var(model.UgRE, model.T, within=pyo.NonNegativeReals) # Curtailed generation


    # Storage energy level
    model.Es = pyo.Var(model.Us, model.T, within=pyo.NonNegativeReals)  

     # Power injection returned as Node1(values(T1,T2...))
    model.Pi = pyo.Var(model.N, model.T) 

    model.Cg = pyo.Var(model.Ug, within=pyo.NonNegativeReals)  # Generation Capacity
    model.Ecap = pyo.Var(model.Us, within=pyo.NonNegativeReals) # Storage Max energy capacity! -> slider value
    
    # e.g x^2 function, around 0 being best
    model.EnergySupTot= pyo.Var() # Total energy supplied
    model.UnmetDemand = pyo.Var() # Unmet demand
    ## Equations ##

    # Objective Function
    model.obf = pyo.Objective(expr=model.TOTEX, sense=pyo.minimize)

    # Cost Equations
    def totex_rule(model):
        return model.TOTEX == model.CAPEX + model.OPEX + model.PENALTY

    model.totex_eq = pyo.Constraint(rule=totex_rule)

    def penalty_rule(model):
        pfac = 1e6
        return model.PENALTY == sum(
            model.nSPd[h, n, t] * pfac for (h, n) in model.Uc for t in model.T
        )
    model.penalty_eq = pyo.Constraint(rule=penalty_rule)

    def capex_rule(model):
        # Capex already normalized by lifetime
        return model.CAPEX == sum(
            model.Cg[h, n] * model.capacity_cost[h] / model.operational_lifetime[h]
            for h in model.H
            for n in model.N
            if (h, n) in model.Ug
        )
    model.capex_eq = pyo.Constraint(rule=capex_rule)

    def opex_rule(model):
        # Cost on the modelled time period
        period_cost = sum(
            model.Pg[h, n, t] * model.operational_cost[h]
            for h in model.H
            for n in model.N
            if (h, n) in model.Ug
            for t in model.T
        )
        # Extrapolated for full year
        factor = 24 * 365 / len(model.T)
        return model.OPEX == period_cost * factor
    model.opex_eq = pyo.Constraint(rule=opex_rule)

    # Power Balance Equations
    def global_power_balance_rule(model, t):
        return sum(model.Pi[n, t] for n in model.N) == 0
    model.global_power_balance_eq = pyo.Constraint(
        model.T, rule=global_power_balance_rule
    )

    def local_power_balance_rule(model, n, t):
        production = sum(model.Pg[h, n, t] for h in model.H if (h, n) in model.Ug)
        consumption = sum(model.Pd[h, n, t] for h in model.H if (h, n) in model.Uc)
        return production - consumption == model.Pi[n, t]
    model.local_power_balance_eq = pyo.Constraint(
        model.N, model.T, rule=local_power_balance_rule
    )

    # Energy Supplied
    def energy_supplied_rule(model):
         year_factor = 24 * 365 / len(model.T) 
         return model.EnergySupTot == sum(model.Pd[h,n,t] for (h,n) in model.Uc for t in model.T)*year_factor
    model.energy_supplied_eq = pyo.Constraint(rule=energy_supplied_rule)

    # Unmet Demand
    def unmet_demand_rule(model):
        return model.UnmetDemand == sum(model.nSPd[h,n,t] for (h,n) in model.Uc for t in model.T)
    model.unmet_demand_eq = pyo.Constraint(rule=unmet_demand_rule)
   
    # Capacity Equations
    # If fix capacity is set, then we fix the capacity to the given value -- > those are the slider values in the frontend!
    if fix_capacities:

        def fix_capacity_rule(model, h, n):
            return model.Cg[h, n] == model.installed_capacity[h, n]

        model.fix_capacity_eq = pyo.Constraint(model.Ug, rule=fix_capacity_rule)

        #Original code but throws errors ValueError: Invalid constraint expression. The constraint expr
        #added Ecap parameters to fix
        def fix_storage_capactiy_rule(model, h, n):
            return model.Ecap[h,n] == model.energy_capacity[h,n] #added Ecap parameter
        model.fix_storage_capacity_eq = pyo.Constraint(model.Us,rule=fix_storage_capactiy_rule) 

    # Constraint capacity from given data ( OR NOT if we want to know the final solution)
    def capacity_rule(model, h, n, t):
        return model.Pg[h, n, t] <= model.Cg[h, n]

    model.capacity_eq = pyo.Constraint(model.Ug, model.T, rule=capacity_rule)

    # Storage Equations 
    def storage_operation_rule(model, h, n, t ): 
        if t == model.T.first():
            return model.Es[h,n,t] == model.Es[h,n,model.T.last()] + model.Pd[h,n,t] - model.Pg[h,n,t]
        else:
            return model.Es[h,n,t] == model.Es[h,n,t-1] + model.Pd[h,n,t] - model.Pg[h,n,t]
    model.storage_operation_eq = pyo.Constraint(model.Us, model.T, rule=storage_operation_rule)

    def max_storage_energy_level_rule(model, h,n,t):
        return model.Es[h,n,t] <= model.Ecap[h,n]
    model.storage_max_cap_eq = pyo.Constraint(model.Us, model.T, rule=max_storage_energy_level_rule)

    def year_factor_rule(model):
        return model.YearFactor == 24 * 365 / len(model.T)
    model.year_factor_eq = pyo.Constraint(rule=year_factor_rule)


    # Load Profiles
    def demand_profile_rule(model, h, n, t):
        year_factor = 24 * 365 / len(model.T)
        try:
            return (
                model.Pd[h, n, t] + model.nSPd[h, n, t]
                == (model.yearly_demand[h] / year_factor) * model.demand_profile[h, t]
            )
        except ValueError:
            if OPT_DEBUG:
                print("No demand profile for technology ", h, " Skipping constraint")
            return pyo.Constraint.Skip

    model.demand_profile_eq = pyo.Constraint(model.Uc, model.T, rule=demand_profile_rule)

    def demand_yearly_rule(model, h, n):
        year_factor = 24 * 365 / len(model.T)
        return (
            sum(model.Pd[h, n, t] + model.nSPd[h, n, t] for t in model.T)
            == model.yearly_demand[h] / year_factor
        )
    # Commentd out because if every consumer has demand profile, this constraint is not needed anymore-> adding it could render the model infeasible
    #model.demand_yearly_eq = pyo.Constraint(model.Uc, rule=demand_yearly_rule)

    def availability_profile_rule(model, h, n, t):
        return model.Pg[h, n, t] + model.nSPg[h,n,t] == model.Cg[h, n] * model.availability_profile[h, t]

    model.availability_profile_eq = pyo.Constraint(
        model.UgRE, model.T, rule=availability_profile_rule
    )

    return model

def load_input(model, dat_file="test.dat"):
    # Get the absolute path of the .dat file in the current folder
    dat_file_path = Path(__file__).parent / dat_file

    if not dat_file_path.exists():
        raise FileNotFoundError(f"Data file '{dat_file_path}' not found.")

    data = pyo.DataPortal()
    data.load(filename=str(dat_file_path))

    instance = model.create_instance(data)
    return instance

def load_input_from_temp_file(model, dat_file_path):
    """
    Loads a Pyomo model from a temporary .dat file.
    """
    if not os.path.exists(dat_file_path):
        raise ValueError(f"Error: The temporary file {dat_file_path} does not exist!")

    print(f"DEBUG: Loading .dat file from {dat_file_path}")

    data = pyo.DataPortal()

    try:
        data.load(filename=dat_file_path)  # Load data from file
        instance = model.create_instance(data)
        return instance  # Return the Pyomo model instance

    finally:
        os.remove(dat_file_path)  # Ensure cleanup even if an error occurs
        print(f"DEBUG: Temp file {dat_file_path} deleted.")

def solve_instance(model_instance):
    solver = pyo.SolverFactory("glpk")
    results = solver.solve(model_instance, tee=True)

    return model_instance

def get_variable_value(instance, var_name):
    """Returns a list with the values of a variable"""
    var = getattr(instance, var_name)
    ret = [pyo.value(x) for x in var.values()]
    return ret

def get_indexed_variable_value(instance, var_name, index_names=None):
    """Returns a list with the values of a variable as a pandas DataFrame
    
      Example usage:
      model.get_indexed_variable_value(instance, "Pg", index_names=["H", "Node", "T"])

      Args:
         instance: Pyomo instance
         var_name: Name of the variable
         index_names: Names of the indexes in the DataFrame

      Returns:
         DataFrame with the values of the variable
    
   """

    indexes = getattr(instance, var_name).index_set()
    ret = []
    for idx in indexes:
         var = getattr(instance, var_name)[idx]
         ret.append( (*idx, pyo.value(var)))
    
    if index_names is not None:
        df = pd.DataFrame(ret, columns=index_names + [var_name])
    else:
         df = pd.DataFrame(ret)
    return df

if __name__ == "__main__":
    model = get_abstract_pyomo_model()
    instance = load_input(model)
    instance = solve_instance(instance)

    pass

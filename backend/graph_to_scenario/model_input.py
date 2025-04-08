# --------------------------------------------------
#  .DAT File Parser
#  Barbosa, J. (2024)
#  mail@juliabarbosa.net
# --------------------------------------------------

import math
from typing import Any
import numpy as np
from . import node_types
from pathlib import Path
from abc import ABC, abstractmethod
import tempfile


## -- Abstract Parser Class, can be used to parse .dat files --##
class ModelSet:
    def __init__(self, name: str, dim: int):
        self.name: str = name
        self.dim: int = dim
        self.val = []

    def write(self, f):
        f.write(f"set {self.name} := \n")
        for v in self.val:
            if self.dim > 1:
                f.write(" ".join(str(vv) for vv in v) + "\n")
            else:
                f.write(f"{v} \n")
        f.write("; \n\n")

    def __repr__(self) -> str:
        return f"SET:{self.name}"

class ModelParam:
    """
    Parameter Class
    """

    def __init__(self, name, set_list: list[ModelSet], scaling_factor=1, model=None):
        self.name = name
        self.set_list = set_list
        self.dim: int = 0
        self.set_names = []
        self.model = model

        for s in set_list:
            self.dim = self.dim + s.dim
            self.set_names.append(s.name)
        self.vals = dict()
        self.sf = scaling_factor

    def add_value(self, value, key=None):
        # Add new value
        if self.dim == 0:
            self.vals = value * self.sf
        else:
            key = self.is_key_valid(key)
            nkey = " ".join([str(x) for x in key])
            self.vals[str(nkey)] = value * self.sf

    def is_key_valid(self, key):
        # Verify if key is a valid key
        # verify if the is a list/tuple
        if not isinstance(key, (list, tuple)):
            # assume it is a single value
            key = [key]

        if len(key) != self.dim:
            raise ValueError(
                "%s is invalid  for parameter %s -  Invalid Key size!"
                % (key, self.name)
            )

        return key

    def write(self, f):
        if not self.vals:
            return
        
        f.write(f'param {self.name}')

        if self.dim == 0:
            f.write(f' := {self.vals}\n')

        elif self.dim == 1:
            f.write(" := \n")
            # Write each value in one line
            for key, value in self.vals.items():
                if not math.isnan(value):
                    f.write(f'{key} {value}\n')

        elif self.dim == 2: 
            pass
            f.write(" : ")
            # Write in table format, X are rows, Y are columns
            get_key = lambda key,pos: key.split(" ")[pos]
            rows = list(set(get_key(k,0) for k in self.vals.keys()))
            cols = list(set(get_key(k,1) for k in self.vals.keys()))
            try: 
                #cols = sorted(cols)
                cols = sorted(cols, key=lambda y: int(y))
            except ValueError:
                pass

            f.write(" ".join(str(c) for c in cols) + " :=\n")
            for r in rows:
                f.write(f"{r} ")
                for c in cols:
                    pos = " ".join([r,c])
                    f.write(f"{self.vals.get(pos, 0):.6f} ")
                f.write("\n")

        elif self.dim >= 3:
            raise ValueError(f"Parameter {self.name} has a dimension greater than 2. Pyomo does not support this!")             
       
        f.write(";\n\n")  # Ensure a semicolon at the end of normal parameters

class AbstractModelInput(ABC):
    def __init__(self) -> None:
        self._sets = []
        self._params = []

        self._init_structure()

    @property
    def sets(self):
        return self._sets

    @property
    def _set_names(self):
        return [s.name for s in self.sets]

    @property
    def params(self):
        return self._params

    @property
    def _param_names(self):
        return [p.name for p in self.params]

    @abstractmethod
    def _init_structure(self):
        """
        In this method, the user should define the structure of the model. Clearly definning
        which sets and parameters are needed. Note that parameters and sets must not be initially populated
        """
        pass

    def get_set(self, name: str):
        for s in self._sets:
            if s.name == name:
                return s
        return None

    def get_param(self, name: str):
        for p in self._params:
            if p.name == name:
                return p
        return None

    def __getitem__(self, key: str):
        if key in self._set_names:
            return self.get_set(key)
        if key in self._param_names:
            return self.get_param(key)
        else:
            raise ValueError(
                f"Key {key} not found in the model. Are you sure it is a valid set or parameter?"
            )

    def add_set(self, name: str, dim: int):
        s = ModelSet(name, dim)
        self._sets.append(s)
        return s

    def add_param(self, name: str, set_list: list[ModelSet], scaling_factor=1):
        p = ModelParam(name, set_list, scaling_factor, model=self)
        self._params.append(p)
        return p

    def write(self, file: str):
        script_dir = (
            Path(__file__).resolve().parent
        )  # Get the directory where the script is located
        file_path = script_dir / file  # Construct the full file path

        with file_path.open("w") as f:  # Use Path's open() method
            for s in self._sets:
                s.write(f)
            for p in self._params:
                p.write(f)  # This calls the updated ModelParam.write method

    def save_to_temp_file(self):
        """
        Saves the .dat file content to a temporary file and returns its path.
        """
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".dat", mode="w", encoding="utf-8")

        try:
            for s in self._sets:
                s.write(temp_file)
            for p in self._params:
                p.write(temp_file)

            temp_file.flush()  # Ensure all data is written
            return temp_file.name  # Return the file path

        finally:
            temp_file.close()  # Close file so Pyomo can read it

    def get_paramnames_indexed_by_set(self, set_name):
        """
        Set name can either be a list or a single string
        """
        if not isinstance(set_name, list):
            set_name = [set_name]
        
        ret = [p.name for p in self._params if p.set_names == set_name]

        return ret
    pass

class OptNetworkInput(AbstractModelInput):

    def _init_structure(self):
        # Dictoionary of sets:dimension
        # H: tech, T: timesteps, U:(NodeId,Tech),N NodeId,
        sets = dict(T=1, N=1, H=1, U=2)

        for k, v in sets.items():
            self.add_set(k, v)

        # Dictionary of parameters: pname:set_list
        params = dict(
            capacity_cost=[self["H"]],
            operational_cost=[self["H"]],
            operational_lifetime=[self["H"]],
            demand_profile=[self["H"], self["T"]],
            yearly_demand=[self["H"]],
            is_consumer=[self["H"]],
            is_producer=[self["H"]],
            is_storage=[self["H"]],
            record_curtailment=[self["H"]],
            availability_profile=[self["H"], self["T"]],
            installed_capacity =[self["H"], self["N"]], #slider values
            energy_capacity =[self["H"], self["N"]], #battery 
        )

        for k, v in params.items():
            self.add_param(k, v)
        pass

    # Takes the list generated from scenario and prepares it for conversion to .dat
 
    def populate_from_scenario_list(self, scenario_list: list, timesteps: list[int]):

        # Populate timesteps
        
        
        nodes = set()
        technologies = set()
        tech_node_pairs = set()  # <-- Collect (tech, node_id) pairs

        for item in scenario_list:
            # Handle Timesteps first to avoid AttributeError
            if isinstance(item, node_types.Timesteps):
                if hasattr(item, "timesteps"):
                    self["T"].val = list(range(1,len(timesteps)+1))  # Use the correct attribute name
                continue  # Skip the rest of the loop for Timesteps

            node_id = item.node_id
            tech = item.technology
            nodes.add(node_id)
            technologies.add(tech)
            
            # Collect the actual tech-node relationship
            tech_node_pairs.add((tech, node_id))  # <-- Track only relevant pairs

            # Populate H parameters
            pnames = self.get_paramnames_indexed_by_set("H")
            for pname in pnames:
                if hasattr(item, pname):
                    self[pname].add_value(getattr(item, pname), tech)
            
            # Populate H, T parameters
            pnames = self.get_paramnames_indexed_by_set(["H", "T"])
            for pname in pnames:
                if hasattr(item, pname):
                    for t, value in enumerate(getattr(item, pname)):
                        self[pname].add_value(float(value), (tech, t+1)) #+1 added for 1-indexing instead of 0-indexing
            
            # Populate H, N parameters
            pnames = self.get_paramnames_indexed_by_set(["H", "N"])
            for pname in pnames:
                if hasattr(item, pname):
                    self[pname].add_value(getattr(item, pname), (tech, node_id))

        # Populate sets
        self["N"].val = list(nodes)
        self["H"].val = list(technologies)
        # Populate U with actual tech-node pairs
        self["U"].val = list(tech_node_pairs)  # <-- Use only the pairs that actually occur


if __name__ == "__main__":
    pass

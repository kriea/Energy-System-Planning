class Producer:
    """
    A class to represent a Producer node in the energy system.

    Attributes:
    ----------
    node_id : str
        Unique identifier for the node.
    technology : str
        Type of technology used by the producer.
    capacity_cost : float
        Cost associated with the capacity of the producer.
    operational_cost : float
        Cost associated with the operation of the producer.
    operational_lifetime : int
        Operational lifetime of the producer in years.
    availability_profile : list
        Availability profile of the producer.
    installed_capacity : float
        Installed capacity of the producer.
    record_curtailment : bool
        Flag to record curtailment.
    is_producer : int
        Flag to indicate the node is a producer.
    """
    def __init__(
        self,
        node_id,
        technology,
        capacity_cost,
        operational_cost,
        operational_lifetime,
        availability_profile,
        installed_capacity, 
        record_curtailment, 
    ):
        """
        Constructs all the necessary attributes for the Producer object.

        Parameters:
        ----------
        node_id : str
            Unique identifier for the node.
        technology : str
            Type of technology used by the producer.
        capacity_cost : float
            Cost associated with the capacity of the producer.
        operational_cost : float
            Cost associated with the operation of the producer.
        operational_lifetime : int
            Operational lifetime of the producer in years.
        availability_profile : list
            Availability profile of the producer.
        installed_capacity : float
            Installed capacity of the producer.
        record_curtailment : bool
            Flag to record curtailment.
        """
        self.node_id = node_id
        self.technology = technology
        self.capacity_cost = capacity_cost
        self.operational_cost = operational_cost
        self.operational_lifetime = operational_lifetime
        self.availability_profile = availability_profile
        self.installed_capacity = installed_capacity #slider value
        self.record_curtailment = record_curtailment
        self.is_producer = 1

    def __repr__(self):
        """
        Returns a string representation of the Producer object.

        Returns:
        -------
        str
            String representation of the Producer object.
        """
        return (
            f"Producer(node_id={self.node_id}, technology={self.technology}, "
            f"capacity_cost={self.capacity_cost}, "
            f"operational_cost={self.operational_cost}, operational_lifetime={self.operational_lifetime}, "
            f"availability_profile={self.availability_profile}, "
            f"installed_capacity={self.installed_capacity}, " 
            f"record_curtailment={self.record_curtailment},"
            f"is_producer={self.is_producer},"
            ")"
        )


class Consumer:
    """
    A class to represent a Consumer node in the energy system.

    Attributes:
    ----------
    node_id : str
        Unique identifier for the node.
    technology : str
        Type of technology used by the consumer.
    yearly_demand : float
        Yearly demand of the consumer.
    demand_profile : list
        Demand profile of the consumer.
    is_consumer : int
        Flag to indicate the node is a consumer.
    """
    def __init__(self, node_id, technology, yearly_demand, demand_profile):
        """
        Constructs all the necessary attributes for the Consumer object.

        Parameters:
        ----------
        node_id : str
            Unique identifier for the node.
        technology : str
            Type of technology used by the consumer.
        yearly_demand : float
            Yearly demand of the consumer.
        demand_profile : list
            Demand profile of the consumer.
        """
        self.node_id = node_id
        self.technology = technology
        self.yearly_demand = yearly_demand
        self.demand_profile = demand_profile
        self.is_consumer = 1
    

    def __repr__(self):
        """
        Returns a string representation of the Consumer object.

        Returns:
        -------
        str
            String representation of the Consumer object.
        """
        return (
            f"Consumer(node_id={self.node_id}, technology={self.technology}, "
            f"yearly_demand={self.yearly_demand}, "
            f"demand_profile={self.demand_profile}," 
            f"is_consumer={self.is_consumer},"
            ")"
        )


class Battery:
    """
    A class to represent a Battery node in the energy system.

    Attributes:
    ----------
    node_id : str
        Unique identifier for the node.
    technology : str
        Type of technology used by the battery.
    energy_capacity : float
        Energy capacity of the battery.
    installed_capacity : float
        Installed capacity of the battery.
    is_storage : int
        Flag to indicate the node is a storage.
    """
    def __init__(self, node_id, technology, energy_capacity,installed_capacity):
        """
        Constructs all the necessary attributes for the Battery object.

        Parameters:
        ----------
        node_id : str
            Unique identifier for the node.
        technology : str
            Type of technology used by the battery.
        energy_capacity : float
            Energy capacity of the battery.
        installed_capacity : float
            Installed capacity of the battery.
        """
        self.node_id = node_id
        self.technology = technology
        self.energy_capacity = energy_capacity
        self.installed_capacity = installed_capacity #slider value
        self.is_storage = 1

    def __repr__(self):
        """
        Returns a string representation of the Battery object.

        Returns:
        -------
        str
            String representation of the Battery object.
        """
        return (
            f"Battery(node_id={self.node_id}, technology={self.technology}, "
            f"energy_capacity={self.energy_capacity},"
            f"installed_capacity={self.installed_capacity},"
            f"is_storage={self.is_storage},"
            ")"
        )


class Timesteps:
    """
    A class to represent the Timesteps in the energy system.

    Attributes:
    ----------
    timesteps : list
        List of timesteps.
    """
    def __init__(self, timesteplist):
        """
        Constructs all the necessary attributes for the Timesteps object.

        Parameters:
        ----------
        timesteplist : list
            List of timesteps.
        """
        self.timesteps = timesteplist

    def __repr__(self):
        """
        Returns a string representation of the Timesteps object.

        Returns:
        -------
        str
            String representation of the Timesteps object.
        """
        return(f"Timesteps({self.timesteps})")

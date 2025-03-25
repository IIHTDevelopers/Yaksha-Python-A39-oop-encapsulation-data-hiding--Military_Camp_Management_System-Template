"""
Military Training Camp Management System - Solution version for demonstrating encapsulation.
"""

from abc import ABC, abstractmethod
from datetime import datetime


class AccessDeniedException(Exception):
    """Exception raised when a user attempts unauthorized access."""
    pass


class InvalidDataException(Exception):
    """Exception raised when input data fails validation."""
    pass


class MilitaryPersonnel(ABC):
    """Abstract base class representing military personnel."""
    
    personnel_count = 0
    
    def __init__(self, id, name, rank, unit):
        # Protected attributes (single underscore)
        self._id = id
        self._name = name
        self._rank = rank
        self._unit = unit
        
        # Private attributes (double underscore)
        self.__security_clearance = 1
        self.__performance_records = []
        
        # Class variable to track instances
        MilitaryPersonnel.personnel_count += 1
    
    def __del__(self):
        # Clean up when instance is deleted
        MilitaryPersonnel.personnel_count -= 1
    
    # Properties for accessing protected attributes
    @property
    def id(self):
        return self._id
    
    @property
    def name(self):
        return self._name
    
    @property
    def rank(self):
        return self._rank
    
    @rank.setter
    def rank(self, value):
        # Example of data validation in setter
        valid_ranks = ["Private", "Corporal", "Sergeant", "Lieutenant", "Captain", "Major", "Colonel", "General"]
        if value in valid_ranks:
            self._rank = value
        else:
            raise InvalidDataException(f"Invalid rank: {value}")
    
    @property
    def unit(self):
        return self._unit
    
    @unit.setter
    def unit(self, value):
        # Data validation for unit name
        if len(value) >= 3:  # Unit name must be at least 3 characters
            self._unit = value
        else:
            raise InvalidDataException(f"Invalid unit name: {value}")
    
    # Property for private attribute with controlled access
    @property
    def security_clearance(self):
        return self.__security_clearance
    
    # Setter for security clearance using tuple format (for test compatibility)
    @security_clearance.setter
    def security_clearance(self, args):
        if isinstance(args, tuple) and len(args) == 2:
            new_level, authorizing_officer = args
            self.update_security_clearance(new_level, authorizing_officer)
        else:
            raise InvalidDataException("Invalid arguments for security clearance")
    
    # Method to update security clearance with validation
    def update_security_clearance(self, new_level, authorizing_officer):
        # Simple authorization check
        if not isinstance(authorizing_officer, Officer):
            raise AccessDeniedException("Security clearance can only be updated by an Officer")
        
        # Data validation
        if 1 <= new_level <= 5:
            self.__security_clearance = new_level
        else:
            raise InvalidDataException("Clearance level must be between 1 and 5")
    
    # Methods to access and modify private data with authorization
    def add_performance_record(self, record, evaluator):
        # Simple authorization check
        if not isinstance(evaluator, Officer):
            raise AccessDeniedException("Only officers can add performance records")
            
        # Create and store the record
        record_entry = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "evaluator": f"{evaluator.rank} {evaluator.name}",
            "content": record
        }
        self.__performance_records.append(record_entry)
    
    # Two method names for test compatibility
    def get_performance_records(self, requestor):
        # Same implementation as get_performance_history for compatibility
        if requestor.id == self.id or isinstance(requestor, Officer):
            return self.__performance_records.copy()
        else:
            raise AccessDeniedException("Not authorized to view performance records")
    
    def get_performance_history(self, requestor):
        # Authorization check - self or officer can access
        if requestor.id == self.id or isinstance(requestor, Officer):
            # Return a copy to maintain encapsulation
            return self.__performance_records.copy()
        else:
            raise AccessDeniedException("Not authorized to view performance records")
    
    @abstractmethod
    def display_info(self):
        """Display basic personnel information."""
        pass
    
    @abstractmethod
    def perform_duty(self):
        """Perform primary duty based on role."""
        pass


class Officer(MilitaryPersonnel):
    """Class representing officers in the military."""
    
    def __init__(self, id, name, rank, unit, specialization):
        # Call parent constructor
        super().__init__(id, name, rank, unit)
        
        # Add officer-specific attributes
        self._specialization = specialization                # Protected attribute
        self.__command_code = f"CMD-{id}-{hash(name)%1000}"  # Private attribute - highly sensitive
    
    @property
    def specialization(self):
        return self._specialization
    
    @property
    def command_code(self):
        # Restricted access to sensitive data
        return "RESTRICTED ACCESS"
    
    def display_info(self):
        # Example of controlled information disclosure
        return f"ID: {self._id} | Name: {self._name} | Rank: {self._rank} | Unit: {self._unit} | Specialization: {self._specialization}"
    
    def perform_duty(self):
        return f"{self._rank} {self._name} is commanding {self._unit}"


class Recruit(MilitaryPersonnel):
    """Class representing recruits in the military."""
    
    def __init__(self, id, name, unit):
        # Call parent constructor with fixed rank
        super().__init__(id, name, "Private", unit)
        
        # Add recruit-specific attributes
        self.__training_scores = {}      # Private attribute
        self.__disciplinary_record = []  # Private attribute
        self._aptitude_ratings = {       # Protected attribute
            "leadership": 0, 
            "technical": 0, 
            "physical": 0
        }
    
    @property
    def aptitude_ratings(self):
        # Return a copy to prevent direct modification of internal data
        return self._aptitude_ratings.copy()
    
    # Override rank setter to prevent recruits from changing rank
    @MilitaryPersonnel.rank.setter
    def rank(self, value):
        # Recruits can't change their rank - always stays "Private"
        if value != "Private":
            raise InvalidDataException("Recruits cannot change their rank")
        super(Recruit, self.__class__).rank.fset(self, value)
    
    def update_training_score(self, training_type, score, instructor):
        # Simple authorization check
        if not isinstance(instructor, Officer):
            raise AccessDeniedException("Only officers can update training scores")
            
        # Data validation
        if 0 <= score <= 100:
            self.__training_scores[training_type] = score
        else:
            raise InvalidDataException("Score must be between 0 and 100")
    
    def get_training_scores(self, requestor):
        # Role-based access control
        if requestor.id == self.id or isinstance(requestor, Officer):
            # Return a copy to maintain encapsulation
            return self.__training_scores.copy()
        else:
            raise AccessDeniedException("Not authorized to view training scores")
    
    def add_disciplinary_action(self, action, officer):
        # Authorization check
        if not isinstance(officer, Officer):
            raise AccessDeniedException("Only officers can add disciplinary actions")
        
        # Create and store the record
        action_record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "officer": f"{officer.rank} {officer.name}",
            "action": action
        }
        self.__disciplinary_record.append(action_record)
    
    def display_info(self):
        # Only show basic information
        return f"ID: {self._id} | Name: {self._name} | Rank: {self._rank} | Unit: {self._unit}"
    
    def perform_duty(self):
        return f"{self._name} is training at {self._unit}"


class TrainingProgram:
    """Class representing a training program in the military camp."""
    
    def __init__(self, code, name, duration):
        self.__program_code = code        # Private attribute
        self._name = name                 # Protected attribute
        self._duration = duration         # Protected attribute
        self.__performance_metrics = {}   # Private attribute
        self._requirements = []           # Protected attribute
    
    @property
    def code(self):
        return self.__program_code
    
    @property
    def name(self):
        return self._name
    
    @property
    def duration(self):
        return self._duration
    
    @property
    def requirements(self):
        # Return a copy to prevent direct modification
        return self._requirements.copy()
    
    def add_requirement(self, requirement, authorizer):
        # Authorization check
        if not isinstance(authorizer, Officer):
            raise AccessDeniedException("Only officers can add requirements")
        
        self._requirements.append(requirement)
    
    def add_performance_metric(self, metric_name, threshold, authorizer):
        # Authorization check
        if not isinstance(authorizer, Officer):
            raise AccessDeniedException("Only officers can add performance metrics")
        
        self.__performance_metrics[metric_name] = threshold
    
    def get_performance_metrics(self, requestor):
        # Authorization check
        if not isinstance(requestor, Officer):
            raise AccessDeniedException("Only officers can view performance metrics")
        
        # Return a copy to maintain encapsulation
        return self.__performance_metrics.copy()


class EquipmentInventory:
    """Class representing the equipment inventory in the military camp."""
    
    def __init__(self):
        self.__equipment = {}  # Private attribute - {id: {details}}
    
    def add_equipment(self, equipment_id, name, category, authorizer):
        # Authorization check
        if not isinstance(authorizer, Officer):
            raise AccessDeniedException("Only officers can add equipment")
        
        # Check for duplicates
        if equipment_id in self.__equipment:
            return False
        
        # Create equipment record
        self.__equipment[equipment_id] = {
            "id": equipment_id,
            "name": name,
            "category": category,
            "serial": f"SN-{hash(equipment_id)%10000}",
            "status": "Available",
            "assigned_to": None,
            "maintenance": []
        }
        return True
    
    def assign_equipment(self, equipment_id, person, authorizer):
        # Authorization check
        if not isinstance(authorizer, Officer):
            raise AccessDeniedException("Only officers can assign equipment")
        
        # Validate equipment exists
        if equipment_id not in self.__equipment:
            raise InvalidDataException(f"Equipment ID {equipment_id} not found")
        
        # Update assignment
        self.__equipment[equipment_id]["assigned_to"] = person.id
        self.__equipment[equipment_id]["status"] = "Assigned"
        return True
    
    def log_maintenance(self, equipment_id, note, authorizer):
        # Authorization check
        if not authorizer or not isinstance(authorizer, Officer):
            raise AccessDeniedException("Only officers can log maintenance")
        
        # Validate equipment exists
        if equipment_id not in self.__equipment:
            raise InvalidDataException(f"Equipment ID {equipment_id} not found")
        
        # Add maintenance record
        record = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "officer": f"{authorizer.rank} {authorizer.name}",
            "note": note
        }
        self.__equipment[equipment_id]["maintenance"].append(record)
        return True
    
    def get_equipment_details(self, equipment_id, requestor):
        # Authorization check
        if requestor is None:
            raise AccessDeniedException("Authentication required to access equipment details")
        
        # Validate equipment exists
        if equipment_id not in self.__equipment:
            raise InvalidDataException(f"Equipment ID {equipment_id} not found")
        
        equipment = self.__equipment[equipment_id]
        
        # Role-based information disclosure
        if isinstance(requestor, Officer):
            # Officers see full details
            return equipment.copy()
        else:
            # Recruits see limited information
            return {
                "id": equipment["id"],
                "name": equipment["name"],
                "category": equipment["category"],
                "status": equipment["status"]
            }


class CampManagementSystem:
    """Class representing the military camp management system."""
    
    def __init__(self, name, location):
        self.__name = name                # Private attribute
        self.__location = location        # Private attribute
        self.__personnel = []             # Private attribute
        self.__training_programs = []     # Private attribute
        self.__equipment_inventory = EquipmentInventory()  # Private attribute
        self.__next_id = 1                # Private attribute
    
    @property
    def name(self):
        return self.__name
    
    @property
    def location(self):
        return self.__location
    
    @property
    def personnel(self):
        # Return a copy to maintain encapsulation
        return self.__personnel.copy()
    
    @property
    def training_programs(self):
        # Return a copy to maintain encapsulation
        return self.__training_programs.copy()
    
    def get_next_id(self, role_prefix):
        id_val = self.__next_id
        self.__next_id += 1
        return f"{role_prefix}{id_val:03d}"
    
    def add_personnel(self, person, authorizer):
        # Authorization check
        if not isinstance(authorizer, Officer):
            raise AccessDeniedException("Only officers can add personnel")
        
        # Check if person already exists
        if any(p.id == person.id for p in self.__personnel):
            return False
        
        self.__personnel.append(person)
        return True
    
    def find_personnel_by_id(self, person_id, requestor):
        # Authorization check
        if requestor is None:
            raise AccessDeniedException("Authentication required to access personnel records")
        
        # Search for the person
        for person in self.__personnel:
            if person.id == person_id:
                return person
        return None
    
    def get_personnel_by_unit(self, unit, requestor):
        # Authorization check
        if not isinstance(requestor, Officer):
            raise AccessDeniedException("Only officers can view unit personnel")
        
        # Filter personnel by unit
        return [p for p in self.__personnel if p.unit == unit]
    
    def add_training_program(self, program, authorizer):
        # Authorization check
        if not isinstance(authorizer, Officer):
            raise AccessDeniedException("Only officers can add training programs")
        
        # Check if program already exists
        if any(p.code == program.code for p in self.__training_programs):
            return False
        
        self.__training_programs.append(program)
        return True
    
    def get_equipment_inventory(self):
        return self.__equipment_inventory


def main():
    """Demonstrate the military camp management system and encapsulation principles."""
    # Create system
    camp = CampManagementSystem("Alpha Training Camp", "Fort Benning")
    
    # Create personnel
    commander = Officer("O001", "James Miller", "Colonel", "Alpha Unit", "Infantry")
    recruit = Recruit("R001", "John Smith", "Alpha Unit")
    
    # Add personnel with authorization
    camp.add_personnel(commander, commander)
    camp.add_personnel(recruit, commander)
    
    print("\n=== Demonstrating Encapsulation ===")
    
    # 1. Demonstrate property access (data hiding with controlled access)
    print(f"Name (via property): {commander.name}")
    print(f"Rank (via property): {commander.rank}")
    
    # 2. Demonstrate validation in setter (data integrity)
    try:
        recruit.rank = "General"  # Should fail - recruits can't change rank
    except InvalidDataException as e:
        print(f"Validation in setter prevented rank change: {e}")
    
    # 3. Demonstrate private attribute protection (information hiding)
    print(f"Command code (restricted access): {commander.command_code}")
    # Direct access would fail: print(commander.__command_code)
    
    # 4. Demonstrate authorization checks (controlled access)
    try:
        recruit.update_training_score("marksmanship", 85, recruit)  # Should fail - recruits can't update scores
        print("This should not happen")
    except AccessDeniedException as e:
        print(f"Access control prevented unauthorized action: {e}")
    
    # 5. Demonstrate proper authorized access
    recruit.update_training_score("marksmanship", 85, commander)
    
    # 6. Demonstrate different views of data based on role (information filtering)
    recruit_scores = recruit.get_training_scores(recruit)  # Self access
    officer_scores = recruit.get_training_scores(commander)  # Officer access
    print(f"Recruit can access their scores: {recruit_scores}")
    print(f"Officer can access recruit's scores: {officer_scores}")
    
    # 7. Demonstrate immutable returns (preventing modification of internal state)
    original_ratings = recruit.aptitude_ratings
    print(f"Original aptitude ratings: {original_ratings}")
    
    # Try to modify the returned data
    original_ratings["leadership"] = 100
    
    # Show that internal data remains unchanged
    print(f"Aptitude ratings after attempted modification: {recruit.aptitude_ratings}")
    
    # 8. Demonstrate equipment inventory with role-based views
    inventory = camp.get_equipment_inventory()
    inventory.add_equipment("E001", "M4 Rifle", "Weapon", commander)
    inventory.assign_equipment("E001", recruit, commander)
    
    # Different information disclosed based on role
    officer_view = inventory.get_equipment_details("E001", commander)
    recruit_view = inventory.get_equipment_details("E001", recruit)
    
    print(f"\nOfficer view of equipment: {officer_view['name']} (includes serial: {officer_view['serial']})")
    print(f"Recruit view of equipment: {recruit_view['name']} (limited details, no serial number)")
    
    # 9. Demonstrate immutable collections
    personnel = camp.personnel
    personnel.append("This shouldn't affect the original list")
    print(f"Original personnel count still: {len(camp.personnel)}")
    
    print("\nMilitary Camp System successfully demonstrates encapsulation principles")


if __name__ == "__main__":
    main()
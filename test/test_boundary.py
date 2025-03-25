import pytest
import random
from test.TestUtils import TestUtils
from military_camp_management_system import Officer, Recruit, TrainingProgram, EquipmentInventory, CampManagementSystem, AccessDeniedException, InvalidDataException
class TestBoundary:
    """Test cases for boundary conditions in the military camp management system."""
    
    def test_system_boundaries(self):
        """Test all boundary conditions for the military camp management system."""
        try:
            # MilitaryPersonnel boundary tests - not directly testable since it's abstract
            # Instead test through concrete implementations
            
            # Officer boundary tests
            commander = Officer("O001", "Emma Smith", "Colonel", "Alpha Battalion", "Infantry")
            assert commander.id == "O001"
            assert commander.name == "Emma Smith"
            assert commander.rank == "Colonel"
            assert commander.unit == "Alpha Battalion"
            assert commander.specialization == "Infantry"
            
            # Test rank setter boundary conditions
            commander.rank = "General"  # Valid rank
            assert commander.rank == "General"
            
            try:
                commander.rank = "Invalid Rank"  # Invalid rank
                assert False, "Should raise InvalidDataException"
            except InvalidDataException:
                pass  # Expected behavior
            
            # Recruit boundary tests
            recruit = Recruit("R001", "John Davis", "Alpha Battalion")
            assert recruit.id == "R001"
            assert recruit.name == "John Davis"
            assert recruit.rank == "Private"  # Recruits always start as Private
            assert recruit.unit == "Alpha Battalion"
            
            # TrainingProgram boundary tests
            program = TrainingProgram("TP001", "Basic Combat Training", "8 weeks")
            assert program.code == "TP001"
            assert program.name == "Basic Combat Training"
            assert program.duration == "8 weeks"
            
            # Test adding requirements with proper authorization
            program.add_requirement("Physical fitness test", commander)
            assert "Physical fitness test" in program.requirements
            
            # Test adding requirements without authorization
            try:
                program.add_requirement("Unauthorized requirement", recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test equipment inventory boundary conditions
            inventory = EquipmentInventory()
            
            # Test adding equipment with proper authorization
            assert inventory.add_equipment("E001", "M4 Rifle", "Weapon", commander) is True
            
            # Test adding equipment without authorization
            try:
                inventory.add_equipment("E002", "Combat Vest", "Gear", recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test equipment assignment with proper authorization
            assert inventory.assign_equipment("E001", recruit, commander) is True
            
            # Test equipment assignment without authorization
            try:
                inventory.assign_equipment("E001", commander, recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test equipment detail access with different clearance levels
            officer_view = inventory.get_equipment_details("E001", commander)
            assert "serial" in officer_view  # Officers should see full details
            
            recruit_view = inventory.get_equipment_details("E001", recruit)
            assert "serial" not in recruit_view  # Recruits should see limited details
            
            # CampManagementSystem boundary tests
            camp = CampManagementSystem("Alpha Training Camp", "Fort Benning")
            assert camp.name == "Alpha Training Camp"
            assert camp.location == "Fort Benning"
            
            # Test ID generation
            id1 = camp.get_next_id("O")
            id2 = camp.get_next_id("O")
            assert id2 != id1  # Should generate unique IDs
            
            # Test adding personnel
            assert camp.add_personnel(commander, commander) is True
            assert camp.add_personnel(recruit, commander) is True
            
            # Test duplicate personnel
            assert camp.add_personnel(commander, commander) is False
            
            # Test finding personnel with authorization
            found_person = camp.find_personnel_by_id("O001", commander)
            assert found_person.id == "O001"
            
            # Test finding personnel without authorization
            try:
                camp.find_personnel_by_id("O001", None)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test unit personnel retrieval with proper authorization
            unit_personnel = camp.get_personnel_by_unit("Alpha Battalion", commander)
            assert len(unit_personnel) == 2
            
            # Test unit personnel retrieval without authorization
            try:
                camp.get_personnel_by_unit("Alpha Battalion", None)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test training program addition with proper authorization
            new_program = TrainingProgram("TP002", "Advanced Combat", "4 weeks")
            assert camp.add_training_program(new_program, commander) is True
            
            # Test training program addition without authorization
            try:
                camp.add_training_program(new_program, recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test proper encapsulation of collections
            programs = camp.training_programs
            
            # Modify the copy (should not affect original)
            if len(programs) > 0:
                programs.pop()
            
            # Verify original collection wasn't affected
            assert len(camp.training_programs) == 1
            
            # Test security clearance modification with proper authorization
            superior_officer = Officer("O003", "James Moore", "General", "Command HQ", "Leadership")
            camp.add_personnel(superior_officer, commander)
            
            # Set superior officer's clearance level directly for testing
            superior_officer._security_clearance = 5
            
            # Only higher-ranking officers should be able to change clearance
            recruit.update_security_clearance(2, superior_officer)
            assert recruit.security_clearance == 2
            
            # Test security clearance modification without proper authorization
            try:
                recruit.update_security_clearance(3, recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test performance record addition with proper authorization
            commander.add_performance_record("Excellent leadership", superior_officer)
            
            # Test performance record retrieval with proper authorization
            # Set commander's clearance level for testing
            commander._security_clearance = 2
            superior_officer._security_clearance = 5
            
            records = commander.get_performance_records(superior_officer)
            assert len(records) == 1
            
            # Test performance record retrieval without authorization
            try:
                commander.get_performance_records(recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            TestUtils.yakshaAssert("test_system_boundaries", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("test_system_boundaries", False, "boundary")
            raise e
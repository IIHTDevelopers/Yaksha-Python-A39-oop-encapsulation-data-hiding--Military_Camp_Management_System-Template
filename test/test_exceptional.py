import pytest
import random
from test.TestUtils import TestUtils
from military_camp_management_system import  Officer, Recruit, TrainingProgram, EquipmentInventory, CampManagementSystem, AccessDeniedException, InvalidDataException

class TestExceptional:
    """Test cases for exceptional conditions in the military camp management system."""
    
    def test_exception_handling(self):
        """Test all exception handling across the military camp management system."""
        try:
            # We can't test MilitaryPersonnel directly since it's abstract
            # Testing Officer exceptions
            commander = Officer("O001", "Emma Smith", "Colonel", "Alpha Battalion", "Infantry")
            
            # Test invalid rank assignment
            try:
                commander.rank = "Invalid Rank"
                assert False, "Should raise InvalidDataException"
            except InvalidDataException:
                pass  # Expected behavior
            
            # Test unit validation
            try:
                commander.unit = "AB"  # Too short
                assert False, "Should raise InvalidDataException"
            except InvalidDataException:
                pass  # Expected behavior
            
            # Test security clearance validation
            superior = Officer("O002", "James Moore", "General", "Command HQ", "Leadership")
            superior._security_clearance = 5  # Directly set for testing
            
            # Valid clearance level with proper authorization
            commander.update_security_clearance(3, superior)
            assert commander.security_clearance == 3
            
            # Invalid clearance level
            try:
                commander.update_security_clearance(10, superior)  # Invalid level
                assert False, "Should raise InvalidDataException"
            except InvalidDataException:
                pass  # Expected behavior
            
            # Unauthorized clearance change
            recruit = Recruit("R001", "John Davis", "Alpha Battalion")
            try:
                commander.update_security_clearance(4, recruit)  # Recruit can't change clearance
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test Recruit exceptions
            
            # Test updating training scores with proper authorization
            instructor = Officer("O003", "Michael Brown", "Lieutenant", "Training Division", "Instruction")
            recruit.update_training_score("marksmanship", 85, instructor)
            
            # Test updating training scores without authorization
            try:
                recruit.update_training_score("physical", 90, None)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test score validation
            try:
                recruit.update_training_score("physical", 110, instructor)  # Invalid score
                assert False, "Should raise InvalidDataException"
            except InvalidDataException:
                pass  # Expected behavior
            
            # Test training score access authorization
            scores = recruit.get_training_scores(recruit)  # Self access
            assert "marksmanship" in scores
            
            scores = recruit.get_training_scores(commander)  # Officer access
            assert "marksmanship" in scores
            
            # Test unauthorized access
            other_recruit = Recruit("R002", "Sarah Johnson", "Bravo Battalion")
            try:
                recruit.get_training_scores(other_recruit)  # Another recruit can't access
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test disciplinary action authorization
            recruit.add_disciplinary_action("Late for formation", commander)
            
            # Test unauthorized disciplinary action
            try:
                recruit.add_disciplinary_action("Unauthorized report", other_recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test TrainingProgram exceptions
            program = TrainingProgram("TP001", "Basic Combat Training", "8 weeks")
            
            # Test requirement addition with proper authorization
            program.add_requirement("Physical fitness test", commander)
            
            # Test unauthorized requirement addition
            try:
                program.add_requirement("Unauthorized requirement", recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test performance metric addition with proper authorization
            program.add_performance_metric("run_time", 15, commander)
            
            # Test unauthorized performance metric addition
            try:
                program.add_performance_metric("unauthorized_metric", 10, recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test performance metric access with proper authorization
            metrics = program.get_performance_metrics(commander)
            assert "run_time" in metrics
            
            # Test unauthorized performance metric access
            try:
                program.get_performance_metrics(None)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test EquipmentInventory exceptions
            inventory = EquipmentInventory()
            
            # Test equipment addition with proper authorization
            inventory.add_equipment("E001", "M4 Rifle", "Weapon", commander)
            
            # Test unauthorized equipment addition
            try:
                inventory.add_equipment("E002", "Combat Vest", "Gear", recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test equipment assignment with proper authorization
            inventory.assign_equipment("E001", recruit, commander)
            
            # Test equipment assignment to non-existent equipment
            try:
                inventory.assign_equipment("NONEXISTENT", recruit, commander)
                assert False, "Should raise InvalidDataException"
            except InvalidDataException:
                pass  # Expected behavior
            
            # Test equipment assignment unauthorized
            try:
                inventory.assign_equipment("E001", commander, recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test maintenance logging with proper authorization
            inventory.log_maintenance("E001", "Regular cleaning", commander)
            
            # Test unauthorized maintenance logging
            try:
                inventory.log_maintenance("E001", "Unauthorized note", None)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test equipment details with different authorization levels
            officer_view = inventory.get_equipment_details("E001", commander)
            assert "serial" in officer_view
            assert "maintenance" in officer_view
            
            recruit_view = inventory.get_equipment_details("E001", recruit)
            assert "serial" not in recruit_view
            assert "maintenance" not in recruit_view
            
            # Test equipment detail access to non-existent equipment
            try:
                inventory.get_equipment_details("NONEXISTENT", commander)
                assert False, "Should raise InvalidDataException"
            except InvalidDataException:
                pass  # Expected behavior
            
            # Test equipment detail access without authorization
            try:
                inventory.get_equipment_details("E001", None)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # CampManagementSystem exceptions
            camp = CampManagementSystem("Alpha Training Camp", "Fort Benning")
            
            # Test personnel addition
            camp.add_personnel(commander, commander)
            camp.add_personnel(recruit, commander)
            
            # Test duplicate personnel addition
            assert camp.add_personnel(commander, commander) is False
            
            # Test finding personnel with authorization
            found = camp.find_personnel_by_id("O001", commander)
            assert found.id == "O001"
            
            # Test finding non-existent personnel
            assert camp.find_personnel_by_id("NONEXISTENT", commander) is None
            
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
                camp.get_personnel_by_unit("Alpha Battalion", recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            # Test immutability of collections
            personnel_copy = camp.personnel
            
            # Modify the copy (should not affect original)
            if len(personnel_copy) > 0:
                personnel_copy.pop()
            
            # Original list should be unchanged
            assert len(camp.personnel) == 2
            
            # Test training program addition with proper authorization
            new_program = TrainingProgram("TP002", "Advanced Combat", "4 weeks")
            assert camp.add_training_program(new_program, commander) is True
            
            # Test training program addition without authorization
            try:
                camp.add_training_program(new_program, recruit)
                assert False, "Should raise AccessDeniedException"
            except AccessDeniedException:
                pass  # Expected behavior
            
            TestUtils.yakshaAssert("test_exception_handling", True, "exceptional")
        except Exception as e:
            TestUtils.yakshaAssert("test_exception_handling", False, "exceptional")
            raise e
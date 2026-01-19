# test_singleton_pattern.py - Tests for singleton pattern functionality
import pytest
from src.core.config import Settings
from src.core.log import LogSettings
from src.core.singleton_pattern import Singleton


class TestSingletonMetaclass:
    """Test suite for Singleton metaclass"""

    def test_singleton_creates_single_instance(self):
        """Test that singleton creates only one instance"""

        class TestClass(metaclass=Singleton):
            def __init__(self, value=None):
                self.value = value

        instance1 = TestClass("first")
        instance2 = TestClass("second")

        # Should be the same instance
        assert instance1 is instance2
        assert id(instance1) == id(instance2)

    def test_singleton_preserves_first_initialization(self):
        """Test that singleton preserves first initialization values"""

        class TestClass(metaclass=Singleton):
            def __init__(self, value=None):
                self.value = value

        instance1 = TestClass("first_value")
        instance2 = TestClass("second_value")

        # Should preserve first value
        assert instance1.value == "first_value"
        assert instance2.value == "first_value"

    def test_singleton_with_multiple_classes(self):
        """Test singleton with multiple different classes"""

        class FirstClass(metaclass=Singleton):
            def __init__(self):
                self.name = "first"

        class SecondClass(metaclass=Singleton):
            def __init__(self):
                self.name = "second"

        first_instance1 = FirstClass()
        first_instance2 = FirstClass()
        second_instance1 = SecondClass()
        second_instance2 = SecondClass()

        # Each class should have its own singleton
        assert first_instance1 is first_instance2
        assert second_instance1 is second_instance2
        assert first_instance1 is not second_instance1
        assert first_instance1.name == "first"
        assert second_instance1.name == "second"

    def test_singleton_inheritance(self):
        """Test singleton behavior with inheritance"""

        class BaseClass(metaclass=Singleton):
            def __init__(self):
                self.base_value = "base"

        class DerivedClass(BaseClass):
            def __init__(self):
                super().__init__()
                self.derived_value = "derived"

        base_instance = BaseClass()
        derived_instance = DerivedClass()

        # Should be different instances (different classes)
        assert base_instance is not derived_instance
        assert hasattr(base_instance, "base_value")
        assert hasattr(derived_instance, "base_value")
        assert hasattr(derived_instance, "derived_value")

    def test_singleton_thread_safety(self):
        """Test singleton behavior in concurrent scenarios"""
        import threading
        import time

        class TestClass(metaclass=Singleton):
            def __init__(self):
                # Simulate some initialization time
                time.sleep(0.01)
                self.thread_id = threading.current_thread().ident
                self.created_at = time.time()

        instances = []
        threads = []

        def create_instance():
            instance = TestClass()
            instances.append(instance)

        # Create multiple threads that try to create instances
        for _ in range(5):
            thread = threading.Thread(target=create_instance)
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

        # All instances should be the same
        first_instance = instances[0]
        for instance in instances:
            assert instance is first_instance
            assert instance.thread_id == first_instance.thread_id
            assert instance.created_at == first_instance.created_at

    def test_singleton_instance_tracking(self):
        """Test that singleton tracks instances correctly"""

        class TestClass(metaclass=Singleton):
            pass

        # Before creating instances, should be empty
        assert TestClass not in TestClass._instances

        instance1 = TestClass()
        # After creating instance, should be tracked
        assert TestClass in TestClass._instances
        assert TestClass._instances[TestClass] is instance1

        instance2 = TestClass()
        # Should still be the same tracked instance
        assert TestClass._instances[TestClass] is instance2
        assert len(TestClass._instances) == 1

    def test_singleton_with_arguments(self):
        """Test singleton with constructor arguments"""

        class TestClass(metaclass=Singleton):
            def __init__(self, name, value):
                self.name = name
                self.value = value

        # Create first instance with arguments
        instance1 = TestClass("test", 42)

        # Create second instance with different arguments
        instance2 = TestClass("different", 99)

        # Should be same instance with first arguments
        assert instance1 is instance2
        assert instance1.name == "test"
        assert instance1.value == 42
        assert instance2.name == "test"
        assert instance2.value == 42

    def test_singleton_without_arguments(self):
        """Test singleton without constructor arguments"""

        class TestClass(metaclass=Singleton):
            def __init__(self):
                self.created = True

        instance1 = TestClass()
        instance2 = TestClass()

        assert instance1 is instance2
        assert hasattr(instance1, "created")
        assert hasattr(instance2, "created")


class TestSettingsSingleton:
    """Test suite for Settings class singleton behavior"""

    def test_settings_is_singleton(self):
        """Test that Settings class follows singleton pattern"""
        settings1 = Settings()
        settings2 = Settings()

        assert settings1 is settings2
        assert id(settings1) == id(settings2)

    def test_settings_configuration_persistence(self):
        """Test that settings configuration persists"""
        settings1 = Settings()
        original_database_url = settings1.DATABASE_URL

        settings2 = Settings()
        assert settings2.DATABASE_URL == original_database_url


class TestLogSettingsSingleton:
    """Test suite for LogSettings class singleton behavior"""

    def test_log_settings_is_singleton(self):
        """Test that LogSettings class follows singleton pattern"""
        log_settings1 = LogSettings()
        log_settings2 = LogSettings()

        assert log_settings1 is log_settings2
        assert id(log_settings1) == id(log_settings2)

    def test_log_settings_configuration_persistence(self):
        """Test that log settings configuration persists"""
        log_settings1 = LogSettings()
        original_log_level = log_settings1.LOG_LEVEL

        log_settings2 = LogSettings()
        assert log_settings2.LOG_LEVEL == original_log_level


class TestSingletonIntegration:
    """Integration tests for singleton pattern"""

    def test_multiple_singletons_coexist(self):
        """Test that multiple singleton classes can coexist"""

        class FirstSingleton(metaclass=Singleton):
            def __init__(self):
                self.type = "first"

        class SecondSingleton(metaclass=Singleton):
            def __init__(self):
                self.type = "second"

        class ThirdSingleton(metaclass=Singleton):
            def __init__(self):
                self.type = "third"

        first = FirstSingleton()
        second = SecondSingleton()
        third = ThirdSingleton()

        # All should be different instances
        assert first is not second
        assert first is not third
        assert second is not third

        # But each should be singleton within its class
        assert FirstSingleton() is first
        assert SecondSingleton() is second
        assert ThirdSingleton() is third

        # Check the instances tracking
        assert len(Singleton._instances) >= 3
        assert FirstSingleton in Singleton._instances
        assert SecondSingleton in Singleton._instances
        assert ThirdSingleton in Singleton._instances

    def test_singleton_with_application_classes(self):
        """Test singleton behavior with actual application classes"""
        # Test Settings
        settings_a = Settings()
        settings_b = Settings()
        assert settings_a is settings_b

        # Test LogSettings
        log_settings_a = LogSettings()
        log_settings_b = LogSettings()
        assert log_settings_a is log_settings_b

        # They should be different from each other
        assert settings_a is not log_settings_a

    def test_singleton_memory_efficiency(self):
        """Test that singleton doesn't create unnecessary instances"""

        class TestClass(metaclass=Singleton):
            def __init__(self):
                self.creation_count = getattr(self.__class__, "_creation_count", 0) + 1
                self.__class__._creation_count = self.creation_count

        # Create multiple "instances"
        instances = [TestClass() for _ in range(10)]

        # All should be the same instance
        for instance in instances:
            assert instance is instances[0]

        # Creation count should only be 1
        assert instances[0].creation_count == 1
        assert len(TestClass._instances) == 1

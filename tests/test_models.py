"""Tests for data models."""

import unittest
from datetime import datetime
from uuid import uuid4

from red_teaming.models import (
    VulnerabilityType,
    SeverityLevel,
    Message,
    Conversation,
    Vulnerability,
    RedTeamingState,
    AttackPrompt,
)


class TestEnums(unittest.TestCase):
    """Test the enum classes."""

    def test_vulnerability_type_values(self):
        """Test VulnerabilityType enum values."""
        self.assertEqual(
            VulnerabilityType.DECEPTIVE_ALIGNMENT.value, "deceptive_alignment"
        )
        self.assertEqual(VulnerabilityType.REWARD_HACKING.value, "reward_hacking")
        self.assertEqual(
            VulnerabilityType.LYING_AND_DECEPTION.value, "lying_and_deception"
        )
        self.assertEqual(VulnerabilityType.JAILBREAKING.value, "jailbreaking")
        self.assertEqual(VulnerabilityType.PROMPT_INJECTION.value, "prompt_injection")
        self.assertEqual(VulnerabilityType.DATA_EXTRACTION.value, "data_extraction")
        self.assertEqual(
            VulnerabilityType.HARMFUL_CONTENT_GENERATION.value,
            "harmful_content_generation",
        )
        self.assertEqual(
            VulnerabilityType.BIAS_AMPLIFICATION.value, "bias_amplification"
        )
        self.assertEqual(
            VulnerabilityType.MISINFORMATION_GENERATION.value,
            "misinformation_generation",
        )
        self.assertEqual(
            VulnerabilityType.PRIVACY_VIOLATIONS.value, "privacy_violations"
        )

    def test_severity_level_values(self):
        """Test SeverityLevel enum values."""
        self.assertEqual(SeverityLevel.LOW.value, "low")
        self.assertEqual(SeverityLevel.MEDIUM.value, "medium")
        self.assertEqual(SeverityLevel.HIGH.value, "high")
        self.assertEqual(SeverityLevel.CRITICAL.value, "critical")


class TestMessage(unittest.TestCase):
    """Test the Message dataclass."""

    def test_message_creation(self):
        """Test basic message creation."""
        message = Message(role="user", content="Hello world")
        self.assertEqual(message.role, "user")
        self.assertEqual(message.content, "Hello world")
        self.assertIsInstance(message.timestamp, datetime)
        self.assertEqual(message.metadata, {})

    def test_message_with_metadata(self):
        """Test message creation with metadata."""
        metadata = {"source": "test", "confidence": 0.9}
        message = Message(role="assistant", content="Response", metadata=metadata)
        self.assertEqual(message.metadata, metadata)

    def test_message_to_dict(self):
        """Test message serialization to dictionary."""
        message = Message(role="user", content="Test message")
        data = message.to_dict()

        self.assertEqual(data["role"], "user")
        self.assertEqual(data["content"], "Test message")
        self.assertIn("timestamp", data)
        self.assertIsInstance(data["timestamp"], str)  # Should be ISO format
        self.assertEqual(data["metadata"], {})

    def test_message_to_dict_with_metadata(self):
        """Test message serialization with metadata."""
        metadata = {"test": "value"}
        message = Message(role="system", content="System message", metadata=metadata)
        data = message.to_dict()

        self.assertEqual(data["metadata"], metadata)


class TestConversation(unittest.TestCase):
    """Test the Conversation dataclass."""

    def test_conversation_creation(self):
        """Test basic conversation creation."""
        conv = Conversation(id="test-123")
        self.assertEqual(conv.id, "test-123")
        self.assertEqual(conv.messages, [])
        self.assertIsNone(conv.vulnerability_type)
        self.assertIsNone(conv.attack_strategy)
        self.assertFalse(conv.success)
        self.assertIsNone(conv.severity)
        self.assertIsInstance(conv.created_at, datetime)
        self.assertEqual(conv.metadata, {})

    def test_conversation_with_vulnerability_type(self):
        """Test conversation creation with vulnerability type."""
        conv = Conversation(
            id="test-456", vulnerability_type=VulnerabilityType.JAILBREAKING
        )
        self.assertEqual(conv.vulnerability_type, VulnerabilityType.JAILBREAKING)

    def test_add_message(self):
        """Test adding messages to conversation."""
        conv = Conversation(id="test-789")
        conv.add_message("user", "Hello")
        conv.add_message("assistant", "Hi there")

        self.assertEqual(len(conv.messages), 2)
        self.assertEqual(conv.messages[0].role, "user")
        self.assertEqual(conv.messages[0].content, "Hello")
        self.assertEqual(conv.messages[1].role, "assistant")
        self.assertEqual(conv.messages[1].content, "Hi there")

    def test_add_message_with_metadata(self):
        """Test adding message with metadata."""
        conv = Conversation(id="test-meta")
        metadata = {"confidence": 0.8}
        conv.add_message("user", "Test", metadata=metadata)

        self.assertEqual(conv.messages[0].metadata, metadata)

    def test_conversation_to_dict(self):
        """Test conversation serialization."""
        conv = Conversation(
            id="test-conv",
            vulnerability_type=VulnerabilityType.PROMPT_INJECTION,
            attack_strategy="direct",
            success=True,
            severity=SeverityLevel.HIGH,
        )
        conv.add_message("user", "Test prompt")
        conv.add_message("assistant", "Response")

        data = conv.to_dict()

        self.assertEqual(data["id"], "test-conv")
        self.assertEqual(data["vulnerability_type"], "prompt_injection")
        self.assertEqual(data["attack_strategy"], "direct")
        self.assertTrue(data["success"])
        self.assertEqual(data["severity"], "high")
        self.assertEqual(len(data["messages"]), 2)
        self.assertIsInstance(data["created_at"], str)
        self.assertEqual(data["metadata"], {})

    def test_conversation_to_dict_none_values(self):
        """Test conversation serialization with None values."""
        conv = Conversation(id="test-none")
        data = conv.to_dict()

        self.assertIsNone(data["vulnerability_type"])
        self.assertIsNone(data["severity"])


class TestVulnerability(unittest.TestCase):
    """Test the Vulnerability dataclass."""

    def test_vulnerability_creation(self):
        """Test basic vulnerability creation."""
        vuln = Vulnerability(
            id="vuln-123",
            type=VulnerabilityType.DECEPTIVE_ALIGNMENT,
            severity=SeverityLevel.CRITICAL,
            title="Test Vulnerability",
            description="A test vulnerability",
            attack_vector="Test attack",
            conversation_id="conv-456",
            proof_of_concept="Proof of concept",
        )

        self.assertEqual(vuln.id, "vuln-123")
        self.assertEqual(vuln.type, VulnerabilityType.DECEPTIVE_ALIGNMENT)
        self.assertEqual(vuln.severity, SeverityLevel.CRITICAL)
        self.assertEqual(vuln.title, "Test Vulnerability")
        self.assertEqual(vuln.description, "A test vulnerability")
        self.assertEqual(vuln.attack_vector, "Test attack")
        self.assertEqual(vuln.conversation_id, "conv-456")
        self.assertEqual(vuln.proof_of_concept, "Proof of concept")
        self.assertEqual(vuln.mitigation_suggestions, [])
        self.assertIsInstance(vuln.discovered_at, datetime)
        self.assertEqual(vuln.metadata, {})

    def test_vulnerability_with_mitigations(self):
        """Test vulnerability with mitigation suggestions."""
        mitigations = ["Fix A", "Fix B", "Fix C"]
        vuln = Vulnerability(
            id="vuln-456",
            type=VulnerabilityType.JAILBREAKING,
            severity=SeverityLevel.MEDIUM,
            title="Test",
            description="Test",
            attack_vector="Test",
            conversation_id="conv-789",
            proof_of_concept="Test",
            mitigation_suggestions=mitigations,
        )

        self.assertEqual(vuln.mitigation_suggestions, mitigations)

    def test_vulnerability_to_dict(self):
        """Test vulnerability serialization."""
        metadata = {"confidence": 0.95, "source": "automated"}
        vuln = Vulnerability(
            id="vuln-serialize",
            type=VulnerabilityType.DATA_EXTRACTION,
            severity=SeverityLevel.HIGH,
            title="Data Extraction Test",
            description="Test vulnerability for data extraction",
            attack_vector="Malicious prompt",
            conversation_id="conv-serialize",
            proof_of_concept="Successfully extracted data",
            mitigation_suggestions=["Input validation", "Output filtering"],
            metadata=metadata,
        )

        data = vuln.to_dict()

        self.assertEqual(data["id"], "vuln-serialize")
        self.assertEqual(data["type"], "data_extraction")
        self.assertEqual(data["severity"], "high")
        self.assertEqual(data["title"], "Data Extraction Test")
        self.assertEqual(data["description"], "Test vulnerability for data extraction")
        self.assertEqual(data["attack_vector"], "Malicious prompt")
        self.assertEqual(data["conversation_id"], "conv-serialize")
        self.assertEqual(data["proof_of_concept"], "Successfully extracted data")
        self.assertEqual(
            data["mitigation_suggestions"], ["Input validation", "Output filtering"]
        )
        self.assertIsInstance(data["discovered_at"], str)
        self.assertEqual(data["metadata"], metadata)


class TestRedTeamingState(unittest.TestCase):
    """Test the RedTeamingState dataclass."""

    def test_red_teaming_state_creation(self):
        """Test basic state creation."""
        state = RedTeamingState()

        self.assertIsNone(state.current_conversation)
        self.assertEqual(state.discovered_vulnerabilities, [])
        self.assertEqual(state.failed_attempts, [])
        self.assertIsNone(state.current_vulnerability_type)
        self.assertEqual(state.conversation_turn, 0)
        self.assertEqual(state.max_turns, 10)
        self.assertEqual(state.attack_strategies_tried, [])

    def test_red_teaming_state_custom_max_turns(self):
        """Test state creation with custom max turns."""
        state = RedTeamingState(max_turns=5)
        self.assertEqual(state.max_turns, 5)

    def test_issues_found_property(self):
        """Test issues_found property."""
        state = RedTeamingState()
        self.assertEqual(state.issues_found, 0)

        # Add some vulnerabilities
        vuln1 = Vulnerability(
            id="v1",
            type=VulnerabilityType.JAILBREAKING,
            severity=SeverityLevel.LOW,
            title="Test",
            description="Test",
            attack_vector="Test",
            conversation_id="c1",
            proof_of_concept="Test",
        )
        vuln2 = Vulnerability(
            id="v2",
            type=VulnerabilityType.PROMPT_INJECTION,
            severity=SeverityLevel.HIGH,
            title="Test",
            description="Test",
            attack_vector="Test",
            conversation_id="c2",
            proof_of_concept="Test",
        )

        state.discovered_vulnerabilities.append(vuln1)
        self.assertEqual(state.issues_found, 1)

        state.discovered_vulnerabilities.append(vuln2)
        self.assertEqual(state.issues_found, 2)

    def test_is_complete_property(self):
        """Test is_complete property."""
        state = RedTeamingState()
        self.assertFalse(state.is_complete)

        # Add 5 vulnerabilities to reach completion
        for i in range(5):
            vuln = Vulnerability(
                id=f"v{i}",
                type=VulnerabilityType.JAILBREAKING,
                severity=SeverityLevel.LOW,
                title="Test",
                description="Test",
                attack_vector="Test",
                conversation_id=f"c{i}",
                proof_of_concept="Test",
            )
            state.discovered_vulnerabilities.append(vuln)

        self.assertTrue(state.is_complete)

    def test_red_teaming_state_to_dict(self):
        """Test state serialization."""
        # Create a state with some data
        conv = Conversation(id="test-conv")
        vuln = Vulnerability(
            id="test-vuln",
            type=VulnerabilityType.BIAS_AMPLIFICATION,
            severity=SeverityLevel.MEDIUM,
            title="Test",
            description="Test",
            attack_vector="Test",
            conversation_id="test-conv",
            proof_of_concept="Test",
        )
        failed_conv = Conversation(id="failed-conv")

        state = RedTeamingState(
            current_conversation=conv,
            current_vulnerability_type=VulnerabilityType.BIAS_AMPLIFICATION,
            conversation_turn=3,
            max_turns=5,
            attack_strategies_tried=["direct", "indirect"],
        )
        state.discovered_vulnerabilities.append(vuln)
        state.failed_attempts.append(failed_conv)

        data = state.to_dict()

        self.assertIsInstance(data["current_conversation"], dict)
        self.assertEqual(data["current_conversation"]["id"], "test-conv")
        self.assertEqual(len(data["discovered_vulnerabilities"]), 1)
        self.assertIsInstance(data["discovered_vulnerabilities"][0], dict)
        self.assertEqual(len(data["failed_attempts"]), 1)
        self.assertIsInstance(data["failed_attempts"][0], dict)
        self.assertEqual(data["current_vulnerability_type"], "bias_amplification")
        self.assertEqual(data["conversation_turn"], 3)
        self.assertEqual(data["max_turns"], 5)
        self.assertEqual(data["attack_strategies_tried"], ["direct", "indirect"])
        self.assertEqual(data["issues_found"], 1)
        self.assertFalse(data["is_complete"])

    def test_red_teaming_state_to_dict_none_values(self):
        """Test state serialization with None values."""
        state = RedTeamingState()
        data = state.to_dict()

        self.assertIsNone(data["current_conversation"])
        self.assertIsNone(data["current_vulnerability_type"])


class TestAttackPrompt(unittest.TestCase):
    """Test the AttackPrompt dataclass."""

    def test_attack_prompt_creation(self):
        """Test basic attack prompt creation."""
        prompt = AttackPrompt(
            content="Test attack prompt",
            vulnerability_type=VulnerabilityType.HARMFUL_CONTENT_GENERATION,
            strategy="direct_approach",
            expected_outcome="Model generates harmful content",
        )

        self.assertEqual(prompt.content, "Test attack prompt")
        self.assertEqual(
            prompt.vulnerability_type, VulnerabilityType.HARMFUL_CONTENT_GENERATION
        )
        self.assertEqual(prompt.strategy, "direct_approach")
        self.assertEqual(prompt.expected_outcome, "Model generates harmful content")
        self.assertEqual(prompt.follow_up_prompts, [])
        self.assertEqual(prompt.metadata, {})

    def test_attack_prompt_with_follow_ups(self):
        """Test attack prompt with follow-up prompts."""
        follow_ups = ["Follow up 1", "Follow up 2"]
        prompt = AttackPrompt(
            content="Initial prompt",
            vulnerability_type=VulnerabilityType.MISINFORMATION_GENERATION,
            strategy="escalation",
            expected_outcome="Generate misinformation",
            follow_up_prompts=follow_ups,
        )

        self.assertEqual(prompt.follow_up_prompts, follow_ups)

    def test_attack_prompt_to_dict(self):
        """Test attack prompt serialization."""
        metadata = {"difficulty": "high", "category": "social"}
        prompt = AttackPrompt(
            content="Complex attack prompt",
            vulnerability_type=VulnerabilityType.PRIVACY_VIOLATIONS,
            strategy="social_engineering",
            expected_outcome="Extract private information",
            follow_up_prompts=["Escalation 1", "Escalation 2"],
            metadata=metadata,
        )

        data = prompt.to_dict()

        self.assertEqual(data["content"], "Complex attack prompt")
        self.assertEqual(data["vulnerability_type"], "privacy_violations")
        self.assertEqual(data["strategy"], "social_engineering")
        self.assertEqual(data["expected_outcome"], "Extract private information")
        self.assertEqual(data["follow_up_prompts"], ["Escalation 1", "Escalation 2"])
        self.assertEqual(data["metadata"], metadata)


class TestDataclassIntegration(unittest.TestCase):
    """Test integration between different dataclasses."""

    def test_conversation_with_vulnerability_workflow(self):
        """Test a complete workflow with conversation and vulnerability."""
        # Create conversation
        conv = Conversation(
            id=str(uuid4()),
            vulnerability_type=VulnerabilityType.REWARD_HACKING,
            attack_strategy="reward_manipulation",
        )

        # Add messages
        conv.add_message("user", "Manipulative prompt for reward hacking")
        conv.add_message("assistant", "Response showing vulnerability")

        # Mark as successful
        conv.success = True
        conv.severity = SeverityLevel.CRITICAL

        # Create vulnerability from conversation
        vuln = Vulnerability(
            id=str(uuid4()),
            type=conv.vulnerability_type,
            severity=conv.severity,
            title="Reward Hacking Vulnerability",
            description="Model can be manipulated to optimize for wrong rewards",
            attack_vector=conv.messages[0].content,
            conversation_id=conv.id,
            proof_of_concept=conv.messages[1].content,
            mitigation_suggestions=["Reward function alignment", "Better training"],
        )

        # Create state with this data
        state = RedTeamingState(
            current_conversation=conv,
            current_vulnerability_type=VulnerabilityType.REWARD_HACKING,
            conversation_turn=1,
        )
        state.discovered_vulnerabilities.append(vuln)

        # Test serialization of complete workflow
        state_data = state.to_dict()
        vuln_data = vuln.to_dict()
        conv_data = conv.to_dict()

        self.assertEqual(state_data["issues_found"], 1)
        self.assertEqual(state_data["current_vulnerability_type"], "reward_hacking")
        self.assertEqual(vuln_data["type"], "reward_hacking")
        self.assertEqual(vuln_data["severity"], "critical")
        self.assertEqual(conv_data["vulnerability_type"], "reward_hacking")
        self.assertTrue(conv_data["success"])
        self.assertEqual(len(conv_data["messages"]), 2)

    def test_serialization_roundtrip_compatibility(self):
        """Test that all dataclasses can be serialized without errors."""
        # Create instances of all dataclasses
        message = Message(role="user", content="Test")

        conv = Conversation(id="test")
        conv.add_message("user", "Hello")

        vuln = Vulnerability(
            id="vuln1",
            type=VulnerabilityType.JAILBREAKING,
            severity=SeverityLevel.LOW,
            title="Test",
            description="Test",
            attack_vector="Test",
            conversation_id="conv1",
            proof_of_concept="Test",
        )

        state = RedTeamingState()
        state.discovered_vulnerabilities.append(vuln)

        prompt = AttackPrompt(
            content="Test",
            vulnerability_type=VulnerabilityType.JAILBREAKING,
            strategy="test",
            expected_outcome="test",
        )

        # Test that all can be serialized without errors
        message_dict = message.to_dict()
        conv_dict = conv.to_dict()
        vuln_dict = vuln.to_dict()
        state_dict = state.to_dict()
        prompt_dict = prompt.to_dict()

        # Basic validation that serialization worked
        self.assertIsInstance(message_dict, dict)
        self.assertIsInstance(conv_dict, dict)
        self.assertIsInstance(vuln_dict, dict)
        self.assertIsInstance(state_dict, dict)
        self.assertIsInstance(prompt_dict, dict)

        # Ensure no None values where there shouldn't be
        self.assertEqual(message_dict["role"], "user")
        self.assertEqual(conv_dict["id"], "test")
        self.assertEqual(vuln_dict["id"], "vuln1")
        self.assertEqual(state_dict["issues_found"], 1)
        self.assertEqual(prompt_dict["content"], "Test")


if __name__ == "__main__":
    unittest.main()

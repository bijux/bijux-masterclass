from __future__ import annotations

import unittest

from labs.study_practice.transfer import CAPSTONE_TRANSFERS, transfer_for


class StudyPracticeTransferTests(unittest.TestCase):
    def test_every_substantive_module_has_one_transfer(self) -> None:
        self.assertEqual(
            [transfer.module for transfer in CAPSTONE_TRANSFERS],
            list(range(1, 11)),
        )

    def test_every_transfer_is_course_owned_and_observational(self) -> None:
        for transfer in CAPSTONE_TRANSFERS:
            with self.subTest(module=transfer.module):
                self.assertTrue(transfer.root_command.startswith("capstone-"))
                self.assertTrue(transfer.course_command.startswith("capstone-"))
                self.assertFalse(transfer.constructs_plugin)
                self.assertFalse(transfer.invokes_action)

    def test_every_transfer_names_proof_and_nonclaim(self) -> None:
        for transfer in CAPSTONE_TRANSFERS:
            with self.subTest(module=transfer.module):
                self.assertGreater(len(transfer.proves), 30)
                self.assertGreater(len(transfer.does_not_prove), 30)
                self.assertNotEqual(transfer.proves, transfer.does_not_prove)

    def test_reused_commands_ask_distinct_module_questions(self) -> None:
        module_one = transfer_for(1)
        module_two = transfer_for(2)
        module_six = transfer_for(6)
        module_nine = transfer_for(9)

        self.assertEqual(module_one.capstone_command, module_two.capstone_command)
        self.assertNotEqual(module_one.question, module_two.question)
        self.assertEqual(module_six.capstone_command, module_nine.capstone_command)
        self.assertNotEqual(module_six.question, module_nine.question)

    def test_unknown_module_is_refused(self) -> None:
        with self.assertRaisesRegex(ValueError, "between 1 and 10"):
            transfer_for(0)


if __name__ == "__main__":
    unittest.main()

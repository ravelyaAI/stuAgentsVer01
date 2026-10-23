import csv
import json
from pathlib import Path
import tempfile
import unittest
import agents


class FakeBackend:
    """Software-test fixture only; not a model or scientific observation."""
    def __init__(self, fail_reporting=False):
        self.calls = []
        self.fail_reporting = fail_reporting

    def generate(self, messages, spec, phase):
        self.calls.append((messages, phase))
        if phase == "recognition":
            return {"assessment": "incorrect", "issue_description": "70 is excluded",
                    "proposed_check": "Try [70]", "confidence": 90,
                    "brief_explanation": "Boundary mismatch"}, {"response_id": "TEST_ONLY"}
        if self.fail_reporting:
            raise RuntimeError("TEST_ONLY injected failure")
        return {"report_decision": "report", "report_text": "Include 70",
                "brief_explanation": "Requirement mismatch", "perceived_connection": 2}, {"response_id": "TEST_ONLY"}


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.task = json.loads((agents.ROOT / "task.json").read_text())

    def test_five_profiles_change_one_domain_and_three_facets(self):
        for domain in agents.DOMAINS:
            profile = agents.PROFILES[domain]
            self.assertEqual([d for d, level in profile["domains"].items() if level == "high"], [domain])
            self.assertEqual(sum(v == "high" for v in profile["facets"].values()), 3)
            self.assertEqual(len(profile["facets"]), 15)
        self.assertTrue(all(v == "moderate" for v in agents.PROFILES["baseline"]["domains"].values()))

    def test_answer_key_and_hypothesis_not_leaked(self):
        messages = agents.StudentAgent("agreeableness").initial_messages(self.task, "social")
        blob = json.dumps(messages)
        self.assertNotIn(self.task["researcher_only"]["fix"], blob)
        self.assertNotIn("recognition_rubric", blob)
        self.assertNotIn("H2", blob)

    def test_same_technical_stimulus(self):
        agent = agents.StudentAgent("extraversion")
        for condition in ("neutral", "social"):
            messages = agent.initial_messages(self.task, condition)
            self.assertIn(self.task["assistant_solution"], messages[1]["content"])
            self.assertIn(self.task["assignment"], messages[1]["content"])

    def test_counterexample_and_fix(self):
        # This executes only our authored, fixed test stimulus, never model output.
        namespace = {}
        code = self.task["assistant_solution"]
        exec(code, namespace)
        values = [69, 70, 71]
        self.assertEqual(namespace["passing_scores"](values), [71])
        self.assertEqual(values, [69, 70, 71])
        exec(code.replace("score > 70", "score >= 70"), namespace)
        for check in self.task["researcher_only"]["checks"]:
            self.assertEqual(namespace["passing_scores"](check["input"]), check["expected"])

    def test_schedule_complete_and_reproducible(self):
        jobs = agents.schedule(list(agents.PROFILES), ["neutral", "social"], 2, 42)
        self.assertEqual(len(jobs), 24)
        self.assertEqual(len(set(jobs)), 24)
        self.assertEqual(jobs, agents.schedule(list(agents.PROFILES), ["neutral", "social"], 2, 42))

    def test_validation_rejects_boolean_confidence_and_invalid_reports(self):
        answer, _ = FakeBackend().generate([], {}, "recognition")
        answer["confidence"] = True
        with self.assertRaises(ValueError):
            agents.validate_answer(answer, agents.RECOGNITION_SCHEMA)
        report, _ = FakeBackend().generate([], {}, "reporting")
        report["report_text"] = ""
        with self.assertRaises(ValueError):
            agents.validate_answer(report, agents.REPORT_SCHEMA)

    def test_histories_reset_and_reporting_follows_recognition(self):
        with tempfile.TemporaryDirectory() as folder:
            args = agents.parser().parse_args(["--baseline", "--out", folder, "--model", "TEST_ONLY"])
            backend = FakeBackend()
            out, records = agents.run(args, backend)
            self.assertEqual(len(records), 12)
            self.assertEqual(len(backend.calls), 24)
            for i in range(0, 24, 2):
                initial, phase = backend.calls[i]
                reporting, next_phase = backend.calls[i + 1]
                self.assertEqual(phase, "recognition")
                self.assertEqual(next_phase, "reporting")
                self.assertEqual(len(initial), 2)
                self.assertEqual(len(reporting), 4)
                self.assertEqual(reporting[:2], initial)
                self.assertEqual(json.loads(reporting[2]["content"])["assessment"], "incorrect")
            with (out / "results.csv").open() as file:
                rows = list(csv.DictReader(file))
            self.assertEqual(len(rows), 12)
            self.assertTrue(all(r["recognition_verified_by_human"] == "" for r in rows))

    def test_reporting_failure_retains_recognition_and_stops(self):
        with tempfile.TemporaryDirectory() as folder:
            args = agents.parser().parse_args(["--out", folder, "--model", "TEST_ONLY"])
            out, records = agents.run(args, FakeBackend(True))
            self.assertEqual(len(records), 1)
            saved = json.loads((out / "trial_001.json").read_text())
            self.assertEqual(saved["status"], "failed")
            self.assertIn("recognition", saved)
            self.assertNotIn("reporting", saved)

    def test_preview_has_no_responses_and_no_calls(self):
        with tempfile.TemporaryDirectory() as folder:
            args = agents.parser().parse_args(["--preview", "--out", folder])
            backend = FakeBackend()
            out, records = agents.run(args, backend)
            self.assertEqual(backend.calls, [])
            self.assertEqual(len(records), 10)
            self.assertTrue(all("recognition" not in r for r in records))
            self.assertEqual(json.loads((out / "manifest.json").read_text())["planned_api_calls"], 0)


if __name__ == "__main__":
    unittest.main()

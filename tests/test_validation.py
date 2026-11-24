import argparse
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch

import yaml

from tools import validate


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for folder in ("scenarios", "models", "publications", "software", "evidence", "catalogue"):
            shutil.copytree(validate.ROOT / folder, self.root / folder)

    def alter(self, path, edit):
        file = self.root / path
        document = yaml.safe_load(file.read_text(encoding="utf-8"))
        edit(document)
        file.write_text(yaml.safe_dump(document), encoding="utf-8")

    def test_existing_catalogue(self):
        _, records = validate.validate_catalogue(self.root)
        self.assertIn("SCN-0001", records)

    def test_duplicate_yaml_key(self):
        path = self.root / "models/MOD-0001.yaml"
        with path.open("a", encoding="utf-8") as stream:
            stream.write("\nname: duplicate\n")
        with self.assertRaisesRegex(ValueError, "Duplicate YAML key"):
            validate.validate_catalogue(self.root)

    def test_required_model_definition(self):
        self.alter("models/MOD-0001.yaml", lambda model: model.pop("definition"))
        with self.assertRaisesRegex(ValueError, "definition.*required"):
            validate.validate_catalogue(self.root)

    def test_duplicate_record_id(self):
        self.alter("software/software.yaml", lambda doc: doc["software"].append(doc["software"][0].copy()))
        with self.assertRaisesRegex(ValueError, "Duplicate record ID"):
            validate.validate_catalogue(self.root)

    def test_invalid_interaction_type(self):
        self.alter("scenarios/SCN-0001/interactions.yaml", lambda doc: doc["interactions"][0].update(interaction_type="guessed"))
        with self.assertRaisesRegex(ValueError, "interaction_type"):
            validate.validate_catalogue(self.root)

    def test_cross_scenario_endpoint(self):
        self.alter("scenarios/SCN-0001/interactions.yaml", lambda doc: doc["interactions"][0].update(source_participation_id="PART-0006"))
        with self.assertRaisesRegex(ValueError, "outside SCN-0001"):
            validate.validate_catalogue(self.root)

    def test_invalid_evidence_reference(self):
        self.alter("scenarios/SCN-0001/scenario.yaml", lambda doc: doc.update(evidence_ids=["EVD-9999"]))
        with self.assertRaisesRegex(ValueError, "invalid reference"):
            validate.validate_catalogue(self.root)

    def test_cross_scenario_evidence(self):
        self.alter("scenarios/SCN-0001/scenario.yaml", lambda doc: doc.update(evidence_ids=["EVD-0018"]))
        with self.assertRaisesRegex(ValueError, "outside the scenario"):
            validate.validate_catalogue(self.root)

    def test_identified_model_requires_id(self):
        self.alter("scenarios/SCN-0001/participations.yaml", lambda doc: doc["participations"][0].update(model_id=None))
        with self.assertRaisesRegex(ValueError, "lacks model_id"):
            validate.validate_catalogue(self.root)

    def test_research_scenario_requires_primary_publication(self):
        self.alter("scenarios/SCN-0002/scenario.yaml", lambda doc: doc.update(scientific_publication_id=None))
        with self.assertRaisesRegex(ValueError, "scientific_publication_id"):
            validate.validate_catalogue(self.root)

    def test_acceptance_requires_human_record(self):
        self.alter("scenarios/SCN-0001/scenario.yaml", lambda doc: doc.update(review_status="accepted"))
        with self.assertRaisesRegex(ValueError, "human_review"):
            validate.validate_catalogue(self.root)

    def test_catalogue_consistency(self):
        self.alter("scenarios/SCN-0001/scenario.yaml", lambda doc: doc.update(title="Wrong title"))
        with self.assertRaisesRegex(ValueError, "catalogue title"):
            validate.validate_catalogue(self.root)


class EvidenceReviewTests(unittest.TestCase):
    def test_blind_pass_structured_review_and_lifecycle(self):
        from tools import review

        docs, records = validate.validate_catalogue()
        result = {
            "source_assessment": "consistent", "limitations": [],
            "findings": [{
                "category": "supported", "catalogue_field": "SCN-0001.configuration",
                "claim": "Reviewed setting", "artifact_id": "A99", "locator": "p. 1",
                "explanation": "The artifact was invented.", "recommended_correction": "",
            }],
        }
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "source.txt"
            source.write_text("Original evidence", encoding="utf-8")
            args = argparse.Namespace(
                scenario="SCN-0001", source=[source], manifest=None, git_checkout=None,
                output_dir=directory, github_repo=None, github_revision=None,
            )
            with patch.object(review, "settings", return_value={"OPENAI_API_KEY": "test"}), patch.object(
                review, "request_review", side_effect=["Blind source extraction", json.dumps(result)]
            ) as api, patch("builtins.print"):
                review.run_reviews(args, docs, records)
            first, second = api.call_args_list
            self.assertNotIn("SCN-0001", first.args[2])
            self.assertIn("SCN-0001", second.args[2])
            self.assertEqual(second.args[3]["type"], "json_schema")
            path = directory / "SCN-0001/review.json"
            report = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(report["review_status"], "evidence_checked")
            self.assertEqual(report["declared_review_status"], "draft")
            self.assertEqual(report["ai_review"]["findings"][0]["category"], "needs_evidence")
            self.assertTrue(path.with_name("review.md").is_file())
            args.source = []
            with patch.object(review, "request_review") as api, patch("builtins.print"):
                review.run_reviews(args, docs, records)
                api.assert_not_called()
            self.assertEqual(json.loads(path.read_text(encoding="utf-8"))["ai_review"]["status"], "completed")


if __name__ == "__main__":
    unittest.main()
